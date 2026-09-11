import pygame

from src.core.entities import Direction
from src.core.cheats import CheatCode

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
        action = self.hud.handle_event(event)
        if action == "pause":
            self.engine.toggle_pause()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                self.engine.toggle_pause()
                action = "pause"
            if event.key == pygame.K_r:
                self.engine.start_new_game()
                action = "replay"
            if event.key == pygame.K_q:
                action = "menu"
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                self.engine.set_player_direction(Direction.UP)
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                self.engine.set_player_direction(Direction.DOWN)
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                self.engine.set_player_direction(Direction.LEFT)
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                self.engine.set_player_direction(Direction.RIGHT)
            if event.key == pygame.K_k:
                self.engine.toggle_cheat(CheatCode.SKIP_LEVEL)
            if event.key == pygame.K_l:
                self.engine.toggle_cheat(CheatCode.SPEED)
            if event.key == pygame.K_h:
                self.engine.toggle_cheat(CheatCode.UNLIMITED_LIFE)
            if event.key == pygame.K_j:
                self.engine.toggle_cheat(CheatCode.FREEZE_GHOSTS)
        if self.engine.gamestate.is_game_over:
            action = "gameover"
        if self.engine.gamestate.is_victory:
            action = "victory"
        return action

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
            self.engine.gamestate.active_cheats
        )
        self.sprite_view.draw(self.engine.gamestate, dt)
