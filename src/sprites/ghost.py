import pygame


class PacGum(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.sprites = []
        self.assets = [
            "assets/icons/dead-pacman1.png",
            "assets/icons/dead-pacman2.png",
            "assets/icons/dead-pacman3.png",
            "assets/icons/dead-pacman4.png",
            "assets/icons/dead-pacman5.png",
            "assets/icons/dead-pacman6.png",
            "assets/icons/dead-pacman7.png",
            "assets/icons/dead-pacman8.png",
            "assets/icons/dead-pacman9.png",
            "assets/icons/dead-pacman10.png",
            "assets/icons/dead-pacman11.png",
            "assets/icons/dead-pacman12.png",
            "assets/icons/dead-pacman13.png",
            "assets/icons/dead-pacman14.png",
            ]

        for asset in self.assets:
            image = pygame.image.load(asset)
            image = pygame.transform.scale(image, (50, 50))
            self.sprites.append(image)

        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]

        self.rect = self.image.get_rect()
        self.rect.center = [pos_x, pos_y]

    def update(self):
        self.current_sprite += 0.25
        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0
        self.image = self.sprites[int(self.current_sprite)]
