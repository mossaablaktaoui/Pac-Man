import pygame


class PacGum(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.sprites = []

        self.assets = self.right
        self.link_assets()

        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]

        self.rect = self.image.get_rect()
        self.rect.center = [pos_x, pos_y]

    def link_assets(self):
        for asset in self.assets:
            image = pygame.image.load(asset)
            image = pygame.transform.scale(image, (50, 50))
            self.sprites.append(image)

    def update(self):
        self.current_sprite += 0.25
        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0
        self.image = self.sprites[int(self.current_sprite)]
