"""HUD overlay component for drawing in-game status boards."""

import pygame

from typing import Tuple


class HUD:
    """Manages loading and rendering game status boards and text."""

    def __init__(
        self,
        font_path: str = "assets/fonts/pacfont.ttf",
        font_size: int = 14,
        scale_factor: float = 0.5,
    ) -> None:
        """Initialize fonts and preload all board panels.

        Args:
            font_path: Path to the TrueType font file.
            font_size: Size of the rendered font.
            scale_factor: Scale multiplier for the board images.
        """
        try:
            self.font = pygame.font.Font(font_path, font_size)
        except (FileNotFoundError, pygame.error):
            self.font = pygame.font.Font(None, font_size)

        self.text_color = (0, 255, 255)
        self._boards: list[tuple[str, pygame.Surface, pygame.Rect]] = []

        # Define board metadata: (key, filename, screen_pos)
        configs = [
            ("score", "scoreboard.png", (100, 100)),
            ("lives", "livesboard.png", (100, 200)),
            ("time", "timerboard.png", (100, 300)),
            ("level", "levelboard.png", (100, 400)),
        ]

        images_dir = "assets/images/boards"
        for key, filename, pos in configs:
            img = pygame.image.load(f"{images_dir}/{filename}")
            if pygame.display.get_surface() is not None:
                img = img.convert_alpha()
            scaled_img = pygame.transform.scale_by(img, scale_factor)
            rect = scaled_img.get_rect(topleft=pos)
            self._boards.append((key, scaled_img, rect))

    def draw(
        self,
        screen: pygame.Surface,
        score: int,
        lives: int,
        time_left: float,
        level: int,
    ) -> None:
        """Draw all boards and center their dynamic text values.

        Args:
            screen: The target surface to draw onto.
            score: Current player score.
            lives: Remaining player lives.
            time_left: Remaining time in seconds.
            level: Current level number.
        """
        # Map values to their respective board keys
        display_values: dict[str, Tuple[str, Tuple[int, int, int]]] = {
            "score": (f"Score: {score:06d}", (0, 255, 255)),
            "lives": (f"Lives: x{lives}", (255, 215, 0)),
            "time": (f"Time: {int(time_left):02d}s", (255, 191, 0)),
            "level": (f"LVL {level}", (190, 0, 255)),
        }

        # Single loop handles all boards and text centering
        for key, image, rect in self._boards:
            screen.blit(image, rect)

            info = display_values.get(key, "")
            text_surf = self.font.render(info[0], True, info[1])
            text_rect = text_surf.get_rect(center=rect.center)
            screen.blit(text_surf, text_rect)
