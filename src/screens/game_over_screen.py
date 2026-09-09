import sys
import pygame


class GameOver:
    def __init__(self,
                 screen_width: int = 1920,
                 screen_height: int = 1080
                 ) -> None:

        self.screen = pygame.display.set_mode(
            (screen_width, screen_height))
        self.background = pygame.image.load(
            "assets/images/backgrounds/your_name.jpg")
        self.background = pygame.transform.scale(self.background, (1920, 1080))

    def run(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.crosshair.click()

        self.screen.blit(self.background, (0, 0))
        pygame.display.flip()
