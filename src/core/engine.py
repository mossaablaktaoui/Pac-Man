class IGameEngine:
    def load_config(self, config_data: dict) -> None:
        """Initialize engine settings from validated config."""
        ...

    def start_new_game(self) -> None:
        """Reset scores, lives, level count, and spawn entities."""
        ...

    def update(self, dt: float) -> None:
        """Advance game physics and timers by delta-time (dt in seconds)."""
        ...

    def set_player_direction(self, direction: Direction) -> None:
        """Queue the next intended direction for Pac-Man."""
        ...

    def toggle_pause(self) -> bool:
        """Toggle paused state; returns new pause status."""
        ...

    def trigger_cheat(self, cheat_code: str) -> None:
        """Toggle cheat features: 'INVINCIBILITY', 'SKIP_LEVEL', 'FREEZE_GHOSTS', 'ADD_LIFE', 'SPEED'."""
        ...

    def get_state(self) -> GameStateDTO:
        """Return an immutable snapshot of current game state for rendering."""
        ...

    def get_wall_matrix(self) -> List[List[int]]:
        """Return 2D grid of 4-bit wall bitmasks for the current level."""
        ...