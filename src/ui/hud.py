import pygame

IMAGES = "assets/images"


class HUD:
    def __init__(self):
        self._images_cache = {}
        self.boards = [
            {
                "name": "score",
                "image": (f"{IMAGES}/boards/scoreboard.png"),
                "position": (0, 0),
                "value": 0
            },
            {
                "name": "level",
                "image": (f"{IMAGES}/boards/levelboard.png"),
                "position": (0, 0),
                "value": 0
            },
            {
                "name": "timer",
                "image": (f"{IMAGES}/boards/timerboard.png"),
                "position": (0, 0),
                "value": 0
            },
            {
                "name": "lives",
                "image": (f"{IMAGES}/boards/livesboard.png"),
                "position": (0, 0),
                "value": 0
            }
        ]

    def draw(self):
        for board in self.boards:
            if board["image"] not in self._images_cache:
                image = pygame.image.load(board["image"])
                image = pygame.transform.scale_by(image, 0.5)
                self._image_cache[board["image"]] = image
            
