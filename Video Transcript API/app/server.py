from __future__ import annotations

import json
import os
import threading
import traceback
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

from app.asr_worker import check_dependencies as check_asr_dependencies
from app.asr_worker import run_asr_for_task
from app.bilibili_adapter import BBDownConfig, BilibiliAdapter
from app.storage import TaskStore
from app.xhs_adapter import XHSAdapter, XHSDownloaderConfig


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = Path(os.getenv("VIDEO_TRANSCRIPT_DATA_DIR", BASE_DIR / "data" / "tasks"))
STORE = TaskStore(DATA_DIR)


def make_bilibili_adapter() -> BilibiliAdapter:
    return BilibiliAdapter(
        BBDownConfig(
            binary=os.getenv("BBDOWN_BIN", "BBDown"),
            ffmpeg_path=os.getenv("FFMPEG_PATH"),
            cookie=os.getenv("BBDOWN_COOKIE"),
        )
    )


def make_xhs_adapter() -> XHSAdapter:
    return XHSAdapter(
        XHSDownloaderConfig(
            api_base_url=os.getenv("XHS_API_BASE_URL", "http://127.0.0.1:5556"),
            cookie=os.getenv("XHS_COOKIE"),
            proxy=os.getenv("XHS_PROXY"),
            ffmpeg_path=os.getenv("FFMPEG_PATH"),
        )
    )


class Handler(BaseHTTPRequestHandler):
    server_version = "VideoTranscriptAPI/0.1"

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path == "/health":
            deps = {
                "bilibili": make_bilibili_adapter().check_dependencies(),
                "xiaohongshu": make_xhs_adapter().check_dependencies(),
                "asr": check_asr_dependencies(),
            }
            self.respond(200, {"ok": True, "dependencies": deps})
            return
        if parsed.path == "/api/platforms":
            self.respond(
                200,
                {
                    "platforms": [
                        {
                            "id": "bilibili",
                            "status": "enabled",
                            "adapter": "BBDown",
                            "outputs": ["subtitles", "audio", "cover", "metadata", "pages"],
                        },
                        {
                            "id": "xiaohongshu",
                            "aliases": ["xhs"],
                            "status": "enabled",
                            "adapter": "XHS-Downloader API",
                            "outputs": ["audio", "video", "metadata", "text"],
                        }
                    ]
                },
            )
            return
        if parsed.path == "/api/jobs":
            self.respond(200, {"jobs": STORE.list()})
            return
        if parsed.path.startswith("/api/jobs/"):
            task_id = parsed.path.rsplit("/", 1)[-1]
            task = STORE.get(task_id)
            self.respond(200, task) if task else self.respond(404, {"error": "job not found"})
            return
        self.respond(404, {"error": "not found"})

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path.startswith("/api/jobs/") and parsed.path.endswith("/asr"):
            task_id = parsed.path.split("/")[-2]
            task = STORE.get(task_id)
            if not task:
                self.respond(404, {"error": "job not found"})
                return
            if task.get("status") != "needs_asr":
                self.respond(409, {"error": f"job is not ready for ASR: {task.get('status')}"})
                return
            thread = threading.Thread(target=run_asr_task, args=(task_id,), daemon=True)
            thread.start()
            self.respond(202, {**task, "status": "asr_queued"})
            return

        platform_by_path = {
            "/api/bilibili/jobs": "bilibili",
            "/api/xhs/jobs": "xiaohongshu",
            "/api/xiaohongshu/jobs": "xiaohongshu",
        }
        platform = platform_by_path.get(parsed.path)
        if not platform:
            self.respond(404, {"error": "not found"})
            return

        try:
            payload = self.read_json()
            if not payload.get("url"):
                self.respond(400, {"error": "url is required"})
                return
            task = STORE.create(payload, platform=platform)
            thread = threading.Thread(target=run_task, args=(task["id"],), daemon=True)
            thread.start()
            self.respond(202, task)
        except json.JSONDecodeError:
            self.respond(400, {"error": "invalid json"})

    def read_json(self) -> dict:
        length = int(self.headers.get("content-length", "0"))
        raw = self.rfile.read(length).decode("utf-8")
        return json.loads(raw or "{}")

    def respond(self, status: int, payload: dict) -> None:
        body = json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("content-type", "application/json; charset=utf-8")
        self.send_header("content-length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt: str, *args) -> None:
        print(f"{self.address_string()} - {fmt % args}")


def run_task(task_id: str) -> None:
    task = STORE.get(task_id)
    if not task:
        return
    try:
        task["status"] = "running"
        STORE.save(task)
        if task["platform"] == "bilibili":
            adapter = make_bilibili_adapter()
            result = adapter.process(
                task["source_url"],
                STORE.task_workspace(task_id),
                select_page=task["options"].get("select_page", "ALL"),
                download_audio_if_no_subtitle=task["options"].get(
                    "download_audio_if_no_subtitle", True
                ),
                download_audio=task["options"].get("download_audio", True),
            )
        elif task["platform"] == "xiaohongshu":
            adapter = make_xhs_adapter()
            result = adapter.process(
                task["source_url"],
                STORE.task_workspace(task_id),
                download_video=task["options"].get("download_video", True),
                extract_audio=task["options"].get("extract_audio", True),
                skip_existing_download_record=task["options"].get(
                    "skip_existing_download_record", False
                ),
            )
        else:
            raise ValueError(f"Unsupported platform: {task['platform']}")
        task["result"] = result
        if result["status"] == "audio_ready_for_asr":
            task["status"] = "needs_asr"
        elif result["status"] == "subtitle_ready":
            task["status"] = "completed"
        elif result["status"] in {"video_url_ready", "video_ready_for_audio_extraction"}:
            task["status"] = "needs_audio_extraction"
        elif result["status"] == "text_only_note":
            task["status"] = "completed"
        else:
            task["status"] = "failed"
        STORE.save(task)
    except Exception as exc:
        task["status"] = "failed"
        task["error"] = {
            "message": str(exc),
            "traceback": traceback.format_exc(),
        }
        STORE.save(task)


def run_asr_task(task_id: str) -> None:
    try:
        run_asr_for_task(STORE, task_id)
    except Exception:
        print(traceback.format_exc())


def main() -> None:
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", "8765"))
    server = ThreadingHTTPServer((host, port), Handler)
    print(f"Video Transcript API listening on http://{host}:{port}")
    print(f"Data dir: {DATA_DIR}")
    server.serve_forever()


if __name__ == "__main__":
    main()
