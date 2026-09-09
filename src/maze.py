from typing import Tuple, Iterator, List
from mazegenerator import MazeGenerator


class MazeAdapter:
    SIZE = (20, 20)

    def __init__(self, seed: int):
        self.mazegenerator = MazeGenerator(size=SIZE, seed=seed)
        self.mazegenerator.generate()
        self.maze = self.mazegenerator.maze
        self.width = self.mazegenerator.width
        self.height = self.mazegenerator.height

    def get_cells(self) -> Iterator[tuple[int, int, int]]:
        """Yield coordinates and values for each cell in the maze.

        Yields:
            tuple[int, int, int]: (col, row, cell_value)
                - col: X coordinate (horizontal).
                - row: Y coordinate (vertical).
                - cell_value: The 4-bit integer wall mask.
        """
        for row_idx, row in enumerate(self.maze):
            for col_idx, cell_value in enumerate(row):
                yield (row_idx, col_idx, cell_value)

    def can_move(self, x: int, y: int, direction: str) -> bool:
        cell_value = self.maze[x][y]

        bin_str = f"{cell_value:04b}"

        if direction == "UP":
            return bin_str[0] == "1"
        elif direction == "RIGHT":
            return bin_str[1] == "1"
        elif direction == "LEFT":
            return bin_str[2] == "1"
        elif direction == "DOWN":
            return bin_str[3] == "1"
        
        return False
        
    def is_inside(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def get_neighbors(self, x: int, y: int) -> List[Tuple[int, int]]:
        neighbors: List[Tuple[int, int]] = []
        
        if self.can_move(x, y, "UP") and self.is_inside(x, y - 1):
            neighbors.append((x, y - 1))
        if self.can_move(x, y, "RIGHT") and self.is_inside(x + 1, y):
            neighbors.append((x + 1, y))
        if self.can_move(x, y, "DOWN") and self.is_inside(x, y + 1):
            neighbors.append((x, y + 1))
        if self.can_move(x, y, "LEFT") and self.is_inside(x - 1, y):
            neighbors.append((x - 1, y))

        return neighbors
