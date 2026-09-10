import pygame

from src.core.engine import GameEngine
from src.views.maze_view import MazeRenderer
from src.views.hud_view import HUD

IMAGES = "assets/images"


class InGame:
    def __init__(self,
                 screen: pygame.surface.Surface,
                 engine: GameEngine) -> None:
        self.screen = screen
        self.engine = engine

        # Maze pre-rendring
        self.maze_renderer = MazeRenderer(self.engine)
        self.maze_surface = self.maze_renderer.draw()
        self.maze_xoffset = (self.screen.get_width() -
                             self.maze_surface.get_width()) // 2
        self.maze_yoffset = (self.screen.get_height() -
                             self.maze_surface.get_height()) // 2

        # Set the on screen layouts
        self.hud = HUD(self.screen)

    def run(self):
        self.screen.blit(
            self.maze_surface,
            (self.maze_xoffset, self.maze_yoffset)
        )
        self.hud.draw(
            self.engine.gamestate.score,
            self.engine.gamestate.lives,
            self.engine.gamestate.time_remaining,
            self.engine.gamestate.level,
        )

        action = None
        for event in pygame.event.get():
            result = self.hud.handle_event(event)
            if result:
                action = result
        pygame.display.flip()
        return action
