import pygame

from src.game_manager import GameManager


class Renderer:
    def __init__(self,
                 screen_width: int = 1920,
                 screen_height: int = 1080):
        pygame.init()
        pygame.mixer.init()
        pygame.mouse.set_visible(False)
        self.clock = pygame.time.Clock()

        self.game_manager = GameManager(screen_width, screen_height)

    def run(self):
        while True:
            self.game_manager.run()

            self.clock.tick(60)


if __name__ == "__main__":
    maze = Renderer()
