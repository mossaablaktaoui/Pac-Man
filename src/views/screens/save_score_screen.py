import pygame
from src.core.engine import GameEngine


class ScrSaveScore:
    def __init__(self, screen: pygame.Surface, engine: GameEngine) -> None:
        self.screen = screen
        self.engine = engine

        try:
            self.font = pygame.font.Font("assets/fonts/pacfont.ttf", 22)
        except (FileNotFoundError, pygame.error):
            self.font = pygame.font.Font(None, 22)

        self.width = self.screen.get_width()
        self.height = self.screen.get_height()
        self.user_text = ""
        self._load_assets()

    def _load_assets(self) -> None:
        boards_dir = "assets/images/boards"
        self.board_img = pygame.image.load(
            f"{boards_dir}/save_score_board.png")
        self.board_img = pygame.transform.scale_by(self.board_img, 0.25)
        self.board_rect = self.board_img.get_rect()
        self.board_rect.center = (self.width // 2, self.height // 2)

    def draw_name_text(self) -> None:
        text_surf = self.font.render(self.user_text, True, (255, 255, 255))
        text_rect = text_surf.get_rect()
        text_rect.center = (int(self.width * 0.5), int(self.height * 0.52))
        self.screen.blit(text_surf, text_rect)

    def handle_event(self, event: pygame.event.Event) -> str | None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.user_text = self.user_text[:-1]

            elif event.key == pygame.K_RETURN:
                if len(self.user_text) > 0:
                    if self.engine.gamestate.is_victory:
                        return "victory"
                    return "gameover"

            elif len(self.user_text) < 10 and event.unicode.isalnum():
                self.user_text += event.unicode

        return None

    def draw(self) -> None:
        self.screen.blit(self.board_img, self.board_rect)
        self.draw_name_text()
