from typing import Tuple, List
from mazegenerator import MazeGenerator
from src.core.entities import Direction
import random


class MazeAdapter:
    SIZE = (15, 15)

    def __init__(self, seed: int):
        self.mazegenerator = MazeGenerator(size=self.SIZE, seed=seed)
        self.maze = self.mazegenerator.maze
        self.width = self.SIZE[0]
        self.height = self.SIZE[1]
        self.seed = seed

    def can_move(self, x: int, y: int, direction: Direction) -> bool:
        cell_value = self.maze[y][x]

        bin_str = f"{cell_value:04b}"

        if direction == Direction.UP:
            return bin_str[3] == "0"
        elif direction == Direction.RIGHT:
            return bin_str[2] == "0"
        elif direction == Direction.DOWN:
            return bin_str[1] == "0"
        elif direction == Direction.LEFT:
            return bin_str[0] == "0"

        return False

    def is_inside(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def get_neighbors(self, x: int, y: int) -> List[Tuple[int, int]]:
        neighbors: List[Tuple[int, int]] = []

        if self.can_move(x, y, Direction.UP) and self.is_inside(x, y - 1):
            neighbors.append((x, y - 1))
        if self.can_move(x, y, Direction.RIGHT) and self.is_inside(x + 1, y):
            neighbors.append((x + 1, y))
        if self.can_move(x, y, Direction.DOWN) and self.is_inside(x, y + 1):
            neighbors.append((x, y + 1))
        if self.can_move(x, y, Direction.LEFT) and self.is_inside(x - 1, y):
            neighbors.append((x - 1, y))

        return neighbors

    def is_walkable(self, x: int, y: int) -> bool:
        return self.maze[y][x] != 15

    def create_random_maze(self) -> None:
        random_seed = random.randint(1, 100)
        self.mazegenerator = MazeGenerator(size=self.SIZE, seed=random_seed)
        self.maze = self.mazegenerator.maze

    def reset(self):
        self.mazegenerator = MazeGenerator(size=self.SIZE, seed=self.seed)
        self.maze = self.mazegenerator.maze

    def get_random_cell(self) -> tuple[int, int]:
        while True:
            x = random.randrange(self.width)
            y = random.randrange(self.height)

            if self.is_walkable(x, y):
                return x, y
