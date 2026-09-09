import pygame


class CrossHair(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/images/icons/crosshair.png")
        self.sound = pygame.mixer.Sound("assets/sounds_effect/crosshair.mp3")
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()

    def click(self):
        self.sound.play()

    def update(self):
        self.rect.center = pygame.mouse.get_pos()
