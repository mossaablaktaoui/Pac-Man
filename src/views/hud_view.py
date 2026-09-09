"""HUD overlay component for drawing in-game status boards."""

import pygame


class HUD:
    """Manages loading and rendering game status boards and text."""

    def __init__(
        self,
        screen,
        font_path: str = "assets/fonts/pacfont.ttf",
        font_size: int = 18,
        scale_factor: float = 0.5,
    ) -> None:
        """Initialize fonts and preload all board panels.

        Args:
            font_path: Path to the TrueType font file.
            font_size: Size of the rendered font.
            scale_factor: Scale multiplier for the board images.
        """
        self.screen = screen
        try:
            self.font = pygame.font.Font(font_path, font_size)
        except (FileNotFoundError, pygame.error):
            self.font = pygame.font.Font(None, font_size)

        self.text_color = (255, 255, 255)

        images_dir = "assets/images/boards"
        self.tb_img = pygame.image.load(f"{images_dir}/topboard.png")
        self.tb_rect = self.tb_img.get_rect()
        self.tb_rect.center = [self.screen.get_width() // 2, 70]

    def draw_board_text(
        self, score: int, lives: int, time_left: float, level: int
    ) -> None:
        """Render and center stats inside their respective slots.

        Args:
            score: Current player score.
            lives: Remaining player lives.
            time_left: Remaining level time in seconds.
            level: Current level number.
        """
        # Horizontal center ratios across the board for each column
        column_ratios: dict[str, tuple[str, float]] = {
            "score": (f"{score:06d}", 0.12),
            "lives": (str(lives), 0.36),
            "level": (str(level), 0.61),
            "time": (f"{int(time_left):02d}s", 0.86),
        }

        # Vertical center in the lower dark area of the board
        y_pos = self.tb_rect.top + int(self.tb_rect.height * 0.65)

        for text_val, ratio in column_ratios.values():
            text_surf = self.font.render(text_val, True, self.text_color)
            x_pos = self.tb_rect.left + int(self.tb_rect.width * ratio)
            text_rect = text_surf.get_rect(center=(x_pos, y_pos))
            self.screen.blit(text_surf, text_rect)

    def draw(
        self,
        score: int, lives: int,
        time_left: float, level: int,
    ) -> None:
        """Draw all boards and center their dynamic text values.

        Args:
            screen: The target surface to draw onto.
            score: Current player score.
            lives: Remaining player lives.
            time_left: Remaining time in seconds.
            level: Current level number.
        """
        self.screen.blit(self.tb_img, self.tb_rect)
        self.draw_board_text(score, lives, time_left, level)
