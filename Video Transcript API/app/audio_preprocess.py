from __future__ import annotations

import json
import os
import shutil
import subprocess
import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from app.bilibili_adapter import as_artifact


Runner = Callable[[list[str], Path, int], subprocess.CompletedProcess[str]]


@dataclass(frozen=True)
class AudioPreprocessConfig:
    enabled: bool = True
    ffmpeg_path: str = "ffmpeg"
    ffprobe_path: str = "ffprobe"
    sample_rate: int = 16000
    timeout_seconds: int = 1800
    vad_enabled: bool = True
    vad_threshold: float = 0.5
    vad_min_speech_ms: int = 250
    vad_min_silence_ms: int = 100
    vad_speech_pad_ms: int = 120
    vad_onnx: bool = True
    full_duration_threshold_seconds: float = 300.0
    long_head_seconds: float = 120.0
    long_middle_seconds: float = 120.0
    long_tail_seconds: float = 60.0


class AudioPreprocessError(RuntimeError):
    pass


def config_from_env() -> AudioPreprocessConfig:
    return AudioPreprocessConfig(
        enabled=os.getenv("ASR_PREPROCESS_ENABLED", "1") != "0",
        ffmpeg_path=os.getenv("FFMPEG_PATH", "ffmpeg"),
        ffprobe_path=os.getenv("FFPROBE_PATH", "ffprobe"),
        sample_rate=int(os.getenv("ASR_SAMPLE_RATE", "16000")),
        timeout_seconds=int(os.getenv("ASR_PREPROCESS_TIMEOUT_SECONDS", "1800")),
        vad_enabled=os.getenv("ASR_VAD_ENABLED", "1") != "0",
        vad_threshold=float(os.getenv("ASR_VAD_THRESHOLD", "0.5")),
        vad_min_speech_ms=int(os.getenv("ASR_VAD_MIN_SPEECH_MS", "250")),
        vad_min_silence_ms=int(os.getenv("ASR_VAD_MIN_SILENCE_MS", "100")),
        vad_speech_pad_ms=int(os.getenv("ASR_VAD_SPEECH_PAD_MS", "120")),
        vad_onnx=os.getenv("ASR_VAD_ONNX", "1") != "0",
        full_duration_threshold_seconds=float(os.getenv("ASR_FULL_DURATION_SECONDS", "300")),
        long_head_seconds=float(os.getenv("ASR_LONG_HEAD_SECONDS", "120")),
        long_middle_seconds=float(os.getenv("ASR_LONG_MIDDLE_SECONDS", "120")),
        long_tail_seconds=float(os.getenv("ASR_LONG_TAIL_SECONDS", "60")),
    )


def check_dependencies(config: AudioPreprocessConfig | None = None) -> dict:
    cfg = config or config_from_env()
    silero_available = True
    try:
        import silero_vad  # noqa: F401
    except ImportError:
        silero_available = False
    return {
        "enabled": cfg.enabled,
        "ffmpeg": shutil.which(cfg.ffmpeg_path),
        "ffprobe": shutil.which(cfg.ffprobe_path),
        "sample_rate": cfg.sample_rate,
        "vad": {
            "enabled": cfg.vad_enabled,
            "engine": "silero_vad",
            "python_package": silero_available,
            "onnx": cfg.vad_onnx,
            "threshold": cfg.vad_threshold,
        },
        "selection": {
            "full_duration_threshold_seconds": cfg.full_duration_threshold_seconds,
            "long_head_seconds": cfg.long_head_seconds,
            "long_middle_seconds": cfg.long_middle_seconds,
            "long_tail_seconds": cfg.long_tail_seconds,
        },
    }


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


