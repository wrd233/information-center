from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from app.bilibili_adapter import as_artifact, default_runner, public_command_record, redact_command


Runner = Callable[[list[str], Path, int], subprocess.CompletedProcess[str]]
HttpClient = Callable[[str, dict, int], dict]


SUPPORTED_INPUT_RE = re.compile(
    r"(xiaohongshu\.com/(explore|discovery/item|user/profile)|xhslink\.com/)"
)


@dataclass(frozen=True)
class XHSDownloaderConfig:
    api_base_url: str = "http://127.0.0.1:5556"
    cookie: str | None = None
    proxy: str | None = None
    ffmpeg_path: str | None = None
    timeout_seconds: int = 180
    download_timeout_seconds: int = 1800


class AdapterError(RuntimeError):
    pass


class XHSAdapter:
    """XHS-Downloader API wrapper for Xiaohongshu video-note acquisition."""

    def __init__(
        self,
        config: XHSDownloaderConfig | None = None,
        http_client: HttpClient = None,
        runner: Runner = default_runner,
    ):
        self.config = config or XHSDownloaderConfig()
        self.http_client = http_client or post_json
        self.runner = runner

    def check_dependencies(self) -> dict:
        ffmpeg = shutil.which(self.config.ffmpeg_path or "ffmpeg")
        return {
            "xhs_downloader_api": self.config.api_base_url.rstrip("/"),
            "ffmpeg": ffmpeg,
            "configured_ffmpeg": self.config.ffmpeg_path,
        }

    def process(
        self,
        url: str,
        workspace: Path,
        download_video: bool = True,
        extract_audio: bool = True,
        skip_existing_download_record: bool = False,
    ) -> dict:
        if not SUPPORTED_INPUT_RE.search(url):
            raise AdapterError("Input does not look like a Xiaohongshu note URL or xhslink URL.")

        workspace.mkdir(parents=True, exist_ok=True)
        metadata_dir = workspace / "metadata"
        video_dir = workspace / "video"
        audio_dir = workspace / "audio"
        for directory in (metadata_dir, video_dir, audio_dir):
            directory.mkdir(parents=True, exist_ok=True)

        payload = {
            "url": url,
            "download": False,
            "skip": skip_existing_download_record,
        }
        if self.config.cookie or os.getenv("XHS_COOKIE"):
            payload["cookie"] = self.config.cookie or os.environ["XHS_COOKIE"]
        if self.config.proxy or os.getenv("XHS_PROXY"):
            payload["proxy"] = self.config.proxy or os.environ["XHS_PROXY"]

        endpoint = f"{self.config.api_base_url.rstrip('/')}/xhs/detail"
        response = self.http_client(endpoint, payload, self.config.timeout_seconds)
        data = response.get("data")
        if not data:
            raise AdapterError(response.get("message") or "XHS-Downloader returned no note data.")

        raw_path = metadata_dir / "xhs_detail.json"
        raw_path.write_text(json.dumps(response, ensure_ascii=False, indent=2), encoding="utf-8")

        video_urls = extract_download_urls(data)
        text = extract_text(data)
        video_files: list[Path] = []
        audio_files: list[Path] = []
        commands: list[dict] = []

        if video_urls and download_video:
            video_files.append(
                download_file(
                    video_urls[0],
                    video_dir,
                    filename_hint=filename_from_note(data, ".mp4"),
                    timeout_seconds=self.config.download_timeout_seconds,
                )
            )

        if video_files and extract_audio:
            deps = self.check_dependencies()
            if not deps["ffmpeg"]:
                raise AdapterError(
                    f"ffmpeg binary not found: {self.config.ffmpeg_path or 'ffmpeg'}. "
                    "Install it or set FFMPEG_PATH."
                )
            audio_path = audio_dir / f"{video_files[0].stem}.m4a"
            command = [
                self.config.ffmpeg_path or "ffmpeg",
                "-y",
                "-i",
                str(video_files[0]),
                "-vn",
                "-c:a",
                "copy",
                str(audio_path),
            ]
            completed = self.runner(command, workspace, self.config.download_timeout_seconds)
            commands.append(
                public_command_record(
                    {
                        "command": redact_command(command),
                        "exit_code": completed.returncode,
                        "output_tail": (completed.stdout or "")[-4000:],
                    }
                )
            )
            if completed.returncode != 0 or not audio_path.exists():
                fallback_path = audio_dir / f"{video_files[0].stem}.mp3"
                fallback = [
                    self.config.ffmpeg_path or "ffmpeg",
                    "-y",
                    "-i",
                    str(video_files[0]),
                    "-vn",
                    "-acodec",
                    "libmp3lame",
                    fallback_path.name,
                ]
                completed = self.runner(fallback, audio_dir, self.config.download_timeout_seconds)
                commands.append(
                    public_command_record(
                        {
                            "command": redact_command(fallback),
                            "exit_code": completed.returncode,
                            "output_tail": (completed.stdout or "")[-4000:],
                        }
                    )
                )
                if completed.returncode == 0 and fallback_path.exists():
                    audio_files.append(fallback_path)
            else:
                audio_files.append(audio_path)

        status = determine_status(video_urls, video_files, audio_files, text)
        result = {
            "platform": "xiaohongshu",
            "source_url": url,
            "status": status,
            "title": first_text(data, "作品标题", "title", "标题"),
            "description": first_text(data, "作品描述", "desc", "description"),
            "author": first_text(data, "作者昵称", "nickname", "author"),
            "note_id": first_text(data, "作品ID", "note_id", "noteId", "id"),
            "note_type": first_text(data, "作品类型", "type"),
            "text": text,
            "video_urls": video_urls,
            "video": [as_artifact(path, workspace) for path in video_files],
            "audio": [as_artifact(path, workspace) for path in audio_files],
            "metadata": as_artifact(raw_path, workspace),
            "raw_requests": [
                {
                    "url": endpoint,
                    "payload": redact_payload(payload),
                    "message": response.get("message"),
                }
            ],
            "raw_commands": commands,
        }
        (workspace / "adapter_result.json").write_text(
            json.dumps(result, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        if text:
            (workspace / "note_text.txt").write_text(text, encoding="utf-8")
        return result


def post_json(url: str, payload: dict, timeout_seconds: int) -> dict:
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=body,
        headers={"content-type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.URLError as exc:
        raise AdapterError(f"Failed to call XHS-Downloader API: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise AdapterError("XHS-Downloader API returned invalid JSON.") from exc


def download_file(
    url: str,
    directory: Path,
    filename_hint: str,
    timeout_seconds: int,
) -> Path:
    parsed = urllib.parse.urlparse(url)
    suffix = Path(parsed.path).suffix or Path(filename_hint).suffix or ".mp4"
    target = unique_path(directory / f"{Path(filename_hint).stem}{suffix}")
    request = urllib.request.Request(url, headers={"user-agent": "VideoTranscriptAPI/0.1"})
    with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
        with target.open("wb") as file:
            shutil.copyfileobj(response, file)
    return target


def extract_download_urls(data: dict) -> list[str]:
    value = data.get("下载地址") or data.get("download_urls") or data.get("video_urls")
    if isinstance(value, str):
        return [item for item in value.split() if item.startswith("http")]
    if isinstance(value, list):
        return [str(item) for item in value if str(item).startswith("http")]
    return []


def extract_text(data: dict) -> str:
    parts = [
        first_text(data, "作品标题", "title", "标题"),
        first_text(data, "作品描述", "desc", "description", "文案"),
    ]
    return "\n".join(part for part in parts if part).strip()


def first_text(data: dict, *keys: str) -> str | None:
    for key in keys:
        value = data.get(key)
        if value is not None and str(value).strip():
            return str(value).strip()
    return None


def filename_from_note(data: dict, suffix: str) -> str:
    raw = first_text(data, "作品标题", "作品ID", "note_id", "noteId", "id") or "xiaohongshu_note"
    cleaned = re.sub(r"[^\w.\-\u4e00-\u9fff]+", "_", raw).strip("._")
    return f"{cleaned[:80] or 'xiaohongshu_note'}{suffix}"


def unique_path(path: Path) -> Path:
    if not path.exists():
        return path
    stem = path.stem
    suffix = path.suffix
    for index in range(1, 1000):
        candidate = path.with_name(f"{stem}_{index}{suffix}")
        if not candidate.exists():
            return candidate
    raise AdapterError(f"Unable to allocate unique path for {path}.")


def determine_status(
    video_urls: list[str], video_files: list[Path], audio_files: list[Path], text: str
) -> str:
    if audio_files:
        return "audio_ready_for_asr"
    if video_files:
        return "video_ready_for_audio_extraction"
    if video_urls:
        return "video_url_ready"
    if text:
        return "text_only_note"
    return "failed_no_video_or_text"


def redact_payload(payload: dict) -> dict:
    redacted = dict(payload)
    if redacted.get("cookie"):
        redacted["cookie"] = "***"
    if redacted.get("proxy") and "@" in str(redacted["proxy"]):
        redacted["proxy"] = "***"
    return redacted
