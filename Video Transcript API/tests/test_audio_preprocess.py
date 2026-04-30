from __future__ import annotations

import unittest

from app.audio_preprocess import AudioPreprocessConfig, choose_selection


class AudioPreprocessTest(unittest.TestCase):
    def test_short_audio_uses_full_selection(self) -> None:
        selection = choose_selection(299.9, AudioPreprocessConfig())
        self.assertEqual(selection["mode"], "full")
        self.assertEqual(selection["windows"], [{"start": 0.0, "duration": 299.9}])

    def test_long_audio_samples_head_middle_and_tail(self) -> None:
        selection = choose_selection(600.0, AudioPreprocessConfig())
        self.assertEqual(selection["mode"], "sampled")
        self.assertEqual(
            selection["windows"],
            [
                {"start": 0.0, "duration": 120.0},
                {"start": 240.0, "duration": 120.0},
                {"start": 540.0, "duration": 60.0},
            ],
        )


if __name__ == "__main__":
    unittest.main()
