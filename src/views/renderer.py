import pygame

from src.views.maze_view import MazeRenderer

IMAGES = "assets/images"


class Renderer:
    def __init__(self,
                 screen_width: int = 1920,
                 screen_height: int = 1080):
        pygame.init()
        pygame.mixer.init()
        pygame.mouse.set_visible(False)
        self.clock = pygame.time.Clock()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.background = pygame.image.load(
            f"{IMAGES}/backgrounds/general_background.jpg")
        self.background = pygame.transform.scale(self.background, (1920, 1080))

        self.maze = MazeRenderer()
        self.maze_surface = self.maze.draw()

    def run(self):
        while True:
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.maze_surface, (100, 100))

            pygame.display.flip()
            self.clock.tick(60)


if __name__ == "__main__":
    maze = Renderer()
