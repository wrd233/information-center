from __future__ import annotations

import argparse
import asyncio
import json
import os
import ssl
import time
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse

from app.audio_preprocess import check_dependencies as check_preprocess_dependencies
from app.audio_preprocess import config_from_env as preprocess_config_from_env
from app.audio_preprocess import preprocess_for_rough_asr
from app.bilibili_adapter import as_artifact
from app.storage import TaskStore


try:
    import websockets
except ImportError:  # pragma: no cover - reported by check_dependencies.
    websockets = None


@dataclass(frozen=True)
class FunASRConfig:
    url: str = "ws://127.0.0.1:10095"
    timeout_seconds: int = 1800
    use_itn: bool = True
    hotwords: str = ""
    chunk_size: tuple[int, int, int] = (5, 10, 5)
    chunk_interval: int = 10


class ASRError(RuntimeError):
    pass


def config_from_env() -> FunASRConfig:
    return FunASRConfig(
        url=os.getenv("FUNASR_WS_URL", "ws://127.0.0.1:10095"),
        timeout_seconds=int(os.getenv("FUNASR_TIMEOUT_SECONDS", "1800")),
        use_itn=os.getenv("FUNASR_USE_ITN", "1") != "0",
        hotwords=os.getenv("FUNASR_HOTWORDS", ""),
    )


def check_dependencies() -> dict:
    return {
        "client": "funasr-websocket",
        "websockets_python_package": websockets is not None,
        "url": config_from_env().url,
        "preprocess": check_preprocess_dependencies(),
    }


def transcribe_file_sync(audio_path: Path, config: FunASRConfig | None = None) -> dict:
    return asyncio.run(transcribe_file(audio_path, config or config_from_env()))


async def transcribe_file(audio_path: Path, config: FunASRConfig) -> dict:
    if websockets is None:
        raise ASRError("Python package 'websockets' is required. Install it with: pip install websockets")
    if not audio_path.exists():
        raise ASRError(f"Audio file not found: {audio_path}")

    parsed = urlparse(config.url)
    if parsed.scheme not in {"ws", "wss"}:
        raise ASRError(f"FUNASR_WS_URL must start with ws:// or wss://, got: {config.url}")

    wav_name = audio_path.stem
    suffix = audio_path.suffix.lower().lstrip(".") or "wav"
    first_message = {
        "mode": "offline",
        "chunk_size": list(config.chunk_size),
        "chunk_interval": config.chunk_interval,
        "wav_name": wav_name,
        "wav_format": suffix,
        "is_speaking": True,
        "hotwords": config.hotwords,
        "itn": config.use_itn,
    }
    ssl_context = None
    if parsed.scheme == "wss":
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE

    started_at = time.time()
    messages: list[dict] = []
    async with websockets.connect(
        config.url,
        subprotocols=["binary"],
        ping_interval=None,
        ssl=ssl_context,
    ) as websocket:
        await websocket.send(json.dumps(first_message, ensure_ascii=False))
        await websocket.send(audio_path.read_bytes())
        await websocket.send(json.dumps({"is_speaking": False}, ensure_ascii=False))

        while True:
            try:
                raw = await asyncio.wait_for(websocket.recv(), timeout=config.timeout_seconds)
            except asyncio.TimeoutError as exc:
                raise ASRError(f"Timed out waiting for FunASR result after {config.timeout_seconds}s.") from exc
            message = json.loads(raw)
            messages.append(message)
            if message.get("text") and (
                message.get("mode") == "offline" or message.get("is_final") is True
            ):
                break

    text = "\n".join(
        str(message.get("text", "")).strip()
        for message in messages
        if str(message.get("text", "")).strip()
    ).strip()
    return {
        "engine": "funasr_paraformer",
        "audio_path": str(audio_path),
        "text": text,
        "duration_seconds": round(time.time() - started_at, 3),
        "raw_messages": messages,
    }


def run_asr_for_task(store: TaskStore, task_id: str, config: FunASRConfig | None = None) -> dict:
    task = store.get(task_id)
    if not task:
        raise ASRError(f"Job not found: {task_id}")
    if task.get("status") != "needs_asr":
        raise ASRError(f"Job {task_id} is not ready for ASR; status={task.get('status')}")

    result = task.get("result") or {}
    audio_items = result.get("audio") or []
    if not audio_items:
        raise ASRError(f"Job {task_id} has no audio artifact.")

    workspace = store.task_workspace(task_id)
    task["status"] = "asr_running"
    store.save(task)
    try:
        asr_results = []
        texts = []
        for item in audio_items:
            audio_path = Path(item["path"])
            preprocess_result = preprocess_for_rough_asr(
                audio_path,
                workspace,
                preprocess_config_from_env(),
            )
            asr_input_path = Path(preprocess_result["audio_path"])
            asr_result = transcribe_file_sync(asr_input_path, config)
            asr_result["source_audio_path"] = str(audio_path)
            asr_result["preprocess"] = preprocess_result
            asr_results.append(asr_result)
            if asr_result["text"]:
                texts.append(asr_result["text"])

        transcript_text = "\n\n".join(texts).strip()
        transcript_path = workspace / "transcript.txt"
        transcript_path.write_text(transcript_text, encoding="utf-8")

        asr_payload = {
            "status": "asr_completed" if transcript_text else "asr_empty",
            "engine": "funasr_paraformer",
            "transcript_text": transcript_text,
            "transcript": as_artifact(transcript_path, workspace),
            "segments": asr_results,
        }
        (workspace / "asr_result.json").write_text(
            json.dumps(asr_payload, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

        result["asr"] = asr_payload
        result["transcript_text"] = transcript_text
        task["result"] = result
        task["status"] = "completed" if transcript_text else "failed"
        if not transcript_text:
            task["error"] = {"message": "ASR returned empty text."}
        store.save(task)
        return task
    except Exception as exc:
        task["status"] = "failed"
        task["error"] = {"message": str(exc)}
        store.save(task)
        raise


def run_pending_once(store: TaskStore, limit: int = 1, config: FunASRConfig | None = None) -> list[dict]:
    tasks = [task for task in store.list() if task.get("status") == "needs_asr"]
    completed = []
    for task in tasks[:limit]:
        completed.append(run_asr_for_task(store, task["id"], config))
    return completed


def main() -> None:
    parser = argparse.ArgumentParser(description="Run rough ASR for Video Transcript API jobs.")
    parser.add_argument("--data-dir", default=os.getenv("VIDEO_TRANSCRIPT_DATA_DIR"))
    parser.add_argument("--job-id")
    parser.add_argument("--once", action="store_true")
    parser.add_argument("--poll-interval", type=float, default=5.0)
    parser.add_argument("--limit", type=int, default=1)
    args = parser.parse_args()

    base_dir = Path(__file__).resolve().parents[1]
    data_dir = Path(args.data_dir) if args.data_dir else base_dir / "data" / "tasks"
    store = TaskStore(data_dir)
    if args.job_id:
        print(json.dumps(run_asr_for_task(store, args.job_id), ensure_ascii=False, indent=2))
        return
    while True:
        completed = run_pending_once(store, limit=args.limit)
        if completed:
            print(f"ASR completed for {len(completed)} job(s).")
        if args.once:
            return
        time.sleep(args.poll_interval)


if __name__ == "__main__":
    main()
