import json
from typing import Any


class HighscoreManagerError(Exception):
    pass


class HighscoreManager:
    def __init__(self, filename: str) -> None:
        self.filename = filename
        self.scores: list[dict[str, Any]] = []

    def load_scores(self) -> None:
        """Load highscores from file."""
        try:
            with open(self.filename, "r") as file:
                data = json.load(file)

            if isinstance(data, list):
                self.scores = data

        except (OSError, json.JSONDecodeError):
            raise HighscoreManagerError("High scores file doesn't"
                                        " fit a JSON list object")

    def validate_name(self, name: str) -> bool:
        """Check player name."""
        return 0 < len(name) <= 10 and all(
            char.isalnum() or char == " " for char in name
        )

    def add_score(self, name: str, score: int) -> bool:
        """Add a new score."""
        if not self.validate_name(name):
            raise HighscoreManagerError("the name is not valid")

        if score < 0:
            raise HighscoreManagerError("the score is not valid")

        self.scores.append(
            {
                "name": name,
                "score": score,
            }
        )

        self.scores.sort(key=lambda item: item["score"],
                         reverse=True)

        self.scores = self.scores[:10]
        return True

    def save_scores(self) -> None:
        """Save highscores to file."""
        try:
            with open(self.filename, "w") as file:
                json.dump(self.scores, file, indent=4)
        except OSError:
            pass

    def get_top_10(self) -> list[dict[str, Any]]:
        """Return the top 10 highscores."""
        return self.scores[:10]
