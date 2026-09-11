"""Entity renderer handling animation states and drawing
for Pac-Man and ghosts."""

import pygame
from src.core.entities import (
    GameStateDT,
    GhostState,
    SpriteDT,
)

TILE_SIZE = 55
ASSETS_SIZE = TILE_SIZE - 10
MARGIN = 7


class SpriteView:
    """Manages animation frame advancement and rendering of game entities."""

    def __init__(self,
                 screen: pygame.Surface,
                 xoffset: int, yoffset: int
                 ) -> None:
        self.screen = screen

        self.xoffset = xoffset
        self.yoffset = yoffset
        # Animation counters
        self.anim_timer = 0.0
        self.move_frame = 0
        self.flash_frame = 0
        self.death_frame_idx = 0.0

        self.pacman_sprites: dict[str, list[pygame.Surface]] = {}
        self.ghost_sprites: dict[str, dict[str, list[pygame.Surface]]] = {}
        self.eyes_sprites: dict[str, pygame.Surface] = {}
        self.special_sprites: dict[str, list[pygame.Surface]] = {}

        self._load_pacman_assets()
        self._load_ghost_assets()

    def grid_to_pixel(self, grid_x: int, grid_y: int) -> tuple[int, int]:
        """Convert maze grid coordinates to centered
        screen pixel coordinates."""
        px = (self.xoffset + MARGIN + grid_x * TILE_SIZE + TILE_SIZE // 2)
        py = (self.yoffset + MARGIN + grid_y * TILE_SIZE + TILE_SIZE // 2)
        return px, py

    def _load_pacman_assets(self) -> None:
        base_dir = "assets/images/pacman"
        directions = ["right", "up", "left", "down"]

        for d in directions:
            frames = []
            for i in range(1, 5):
                img = pygame.image.load(
                    f"{base_dir}/{d}{i}.png").convert_alpha()
                img = pygame.transform.scale(
                    img, (ASSETS_SIZE, ASSETS_SIZE))
                frames.append(img)
            self.pacman_sprites[d] = frames

        self.pacman_sprites["dead"] = [
            pygame.transform.scale(
                pygame.image.load(f"{base_dir}/dead{i}.png").convert_alpha(),
                (ASSETS_SIZE, ASSETS_SIZE),
            )
            for i in range(1, 17)
        ]

    def _load_ghost_assets(self) -> None:
        ghost_dir = "assets/images/ghosts"
        ghost_names = ["blinky", "pinky", "inky", "clyde"]
        directions = ["right", "up", "left", "down"]

        # 1. Directional sprites (using hyphen matching
        # your files: blinky-right1.png)
        for name in ghost_names:
            self.ghost_sprites[name] = {}
            for d in directions:
                frames = []
                for i in range(1, 3):
                    img = pygame.image.load(
                        f"{ghost_dir}/{name}-{d}{i}.png"
                    ).convert_alpha()
                    img = pygame.transform.scale(
                        img, (ASSETS_SIZE, ASSETS_SIZE))
                    frames.append(img)
                self.ghost_sprites[name][d] = frames

        # 2. Edible (Blue) and Flashing (White/Blue)
        self.special_sprites["edible"] = [
            pygame.transform.scale(
                pygame.image.load(
                    f"{ghost_dir}/edible{i}.png").convert_alpha(),
                (ASSETS_SIZE, ASSETS_SIZE),
            )
            for i in range(1, 3)
        ]
        self.special_sprites["flashing"] = [
            pygame.transform.scale(
                pygame.image.load(f"{ghost_dir}/flash{i}.png").convert_alpha(),
                (ASSETS_SIZE, ASSETS_SIZE),
            )
            for i in range(1, 3)
        ]

        # 3. Eyes only (when eaten)
        for i, d in enumerate(directions):
            img = pygame.image.load(
                f"{ghost_dir}/eyes{i + 1}.png").convert_alpha()
            self.eyes_sprites[d] = pygame.transform.scale(
                img, (ASSETS_SIZE, ASSETS_SIZE)
            )

    def update_animations(self, dt: float) -> None:
        """Advance animation counters."""
        self.anim_timer += dt
        if self.anim_timer >= 0.12:
            self.anim_timer = 0.0
            self.move_frame = (self.move_frame + 1) % 4
            self.flash_frame = (self.flash_frame + 1) % 2

    def draw(self, state: GameStateDT, dt: float) -> None:
        """Render pellets, Pac-Man, and ghosts
        at the dynamic maze screen offsets."""
        self.update_animations(dt)
        self._draw_pacgums(state)
        self._draw_pacman(state.pacman, dt)
        self._draw_ghosts(state.ghosts)

    def _draw_pacgums(self, state: GameStateDT) -> None:
        pellet_color = (255, 184, 151)
        for pellet in state.pacgums:
            center = self.grid_to_pixel(pellet.grid_x, pellet.grid_y)
            if pellet.is_super:
                radius = 8 if (self.move_frame % 2 == 0) else 6
                pygame.draw.circle(self.screen, pellet_color, center, radius)
            else:
                pygame.draw.circle(self.screen, pellet_color, center, 3)

    def _draw_pacman(self, pac: SpriteDT, dt: float) -> None:
        center = self.grid_to_pixel(pac.grid_x, pac.grid_y)

        if pac.state == "DEAD":
            self.death_frame_idx += dt * 13.0
            frame = min(int(self.death_frame_idx), 15)
            img = self.pacman_sprites["dead"][frame]
        else:
            self.death_frame_idx = 0.0
            dir_key = pac.direction.value.lower()
            img = self.pacman_sprites[dir_key][self.move_frame]

        rect = img.get_rect(center=center)
        self.screen.blit(img, rect)

    def _draw_ghosts(self, ghosts: list[SpriteDT]) -> None:
        for ghost in ghosts:
            center = self.grid_to_pixel(ghost.grid_x, ghost.grid_y)
            dir_key = ghost.direction.value.lower()
            state_str = (
                ghost.state.value
                if hasattr(ghost.state, "value")
                else str(ghost.state)
            )

            if state_str == GhostState.EDIBLE.value:
                img = self.special_sprites["edible"][self.move_frame % 2]
            elif state_str == GhostState.FLASHING.value:
                img = self.special_sprites["flashing"][self.flash_frame]
            elif state_str == GhostState.EATEN.value:
                img = self.eyes_sprites[dir_key]
            else:
                ghost_id = ghost.id.lower()
                frames = self.ghost_sprites[ghost_id][dir_key]
                img = frames[self.move_frame % 2]

            rect = img.get_rect(center=center)
            self.screen.blit(img, rect)
