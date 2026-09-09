import sys
import pygame

from src.sprites.crosshair import CrossHair


class MainMenu:
    def __init__(self, screen) -> None:

        self.screen = screen
        self.crosshair = CrossHair()

    def run(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.crosshair.click()

        self.crosshair.update()
        pygame.display.flip()
