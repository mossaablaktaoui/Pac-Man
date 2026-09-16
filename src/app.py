"""Application launcher and game execution runner."""

import sys

from src.views.renderer import Renderer


def run_game() -> None:
    """Initialize the game renderer and start the main execution loop."""
    try:
        renderer = Renderer()
        renderer.run()
    except KeyboardInterrupt:
        print("bye")
    except Exception as error:
        print(f"\033[91mError: {error}\033[0m")
        sys.exit(1)
