import pygame

from src.core.engine import GameEngine
from src.views.maze_view import MazeRenderer
from src.views.hud_view import HUD
from src.views.sprite_view import SpriteView


class SrcInGame:
    def __init__(self,
                 screen: pygame.Surface,
                 engine: GameEngine) -> None:
        self.screen = screen
        self.engine = engine

        self.maze_renderer = MazeRenderer(self.engine)
        self.maze_surface = self.maze_renderer.draw()
        self.maze_xoffset = (self.screen.get_width() -
                             self.maze_surface.get_width()) // 2
        self.maze_yoffset = (self.screen.get_height() -
                             self.maze_surface.get_height()) // 2

        self.hud = HUD(self.screen)
        self.sprite_view = SpriteView(
            self.screen, self.maze_xoffset, self.maze_yoffset)

    def handle_event(self, event: pygame.event.Event) -> str | None:
        """Forward events to HUD or process gameplay keys."""
        return self.hud.handle_event(event)

    def draw(self, dt: float) -> None:
        """Render the maze and HUD."""
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
        self.sprite_view.draw(self.engine.gamestate, dt)
