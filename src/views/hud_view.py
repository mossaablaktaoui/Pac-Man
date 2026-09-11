"""HUD overlay component for drawing in-game status boards."""
import sys
import pygame
from typing import Dict, List

from src.core.cheats import CheatCode


class HUD:
    """Manages loading and rendering game status boards and text."""

    def __init__(self, screen) -> None:
        """Initialize fonts and preload all board panels.

        Args:
            font_path: Path to the TrueType font file.
            font_size: Size of the rendered font.
            scale_factor: Scale multiplier for the board images.
        """
        self.screen = screen
        self.width = self.screen.get_width()
        self.height = self.screen.get_height()
        self.buttons: List[Dict] = []
        self.boards: List[Dict] = []
        self.toggle_btns: List[Dict] = []
        try:
            self.font = pygame.font.Font("assets/fonts/pacfont.ttf", 18)
        except (FileNotFoundError, pygame.error):
            self.font = pygame.font.Font(None, 18)

        self.text_color = (255, 255, 255)
        self._load_buttons()
        self._load_boards()
        self._load_onoff()

    def _load_boards(self):
        images_dir = "assets/images/boards"
        boards_config = [
            ("top", (self.width // 2, 60)),
            ("instructions", (self.width * 0.14, self.height // 2)),
            ("cheats", (self.width * 0.86, self.height // 2))
        ]
        for board in boards_config:
            img = pygame.image.load(f"{images_dir}/{board[0]}board.png")
            rect = img.get_rect()
            rect.center = list(board[1])
            if board[0] == "top":
                self.tb_rect = rect  # <-- Added: fixes AttributeError
            self.boards.append({
                "name": board[0],
                "image": img,
                "rect": rect
            })

    def _load_onoff(self):
        icons_dir = "assets/images/icons"
        toggle_config = [
            (CheatCode.SKIP_LEVEL, (self.width * 0.91, self.height * 0.445)),
            (CheatCode.SPEED, (self.width * 0.91, self.height * 0.517)),
            (CheatCode.UNLIMITED_LIFE, (self.width * 0.91, self.height * 0.59)),
            (CheatCode.FREEZE_GHOSTS, (self.width * 0.91, self.height * 0.665)),
        ]
        for toggle, cor in toggle_config:
            on_img = pygame.image.load(f"{icons_dir}/turn_on.png")
            on_img = pygame.transform.scale_by(on_img, 0.08)
            off_img = pygame.image.load(f"{icons_dir}/turn_off.png")
            off_img = pygame.transform.scale_by(off_img, 0.08)
            rect = on_img.get_rect()
            rect.center = list(cor)
            self.toggle_btns.append({
                "name": toggle,
                "on": on_img,
                "off": off_img,
                "rect": rect
            })

    def _load_buttons(self):
        buttons_dir = "assets/images/buttons"
        buttons_config = [
            ("pause", 0.75, (0.86, 0.081)),
            ("menu", 0.6, (0.14, 0.081))
        ]
        for btn in buttons_config:
            img = pygame.image.load(f"{buttons_dir}/{btn[0]}_idle.png")
            img = pygame.transform.scale_by(img, btn[1])
            hover_img = pygame.image.load(f"{buttons_dir}/{btn[0]}_hover.png")
            hover_img = pygame.transform.scale_by(hover_img, btn[1])
            rect = img.get_rect()
            rect.center = [self.width * btn[2][0],
                           self.height * btn[2][1]]
            self.buttons.append({
                "name": btn[0],
                "idle": img,
                "hover": hover_img,
                "rect": rect
            })

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

    def handle_event(self, event: pygame.event.Event) -> str | None:
        """Handle clicks. Returns the button name if clicked, else None."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for btn in self.buttons:
                if btn["rect"].collidepoint(event.pos):
                    if btn["name"] == "quit":
                        pygame.quit()
                        sys.exit(0)
                    return btn["name"]
        return None

    def draw(
        self,
        score: int, lives: int,
        time_left: float, level: int,
        cheats: List[CheatCode]
    ) -> None:
        """Draw all boards and center their dynamic text values.

        Args:
            screen: The target surface to draw onto.
            score: Current player score.
            lives: Remaining player lives.
            time_left: Remaining time in seconds.
            level: Current level number.
        """
        mouse_pos = pygame.mouse.get_pos()
        for btn in self.buttons:
            if btn["rect"].collidepoint(mouse_pos):
                self.screen.blit(btn["hover"], btn["rect"])
            else:
                self.screen.blit(btn["idle"], btn["rect"])
        for board in self.boards:
            self.screen.blit(board["image"], board["rect"])
        for toggle in self.toggle_btns:
            if toggle["name"] in cheats:
                self.screen.blit(toggle["on"], toggle["rect"])
            else:
                self.screen.blit(toggle["off"], toggle["rect"])
        self.draw_board_text(score, lives, time_left, level)
