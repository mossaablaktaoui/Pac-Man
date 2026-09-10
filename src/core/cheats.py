from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.core.entities import GameStateDT


class CheatCode(str, Enum):
    SKIP_LEVEL = "SKIP_LEVEL"
    FREEZE_GHOSTS = "FREEZE_GHOSTS"
    UNLIMITED_LIFE = "UNLIMITED_LIFE"
    SPEED = "SPEED"


class Cheats:
    def __init__(self, gamestate: "GameStateDT") -> None:
        self.gamestate = gamestate

    def toggle(self, cheat_code: CheatCode) -> None:
        """Enable or disable a cheat."""
        if cheat_code == CheatCode.SKIP_LEVEL:
            self.gamestate.is_level_cleared = True
            return

        if cheat_code in self.gamestate.active_cheats:
            self.gamestate.active_cheats.remove(cheat_code)
        else:
            self.gamestate.active_cheats.append(cheat_code)

    def is_active(self, cheat_code: CheatCode) -> bool:
        """Return True when a cheat is active."""
        return cheat_code in self.gamestate.active_cheats
