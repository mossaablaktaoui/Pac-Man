import sys
import pygame

from src.core.engine import GameEngine
from src.views.screens.game_screen import InGame
from src.views.screens.menu_screen import MainMenu

IMAGES = "assets/images"


class Renderer:
    def __init__(self,
                 screen_width: int | None = None,
                 screen_height: int | None = None):
        pygame.init()
        pygame.mixer.init()
        self.clock = pygame.time.Clock()
        self.engine = GameEngine()
        self.running = True
        self.current_screen = "INGAME"

        # Windowed mode to prevent OS display crashes
        monitor_sizes = pygame.display.get_desktop_sizes()
        self.screen_width = (screen_width
                             if screen_width else monitor_sizes[0][0])
        self.screen_height = (screen_height
                              if screen_height else monitor_sizes[0][1])
        self.screen = pygame.display.set_mode(
            (self.screen_width, self.screen_height)
        )
        pygame.display.set_caption("Pac-Man")

        # Load and scale background to current window dimensions
        self.background = pygame.image.load(
            f"{IMAGES}/backgrounds/general_background.jpg"
        ).convert()
        self.background = pygame.transform.scale(
            self.background, (self.screen_width, self.screen_height)
        )
        # Load and scale Menu background to current window dimensions
        self.menu_background = pygame.image.load(
            f"{IMAGES}/backgrounds/menu_background.jpg"
        ).convert()
        self.menu_background = pygame.transform.scale(
            self.menu_background, (self.screen_width, self.screen_height)
        )

        self.ingame = InGame(self.screen, self.engine)
        self.main = MainMenu(self.screen, self.engine)

    def run(self) -> None:
        while self.running:
            # 1. Event pump (mandatory to prevent window freeze)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False

            # 2. Rendering
            self.screen.blit(self.menu_background, (0, 0))
            if self.current_screen == "MAIN":
                state = self.main.run()
                if state and state == "start":
                    self.current_screen = "INGAME"
            elif self.current_screen == "INGAME":
                self.ingame.run()

            # 3. Display update & frame-rate cap
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
        sys.exit(0)


if __name__ == "__main__":
    renderer = Renderer()
    renderer.run()
