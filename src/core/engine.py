from typing import Any, List, Dict
import random

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
    MAX_LEVELS = 10

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

        remaining = min(self.config.pacgum - 4,
                        len(walkable_cells))

        walkable_cells = []

        for y in range(height):
            for x in range(width):
                if (self.maze.is_walkable(x, y)
                    and (x, y) not in super_positions):

                    walkable_cells.append((x, y))

        for x, y in random.sample(walkable_cells, remaining):
            pacgums.append(PacgumDT(x, y, False))

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
        self.maze.reset()
        self.gamestate = self.setup_game_state()

        self.cheats.gamestate = self.gamestate
        self.next_direction = self.gamestate.pacman.direction
        self.pacman_move_timer = 0.0

        self.ghost_manager.reset(self.maze)

    def update(self, dt: float) -> None:
        # stop simulation if the game is paused or over.
        if (self.gamestate.is_paused
            or self.gamestate.is_game_over
            or self.gamestate.is_victory
            or self.gamestate.is_level_cleared):
            return

        # stop the game when the time is over.
        self.gamestate.time_remaining -= dt

        if self.gamestate.time_remaining <= 0.0:
            self.gamestate.time_remaining = 0.0
            self.gamestate.is_game_over = True
            return

        # control pacman speed and increase it in cheat mode.
        self.pacman_move_timer += dt

        move_delay = 0.1 if self.cheats.is_active(CheatCode.SPEED) else 0.2

        if self.pacman_move_timer >= move_delay:
            self._move_pacman()
            self.pacman_move_timer = 0.0
            self._collect_pacgum()

        # update ghosts state while they are not freezed.
        if not self.cheats.is_active(CheatCode.FREEZE_GHOSTS):
            self.ghost_manager.update(self.gamestate, dt)

        # check for being pacman and a ghost in the same cell to end the game.
        self._check_ghost_collision()
        
        # Go to next level when is cleared
        if self.gamestate.is_level_cleared:
            self.start_next_level()

    def set_player_direction(self, direction: Direction) -> None:
        """Queue the next intended direction for Pac-Man."""
        self.next_direction = direction

    def toggle_pause(self) -> bool:
        """Toggle paused state and return new pause status."""
        self.gamestate.is_paused = not self.gamestate.is_paused
        return self.gamestate.is_paused

    def toggle_cheat(self, cheat_code: CheatCode) -> None:
        """Toggle a cheat feature."""
        self.cheats.toggle(cheat_code)

        if cheat_code == CheatCode.SKIP_LEVEL:
            self.start_next_level()

    def get_state(self) -> GameStateDT:
        """Return the current game state."""
        return self.gamestate

    def get_wall_matrix(self) -> List[List[int]]:
        """Return the current maze wall matrix."""
        return self.maze.maze

    def get_highscores(self) -> List[Dict[str, Any]]:
        """Return the top 10 highscores."""
        return self.highscoresmanager.get_highscores()

    def get_highscore(self) -> List[Dict[str, Any]]:
        """Return the top highscore."""
        return self.highscoresmanager.get_highscore()

    def save_highscore(self, name: str) -> None:
        """Save the current game score."""
        self.highscoresmanager.add_score(name, self.gamestate.score)
        self.highscoresmanager.save_scores()

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
                    self.ghost_manager.make_edible(self.gamestate)
                else:
                    self.gamestate.score += (
                        self.config.points_per_pacgum
                    )

                pacgums.remove(pacgum)
                break

        if not pacgums:
            self.gamestate.is_level_cleared = True

    def _check_ghost_collision(self) -> None:

        pacman = self.gamestate.pacman

        for ghost in self.gamestate.ghosts:
            if (ghost.grid_x == pacman.grid_x
                    and ghost.grid_y == pacman.grid_y):

                if ghost.state == GhostState.EDIBLE:
                    self.gamestate.score += self.config.points_per_ghost
                    ghost.state = GhostState.EATEN
                    return

                if ghost.state == GhostState.EATEN:
                    continue

                if self.cheats.is_active(CheatCode.UNLIMITED_LIFE):
                    return

                self.gamestate.lives -= 1

                if self.gamestate.lives <= 0:
                    self.gamestate.is_game_over = True
                    return

                self._reset_positions()
                return

    def _reset_positions(self):
        pacman = self.gamestate.pacman

        pacman.grid_x = self.gamestate.grid_width // 2
        pacman.grid_y = self.gamestate.grid_height // 2

        positions = [
            (0, 0),
            (self.gamestate.grid_width - 1, 0),
            (0, self.gamestate.grid_height - 1),
            (self.gamestate.grid_width - 1, self.gamestate.grid_height - 1),
        ]

        for ghost, (x, y) in zip(self.gamestate.ghosts, positions):
            ghost.grid_x = x
            ghost.grid_y = y
            ghost.state = GhostState.NORMAL

        self.ghost_manager.reset(self.maze)
        return

    def start_next_level(self) -> None:
        if self.gamestate.level >= self.MAX_LEVELS:
            self.gamestate.is_level_cleared = False
            self.gamestate.is_victory = True
            return

        old_score = self.gamestate.score
        old_lives = self.gamestate.lives
        next_level = self.gamestate.level + 1

        self.maze.create_random_maze()
        self.gamestate = self.setup_game_state()

        self.gamestate.score = old_score
        self.gamestate.lives = old_lives
        self.gamestate.level = next_level

        self.cheats.gamestate = self.gamestate
        self.next_direction = self.gamestate.pacman.direction
        self.pacman_move_timer = 0.0

        self.ghost_manager.reset(self.maze)

        return
