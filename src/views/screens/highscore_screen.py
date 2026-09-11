import pygame

from src.core.engine import GameEngine


class ScrHighscores:
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

        self._load_assets()

    def _load_assets(self):
        buttons_dir = "assets/images/buttons"
        self.idle_menu = pygame.image.load(f"{buttons_dir}/menu_idle.png")
        self.idle_menu = pygame.transform.scale_by(self.idle_menu, 0.5)
        self.hover_menu = pygame.image.load(f"{buttons_dir}/menu_hover.png")
        self.hover_menu = pygame.transform.scale_by(self.hover_menu, 0.5)
        self.menu_rect = self.idle_menu.get_rect()
        self.menu_rect.center = [self.width * 0.5, self.height * 0.87]

    def draw_scores_text(self) -> None:
        scores = self.engine.get_highscores()
        for i, score in enumerate(scores):
            name_surf = self.font.render(score["name"], True, (255, 255, 255))
            name_rect = name_surf.get_rect()

            score_surf = self.font.render(str(score["score"]),
                                          True, (255, 255, 255))
            score_rect = score_surf.get_rect()

            name_rect.center = [(self.width * 0.45),
                                (self.height * (0.34 + i * 0.05))]
            score_rect.center = [(self.width * 0.65),
                                 (self.height * (0.34 + i * 0.05))]

            self.screen.blit(name_surf, name_rect)
            self.screen.blit(score_surf, score_rect)

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
        self.draw_scores_text()
