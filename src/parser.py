import json
from typing import Any


class ConfigError(Exception):
    pass


class ConfigParser:
    DEFAULTS = {
        "highscore_filename": "highscores.json",
        "level": [],
        "width": 20,
        "height": 20,
        "lives": 3,
        "pacgum": 42,
        "points_per_pacgum": 10,
        "points_per_super_pacgum": 50,
        "points_per_ghost": 200,
        "seed": 42,
        "level_max_time": 90,
    }

    def __init__(self, filename: str) -> None:
        self.filename = filename

    def read_file(self) -> str:
        """Read config file."""
        try:
            with open(self.filename, "r") as file:
                return file.read()
        except Exception as error:
            raise ConfigError(f"Cannot read config file: {error}") from error

    def remove_comments(self, content: str) -> str:
        """Remove lines starting with #."""
        result = []

        for line in content.splitlines():
            if line.strip().startswith("#"):
                continue
            result.append(line)

        return "\n".join(result)

    def parse_json(self, content: str) -> dict[str, Any]:
        """Convert JSON text into a dictionary."""
        try:
            data = json.loads(content)
        except json.JSONDecodeError as error:
            raise ConfigError("Config file has invalid JSON format") from error

        if not isinstance(data, dict):
            raise ConfigError("Config must contain a JSON object")

        return data

    def validate(self, config: dict[str, Any]) -> dict[str, Any]:
        """Check values and apply safe defaults."""
        result = self.DEFAULTS.copy()

        filename = config.get("highscore_filename")
        if isinstance(filename, str) and filename:
            result["highscore_filename"] = filename

        levels = config.get("level")
        if isinstance(levels, list):
            result["level"] = levels

        numeric_keys = [
            "width",
            "height",
            "lives",
            "pacgum",
            "points_per_pacgum",
            "points_per_super_pacgum",
            "points_per_ghost",
            "seed",
            "level_max_time",
        ]

        for key in numeric_keys:
            value = config.get(key)

            if isinstance(value, int) and value >= 0:
                result[key] = value

        return result

    def load(self) -> dict[str, Any]:
        """Run the complete parsing process."""
        content = self.read_file()
        content = self.remove_comments(content)
        config = self.parse_json(content)
        return self.validate(config)
