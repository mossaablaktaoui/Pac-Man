import pygame
import sys

from src.sprites.crosshair import CrossHair
from src.sprites.ghost import PacGum


class Renderer:
    def __init__(self,
                 screen_width: int = 1920,
                 screen_height: int = 1080):
        pygame.init()
        pygame.mixer.init()
        self.clock = pygame.time.Clock()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.background = pygame.image.load("assets/backgrounds/your_name.jpg")
        self.background = pygame.transform.scale(self.background, (1920, 1080))

        pygame.mouse.set_visible(False)

        self.crosshair = CrossHair()
        self.pacgum = PacGum(100, 100)
        self.crosshairgroup = pygame.sprite.Group()
        self.crosshairgroup.add(self.crosshair)
        self.crosshairgroup.add(self.pacgum)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.crosshair.click()

            pygame.display.flip()
            self.screen.blit(self.background, (0, 0))
            self.crosshairgroup.draw(self.screen)
            self.crosshairgroup.update()
            self.clock.tick(30)


if __name__ == "__main__":
    maze = Renderer()
