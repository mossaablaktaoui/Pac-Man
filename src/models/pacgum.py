class Pacgum:
    """Represent a pacgum or super-pacgum."""

    def __init__(self,
                 x: int,
                 y: int,
                 points: int,
                 is_super: bool = False) -> None:
        self.x = x
        self.y = y
        self.is_super = is_super
        self.eaten = False

    def eat(self) -> None:
        """Mark the pacgum as eaten."""
        self.eaten = True

    def is_eaten(self) -> bool:
        """Check if the pacgum was eaten."""
        return self.eaten
