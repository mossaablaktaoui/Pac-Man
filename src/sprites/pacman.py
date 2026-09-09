from src.player import Player

import pygame


class PacMan(pygame.sprite.Sprite, Player):
    def __init__(self, pos_x, pos_y):
        pygame.sprite.Sprite.__init__(self)
        Player.__init__(self, pos_x, pos_y)
        self.sprites = []
        self._image_cache = {}

        self.dead = [
            f"assets/images/pacman/dead{i}.png" for i in range(1, 17)
        ]

        self.right = [
            f"assets/images/pacman/right{i}.png" for i in range(1, 5)
        ]

        self.left = [
            f"assets/images/pacman/left{i}.png" for i in range(1, 5)
        ]

        self.up = [
            f"assets/images/pacman/up{i}.png" for i in range(1, 5)
        ]

        self.down = [
            f"assets/images/pacman/down{i}.png" for i in range(1, 5)
        ]

        self.current_sprite = 0
        self.assets = self.right
        self._link_assets()
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.center = [pos_x, pos_y]

    def _link_assets(self):
        self.sprites = []
        for asset in self.assets:
            if asset not in self._image_cache:
                image = pygame.image.load(asset)
                image = pygame.transform.scale(image, (50, 50))
                self._image_cache[asset] = image
            self.sprites.append(self._image_cache[asset])

    def move(self, x: int, y: int) -> None:
        super().move(x, y)
        self.rect.center = [self.x, self.y]

    def _check_direction(self):
        prev_assets = self.assets
        if self.direction == "RIGHT":
            self.assets = self.right
        elif self.direction == "LEFT":
            self.assets = self.left
        elif self.direction == "UP":
            self.assets = self.up
        elif self.direction == "DOWN":
            self.assets = self.down

        if self.assets != prev_assets:
            self._link_assets()
            self.current_sprite = 0

    def update(self):
        self._check_direction()
        self.current_sprite += 0.25
        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0
        self.image = self.sprites[int(self.current_sprite)]
