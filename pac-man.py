"""Command-line interface entry point for launching the Pac-Man game."""

from src.app import run_game


if __name__ == "__main__":
    try:
        run_game()
    except Exception as e:
        print(e)
