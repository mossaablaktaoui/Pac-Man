import pygame

from src.maze import MazeAdapter

TILE_SIZE = 40
MAZE_SIZE = 20
MARGIN = 7


class MazeRenderer:
    def __init__(self):
        self.maze = MazeAdapter(45)
        maze_width = int((MAZE_SIZE * TILE_SIZE) + (MARGIN * 2))
        maze_height = int((MAZE_SIZE * TILE_SIZE) + (MARGIN * 2))
        self._maze_surface = pygame.Surface(
            (maze_width, maze_height), pygame.SRCALPHA)
        self._maze_surface.fill((20, 40, 180, 80))
        self._prepare_maze_surface()

    def grid_to_pixel(self, col: int, row: int) -> tuple[int, int]:
        """Convert maze grid (col, row) to center pixel coordinates."""
        px = MARGIN + col * TILE_SIZE + TILE_SIZE // 2
        py = MARGIN + row * TILE_SIZE + TILE_SIZE // 2
        return px, py

    def _draw_cell(
        self,
        cell_value: int,
        px: int,
        py: int,
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
        surface = self._maze_surface
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

    def _prepare_maze_surface(self):
        for col, row, val in self.maze.get_cells():
            px = col * TILE_SIZE + MARGIN
            py = row * TILE_SIZE + MARGIN
            self._draw_cell(val, px, py, TILE_SIZE)
