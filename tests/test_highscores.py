"""Unit tests for highscore loading, validation, and persistence."""

import json
import tempfile
import unittest
from pathlib import Path

from src.core.highscores import HighscoreManager, HighscoreManagerError


class TestHighscores(unittest.TestCase):
    """Test cases verifying HighscoreManager persistence logic."""

    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.file_path = str(Path(self.temp_dir.name) / "test_scores.json")

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_missing_file_initializes_empty_list(self) -> None:
        manager = HighscoreManager(self.file_path)
        self.assertEqual(manager.get_highscores(), [])
        self.assertEqual(manager.get_highscore(), 0)

    def test_load_valid_scores_sorted_descending(self) -> None:
        sample_data = [
            {"name": "PLAYER1", "score": 5000},
            {"name": "PLAYER2", "score": 9000},
            {"name": "PLAYER3", "score": 1200},
        ]
        with open(self.file_path, "w") as f:
            json.dump(sample_data, f)

        manager = HighscoreManager(self.file_path)
        scores = manager.get_highscores()
        self.assertEqual(len(scores), 3)
        self.assertEqual(scores[0]["score"], 9000)
        self.assertEqual(scores[1]["score"], 5000)
        self.assertEqual(scores[2]["score"], 1200)
        self.assertEqual(manager.get_highscore(), 9000)

    def test_corrupted_file_raises_error(self) -> None:
        with open(self.file_path, "w") as f:
            f.write("{ invalid json }")

        with self.assertRaises(HighscoreManagerError):
            HighscoreManager(self.file_path)

    def test_non_list_file_raises_error(self) -> None:
        with open(self.file_path, "w") as f:
            json.dump({"not": "a list"}, f)

        with self.assertRaises(HighscoreManagerError):
            HighscoreManager(self.file_path)

    def test_invalid_entry_raises_error(self) -> None:
        bad_entries = [
            {"name": "TOOLONGNAMEXXX", "score": 100},
            {"name": "VALID", "score": -50},
            {"name": "VALID", "score": "not_int"},
        ]
        for entry in bad_entries:
            with open(self.file_path, "w") as f:
                json.dump([entry], f)
            with self.assertRaises(HighscoreManagerError):
                HighscoreManager(self.file_path)

    def test_validate_name(self) -> None:
        manager = HighscoreManager(self.file_path)
        self.assertTrue(manager.validate_name("PACMAN"))
        self.assertTrue(manager.validate_name("ALAKTAOU"))
        self.assertTrue(manager.validate_name("M LAKTAOU"))
        self.assertTrue(manager.validate_name("1234567890"))

        # Invalid names
        self.assertFalse(manager.validate_name(""))
        # Over 10 characters or disallowed symbols
        self.assertFalse(manager.validate_name("WAYTOOLONGNAME"))
        self.assertFalse(manager.validate_name("PAC-MAN"))
        self.assertFalse(manager.validate_name("USER@42"))

    def test_add_score_and_save(self) -> None:
        manager = HighscoreManager(self.file_path)
        self.assertTrue(manager.add_score("PACMAN", 2500))
        self.assertTrue(manager.add_score("GHOST", 5000))
        manager.save_scores()

        # Reload from disk
        reloaded = HighscoreManager(self.file_path)
        scores = reloaded.get_highscores()
        self.assertEqual(len(scores), 2)
        self.assertEqual(scores[0]["name"], "GHOST")
        self.assertEqual(scores[0]["score"], 5000)
        self.assertEqual(scores[1]["name"], "PACMAN")
        self.assertEqual(scores[1]["score"], 2500)

    def test_add_score_invalid_inputs(self) -> None:
        manager = HighscoreManager(self.file_path)
        with self.assertRaises(HighscoreManagerError):
            manager.add_score("", 1000)
        with self.assertRaises(HighscoreManagerError):
            manager.add_score("VALID", -10)

    def test_top_10_truncation(self) -> None:
        manager = HighscoreManager(self.file_path)
        for i in range(15):
            manager.add_score(f"P{i}", (i + 1) * 100)

        scores = manager.get_highscores()
        self.assertEqual(len(scores), 10)
        self.assertEqual(scores[0]["score"], 1500)
        self.assertEqual(scores[-1]["score"], 600)


if __name__ == "__main__":
    unittest.main()
