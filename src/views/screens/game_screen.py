import sys
import pygame

# from src.sprites.pacman import PacMan
# from src.sprites.ghost import Ghost
# from src.sprites.pacgum import Pacgum
from src.rendering.maze_renderer import MazeRenderer
from src.ui.hud import HUD

IMAGES = "assets/images"
X_OFFSET = 560
Y_OFFSET = 140


class InGame:
    def __init__(self, screen) -> None:
        self.screen = screen
        self.maze_renderer = MazeRenderer()
        self.hud = HUD()

    def run(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        self.screen.blit(
            self.maze_renderer._maze_surface, (X_OFFSET, Y_OFFSET)
        )
        self.hud.draw(
            self.screen,
            score=0,
            lives=3,
            time_left=0.0,
            level=1,
        )
        pygame.display.flip()
