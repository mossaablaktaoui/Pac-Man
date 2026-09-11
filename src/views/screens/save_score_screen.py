import sys
import pygame
from typing import List, Dict

from src.core.engine import GameEngine


class ScrGameOver:
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

    def draw_name_text(self, score: int = 0, highscore: int = 0) -> None:
        # Horizontal center ratios across the board for each column
        text_color = (255, 255, 255)
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
                    if btn["name"] == "reply":
                        self.engine.start_new_game()
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
        self.draw_score_text(self.engine.gamestate.score,
                             self.engine.get_highscore())
