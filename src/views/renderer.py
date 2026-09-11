import sys
import pygame

from src.core.engine import GameEngine
from src.views.screens import (
    SrcInGame, SrcMainMenu,
    ScrHighscores, ScrInstructions,
    ScrPause, ScrVictory, ScrGameOver
    )

IMAGES = "assets/images"


class Renderer:
    def __init__(self,
                 screen_width: int | None = None,
                 screen_height: int | None = None):
        pygame.init()
        pygame.mixer.init()
        self.clock = pygame.time.Clock()
        self.engine = GameEngine()
        self.running = True
        self.current_screen = "GAMEOVER"
        self.backgrounds: dict = {}

        monitor_sizes = pygame.display.get_desktop_sizes()
        self.screen_width = (screen_width
                             if screen_width else monitor_sizes[0][0])
        self.screen_height = (screen_height
                              if screen_height else monitor_sizes[0][1])
        self.screen = pygame.display.set_mode(
            (self.screen_width, self.screen_height)
        )

        self.ingame = SrcInGame(self.screen, self.engine)
        self.main = SrcMainMenu(self.screen, self.engine)
        self.highscores = ScrHighscores(self.screen, self.engine)
        self.instructions = ScrInstructions(self.screen, self.engine)
        self.pause = ScrPause(self.screen, self.engine)
        self.victory = ScrVictory(self.screen, self.engine)
        self.gameover = ScrGameOver(self.screen, self.engine)
        self._load_backgrounds()
        pygame.display.set_caption("Pac-Man")

    def _load_backgrounds(self):
        background_dir = f"{IMAGES}/backgrounds"
        backgrounds_config = [
            "highscores",
            "instructions",
            "menu",
            "victory",
            "gameover",
        ]

        for background in backgrounds_config:
            img = pygame.image.load(
                f"{background_dir}/{background}_background.jpg").convert()
            img = pygame.transform.scale(
                img, (self.screen_width, self.screen_height))
            self.backgrounds[background] = img

    def run(self) -> None:
        dt = 0.0
        while self.running:
            # 1. The ONLY event loop in the whole program
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif (event.type == pygame.KEYDOWN
                      and event.key == pygame.K_ESCAPE):
                    self.running = False

                # Dispatch events to the active screen
                if self.current_screen == "MAIN":
                    action = self.main.handle_event(event)
                    if action == "start":
                        self.current_screen = "INGAME"
                    elif action == "instructions":
                        self.current_screen = "INSTRUCTIONS"
                    elif action == "highscores":
                        self.current_screen = "HIGHSCORES"
                elif self.current_screen == "INGAME":
                    action = self.ingame.handle_event(event)
                    if action == "menu":
                        self.current_screen = "MAIN"
                    elif action == "victory":
                        self.current_screen = "VICTORY"
                    elif action == "gameover":
                        self.current_screen = "GAMEOVER"
                    elif action == "pause":
                        frozen_surface = self.screen.copy()
                        blured_surface = pygame.transform.box_blur(
                            frozen_surface, 8)
                        self.current_screen = "PAUSE"
                elif self.current_screen == "HIGHSCORES":
                    action = self.highscores.handle_event(event)
                    if action == "menu":
                        self.current_screen = "MAIN"
                elif self.current_screen == "INSTRUCTIONS":
                    action = self.instructions.handle_event(event)
                    if action == "menu":
                        self.current_screen = "MAIN"
                    elif action == "start":
                        self.current_screen = "INGAME"
                elif self.current_screen == "PAUSE":
                    action = self.pause.handle_event(event)
                    if action == "menu":
                        self.current_screen = "MAIN"
                    elif action == "replay":
                        pass
                    elif action == "resume":
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
                        pass

            # 2. Draw active screen
            if self.current_screen == "MAIN":
                self.screen.blit(self.backgrounds["menu"], (0, 0))
                self.main.draw()
            elif self.current_screen == "INGAME":
                self.screen.blit(self.backgrounds["menu"], (0, 0))
                self.ingame.draw(dt)
            elif self.current_screen == "HIGHSCORES":
                self.screen.blit(self.backgrounds["highscores"], (0, 0))
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
            elif self.current_screen == "PAUSE":
                overlay = pygame.Surface(blured_surface.get_size(),
                                         pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 120))
                self.screen.blit(blured_surface, (0, 0))
                self.screen.blit(overlay, (0, 0))
                self.pause.draw()

            # 3. Exactly ONE flip per frame
            pygame.display.flip()
            dt = self.clock.tick(60) / 1000.0

        pygame.quit()
        sys.exit(0)


if __name__ == "__main__":
    renderer = Renderer()
    renderer.run()
