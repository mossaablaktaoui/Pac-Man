import sys
import pygame
from typing import Tuple

from src.sprites.pacman import PacMan
# from src.sprites.ghost import Ghost
# from src.sprites.pacgum import Pacgum

IMAGES = "assets/images"
X_OFFSET = 560
Y_OFFSET = 140


class InGame:
    def __init__(self) -> None:

        self.font = pygame.font.Font("assets/fonts/pacfont.ttf", 14)
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.background = pygame.image.load(
            f"{IMAGES}/backgrounds/general_background.jpg")
        self.background = pygame.transform.scale(self.background, (1920, 1080))

        self.spritesgroup = pygame.sprite.Group()
        self.scoreboard = pygame.image.load(f"{IMAGES}/boards/scoreboard.png")
        self.scoreboard = pygame.transform.scale_by(self.scoreboard, 0.5)
        self.sb_rect = self.scoreboard.get_rect()
        self.levelboard = pygame.image.load(f"{IMAGES}/boards/levelboard.png")
        self.levelboard = pygame.transform.scale_by(self.levelboard, 0.5)
        self.livesboard = pygame.image.load(f"{IMAGES}/boards/livesboard.png")
        self.livesboard = pygame.transform.scale_by(self.livesboard, 0.5)
        self.timerboard = pygame.image.load(f"{IMAGES}/boards/timerboard.png")
        self.timerboard = pygame.transform.scale_by(self.timerboard, 0.5)

        # self.ghosts: List[Ghost] = []
        # self.pacgums: List[Pacgum] = []

        self.current_level = 0
        self.level_time = 0.0
        self.score = 0
        text_score = f"SCORE: {self.score}"
        self.score_surface = self._generate_text_surface(
            text_score, (0, 255, 255)
        )

        start_x, start_y = self.grid_to_pixel(9, 10)
        self.player = PacMan(start_x, start_y, size=30)
        self.spritesgroup.add(self.player)

    def _generate_text_surface(
            self, text: str,
            color: Tuple[int, int, int]
            ) -> pygame.surface.Surface:
        return self.font.render(text, True, color)

    def run(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self._maze_surface, (X_OFFSET, Y_OFFSET))
        self.screen.blit(self.scoreboard, (100, 100))
        self.screen.blit(self.livesboard, (100, 200))
        self.screen.blit(self.timerboard, (100, 300))
        self.screen.blit(self.levelboard, (100, 400))
        self.score_surface = self._generate_text_surface(
            f"SCORE: {self.score}", (0, 255, 255)
        )
        self.tsb_rect = self.score_surface.get_rect()
        self.tsb_rect.center = self.sb_rect.center
        self.screen.blit(self.score_surface, (100, 500))
        self.spritesgroup.update()
        self.screen.blit(
            self.player.image,
            (X_OFFSET + self.player.rect.x, Y_OFFSET + self.player.rect.y),
        )
        self.score += 3
        pygame.display.flip()
