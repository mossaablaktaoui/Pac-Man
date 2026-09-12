import sys
import pygame

from src.core.engine import GameEngine
from src.views.screens import (
    SrcInGame,
    SrcMainMenu,
    ScrHighscores,
    ScrInstructions,
    ScrPause,
    ScrVictory,
    ScrGameOver,
    ScrSaveScore,
)

IMAGES = "assets/images"


class Renderer:
    def __init__(
        self,
        screen_width: int | None = None,
        screen_height: int | None = None,
    ) -> None:
        pygame.init()
        pygame.mixer.init()
        self.clock = pygame.time.Clock()
        self.engine = GameEngine()
        self.running = True
        self.current_screen = "MAIN"
        self.current_level = self.engine.gamestate.level
        self.backgrounds: dict[str, pygame.Surface] = {}

        monitor_sizes = pygame.display.get_desktop_sizes()
        self.screen_width = (screen_width
                             if screen_width
                             else monitor_sizes[0][0])
        self.screen_height = (screen_height
                              if screen_height
                              else monitor_sizes[0][1])
        self.screen = pygame.display.set_mode(
            (self.screen_width, self.screen_height)
        )
        pygame.display.set_caption("Pac-Man")

        # Reusable dark overlay for PAUSE and SAVE screens
        self.overlay = pygame.Surface(
            (self.screen_width, self.screen_height), pygame.SRCALPHA
        )
        self.overlay.fill((0, 0, 0, 140))
        self.blurred_surface: pygame.Surface | None = None

        # Screens instantiation
        self.ingame = SrcInGame(self.screen, self.engine)
        self.main = SrcMainMenu(self.screen, self.engine)
        self.highscores = ScrHighscores(self.screen, self.engine)
        self.instructions = ScrInstructions(self.screen, self.engine)
        self.pause = ScrPause(self.screen, self.engine)
        self.victory = ScrVictory(self.screen, self.engine)
        self.gameover = ScrGameOver(self.screen, self.engine)
        self.save_score = ScrSaveScore(self.screen, self.engine)

        self.maze_renderer = self.ingame.maze_renderer
        self._load_backgrounds()

    def _load_backgrounds(self) -> None:
        bg_dir = f"{IMAGES}/backgrounds"
        bg_keys = ["highscores", "instructions", "menu", "victory", "gameover"]

        for key in bg_keys:
            img = pygame.image.load(f"{bg_dir}/{key}_background.jpg").convert()
            self.backgrounds[key] = pygame.transform.scale(
                img, (self.screen_width, self.screen_height)
            )

    def _snapshot_blur(self) -> None:
        """Capture the current frame and apply box blur."""
        frozen = self.screen.copy()
        self.blurred_surface = pygame.transform.box_blur(frozen, 8)

    def run(self) -> None:
        dt = 0.0
        while self.running:
            # 1. EVENT HANDLING (Only one event loop)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False

                if self.current_screen == "MAIN":
                    action = self.main.handle_event(event)
                    if action == "start":
                        self.engine.start_new_game()
                        self.maze_surface = self.maze_renderer.draw()
                        self.current_screen = "INGAME"
                    elif action == "instructions":
                        self.current_screen = "INSTRUCTIONS"
                    elif action == "highscores":
                        self.current_screen = "HIGHSCORES"

                elif self.current_screen == "INGAME":
                    action = self.ingame.handle_event(event)
                    if action == "menu":
                        self.current_screen = "MAIN"
                    elif action == "pause":
                        self._snapshot_blur()
                        self.current_screen = "PAUSE"

                elif self.current_screen == "PAUSE":
                    action = self.pause.handle_event(event)
                    if action == "menu":
                        self.current_screen = "MAIN"
                    elif action in ("resume", "replay"):
                        if action == "replay":
                            self.engine.start_new_game()
                            self.maze_surface = self.maze_renderer.draw()
                        self.current_screen = "INGAME"

                elif self.current_screen == "SAVE":
                    action = self.save_score.handle_event(event)
                    if action in ("victory", "gameover"):
                        self.engine.save_highscore(self.save_score.user_text)
                        self.current_screen = (
                            "VICTORY" if action == "victory" else "GAMEOVER"
                        )

                elif self.current_screen == "HIGHSCORES":
                    action = self.highscores.handle_event(event)
                    if action == "menu":
                        self.current_screen = "MAIN"
                elif self.current_screen == "INSTRUCTIONS":
                    action = self.instructions.handle_event(event)
                    if action == "menu":
                        self.current_screen = "MAIN"
                    elif action == "start":
                        self.engine.start_new_game()
                        self.maze_surface = self.maze_renderer.draw()
                        self.current_screen = "INGAME"
                elif self.current_screen == "VICTORY":
                    action = self.victory.handle_event(event)
                    if action == "menu":
                        self.current_screen = "MAIN"
                    elif action == "highscores":
                        self.current_screen = "HIGHSCORES"
                elif self.current_screen == "GAMEOVER":
                    action = self.gameover.handle_event(event)
                    if action == "menu":
                        self.current_screen = "MAIN"
                    elif action == "replay":
                        self.engine.start_new_game()
                        self.maze_surface = self.maze_renderer.draw()
                        self.current_screen = "INGAME"

            # 2. STATE CHECKS & LOGIC UPDATE
            if self.current_screen == "INGAME":
                if self.current_level != self.engine.gamestate.level:
                    self.maze_surface = self.maze_renderer.draw()
                if (self.engine.gamestate.is_game_over or
                        self.engine.gamestate.is_victory):
                    self.save_score.user_text = ""
                    self._snapshot_blur()
                    self.current_screen = "SAVE"
                elif not self.engine.gamestate.is_paused:
                    self.engine.update(dt)

            # 3. DRAWING
            if self.current_screen == "MAIN":
                self.screen.blit(self.backgrounds["menu"], (0, 0))
                self.main.draw()
            elif self.current_screen == "INGAME":
                self.screen.blit(self.backgrounds["menu"], (0, 0))
                self.ingame.draw(dt)
            elif self.current_screen == "HIGHSCORES":
                self.screen.blit(self.backgrounds["highscores"], (0, 0))
                self.highscores.refresh()
                self.highscores.draw()
            elif self.current_screen == "INSTRUCTIONS":
                self.screen.blit(self.backgrounds["instructions"], (0, 0))
                self.instructions.draw()
            elif self.current_screen == "VICTORY":
                self.screen.blit(self.backgrounds["victory"], (0, 0))
                self.victory.draw()
            elif self.current_screen == "GAMEOVER":
                self.screen.blit(self.backgrounds["gameover"], (0, 0))
                self.gameover.draw()
            elif self.current_screen in ("PAUSE", "SAVE"):
                if self.blurred_surface:
                    self.screen.blit(self.blurred_surface, (0, 0))
                self.screen.blit(self.overlay, (0, 0))
                if self.current_screen == "PAUSE":
                    self.pause.draw()
                else:
                    self.save_score.draw()

            pygame.display.flip()
            dt = self.clock.tick(60) / 1000.0

        pygame.quit()
        sys.exit(0)


if __name__ == "__main__":
    renderer = Renderer()
    renderer.run()
