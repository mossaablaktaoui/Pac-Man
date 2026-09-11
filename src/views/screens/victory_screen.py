import sys
import pygame
from typing import List, Dict

from src.core.engine import GameEngine


class ScrVictory:
    def __init__(self,
                 screen: pygame.Surface,
                 engine: GameEngine) -> None:
        self.screen = screen
        self.engine = engine

        try:
            self.font = pygame.font.Font("assets/fonts/pacfont.ttf", 22)
        except (FileNotFoundError, pygame.error):
            self.font = pygame.font.Font(None, 22)

        self.width = self.screen.get_width()
        self.height = self.screen.get_height()

        self.buttons: List[Dict] = []
        self._load_buttons()

    def _load_buttons(self):
        buttons_dir = "assets/images/buttons"
        buttons_config = [
            ("menu", 0.5, (0.4, 0.695)),
            ("highscores", 0.53, (0.6, 0.695)),
            ("quit", 0.53, (0.5, 0.83)),
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

    def draw_score_text(self, score: int = 0, highscore: int = 0) -> None:
        # Horizontal center ratios across the board for each column
        text_color = (255, 255, 255)
        column_ratios: dict[str, tuple[str, float]] = {
            "score": (f"{self.engine.gamestate.score:06d}", 0.515),
            "lives": (f"{self.engine.get_highscore():06d}", 0.565),
        }

        for text_val, ratio in column_ratios.values():
            text_surf = self.font.render(text_val, True, text_color)
            text_rect = text_surf.get_rect()
            text_rect.center = [self.width * 0.6, self.height * ratio]
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

    def draw(self) -> None:
        """Render the maze and HUD."""
        mouse_pos = pygame.mouse.get_pos()
        for btn in self.buttons:
            if btn["rect"].collidepoint(mouse_pos):
                self.screen.blit(btn["hover"], btn["rect"])
            else:
                self.screen.blit(btn["idle"], btn["rect"])
        self.draw_score_text()
