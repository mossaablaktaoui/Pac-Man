import pygame
from src.core.engine import GameEngine


class ScrHighscores:
    def __init__(self, screen: pygame.Surface, engine: GameEngine) -> None:
        self.screen = screen
        self.engine = engine

        try:
            self.font = pygame.font.Font("assets/fonts/pacfont.ttf", 20)
        except (FileNotFoundError, pygame.error):
            self.font = pygame.font.Font(None, 24)

        self.width = self.screen.get_width()
        self.height = self.screen.get_height()

        # Cache highscores in memory (avoid disk reads 60x/sec)
        self.scores: list[dict] = []
        self._load_assets()
        self.refresh()

    def _load_assets(self) -> None:
        buttons_dir = "assets/images/buttons"
        self.idle_menu = pygame.image.load(
            f"{buttons_dir}/menu_idle.png"
        ).convert_alpha()
        self.idle_menu = pygame.transform.scale_by(self.idle_menu, 0.5)

        self.hover_menu = pygame.image.load(
            f"{buttons_dir}/menu_hover.png"
        ).convert_alpha()
        self.hover_menu = pygame.transform.scale_by(self.hover_menu, 0.5)

        self.menu_rect = self.idle_menu.get_rect()
        self.menu_rect.center = [int(self.width * 0.5),
                                 int(self.height * 0.86)]

    def refresh(self) -> None:
        """Fetch and cache latest scores from the engine."""
        self.scores = self.engine.get_highscores()

    def draw_scores_text(self) -> None:
        if not self.scores:
            empty_surf = self.font.render("NO SCORES YET",
                                          True, (255, 255, 255))
            empty_rect = empty_surf.get_rect(
                center=(self.width // 2, int(self.height * 0.5))
            )
            self.screen.blit(empty_surf, empty_rect)
            return

        score_xpos = self.width * 0.65
        name_xpos = self.width * 0.45
        for i, score in enumerate(self.scores):
            y_ratio = 0.346 + i * 0.048
            color = (255, 215, 0) if i == 0 else (255, 255, 255)

            name_surf = self.font.render(score["name"], True, color)
            name_rect = name_surf.get_rect()
            name_rect.center = [name_xpos, (self.height * y_ratio)]

            score_surf = self.font.render(str(score["score"]), True, color)
            score_rect = score_surf.get_rect()
            score_rect.center = [score_xpos, (self.height * y_ratio)]

            self.screen.blit(name_surf, name_rect)
            self.screen.blit(score_surf, score_rect)

    def handle_event(self, event: pygame.event.Event) -> str | None:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.menu_rect.collidepoint(event.pos):
                return "menu"
        return None

    def draw(self) -> None:
        mouse_pos = pygame.mouse.get_pos()
        if self.menu_rect.collidepoint(mouse_pos):
            self.screen.blit(self.hover_menu, self.menu_rect)
        else:
            self.screen.blit(self.idle_menu, self.menu_rect)

        self.draw_scores_text()
