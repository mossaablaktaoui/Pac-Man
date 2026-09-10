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
        cheat = self.gamestate.active_cheats[cheat_code]

        if cheat["state"] == "on":
            cheat["state"] = "off"

            if "remaining_time" in cheat:
                cheat["remaining_time"] = 0.0

            return

        cheat["state"] = "on"

        if cheat_code == CheatCode.SKIP_LEVEL:
            self.gamestate.is_level_cleared = True
            cheat["level"] = self.gamestate.level

        elif cheat_code == CheatCode.UNLIMITED_LIFE:
            cheat["remaining_time"] = 120.0

        elif cheat_code == CheatCode.FREEZE_GHOSTS:
            cheat["remaining_time"] = 20.0

        elif cheat_code == CheatCode.SPEED:
            cheat["remaining_time"] = 20.0

    def update(self, dt: float) -> None:
        """Update active cheat timers."""
        timed_cheats = (
            CheatCode.UNLIMITED_LIFE,
            CheatCode.FREEZE_GHOSTS,
            CheatCode.SPEED,
        )

        for cheat_code in timed_cheats:
            cheat = self.gamestate.active_cheats[cheat_code]

            if cheat["state"] != "on":
                continue

            cheat["remaining_time"] = max(
                0.0,
                cheat["remaining_time"] - dt,
            )

            if cheat["remaining_time"] == 0.0:
                cheat["state"] = "off"

        skip = self.gamestate.active_cheats[CheatCode.SKIP_LEVEL]

        if (
            skip["state"] == "on"
            and skip["level"] != self.gamestate.level
        ):
            skip["state"] = "off"

    def is_active(self, cheat_code: CheatCode) -> bool:
        """Return True when a cheat is active."""
        return (
            self.gamestate.active_cheats[cheat_code]["state"]
            == "on"
        )
