class Player:
    """Represent the Pac-Man player."""

    VALID_DIRECTIONS = {"UP", "DOWN", "LEFT", "RIGHT"}

    def __init__(self, x: int, y: int, lives: int = 3) -> None:
        """Initialize the player."""
        self.x = x
        self.y = y

        self.start_x = x
        self.start_y = y

        self.direction = "RIGHT"

        self.state = "ALIVE"

        self.initial_lives = lives
        self.lives = lives
        self.score = 0

        self.speed = 1

    def set_direction(self, direction: str) -> None:
        """Set the wanted movement direction."""
        self.direction = direction

    def move(self, x: int, y: int) -> None:
        """Move the player to a new position."""
        self.x = x
        self.y = y

    def add_score(self, points: int) -> None:
        """Add points to the player's score."""
        self.score += points

    def lose_life(self) -> None:
        """Remove one life from the player."""
        if self.invincible:
            return

        if self.lives > 0:
            self.lives -= 1

        if self.lives == 0:
            self.state = "DEAD"

    def respawn(self) -> None:
        """Return the player to the starting position."""
        if self.is_game_over():
            return

        self.x = self.start_x
        self.y = self.start_y
        self.direction = "RIGHT"

    def is_alive(self) -> bool:
        """Check if the player has no lives left."""
        return self.state == "ALIVE"
