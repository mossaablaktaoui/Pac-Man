"""Data transfer objects and enumerations for game state representation."""

from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.core.cheats import CheatCode


class Direction(str, Enum):
    """Enumeration of cardinal navigation directions."""

    UP = "UP"
    DOWN = "DOWN"
    LEFT = "LEFT"
    RIGHT = "RIGHT"


class GhostState(str, Enum):
    """Enumeration of ghost operational behavior states."""

    NORMAL = "NORMAL"
    EDIBLE = "EDIBLE"
    FLASHING = "FLASHING"
    EATEN = "EATEN"


@dataclass()
class SpriteDT:
    """Data transfer object representing an animated grid entity."""

    id: str
    grid_x: int
    grid_y: int
    direction: Direction
    state: str


@dataclass()
class PacgumDT:
    """Data transfer object representing a collectible pellet on the grid."""

    grid_x: int
    grid_y: int
    is_super: bool


@dataclass()
class GameStateDT:
    """Read-only snapshot of the complete game state passed to renderers."""

    level: int
    score: int
    lives: int
    time_remaining: float
    is_paused: bool
    is_game_over: bool
    is_victory: bool
    is_level_cleared: bool
    pacman: SpriteDT
    ghosts: list[SpriteDT]
    pacgums: list[PacgumDT]
    grid_width: int
    grid_height: int
    active_cheats: list["CheatCode"]
