import pygame

from src.core.engine import GameEngine


class ScrHighscores:
    def __init__(self,
                 screen: pygame.Surface,
                 engine: GameEngine) -> None:
        self.screen = screen
        self.engine = engine

        self.width = self.screen.get_width()
        self.height = self.screen.get_height()

        self._load_assets()

    def _load_assets(self):
        buttons_dir = "assets/images/buttons"
        self.idle_menu = pygame.image.load(f"{buttons_dir}/menu_idle.png")
        self.idle_menu = pygame.transform.scale_by(self.idle_menu, 0.5)
        self.hover_menu = pygame.image.load(f"{buttons_dir}/menu_hover.png")
        self.hover_menu = pygame.transform.scale_by(self.hover_menu, 0.5)
        self.menu_rect = self.idle_menu.get_rect()
        self.menu_rect.center = [self.width * 0.5, self.height * 0.87]

    def handle_event(self, event: pygame.event.Event) -> str | None:
        """Forward events to HUD or process gameplay keys."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.menu_rect.collidepoint(event.pos):
                return "menu"
        return None

    def draw(self) -> None:
        """Render the maze and HUD."""
        mouse_pos = pygame.mouse.get_pos()
        if self.menu_rect.collidepoint(mouse_pos):
            self.screen.blit(self.hover_menu, self.menu_rect)
        else:
            self.screen.blit(self.idle_menu, self.menu_rect)
