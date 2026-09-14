"""Unit tests for configuration parsing, validation, and defaults."""

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from src.core.config import Config, ConfigError


class TestConfig(unittest.TestCase):
    """Test cases verifying Config behavior, comments, and fallbacks."""

    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.config_path = Path(self.temp_dir.name) / 'test_config.json'
        valid_data = {
            'highscore_filename': 'scores_test.json',
            'lives': 5,
            'pacgum': 50,
            'points_per_pacgum': 100,
            'points_per_super_pacgum': 250,
            'points_per_ghost': 400,
            'seed': 99,
            'level_max_time': 150,
        }
        with open(self.config_path, 'w') as f:
            json.dump(valid_data, f)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_parse_args_valid(self) -> None:
        with patch.object(sys, 'argv', ['pac-man.py', str(self.config_path)]):
            config = Config()
            self.assertEqual(config.filename, self.config_path)
            self.assertEqual(config.lives, 5)
            self.assertEqual(config.pacgum, 50)
            self.assertEqual(config.seed, 99)

    def test_parse_args_no_argument(self) -> None:
        with patch.object(sys, 'argv', ['pac-man.py']):
            with self.assertRaises(ConfigError) as ctx:
                Config()
            self.assertIn('Expected exactly 1 argument', str(ctx.exception))

    def test_parse_args_too_many_arguments(self) -> None:
        with patch.object(
            sys, 'argv', ['pac-man.py', 'cfg1.json', 'cfg2.json']
        ):
            with self.assertRaises(ConfigError) as ctx:
                Config()
            self.assertIn('Expected exactly 1 argument', str(ctx.exception))

    def test_parse_args_invalid_extension(self) -> None:
        bad_path = Path(self.temp_dir.name) / 'config.txt'
        with patch.object(sys, 'argv', ['pac-man.py', str(bad_path)]):
            with self.assertRaises(ConfigError) as ctx:
                Config()
            self.assertIn('must be a JSON file', str(ctx.exception))

    def test_remove_comments(self) -> None:
        with patch.object(sys, 'argv', ['pac-man.py', str(self.config_path)]):
            config = Config()
            sample_lines = [
                '# Header comment',
                '{',
                '    # Inside comment',
                '    "lives": 3',
                '}',
            ]
            content = chr(10).join(sample_lines)
            cleaned = config.remove_comments(content)
            self.assertNotIn('# Header comment', cleaned)
            self.assertNotIn('# Inside comment', cleaned)
            self.assertIn('"lives": 3', cleaned)
            self.assertEqual(config.remove_comments(''), '')

    def test_parse_json_invalid_format(self) -> None:
        with patch.object(sys, 'argv', ['pac-man.py', str(self.config_path)]):
            config = Config()
            with self.assertRaises(ConfigError) as ctx:
                config.parse_json('{ invalid json format }')
            self.assertIn('invalid JSON format', str(ctx.exception))

    def test_parse_json_non_dict(self) -> None:
        with patch.object(sys, 'argv', ['pac-man.py', str(self.config_path)]):
            config = Config()
            with self.assertRaises(ConfigError) as ctx:
                config.parse_json('[1, 2, 3]')
            self.assertIn('must contain a JSON object', str(ctx.exception))

    def test_validate_defaults_on_missing_keys(self) -> None:
        sparse_file = Path(self.temp_dir.name) / 'sparse.json'
        with open(sparse_file, 'w') as f:
            json.dump({}, f)
        with patch.object(sys, 'argv', ['pac-man.py', str(sparse_file)]):
            config = Config()
            self.assertEqual(config.highscore_filename, 'highscores.json')
            self.assertEqual(config.lives, 3)
            self.assertEqual(config.pacgum, 42)
            self.assertEqual(config.points_per_pacgum, 120)
            self.assertEqual(config.points_per_super_pacgum, 50)
            self.assertEqual(config.points_per_ghost, 200)
            self.assertEqual(config.seed, 42)
            self.assertEqual(config.level_max_time, 120)

    def test_validate_clamps_invalid_values(self) -> None:
        invalid_data = {
            'highscore_filename': '',
            'lives': -3,
            'pacgum': 2,
            'points_per_pacgum': 'not_an_int',
            'points_per_ghost': True,
        }
        bad_file = Path(self.temp_dir.name) / 'bad.json'
        with open(bad_file, 'w') as f:
            json.dump(invalid_data, f)
        with patch.object(sys, 'argv', ['pac-man.py', str(bad_file)]):
            config = Config()
            self.assertEqual(config.highscore_filename, 'highscores.json')
            self.assertEqual(config.lives, 3)
            self.assertEqual(config.pacgum, 42)
            self.assertEqual(config.points_per_pacgum, 120)
            self.assertEqual(config.points_per_ghost, 200)

    def test_auto_create_config_if_missing(self) -> None:
        missing_file = Path(self.temp_dir.name) / 'non_existent.json'
        self.assertFalse(missing_file.exists())
        with patch.object(sys, 'argv', ['pac-man.py', str(missing_file)]):
            config = Config()
            self.assertTrue(missing_file.is_file())
            self.assertEqual(config.lives, 3)


if __name__ == '__main__':
    unittest.main()
