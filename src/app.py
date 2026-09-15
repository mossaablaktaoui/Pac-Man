"""Application launcher and game execution runner."""

from src.views.renderer import Renderer


def run_game() -> None:
    """Initialize the game renderer and start the main execution loop."""
    renderer = Renderer()
    renderer.run()
