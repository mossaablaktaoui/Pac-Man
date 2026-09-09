from typing import Tuple, Iterator

from mazegenerator import MazeGenerator


class MazeAdapter:
    def __init__(self, size: Tuple[int, int], seed: int):
        self.mazegenerator = MazeGenerator(size, seed)
        self.mazegenerator.generate()
        self.maze = self.mazegenerator.maze

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
                yield (col_idx, row_idx, cell_value)
