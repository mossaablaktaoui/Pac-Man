from src.screens import MainMenu, InGame, GameOver


class GameManager:
    def __init__(self,
                 screen,
                 screen_width: int = 1920,
                 screen_height: int = 1080
                 ) -> None:

        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.state = "INGAME"
        self.main_menu = None
        self.ingame = None
        self.current_screen = None

    def _get_current_screen(self):
        if self.state == "MAIN_MENU":
            if self.main_menu is None:
                self.main_menu = MainMenu(
                    self.screen_width, self.screen_height)
            self.current_screen = self.main_menu
        elif self.state == "INGAME":
            if self.ingame is None:
                self.ingame = InGame(self.screen)
            self.current_screen = self.ingame
        elif self.state == "GAME_OVER":
            if self.game_over is None:
                self.game_over = GameOver(
                    self.screen_width, self.screen_height)
            self.current_screen = self.game_over

    def run(self):
        self._get_current_screen()
        self.current_screen.run()
