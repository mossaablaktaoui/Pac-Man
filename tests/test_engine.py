"""Unit tests for core game engine loop, collisions, and state rules."""

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from src.core.cheats import CheatCode
from src.core.engine import GameEngine
from src.core.entities import Direction, GhostState, PacgumDT


class TestEngine(unittest.TestCase):
    """Test cases verifying GameEngine simulation and game rules."""

    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.config_path = Path(self.temp_dir.name) / "engine_config.json"
        self.scores_path = Path(self.temp_dir.name) / "engine_scores.json"

        config_data = {
            "highscore_filename": str(self.scores_path),
            "lives": 3,
            "pacgum": 10,
            "points_per_pacgum": 100,
            "points_per_super_pacgum": 300,
            "points_per_ghost": 200,
            "seed": 42,
            "level_max_time": 60,
        }
        with open(self.config_path, "w") as f:
            json.dump(config_data, f)

        with patch.object(sys, "argv", ["pac-man.py", str(self.config_path)]):
            self.engine = GameEngine()

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_initial_engine_state(self) -> None:
        state = self.engine.get_state()
        self.assertEqual(state.level, 1)
        self.assertEqual(state.score, 0)
        self.assertEqual(state.lives, 3)
        self.assertEqual(state.time_remaining, 60.0)
        self.assertFalse(state.is_paused)
        self.assertFalse(state.is_game_over)
        self.assertFalse(state.is_victory)

        self.assertEqual(state.pacman.grid_x, state.grid_width // 2)
        self.assertEqual(state.pacman.grid_y, state.grid_height // 2)

        ghost_ids = [g.id for g in state.ghosts]
        self.assertEqual(set(ghost_ids), {"blinky", "pinky", "inky", "clyde"})

        self.assertEqual(len(state.pacgums), 10)
        super_count = sum(1 for p in state.pacgums if p.is_super)
        self.assertEqual(super_count, 4)

    def test_toggle_pause(self) -> None:
        self.assertFalse(self.engine.gamestate.is_paused)
        new_status = self.engine.toggle_pause()
        self.assertTrue(new_status)
        self.assertTrue(self.engine.gamestate.is_paused)
        new_status = self.engine.toggle_pause()
        self.assertFalse(new_status)
        self.assertFalse(self.engine.gamestate.is_paused)

    def test_set_player_direction(self) -> None:
        self.engine.set_player_direction(Direction.UP)
        self.assertEqual(self.engine.next_direction, Direction.UP)

    def test_cheats_activation(self) -> None:
        self.assertFalse(self.engine.cheats.is_active(CheatCode.SPEED))
        self.engine.toggle_cheat(CheatCode.SPEED)
        self.assertTrue(self.engine.cheats.is_active(CheatCode.SPEED))

        self.assertFalse(
            self.engine.cheats.is_active(CheatCode.UNLIMITED_LIFE)
        )
        self.engine.toggle_cheat(CheatCode.UNLIMITED_LIFE)
        self.assertTrue(
            self.engine.cheats.is_active(CheatCode.UNLIMITED_LIFE)
        )

        current_lvl = self.engine.gamestate.level
        self.engine.toggle_cheat(CheatCode.SKIP_LEVEL)
        self.assertEqual(self.engine.gamestate.level, current_lvl + 1)

    def test_pacgum_collection_regular(self) -> None:
        pacman = self.engine.gamestate.pacman
        self.engine.gamestate.pacgums = [
            PacgumDT(pacman.grid_x, pacman.grid_y, is_super=False)
        ]

        self.engine._collect_pacgum()
        self.assertEqual(self.engine.gamestate.score, 100)
        self.assertEqual(len(self.engine.gamestate.pacgums), 0)
        self.assertTrue(self.engine.gamestate.is_level_cleared)

    def test_pacgum_collection_super(self) -> None:
        pacman = self.engine.gamestate.pacman
        self.engine.gamestate.pacgums = [
            PacgumDT(pacman.grid_x, pacman.grid_y, is_super=True)
        ]

        self.engine._collect_pacgum()
        self.assertEqual(self.engine.gamestate.score, 300)
        for ghost in self.engine.gamestate.ghosts:
            self.assertEqual(ghost.state, GhostState.EDIBLE)

    def test_ghost_collision_normal_damages_pacman(self) -> None:
        pacman = self.engine.gamestate.pacman
        ghost = self.engine.gamestate.ghosts[0]
        ghost.state = GhostState.NORMAL
        ghost.grid_x = pacman.grid_x
        ghost.grid_y = pacman.grid_y

        self.assertEqual(self.engine.gamestate.lives, 3)
        self.engine._check_ghost_collision()
        self.assertEqual(self.engine.gamestate.lives, 2)
        self.assertEqual(self.engine.gamestate.pacman.state, "DEAD")

    def test_ghost_collision_god_mode_cheat(self) -> None:
        self.engine.cheats.toggle(CheatCode.UNLIMITED_LIFE)
        pacman = self.engine.gamestate.pacman
        ghost = self.engine.gamestate.ghosts[0]
        ghost.state = GhostState.NORMAL
        ghost.grid_x = pacman.grid_x
        ghost.grid_y = pacman.grid_y

        self.assertEqual(self.engine.gamestate.lives, 3)
        self.engine._check_ghost_collision()
        self.assertEqual(self.engine.gamestate.lives, 3)
        self.assertEqual(self.engine.gamestate.pacman.state, "ALIVE")

    def test_ghost_collision_edible_devours_ghost(self) -> None:
        pacman = self.engine.gamestate.pacman
        ghost = self.engine.gamestate.ghosts[0]
        ghost.state = GhostState.EDIBLE
        ghost.grid_x = pacman.grid_x
        ghost.grid_y = pacman.grid_y

        initial_score = self.engine.gamestate.score
        self.engine._check_ghost_collision()
        self.assertEqual(
            self.engine.gamestate.score, initial_score + 200
        )
        self.assertEqual(ghost.state, GhostState.EATEN)

    def test_ghost_collision_flashing_devours_ghost(self) -> None:
        pacman = self.engine.gamestate.pacman
        ghost = self.engine.gamestate.ghosts[0]
        ghost.state = GhostState.FLASHING
        ghost.grid_x = pacman.grid_x
        ghost.grid_y = pacman.grid_y

        initial_score = self.engine.gamestate.score
        self.engine._check_ghost_collision()
        self.assertEqual(
            self.engine.gamestate.score, initial_score + 200
        )
        self.assertEqual(ghost.state, GhostState.EATEN)

    def test_timer_countdown_triggers_game_over(self) -> None:
        self.engine.gamestate.time_remaining = 0.5
        self.engine.update(dt=1.0)
        self.assertEqual(self.engine.gamestate.time_remaining, 0.0)
        self.assertTrue(self.engine.gamestate.is_game_over)

    def test_pacman_movement_open_corridor(self) -> None:
        pacman = self.engine.gamestate.pacman
        self.engine.maze.maze[pacman.grid_y][pacman.grid_x] = 0
        self.engine.next_direction = Direction.RIGHT
        initial_x = pacman.grid_x

        self.engine._move_pacman()
        self.assertEqual(pacman.grid_x, initial_x + 1)
        self.assertEqual(pacman.direction, Direction.RIGHT)

    def test_pacman_movement_blocked_by_wall(self) -> None:
        pacman = self.engine.gamestate.pacman
        self.engine.maze.maze[pacman.grid_y][pacman.grid_x] = 2
        pacman.direction = Direction.RIGHT
        self.engine.next_direction = Direction.RIGHT
        initial_x = pacman.grid_x

        self.engine._move_pacman()
        self.assertEqual(pacman.grid_x, initial_x)

    def test_victory_after_10_levels(self) -> None:
        self.engine.gamestate.level = 10
        self.engine.start_next_level()
        self.assertTrue(self.engine.gamestate.is_victory)
        self.assertFalse(self.engine.gamestate.is_level_cleared)


if __name__ == "__main__":
    unittest.main()
