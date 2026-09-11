import sys
import pygame
from typing import List, Dict

from src.core.engine import GameEngine


class ScrPause:
    def __init__(self,
                 screen: pygame.Surface,
                 engine: GameEngine) -> None:
        self.screen = screen
        self.engine = engine

        self.width = self.screen.get_width()
        self.height = self.screen.get_height()

        self.buttons: List[Dict] = []
        self._load_buttons()

    def _load_buttons(self):
        buttons_dir = "assets/images/buttons"
        buttons_config = [
            ("resume", 0.5, (0.5, 0.305)),
            ("replay", 0.5, (0.5, 0.435)),
            ("menu", 0.5, (0.5, 0.565)),
            ("quit", 0.5, (0.5, 0.695))
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

    def handle_event(self, event: pygame.event.Event) -> str | None:
        """Handle clicks. Returns the button name if clicked, else None."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                self.engine.toggle_pause()
                return "resume"
            if event.key == pygame.K_r:
                self.engine.start_new_game()
                return "replay"
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for btn in self.buttons:
                if btn["rect"].collidepoint(event.pos):
                    if btn["name"] == "quit":
                        pygame.quit()
                        sys.exit(0)
                    if btn["name"] == "resume":
                        self.engine.toggle_pause()
                    if btn["name"] == "replay":
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