def preprocess_for_rough_asr(
    audio_path: Path,
    workspace: Path,
    config: AudioPreprocessConfig | None = None,
    runner: Runner = default_runner,
) -> dict:
    cfg = config or config_from_env()
    if not cfg.enabled:
        duration = probe_duration(audio_path, cfg, runner)
        return {
            "status": "disabled",
            "input": str(audio_path),
            "audio_path": str(audio_path),
            "duration_seconds": duration,
            "selected_duration_seconds": duration,
            "vad": {"enabled": False},
            "selection": {"mode": "full"},
        }

    output_dir = workspace / "asr_preprocess"
    output_dir.mkdir(parents=True, exist_ok=True)
    normalized_path = output_dir / "normalized_16k_mono.wav"
    normalize_to_wav(audio_path, normalized_path, cfg, runner)
    original_duration = probe_duration(normalized_path, cfg, runner)

    vad_path = normalized_path
    vad_segments: list[dict] = []
    vad_status = "disabled"
    if cfg.vad_enabled:
        vad_path = output_dir / "vad_speech_16k_mono.wav"
        vad_segments = run_silero_vad(normalized_path, vad_path, cfg)
        vad_status = "applied" if vad_segments else "no_speech_fallback_to_normalized"
        if not vad_segments:
            vad_path = normalized_path

    speech_duration = probe_duration(vad_path, cfg, runner)
    selected_path = output_dir / "rough_asr_input.wav"
    selection = choose_selection(speech_duration, cfg)
    if selection["mode"] == "full":
        shutil.copyfile(vad_path, selected_path)
    else:
        cut_and_concat(vad_path, selected_path, selection["windows"], cfg, runner)
    selected_duration = probe_duration(selected_path, cfg, runner)

    payload = {
        "status": "ready",
        "input": str(audio_path),
        "audio_path": str(selected_path),
        "normalized": as_artifact(normalized_path, workspace),
        "original_duration_seconds": original_duration,
        "speech_duration_seconds": speech_duration,
        "selected_duration_seconds": selected_duration,
        "vad": {
            "enabled": cfg.vad_enabled,
            "engine": "silero_vad",
            "status": vad_status,
            "segments": vad_segments,
            "speech_audio": as_artifact(vad_path, workspace),
        },
        "selection": selection,
        "artifact": as_artifact(selected_path, workspace),
    }
    (output_dir / "preprocess_result.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return payload


def normalize_to_wav(
    input_path: Path,
    output_path: Path,
    config: AudioPreprocessConfig,
    runner: Runner,
) -> None:
    command = [
        config.ffmpeg_path,
        "-y",
        "-i",
        str(input_path.resolve()),
        "-vn",
        "-ac",
        "1",
        "-ar",
        str(config.sample_rate),
        "-acodec",
        "pcm_s16le",
        str(output_path.resolve()),
    ]
    completed = runner(command, output_path.parent, config.timeout_seconds)
    if completed.returncode != 0 or not output_path.exists():
        raise AudioPreprocessError(f"ffmpeg failed to normalize audio: {completed.stdout}")


def run_silero_vad(
    input_path: Path,
    output_path: Path,
    config: AudioPreprocessConfig,
) -> list[dict]:
    try:
        from silero_vad import (
            collect_chunks,
            get_speech_timestamps,
            load_silero_vad,
            read_audio,
            save_audio,
        )
    except ImportError as exc:
        raise AudioPreprocessError(
            "Silero VAD is enabled but the 'silero-vad' package is not installed. "
            "Install it with: pip install 'silero-vad[onnx-cpu]'"
        ) from exc

    model = load_silero_vad(onnx=config.vad_onnx)
    wav = read_audio(str(input_path), sampling_rate=config.sample_rate)
    timestamps = get_speech_timestamps(
        wav,
        model,
        sampling_rate=config.sample_rate,
        threshold=config.vad_threshold,
        min_speech_duration_ms=config.vad_min_speech_ms,
        min_silence_duration_ms=config.vad_min_silence_ms,
        speech_pad_ms=config.vad_speech_pad_ms,
        return_seconds=True,
    )
    segments = [
        {
            "start": float(item["start"]),
            "end": float(item["end"]),
            "duration": round(float(item["end"]) - float(item["start"]), 3),
        }
        for item in timestamps
    ]
    if not segments:
        return []
    speech = collect_chunks(timestamps, wav, seconds=True, sampling_rate=config.sample_rate)
    save_audio(str(output_path), speech, sampling_rate=config.sample_rate)
    return segments


def choose_selection(duration_seconds: float, config: AudioPreprocessConfig) -> dict:
    if duration_seconds <= config.full_duration_threshold_seconds:
        return {"mode": "full", "windows": [{"start": 0.0, "duration": duration_seconds}]}

    head = clamp_window(0.0, config.long_head_seconds, duration_seconds)
    middle_start = max((duration_seconds - config.long_middle_seconds) / 2, 0.0)
    middle = clamp_window(middle_start, config.long_middle_seconds, duration_seconds)
    tail_start = max(duration_seconds - config.long_tail_seconds, 0.0)
    tail = clamp_window(tail_start, config.long_tail_seconds, duration_seconds)
    return {"mode": "sampled", "windows": merge_windows([head, middle, tail])}


def clamp_window(start: float, duration: float, total_duration: float) -> dict:
    start = max(0.0, min(start, total_duration))
    end = max(start, min(start + duration, total_duration))
    return {
        "start": round(start, 3),
        "duration": round(end - start, 3),
    }


def merge_windows(windows: list[dict]) -> list[dict]:
    ordered = sorted(
        (window for window in windows if window["duration"] > 0),
        key=lambda window: window["start"],
    )
    merged: list[dict] = []
    for window in ordered:
        start = float(window["start"])
        end = start + float(window["duration"])
        if merged and start <= merged[-1]["start"] + merged[-1]["duration"]:
            merged[-1]["duration"] = round(
                max(merged[-1]["start"] + merged[-1]["duration"], end) - merged[-1]["start"],
                3,
            )
        else:
            merged.append({"start": round(start, 3), "duration": round(end - start, 3)})
    return merged


def cut_and_concat(
    input_path: Path,
    output_path: Path,
    windows: list[dict],
    config: AudioPreprocessConfig,
    runner: Runner,
) -> None:
    part_paths = []
    for index, window in enumerate(windows):
        part_path = output_path.with_name(f"{output_path.stem}.part{index}.wav")
        command = [
            config.ffmpeg_path,
            "-y",
            "-ss",
            str(window["start"]),
            "-t",
            str(window["duration"]),
            "-i",
            str(input_path.resolve()),
            "-acodec",
            "pcm_s16le",
            str(part_path.resolve()),
        ]
        completed = runner(command, output_path.parent, config.timeout_seconds)
        if completed.returncode != 0 or not part_path.exists():
            raise AudioPreprocessError(f"ffmpeg failed to cut audio: {completed.stdout}")
        part_paths.append(part_path)

    concat_list = output_path.with_name(f"{output_path.stem}.concat.txt")
    concat_list.write_text(
        "\n".join(f"file '{path.name}'" for path in part_paths),
        encoding="utf-8",
    )
    command = [
        config.ffmpeg_path,
        "-y",
        "-f",
        "concat",
        "-safe",
        "0",
        "-i",
        str(concat_list.resolve()),
        "-c",
        "copy",
        str(output_path.resolve()),
    ]
    completed = runner(command, output_path.parent, config.timeout_seconds)
    if completed.returncode != 0 or not output_path.exists():
        raise AudioPreprocessError(f"ffmpeg failed to concat audio: {completed.stdout}")
    for path in [*part_paths, concat_list]:
        path.unlink(missing_ok=True)


def probe_duration(
    path: Path,
    config: AudioPreprocessConfig,
    runner: Runner,
) -> float:
    command = [
        config.ffprobe_path,
        "-v",
        "error",
        "-show_entries",
        "format=duration",
        "-of",
        "default=noprint_wrappers=1:nokey=1",
        str(path.resolve()),
    ]
    completed = runner(command, path.parent, config.timeout_seconds)
    if completed.returncode != 0:
        raise AudioPreprocessError(f"ffprobe failed: {completed.stdout}")
    try:
        return round(float((completed.stdout or "0").strip()), 3)
    except ValueError as exc:
        raise AudioPreprocessError(f"Unable to parse ffprobe duration: {completed.stdout}") from exc


def main() -> None:
    parser = argparse.ArgumentParser(description="Prepare audio for rough ASR.")
    parser.add_argument("audio")
    parser.add_argument("--workspace", default=None)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    audio_path = Path(args.audio)
    workspace = Path(args.workspace) if args.workspace else audio_path.parent.parent
    result = preprocess_for_rough_asr(audio_path, workspace)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(result["audio_path"])


if __name__ == "__main__":
    main()
