from typing import Any, List, Dict

from src.core.highscores import HighscoreManager
from src.core.cheats import Cheats, CheatCode
from src.core.maze_adapter import MazeAdapter
from src.core.config import Config
from src.core.ghost import GhostManager
from src.core.entities import (
    GameStateDT,
    SpriteDT,
    PacgumDT,
    Direction,
    GhostState,
)


class GameEngine:
    def __init__(self) -> None:
        self.config = Config()

        self.maze = MazeAdapter(self.config.seed)
        self.gamestate = self.setup_game_state()
        self.cheats = Cheats(self.gamestate)
        self.highscoresmanager = HighscoreManager(self.config.highscore_filename)
        self.next_direction = self.gamestate.pacman.direction
        self.pacman_move_timer = 0.0
        self.ghost_manager = GhostManager(self.maze)

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
            active_cheats=[],
        )
        return gamestate

    def start_new_game(self) -> None:
        """Reset scores, lives, level count, and spawn entities."""
        self.gamestate = self.setup_game_state()
        self.cheats = Cheats(self.gamestate)

    def update(self, dt: float) -> None:
        self.pacman_move_timer += dt

        if self.pacman_move_timer >= 0.2:
            self._move_pacman()
            self.pacman_move_timer = 0.0
            self._collect_pacgum()

        self.ghost_manager.update(self.gamestate, dt)

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
        return self.maze.maze

    def get_highscores(self) -> List[Dict[str, Any]]:
        """Return the top 10 highscores."""
        return self.highscoresmanager.get_top_10()

    def save_highscore(self, name: str) -> None:
        """Save the current game score."""
        self.highscores.add_score(
            name,
            self.gamestate.score,
        )
        self.highscores.save_scores()

    def _move_pacman(self) -> None:
        pacman = self.gamestate.pacman
        pac_x = pacman.grid_x
        pac_y = pacman.grid_y

        if self.maze.can_move(pac_x, pac_y, self.next_direction):
            pacman.direction = self.next_direction

        direction = pacman.direction

        if self.maze.can_move(pac_x, pac_y, direction):
            if direction == Direction.UP:
                pacman.grid_y -= 1
            elif direction == Direction.RIGHT:
                pacman.grid_x += 1
            elif direction == Direction.DOWN:
                pacman.grid_y += 1
            elif direction == Direction.LEFT:
                pacman.grid_x -= 1

    def _collect_pacgum(self) -> None:
        pacman = self.gamestate.pacman
        pacgums = self.gamestate.pacgums
        pac_x = pacman.grid_x
        pac_y = pacman.grid_y

        for pacgum in pacgums:
            if pacgum.grid_x == pac_x and pacgum.grid_y == pac_y:
                if pacgum.is_super:
                    self.gamestate.score += (
                        self.config.points_per_super_pacgum
                    )
                else:
                    self.gamestate.score += (
                        self.config.points_per_pacgum
                    )

                pacgums.remove(pacgum)
                break

        if not pacgums:
            self.gamestate.is_level_cleared = True
