from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from app.asr_worker import ASRError, run_asr_for_task
from app.storage import TaskStore


class ASRWorkerTest(unittest.TestCase):
    def test_run_asr_for_task_writes_transcript_and_completes_job(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            store = TaskStore(Path(temp_dir))
            task = store.create({"url": "https://www.bilibili.com/video/BV1xx411c7mD"}, "bilibili")
            workspace = store.task_workspace(task["id"])
            audio = workspace / "audio" / "demo.m4a"
            audio.parent.mkdir(parents=True, exist_ok=True)
            audio.write_bytes(b"audio")
            task["status"] = "needs_asr"
            task["result"] = {
                "status": "audio_ready_for_asr",
                "audio": [
                    {
                        "path": str(audio),
                        "relative_path": "audio/demo.m4a",
                        "size_bytes": audio.stat().st_size,
                    }
                ],
            }
            store.save(task)

            with patch(
                "app.asr_worker.preprocess_for_rough_asr",
                return_value={"audio_path": str(audio), "status": "ready"},
            ), patch(
                "app.asr_worker.transcribe_file_sync",
                return_value={"engine": "funasr_paraformer", "text": "粗筛转录正文"},
            ):
                updated = run_asr_for_task(store, task["id"])

            self.assertEqual(updated["status"], "completed")
            self.assertEqual((workspace / "transcript.txt").read_text(encoding="utf-8"), "粗筛转录正文")
            self.assertEqual(updated["result"]["transcript_text"], "粗筛转录正文")
            self.assertEqual(updated["result"]["asr"]["status"], "asr_completed")

    def test_rejects_job_without_audio(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            store = TaskStore(Path(temp_dir))
            task = store.create({"url": "https://www.bilibili.com/video/BV1xx411c7mD"}, "bilibili")
            task["status"] = "needs_asr"
            task["result"] = {"audio": []}
            store.save(task)

            with self.assertRaises(ASRError):
                run_asr_for_task(store, task["id"])


if __name__ == "__main__":
    unittest.main()
