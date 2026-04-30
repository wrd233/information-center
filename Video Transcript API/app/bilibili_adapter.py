from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Iterable


Runner = Callable[[list[str], Path, int], subprocess.CompletedProcess[str]]


SUPPORTED_INPUT_RE = re.compile(
    r"(bilibili\.com/(video|bangumi)|^BV[0-9A-Za-z]+$|^av\d+$|^AV\d+$|^ep\d+$|^ss\d+$)"
)


@dataclass(frozen=True)
class BBDownConfig:
    binary: str = "BBDown"
    ffmpeg_path: str | None = None
    cookie: str | None = None
    timeout_seconds: int = 1800


class AdapterError(RuntimeError):
    pass


def default_runner(
    command: list[str], cwd: Path, timeout_seconds: int
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=str(cwd),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=timeout_seconds,
        check=False,
    )


class BilibiliAdapter:
    """Small BBDown wrapper for Bilibili capture.

    The adapter intentionally stops at acquisition. It does not run ASR,
    summarization, storage routing, or knowledge-base logic.
    """

    def __init__(self, config: BBDownConfig | None = None, runner: Runner = default_runner):
        self.config = config or BBDownConfig()
        self.runner = runner

    def check_dependencies(self) -> dict:
        return {
            "bbdown": shutil.which(self.config.binary) is not None,
            "bbdown_binary": shutil.which(self.config.binary),
            "ffmpeg": shutil.which(self.config.ffmpeg_path or "ffmpeg"),
            "configured_binary": self.config.binary,
        }

    def process(
        self,
        url: str,
        workspace: Path,
        select_page: str = "ALL",
        download_audio_if_no_subtitle: bool = True,
        download_audio: bool = True,
    ) -> dict:
        if not SUPPORTED_INPUT_RE.search(url):
            raise AdapterError("Input does not look like a Bilibili BV/AV/ep/ss id or URL.")

        deps = self.check_dependencies()
        if not deps["bbdown"]:
            raise AdapterError(
                f"BBDown binary not found: {self.config.binary}. Install it or set BBDOWN_BIN."
            )

        workspace.mkdir(parents=True, exist_ok=True)
        metadata_dir = workspace / "metadata"
        subtitle_dir = workspace / "subtitles"
        cover_dir = workspace / "cover"
        audio_dir = workspace / "audio"
        for directory in (metadata_dir, subtitle_dir, cover_dir, audio_dir):
            directory.mkdir(parents=True, exist_ok=True)

        commands: list[dict] = []

        info = self._run_bbdown(
            url,
            metadata_dir,
            ["--only-show-info", "--show-all", "--select-page", select_page],
        )
        commands.append(public_command_record(info))

        subtitle = self._run_bbdown(
            url,
            subtitle_dir,
            ["--sub-only", "--show-all", "--select-page", select_page],
        )
        commands.append(public_command_record(subtitle))

        cover = self._run_bbdown(
            url,
            cover_dir,
            ["--cover-only", "--select-page", select_page],
        )
        commands.append(public_command_record(cover))

        subtitles = list_media_files(subtitle_dir, {".srt", ".vtt", ".ass", ".json", ".lrc"})
        acquisition_status = "subtitle_ready" if subtitles else "subtitle_missing"

        should_download_audio = download_audio or (not subtitles and download_audio_if_no_subtitle)
        if should_download_audio:
            audio = self._run_bbdown(
                url,
                audio_dir,
                ["--audio-only", "--select-page", select_page],
            )
            commands.append(public_command_record(audio))
        audio_files = list_media_files(audio_dir, {".m4a", ".mp3", ".aac", ".flac", ".wav"})
        if not subtitles:
            acquisition_status = "audio_ready_for_asr" if audio_files else "failed_no_subtitle_or_audio"

        covers = list_media_files(cover_dir, {".jpg", ".jpeg", ".png", ".webp"})
        transcript_text = build_transcript_text(subtitles)

        result = {
            "platform": "bilibili",
            "source_url": url,
            "status": acquisition_status,
            "title": parse_title(info["output"]),
            "pages": parse_pages(info["output"]),
            "subtitles": [as_artifact(path, workspace) for path in subtitles],
            "audio": [as_artifact(path, workspace) for path in audio_files],
            "cover": as_artifact(covers[0], workspace) if covers else None,
            "transcript_text": transcript_text,
            "summary": simple_summary(transcript_text),
            "raw_commands": commands,
        }

        (workspace / "adapter_result.json").write_text(
            json.dumps(result, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        if transcript_text:
            (workspace / "transcript.txt").write_text(transcript_text, encoding="utf-8")
        return result

    def _run_bbdown(self, url: str, cwd: Path, options: list[str]) -> dict:
        command = [self.config.binary, url, *options, "--work-dir", str(cwd)]
        if self.config.ffmpeg_path:
            command.extend(["--ffmpeg-path", self.config.ffmpeg_path])
        if self.config.cookie or os.getenv("BBDOWN_COOKIE"):
            command.extend(["--cookie", self.config.cookie or os.environ["BBDOWN_COOKIE"]])

        completed = self.runner(command, cwd, self.config.timeout_seconds)
        output = completed.stdout or ""
        return {
            "command": redact_command(command),
            "exit_code": completed.returncode,
            "output_tail": sanitize_output(output[-4000:]),
            "output": output,
        }


def list_media_files(root: Path, suffixes: set[str]) -> list[Path]:
    return sorted(
        path for path in root.rglob("*") if path.is_file() and path.suffix.lower() in suffixes
    )


def as_artifact(path: Path, base: Path) -> dict:
    return {
        "path": str(path),
        "relative_path": str(path.relative_to(base)),
        "size_bytes": path.stat().st_size,
    }


def redact_command(command: list[str]) -> list[str]:
    redacted = []
    skip_next = False
    for part in command:
        if skip_next:
            redacted.append("***")
            skip_next = False
            continue
        redacted.append(part)
        if part in {"--cookie", "-c", "--access-token", "-token"}:
            skip_next = True
    return redacted


def public_command_record(record: dict) -> dict:
    return {
        "command": record["command"],
        "exit_code": record["exit_code"],
        "output_tail": record["output_tail"],
    }


def sanitize_output(output: str) -> str:
    return re.sub(r"https?://\S+", "[url]", output)


def parse_title(output: str) -> str | None:
    patterns = [
        r"(?:标题|Title)\s*[:：]\s*(.+)",
        r"(?:视频标题|Video Title)\s*[:：]\s*(.+)",
    ]
    for pattern in patterns:
        match = re.search(pattern, output)
        if match:
            return match.group(1).strip()
    return None


def parse_pages(output: str) -> list[dict]:
    pages: list[dict] = []
    for line in output.splitlines():
        match = re.search(r"(?:\] - )?P(\d+)\s*[:：]\s*(.+)", line.strip())
        if match:
            pages.append({"page": int(match.group(1)), "title": match.group(2).strip()})
    return pages


def build_transcript_text(paths: Iterable[Path]) -> str:
    chunks: list[str] = []
    for path in paths:
        if path.suffix.lower() in {".srt", ".vtt"}:
            chunks.append(strip_srt_or_vtt(path.read_text(encoding="utf-8", errors="ignore")))
        elif path.suffix.lower() == ".ass":
            chunks.append(strip_ass(path.read_text(encoding="utf-8", errors="ignore")))
        elif path.suffix.lower() == ".json":
            chunks.append(strip_json_subtitle(path.read_text(encoding="utf-8", errors="ignore")))
        else:
            chunks.append(path.read_text(encoding="utf-8", errors="ignore"))
    return "\n".join(chunk for chunk in chunks if chunk).strip()


def strip_srt_or_vtt(text: str) -> str:
    lines: list[str] = []
    seen = set()
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.isdigit() or "-->" in line or line.upper() == "WEBVTT":
            continue
        line = re.sub(r"<[^>]+>", "", line).strip()
        if line and line not in seen:
            seen.add(line)
            lines.append(line)
    return "\n".join(lines)


def strip_ass(text: str) -> str:
    lines: list[str] = []
    for raw in text.splitlines():
        if not raw.startswith("Dialogue:"):
            continue
        parts = raw.split(",", 9)
        if len(parts) == 10:
            line = re.sub(r"\{[^}]+\}", "", parts[-1]).replace(r"\N", "\n").strip()
            if line:
                lines.append(line)
    return "\n".join(lines)


def strip_json_subtitle(text: str) -> str:
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return ""
    candidates = data.get("body") if isinstance(data, dict) else data
    if not isinstance(candidates, list):
        return ""
    lines = []
    for item in candidates:
        if isinstance(item, dict):
            content = item.get("content") or item.get("text")
            if content:
                lines.append(str(content).strip())
    return "\n".join(line for line in lines if line)


def simple_summary(text: str, limit: int = 500) -> str | None:
    normalized = re.sub(r"\s+", " ", text).strip()
    if not normalized:
        return None
    return normalized[:limit] + ("..." if len(normalized) > limit else "")
