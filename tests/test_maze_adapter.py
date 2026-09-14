"""Unit tests for A-Maze-ing maze adapter and wall bitmask decoding."""

import unittest
from src.core.entities import Direction
from src.core.maze_adapter import MazeAdapter


class TestMazeAdapter(unittest.TestCase):
    """Test cases verifying MazeAdapter grid queries and bitmasks."""

    def setUp(self) -> None:
        self.adapter = MazeAdapter(seed=42)

    def test_grid_dimensions(self) -> None:
        self.assertEqual(self.adapter.width, 15)
        self.assertEqual(self.adapter.height, 15)
        self.assertEqual(len(self.adapter.maze), 15)
        self.assertEqual(len(self.adapter.maze[0]), 15)

    def test_is_inside(self) -> None:
        self.assertTrue(self.adapter.is_inside(0, 0))
        self.assertTrue(self.adapter.is_inside(14, 14))
        self.assertTrue(self.adapter.is_inside(7, 7))

        self.assertFalse(self.adapter.is_inside(-1, 0))
        self.assertFalse(self.adapter.is_inside(0, -1))
        self.assertFalse(self.adapter.is_inside(15, 0))
        self.assertFalse(self.adapter.is_inside(0, 15))

    def test_is_walkable(self) -> None:
        # Mock a solid obstacle (15) and an open path (0)
        self.adapter.maze[0][0] = 15
        self.assertFalse(self.adapter.is_walkable(0, 0))

        self.adapter.maze[0][1] = 0
        self.assertTrue(self.adapter.is_walkable(1, 0))

    def test_can_move_bitmasks(self) -> None:
        # Cell bitmask encoding: 1=N, 2=E, 4=S, 8=W.
        # In can_move, direction is open if bin_str[bit] == '0'.

        # Value 0: All directions open
        self.adapter.maze[5][5] = 0
        self.assertTrue(self.adapter.can_move(5, 5, Direction.UP))
        self.assertTrue(self.adapter.can_move(5, 5, Direction.RIGHT))
        self.assertTrue(self.adapter.can_move(5, 5, Direction.DOWN))
        self.assertTrue(self.adapter.can_move(5, 5, Direction.LEFT))

        # Value 1 (bit 0): North wall
        self.adapter.maze[5][5] = 1
        self.assertFalse(self.adapter.can_move(5, 5, Direction.UP))
        self.assertTrue(self.adapter.can_move(5, 5, Direction.RIGHT))
        self.assertTrue(self.adapter.can_move(5, 5, Direction.DOWN))
        self.assertTrue(self.adapter.can_move(5, 5, Direction.LEFT))

        # Value 2 (bit 1): East wall
        self.adapter.maze[5][5] = 2
        self.assertTrue(self.adapter.can_move(5, 5, Direction.UP))
        self.assertFalse(self.adapter.can_move(5, 5, Direction.RIGHT))
        self.assertTrue(self.adapter.can_move(5, 5, Direction.DOWN))
        self.assertTrue(self.adapter.can_move(5, 5, Direction.LEFT))

        # Value 4 (bit 2): South wall
        self.adapter.maze[5][5] = 4
        self.assertTrue(self.adapter.can_move(5, 5, Direction.UP))
        self.assertTrue(self.adapter.can_move(5, 5, Direction.RIGHT))
        self.assertFalse(self.adapter.can_move(5, 5, Direction.DOWN))
        self.assertTrue(self.adapter.can_move(5, 5, Direction.LEFT))

        # Value 8 (bit 3): West wall
        self.adapter.maze[5][5] = 8
        self.assertTrue(self.adapter.can_move(5, 5, Direction.UP))
        self.assertTrue(self.adapter.can_move(5, 5, Direction.RIGHT))
        self.assertTrue(self.adapter.can_move(5, 5, Direction.DOWN))
        self.assertFalse(self.adapter.can_move(5, 5, Direction.LEFT))

    def test_get_neighbors(self) -> None:
        # Create an open cell in the middle
        self.adapter.maze[7][7] = 0
        neighbors = self.adapter.get_neighbors(7, 7)
        # Should include cardinal adjacent cells
        self.assertIn((7, 6), neighbors)
        self.assertIn((8, 7), neighbors)
        self.assertIn((7, 8), neighbors)
        self.assertIn((6, 7), neighbors)

    def test_get_random_cell(self) -> None:
        x, y = self.adapter.get_random_cell()
        self.assertTrue(self.adapter.is_inside(x, y))
        self.assertTrue(self.adapter.is_walkable(x, y))

    def test_reset_and_random_maze(self) -> None:
        initial_maze = [row[:] for row in self.adapter.maze]
        self.adapter.create_random_maze()
        # Reset restores original seed layout
        self.adapter.reset()
        self.assertEqual(self.adapter.maze, initial_maze)


if __name__ == "__main__":
    unittest.main()
