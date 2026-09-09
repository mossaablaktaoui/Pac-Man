from typing import List

from src.core.maze_adapter import MazeAdapter
from src.core.config import Config
from src.core.entities import GameStateDT, Direction


class GameEngine:
    def __init__(self):
        self.maze = MazeAdapter(42)
        self.config = Config()
        self.gamestate = GameStateDT(
            level=1,
            score=0,
            lives=3,
            time_remaining=300,
            is_paused=False,
            is_game_over=False,
            is_victory=False,
            is_level_cleared=False,
            pacman=None,
            ghosts=[],
            pacgums=[],
            grid_width=20,
            grid_height=20,
            active_cheats=[]
        )

    def setup_game_state(self):
        self.gamestate.level = 1
        self.gamestate.score = 0
        self.gamestate.lives = self.config.lives
        self.gamestate.level = 1
        self.gamestate.level = 1
        self.gamestate.level = 1
    #
    # level: int
    # score: int
    # lives: int
    # time_remaining: float
    # is_paused: bool
    # is_game_over: bool
    # is_victory: bool
    # is_level_cleared: bool
    # pacman: SpriteDT
    # ghosts: List[SpriteDT]
    # pacgums: List[PacgumDT]
    # grid_width: int
    # grid_height: int
    # active_cheats: List[str]

    def start_new_game(self) -> None:
        """Reset scores, lives, level count, and spawn entities."""
        pass

    def update(self, dt: float) -> None:
        """Advance game physics and timers by delta-time (dt in seconds)."""
        pass

    def set_player_direction(self, direction: Direction) -> None:
        """Queue the next intended direction for Pac-Man."""
        pass

    def toggle_pause(self) -> bool:
        """Toggle paused state; returns new pause status."""
        pass

    def trigger_cheat(self, cheat_code: str) -> None:
        """Toggle cheat features: 'INVINCIBILITY', 'SKIP_LEVEL',
        'FREEZE_GHOSTS', 'ADD_LIFE', 'SPEED'."""
        pass

    def get_state(self) -> GameStateDT:
        """Return an immutable snapshot of current game state for rendering."""
        pass

    def get_wall_matrix(self) -> List[List[int]]:
        """Return 2D grid of 4-bit wall bitmasks for the current level."""
        return self.maze.maze
