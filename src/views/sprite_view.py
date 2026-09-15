"""Entity renderer handling animation states and drawing
for Pac-Man and ghosts."""

from typing import Any
import pygame
from src.core.engine import GameEngine
from src.core.entities import (
    GameStateDT,
    GhostState,
    SpriteDT,
    PacgumDT,
)

TILE_SIZE = 55
ASSETS_SIZE = TILE_SIZE - 10
MARGIN = 7


class SpriteView:
    """Manages animation frame advancement and rendering of game entities."""

    def __init__(self,
                 screen: pygame.Surface,
                 engine: GameEngine,
                 xoffset: int, yoffset: int
                 ) -> None:
        """Initialize entity sprite view, animation timers, and assets."""
        self.screen = screen
        self.engine = engine

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
        self.entity_tracks: dict[str, dict[str, Any]] = {}

        self._load_pacman_assets()
        self._load_ghost_assets()

    def grid_to_pixel(self, entity: SpriteDT | PacgumDT) -> tuple[int, int]:
        """Convert maze grid coordinates to centered
        screen pixel coordinates."""
        x = entity.grid_x
        y = entity.grid_y

        px = (self.xoffset + MARGIN + x * TILE_SIZE + TILE_SIZE // 2)
        py = (self.yoffset + MARGIN + y * TILE_SIZE + TILE_SIZE // 2)
        return px, py

    def _get_interpolated_pixel(
            self, entity_id: str, grid_x: int, grid_y: int,
            dt: float, duration: float = 0.2) -> tuple[int, int]:
        """Calculate smooth sub-tile pixel coordinate interpolated
        across dt."""

        if entity_id not in self.entity_tracks:
            self.entity_tracks[entity_id] = {
                "prev_x": float(grid_x),
                "prev_y": float(grid_y),
                "curr_x": grid_x,
                "curr_y": grid_y,
                "timer": duration,
            }

        track = self.entity_tracks[entity_id]

        if grid_x != track["curr_x"] or grid_y != track["curr_y"]:
            dist = (abs(grid_x - track["curr_x"]) +
                    abs(grid_y - track["curr_y"]))

            if dist > 1:
                track["prev_x"] = float(grid_x)
                track["prev_y"] = float(grid_y)
            else:
                track["prev_x"] = float(track["curr_x"])
                track["prev_y"] = float(track["curr_y"])

            track["curr_x"] = grid_x
            track["curr_y"] = grid_y
            track["timer"] = 0.0

        track["timer"] = min(duration, track["timer"] + dt)
        progress = track["timer"] / duration if duration > 0 else 1.0

        interp_x = (track["prev_x"] + (track["curr_x"] - track["prev_x"])
                    * progress)
        interp_y = (track["prev_y"] + (track["curr_y"] - track["prev_y"])
                    * progress)

        px = int(self.xoffset + MARGIN + interp_x * TILE_SIZE + TILE_SIZE // 2)
        py = int(self.yoffset + MARGIN + interp_y * TILE_SIZE + TILE_SIZE // 2)
        return px, py

    def _load_pacman_assets(self) -> None:
        """Load and scale directional and death sprites for Pac-Man."""
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
        """Load and scale ghost sprites for all directions and states."""
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
        """Advance animation frame counters based on delta-time."""
        """Advance animation counters."""
        self.anim_timer += dt
        if self.anim_timer >= 0.12:
            self.anim_timer = 0.0
            self.move_frame = (self.move_frame + 1) % 4
            self.flash_frame = (self.flash_frame + 1) % 2

    def draw(self, state: GameStateDT, dt: float) -> None:
        """Render all active pellets, Pac-Man, and ghost entities."""
        """Render pellets, Pac-Man, and ghosts
        at the dynamic maze screen offsets."""
        if not self.engine.level_cleared:
            self.update_animations(dt)
        self._draw_pacgums(state)
        self._draw_ghosts(state.ghosts, dt)
        self._draw_pacman(state.pacman, dt)

    def _draw_pacgums(self, state: GameStateDT) -> None:
        """Draw collectible standard pellets and energized super-pacgums."""
        pellet_color = (255, 184, 151)
        for pellet in state.pacgums:
            center = self.grid_to_pixel(pellet)
            if pellet.is_super:
                radius = 8 if (self.move_frame % 2 == 0) else 6
                pygame.draw.circle(self.screen, pellet_color, center, radius)
            else:
                pygame.draw.circle(self.screen, pellet_color, center, 3)

    def _draw_pacman(self, pac: SpriteDT, dt: float) -> None:
        """Draw animated Pac-Man sprite at its interpolated pixel position."""
        # Smoothly glide Pac-Man across 0.2s
        center = self._get_interpolated_pixel(
            "pacman", pac.grid_x, pac.grid_y, dt, duration=0.2)

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

    def _draw_ghosts(self, ghosts: list[SpriteDT], dt: float) -> None:
        """Draw animated ghosts and floating eyes at interpolated
        coordinates."""
        if self.engine.gamestate.pacman.state == "ALIVE":
            for ghost in ghosts:
                center = self._get_interpolated_pixel(
                    ghost.id, ghost.grid_x, ghost.grid_y, dt, duration=0.25)
                dir_key = ghost.direction.value.lower()
                state_str = (
                    ghost.state.value
                    if hasattr(ghost.state, "value") else str(ghost.state)
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
