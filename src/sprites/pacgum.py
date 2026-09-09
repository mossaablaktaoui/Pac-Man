import pygame

from src.models.pacgum import Pacgum


class PacGum(pygame.sprite.Sprite, Pacgum):
    def __init__(self):
        pygame.sprite.Sprite.__init__()
        Pacgum.__init__()
