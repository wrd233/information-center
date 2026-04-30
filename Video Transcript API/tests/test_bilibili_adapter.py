from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path

from app.bilibili_adapter import (
    BBDownConfig,
    BilibiliAdapter,
    build_transcript_text,
    redact_command,
    strip_srt_or_vtt,
)


class BilibiliAdapterTest(unittest.TestCase):
    def test_strip_srt(self) -> None:
        text = """1
00:00:00,000 --> 00:00:01,000
你好，世界

2
00:00:01,000 --> 00:00:02,000
你好，世界

3
00:00:02,000 --> 00:00:03,000
第二句
"""
        self.assertEqual(strip_srt_or_vtt(text), "你好，世界\n第二句")

    def test_redacts_cookie(self) -> None:
        command = ["BBDown", "BV1xx", "--cookie", "SESSDATA=secret"]
        self.assertEqual(redact_command(command), ["BBDown", "BV1xx", "--cookie", "***"])

    def test_process_keeps_audio_when_subtitle_exists_by_default(self) -> None:
        calls = []

        def runner(command: list[str], cwd: Path, timeout: int):
            calls.append(command)
            if "--sub-only" in command:
                (cwd / "test.srt").write_text(
                    "1\n00:00:00,000 --> 00:00:01,000\n字幕正文\n",
                    encoding="utf-8",
                )
            if "--audio-only" in command:
                (cwd / "test.m4a").write_bytes(b"audio")
            return subprocess.CompletedProcess(command, 0, stdout="标题: 测试视频\nP1 第一集")

        with tempfile.TemporaryDirectory() as temp_dir:
            adapter = BilibiliAdapter(BBDownConfig(binary="python3"), runner=runner)
            result = adapter.process("BV1xx411c7mD", Path(temp_dir))

        self.assertEqual(result["status"], "subtitle_ready")
        self.assertEqual(result["transcript_text"], "字幕正文")
        self.assertTrue(any("--audio-only" in call for call in calls))
        self.assertEqual(result["audio"][0]["relative_path"], "audio/test.m4a")

    def test_build_transcript_from_json(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "sub.json"
            path.write_text('{"body":[{"content":"第一句"},{"content":"第二句"}]}', encoding="utf-8")
            self.assertEqual(build_transcript_text([path]), "第一句\n第二句")


if __name__ == "__main__":
    unittest.main()
