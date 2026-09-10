from typing import Any, List, Dict

from src.core.highscores import HighscoreManager
from src.core.maze_adapter import MazeAdapter
from src.core.config import Config
from src.core.entities import (
    GameStateDT,
    SpriteDT,
    PacgumDT,
    Direction,
    GhostState,
)
from src.core.cheats import Cheats, CheatCode


class GameEngine:
    def __init__(self) -> None:
        self.config = Config()

        self.maze = MazeAdapter(self.config.seed)
        self.gamestate = self.setup_game_state()
        self.cheats = Cheats(self.gamestate)
        self.highscoresmanager = HighscoreManager(self.config.highscore_filename)

    def setup_game_state(self) -> GameStateDT:
        """Create the initial game state."""
        width = self.maze.width
        height = self.maze.height

        pacman = SpriteDT(
            id="pacman",
            grid_x=width // 2,
            grid_y=height // 2,
            direction=Direction.RIGHT,
            state="ALIVE",
        )

        ghosts = [
            SpriteDT(
                id="blinky",
                grid_x=0,
                grid_y=0,
                direction=Direction.RIGHT,
                state=GhostState.NORMAL,
            ),
            SpriteDT(
                id="pinky",
                grid_x=width - 1,
                grid_y=0,
                direction=Direction.LEFT,
                state=GhostState.NORMAL,
            ),
            SpriteDT(
                id="inky",
                grid_x=0,
                grid_y=height - 1,
                direction=Direction.RIGHT,
                state=GhostState.NORMAL,
            ),
            SpriteDT(
                id="clyde",
                grid_x=width - 1,
                grid_y=height - 1,
                direction=Direction.LEFT,
                state=GhostState.NORMAL,
            ),
        ]

        pacgums = []

        super_positions = {
            (0, 0),
            (width - 1, 0),
            (0, height - 1),
            (width - 1, height - 1),
        }

        for x, y in super_positions:
            pacgums.append(PacgumDT(x, y, True))

        remaining = self.config.pacgum - 4

        for y in range(height):
            for x in range(width):
                if remaining <= 0:
                    break

                if (x, y) in super_positions:
                    continue

                if not self.maze.is_walkable(x, y):
                    continue

                pacgums.append(PacgumDT(x, y, False))
                remaining -= 1

        gamestate = GameStateDT(
            level=1,
            score=0,
            lives=self.config.lives,
            time_remaining=float(self.config.level_max_time),
            is_paused=False,
            is_game_over=False,
            is_victory=False,
            is_level_cleared=False,
            pacman=pacman,
            ghosts=ghosts,
            pacgums=pacgums,
            grid_width=width,
            grid_height=height,
            active_cheats={
                CheatCode.SKIP_LEVEL: {
                    "state": "off",
                    "level": 0,
                },
                CheatCode.UNLIMITED_LIFE: {
                    "state": "off",
                    "remaining_time": 0.0,
                },
                CheatCode.FREEZE_GHOSTS: {
                    "state": "off",
                    "remaining_time": 0.0,
                },
                CheatCode.SPEED: {
                    "state": "off",
                    "remaining_time": 0.0,
                },
            },
        )
        return gamestate

    def start_new_game(self) -> None:
        """Reset scores, lives, level count, and spawn entities."""
        self.gamestate = self.setup_game_state()
        self.cheats = Cheats(self.gamestate)

    def update(self, dt: float) -> None:
        """Advance game physics and timers."""
        self.cheats.update(dt)

    def set_player_direction(self, direction: Direction) -> None:
        """Queue the next intended direction for Pac-Man."""
        self.gamestate.pacman.direction = direction

    def toggle_pause(self) -> bool:
        """Toggle paused state and return new pause status."""
        self.gamestate.is_paused = not self.gamestate.is_paused
        return self.gamestate.is_paused

    def toggle_cheat(self, cheat_code: CheatCode) -> None:
        """Toggle a cheat feature."""
        self.cheats.toggle(cheat_code)

    def get_state(self) -> GameStateDT:
        """Return the current game state."""
        return self.gamestate

    def get_wall_matrix(self) -> List[List[int]]:
        """Return the current maze wall matrix."""

     def get_highscores(self) -> List[Dict[str, Any]]:
        """Return the top 10 highscores."""
        return self.highscoresmanager.get_top_10()

    def save_highscore(self, name: str) -> None:
        """Save the current game score."""
        self.highscores.add_score(
            name,
            self.gamestate.score,
        )
        self.highscores.save_scores()       return self.maze.maze
