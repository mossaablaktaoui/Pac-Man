class Ghost:
    """Represent a ghost."""

    def __init__(self,
                 ghost_id: int,
                 x: int, y: int,
                 direction: str = "RIGHT") -> None:
        self.ghost_id = ghost_id

        self.x = x
        self.y = y

        self.start_x = x
        self.start_y = y

        self.direction = direction
        self.state = "NORMAL"

        self.respawn_timer = 0.0
        self.edible_timer = 0.0

    def set_direction(self, direction: str) -> None:
        """Set the movement direction."""
        self.direction = direction

    def move(self, x: int, y: int) -> None:
        """Move the ghost."""
        self.x = x
        self.y = y

    def become_edible(self, duration: float) -> None:
        """Make the ghost edible."""
        self.state = "EDIBLE"
        self.edible_timer = duration

    def respawn(self) -> None:
        """Reset the ghost to its start position."""
        self.x = self.start_x
        self.y = self.start_y

        self.direction = "RIGHT"
        self.state = "NORMAL"
        self.respawn_timer = 0.0

