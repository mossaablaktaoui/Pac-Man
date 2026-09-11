import json
import sys
from pathlib import Path
from typing import Any


class ConfigError(Exception):
    pass


class Config:
    def __init__(self) -> None:
        self.filename = self.parse_args()

        self.highscore_filename = "highscores.json"
        self.lives = 3
        self.pacgum = 42
        self.points_per_pacgum = 120
        self.points_per_super_pacgum = 50
        self.points_per_ghost = 200
        self.seed = 42
        self.level_max_time = 120

        self.load()

    def parse_args(self) -> Path:
        """Parse the configuration file argument."""
        args = sys.argv[1:]

        if len(args) != 1:
            raise ConfigError(
                "Error: Expected exactly 1 argument (config file)."
            )

        filename = Path(args[0])

        if filename.suffix.lower() != ".json":
            raise ConfigError("Error: Config file must be a JSON file.")

        return filename

    def read_file(self) -> str:
        """Read config file."""
        try:
            if not self.filename.is_file():
                self.create_config()

            with open(self.filename, "r") as file:
                return file.read()

        except OSError as error:
            raise ConfigError(
                f"Cannot read config file: {error}"
            ) from error

    def remove_comments(self, content: str) -> str:
        """Remove lines starting with #."""
        if not content:
            return ""

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
            raise ConfigError(
                "Config file has invalid JSON format"
            ) from error

        if not isinstance(data, dict):
            raise ConfigError("Config must contain a JSON object")

        return data

    def validate(self, config: dict[str, Any]) -> None:
        """Check values and apply safe defaults."""
        filename = config.get("highscore_filename")

        if isinstance(filename, str) and filename:
            self.highscore_filename = filename
        elif filename is not None:
            print(
                "Warning: invalid 'highscore_filename', "
                "using default value"
            )

        numeric_keys = [
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

            if value is None:
                print(
                    f"Warning: missing '{key}', "
                    "using default value"
                )
                continue

            if (
                not isinstance(value, int)
                or isinstance(value, bool)
                or value < 0
                or (key == "pacgum" and value < 4)):

                print(f"Warning: invalid '{key}', "
                      "using default value")
                continue

            setattr(self, key, value)

    def create_config(self) -> None:
        """Create a config file using default values."""
        try:
            with open(self.filename, "w") as json_file:
                json.dump(
                    {
                        "highscore_filename": self.highscore_filename,
                        "lives": self.lives,
                        "pacgum": self.pacgum,
                        "points_per_pacgum": self.points_per_pacgum,
                        "points_per_super_pacgum":
                            self.points_per_super_pacgum,
                        "points_per_ghost": self.points_per_ghost,
                        "seed": self.seed,
                        "level_max_time": self.level_max_time,
                    },
                    json_file,
                    indent=4,
                )

        except OSError as error:
            raise ConfigError(
                f"Cannot create config file: {error}")

    def load(self) -> None:
        """Run the complete parsing process."""
        content = self.read_file()
        content = self.remove_comments(content)
        config = self.parse_json(content)
        self.validate(config)
