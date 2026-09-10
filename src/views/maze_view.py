import pygame

from src.core.engine import GameEngine

TILE_SIZE = 40
MARGIN = 7


class MazeRenderer:
    def __init__(self, engine: GameEngine):
        self.engine = engine
        self.grid = self.engine.get_wall_matrix()
        self.maze_size = (
            len(self.grid[0]) * TILE_SIZE + 2 * MARGIN,
            len(self.grid) * TILE_SIZE + 2 * MARGIN
            )

        self.maze_surface = pygame.Surface(self.maze_size, pygame.SRCALPHA)
        self._render_maze()

    def grid_to_pixel(self, col: int, row: int) -> tuple[int, int]:
        """Convert maze grid (col, row) to center pixel coordinates."""
        px = MARGIN + col * TILE_SIZE + TILE_SIZE // 2
        py = MARGIN + row * TILE_SIZE + TILE_SIZE // 2
        return px, py

    def _draw_cell(self,
                   cell_value: int,
                   px: int, py: int,
                   tile_size: int,
                   wall_color: tuple[int, int, int] = (20, 40, 180),
                   thickness: int = 5,
                   ) -> None:
        """Draw a single maze cell on the target surface based on its bitmask.

        Args:
            surface: The pygame Surface to draw onto.
            cell_value: 4-bit integer bitmask (1=N, 2=E, 4=S, 8=W, 15=solid).
            px: Top-left X coordinate in pixels.
            py: Top-left Y coordinate in pixels.
            tile_size: Width and height of the cell in pixels.
            wall_color: RGB tuple for the wall color.
            thickness: Line width in pixels.
        """
        surface = self.maze_surface
        # 15 represents a solid obstacle block (e.g., the center '42')
        if cell_value == 15:
            rect = pygame.Rect(px, py, tile_size, tile_size)
            pygame.draw.rect(surface, wall_color, rect)
            return

        # North (Top)
        if cell_value & 1:
            start = (px, py)
            end = (px + tile_size, py)
            pygame.draw.line(surface, wall_color, start, end, thickness)
            pygame.draw.line(surface, (130, 200, 255), start, end, 1)

        # East (Right)
        if cell_value & 2:
            start = (px + tile_size, py)
            end = (px + tile_size, py + tile_size)
            pygame.draw.line(surface, wall_color, start, end, thickness)
            pygame.draw.line(surface, (130, 200, 255), start, end, 2)

        # South (Bottom)
        if cell_value & 4:
            start = (px, py + tile_size)
            end = (px + tile_size, py + tile_size)
            pygame.draw.line(surface, wall_color, start, end, thickness)
            pygame.draw.line(surface, (130, 200, 255), start, end, 2)

        # West (Left)
        if cell_value & 8:
            start = (px, py)
            end = (px, py + tile_size)
            pygame.draw.line(surface, wall_color, start, end, thickness)
            pygame.draw.line(surface, (130, 200, 255), start, end, 2)

    def _render_maze(self) -> None:
        """Draw all walls onto the cached surface one time."""
        self.maze_surface.fill((20, 40, 180, 80))
        for row_idx, row in enumerate(self.grid):
            for col_idx, cell_value in enumerate(row):
                px = col_idx * TILE_SIZE + MARGIN
                py = row_idx * TILE_SIZE + MARGIN
                self._draw_cell(cell_value, px, py, TILE_SIZE)
        return self.maze_surface

    def draw(self) -> pygame.Surface:
        """Instantly return the pre-rendered surface
        (runs at 60 FPS without lag)."""
        return self.maze_surface
