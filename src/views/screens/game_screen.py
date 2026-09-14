"""In-game active gameplay screen controller and renderer."""

import pygame

from src.core.entities import Direction
from src.core.cheats import CheatCode

from src.core.engine import GameEngine
from src.views.maze_view import MazeRenderer
from src.views.hud_view import HUD
from src.views.sprite_view import SpriteView


class SrcInGame:
    """Manages gameplay view, input handling, and ready timers."""

    def __init__(self,
                 screen: pygame.Surface,
                 engine: GameEngine) -> None:
        self.screen = screen
        self.engine = engine
        self.ready_timer = 5.0

        self.width = self.screen.get_width()
        self.height = self.screen.get_height()

        self.maze_renderer = MazeRenderer(self.engine)
        self.maze_surface = self.maze_renderer.draw()
        self.maze_xoffset = (self.width - self.maze_surface.get_width()) // 2
        self.maze_yoffset = (self.height - self.maze_surface.get_height()) // 2

        try:
            self.font = pygame.font.Font("assets/fonts/pacfont.ttf", 40)
        except (FileNotFoundError, pygame.error):
            self.font = pygame.font.Font(None, 40)

        self.hud = HUD(self.screen)
        self.sprite_view = SpriteView(
            self.screen, self.engine, self.maze_xoffset, self.maze_yoffset)

        self._snapshot_blur()

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
                self.maze_surface = self.maze_renderer.draw()
            if event.key == pygame.K_l:
                self.engine.toggle_cheat(CheatCode.SPEED)
            if event.key == pygame.K_h:
                self.engine.toggle_cheat(CheatCode.UNLIMITED_LIFE)
            if event.key == pygame.K_j:
                self.engine.toggle_cheat(CheatCode.FREEZE_GHOSTS)
        return action

    def reset_ready(self) -> None:
        """Reset countdown for game start or new levels."""
        self.ready_timer = 4.0

    def _snapshot_blur(self) -> None:
        """Capture the current frame and apply box blur."""
        frozen = self.screen.copy()
        self.blurred_surface = pygame.transform.box_blur(frozen, 8)
        self.overlay = pygame.Surface(
                (self.width, self.height), pygame.SRCALPHA
        )
        self.overlay.fill((0, 0, 0, 140))

    def draw(self, dt: float) -> None:
        """Render the maze, HUD, entity sprites, and ready banner."""
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

        if self.ready_timer > 0:
            self.screen.blit(self.blurred_surface, (0, 0))
            self.screen.blit(self.overlay)
            self.ready_timer -= dt
            text = (f"LEVEL {self.engine.gamestate.level}"
                    if self.ready_timer > 4 else str(int(self.ready_timer))
                    if self.ready_timer > 1 else "READY!")
            ready_text = self.font.render(text, True, (255, 255, 255))
            ready_rect = ready_text.get_rect()
            ready_rect.center = [self.width // 2, self.height // 2]
            self.screen.blit(ready_text, ready_rect)
