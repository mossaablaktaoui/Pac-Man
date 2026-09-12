import sys
import pygame
from typing import Dict, List

from src.core.engine import GameEngine

BUTTONS_DIR = "assets/images/buttons"
GHOSTS_DIR = "assets/images/ghosts"
PACMAN_DIR = "assets/images/pacman"


class SrcMainMenu:
    def __init__(self,
                 screen: pygame.surface.Surface,
                 engine: GameEngine) -> None:
        self.screen = screen
        self.buttons: List[Dict] = []
        self.ghosts: List[Dict] = []
        self.pacman_frames: List = []
        self.selected_btn = "START"

        self.width = self.screen.get_width()
        self.height = self.screen.get_height()

        center_x = self.width // 2
        self.logo = pygame.image.load(f"{BUTTONS_DIR}/Pacman-logo.png")
        self.logo = pygame.transform.scale_by(self.logo, 0.25)
        self.logo_rect = self.logo.get_rect()
        self.logo_rect.center = (center_x, int(self.screen.get_height() * 0.2))
        self._load_buttons()
        self._load_pacman()
        self._load_ghosts()

    def _load_pacman(self) -> None:
        for i in range(1, 5):
            img = pygame.image.load(f"{PACMAN_DIR}/pacman{i}.png"
                                    ).convert_alpha()
            img = pygame.transform.scale_by(img, 6)
            self.pacman_frames.append(img)
        self.pacman_rect = self.pacman_frames[0].get_rect()
        self.pacman_rect.center = (int(self.width * 0.23),
                                   int(self.height * 0.62))

    def _load_buttons(self) -> None:
        button_configs = [
            ("start", 0.35),
            ("instructions", 0.47),
            ("highscores", 0.59),
            ("quit", 0.71),
        ]

        center_x = self.width // 2
        for name, y_ratio in button_configs:
            idle_img = pygame.image.load(
                f"{BUTTONS_DIR}/{name}_idle.png"
            ).convert_alpha()
            hover_img = pygame.image.load(
                f"{BUTTONS_DIR}/{name}_hover.png"
            ).convert_alpha()
            idle_img = pygame.transform.scale_by(idle_img, 0.5)
            hover_img = pygame.transform.scale_by(hover_img, 0.5)

            rect = idle_img.get_rect()
            rect.center = (center_x, int(self.screen.get_height() * y_ratio))

            self.buttons.append({
                "name": name,
                "idle": idle_img,
                "hover": hover_img,
                "rect": rect,
            })

    def _load_ghosts(self) -> None:
        # Ghosts on the left face right; ghosts on the right face left
        ghost_configs = [
            ("blinky", (0.14, 0.32), "right"),
            ("clyde",  (0.22, 0.41), "right"),
            ("inky",   (0.76, 0.55), "left"),
            ("pinky",  (0.85, 0.29), "left"),
        ]

        for name, ratio, direction in ghost_configs:
            frames = []
            for frame_num in (1, 2):
                img = pygame.image.load(
                    f"{GHOSTS_DIR}/{name}-{direction}{frame_num}.png"
                ).convert_alpha()
                img = pygame.transform.scale_by(img, 7)
                frames.append(img)

            rect = frames[0].get_rect()
            rect.center = (int(self.width * ratio[0]),
                           int(self.height * ratio[1]))

            self.ghosts.append({
                "frames": frames,
                "rect": rect,
            })

    def _draw_pacgums(self) -> None:
        pellet_color = (255, 227, 0)
        y = int(self.height * 0.62)
        spacing = 45
        mouth_x = self.pacman_rect.centerx
        end_x = int(self.width * 0.50)

        offset = (pygame.time.get_ticks() // 12) % spacing

        # Start drawing just to the right of Pac-Man's mouth
        x = mouth_x + spacing - offset
        while x < end_x:
            pygame.draw.circle(self.screen, pellet_color,
                               (int(x), y), radius=9)
            x += spacing

    def handle_event(self, event: pygame.event.Event) -> str | None:
        """Handle mouse clicks. Returns button name or None."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for btn in self.buttons:
                if btn["rect"].collidepoint(event.pos):
                    if btn["name"] == "quit":
                        pygame.quit()
                        sys.exit(0)
                    return str(btn["name"])
        return None

    def draw(self) -> None:
        """Draw buttons based on current mouse hover position."""
        mouse_pos = pygame.mouse.get_pos()
        self.screen.blit(self.logo, self.logo_rect)
        self._draw_pacgums()

        for btn in self.buttons:
            if btn["rect"].collidepoint(mouse_pos):
                self.screen.blit(btn["hover"], btn["rect"])
            else:
                self.screen.blit(btn["idle"], btn["rect"])

        frame_idx = (pygame.time.get_ticks() // 200) % 2
        for ghost in self.ghosts:
            self.screen.blit(ghost["frames"][frame_idx], ghost["rect"])

        pac_idx = (pygame.time.get_ticks() // 200) % 4
        self.screen.blit(self.pacman_frames[pac_idx], self.pacman_rect)
