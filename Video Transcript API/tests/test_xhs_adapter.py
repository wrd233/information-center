from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from app.xhs_adapter import (
    AdapterError,
    XHSAdapter,
    XHSDownloaderConfig,
    extract_download_urls,
    extract_text,
)


class XHSAdapterTest(unittest.TestCase):
    def test_extracts_video_urls_from_xhs_data(self) -> None:
        self.assertEqual(
            extract_download_urls({"下载地址": "https://cdn.example/a.mp4 https://cdn.example/b.mp4"}),
            ["https://cdn.example/a.mp4", "https://cdn.example/b.mp4"],
        )
        self.assertEqual(
            extract_download_urls({"下载地址": ["https://cdn.example/a.mp4"]}),
            ["https://cdn.example/a.mp4"],
        )

    def test_extracts_text_from_title_and_description(self) -> None:
        self.assertEqual(
            extract_text({"作品标题": "标题", "作品描述": "正文"}),
            "标题\n正文",
        )

    def test_process_downloads_video_and_extracts_audio(self) -> None:
        requests = []
        commands = []

        def http_client(url: str, payload: dict, timeout: int) -> dict:
            requests.append((url, payload, timeout))
            return {
                "message": "获取小红书作品数据成功",
                "data": {
                    "作品ID": "abc123",
                    "作品类型": "视频",
                    "作品标题": "测试视频",
                    "作品描述": "小红书文案",
                    "作者昵称": "作者",
                    "下载地址": ["https://cdn.example/video.mp4"],
                },
            }

        def fake_download(url: str, directory: Path, filename_hint: str, timeout_seconds: int) -> Path:
            path = directory / "video.mp4"
            path.write_bytes(b"fake video")
            return path

        def runner(command: list[str], cwd: Path, timeout: int):
            commands.append(command)
            Path(command[-1]).write_bytes(b"fake audio")
            return subprocess.CompletedProcess(command, 0, stdout="ok")

        with tempfile.TemporaryDirectory() as temp_dir:
            adapter = XHSAdapter(
                XHSDownloaderConfig(
                    api_base_url="http://127.0.0.1:5556",
                    cookie="a1=secret",
                    ffmpeg_path="python3",
                ),
                http_client=http_client,
                runner=runner,
            )
            with patch("app.xhs_adapter.download_file", side_effect=fake_download):
                result = adapter.process(
                    "https://www.xiaohongshu.com/explore/abc123?xsec_token=xxx",
                    Path(temp_dir),
                )

        self.assertEqual(result["status"], "audio_ready_for_asr")
        self.assertEqual(result["title"], "测试视频")
        self.assertEqual(result["text"], "测试视频\n小红书文案")
        self.assertEqual(result["raw_requests"][0]["payload"]["cookie"], "***")
        self.assertEqual(requests[0][1]["download"], False)
        self.assertTrue(commands)
        self.assertEqual(result["audio"][0]["relative_path"], "audio/video.m4a")

    def test_rejects_non_xhs_url(self) -> None:
        adapter = XHSAdapter(http_client=lambda *_: {})
        with tempfile.TemporaryDirectory() as temp_dir:
            with self.assertRaises(AdapterError):
                adapter.process("https://example.com/video/1", Path(temp_dir))


if __name__ == "__main__":
    unittest.main()
