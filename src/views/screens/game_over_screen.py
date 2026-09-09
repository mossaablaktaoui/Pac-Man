import sys
import pygame


class GameOver:
    def __init__(self, screen) -> None:
        self.screen = screen

    def run(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.flip()
