from dataclasses import dataclass
from enum import Enum
from typing import List


class Direction(str, Enum):
    UP = "UP"
    DOWN = "DOWN"
    LEFT = "LEFT"
    RIGHT = "RIGHT"


class GhostState(str, Enum):
    NORMAL = "NORMAL"
    EDIBLE = "EDIBLE"
    FLASHING = "FLASHING"
    EATEN = "EATEN"


@dataclass(frozen=True)
class SpriteDT:
    id: str                     # "pacman", "blinky", "pinky", "inky", "clyde"
    grid_x: int                      # Current column in maze
    grid_y: int                      # Current row in maze
    direction: Direction
    state: str                       # e.g. "ALIVE", "DEAD", or GhostState


@dataclass(frozen=True)
class PacgumDT:
    grid_x: int
    grid_y: int
    is_super: bool


@dataclass(frozen=True)
class GameStateDT:
    level: int
    score: int
    lives: int
    time_remaining: float
    is_paused: bool
    is_game_over: bool
    is_victory: bool
    is_level_cleared: bool
    pacman: SpriteDT
    ghosts: List[SpriteDT]
    pacgums: List[PacgumDT]
    grid_width: int
    grid_height: int
    active_cheats: List[str]
