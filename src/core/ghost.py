"""Ghost artificial intelligence manager and pathfinding state machine."""

from src.core.maze_adapter import MazeAdapter
from src.core.entities import GameStateDT, SpriteDT, Direction, GhostState
from collections import deque
import random
from typing import Tuple, Dict


class GhostManager:
    """Coordinates ghost AI behaviors, BFS pathfinding, and timers."""

    def __init__(self, maze: MazeAdapter) -> None:
        """Initialize ghost movement timers and maze reference."""
        self.maze = maze
        self.move_timer = 0.0
        self.edible_move_timer = 0.0
        self.edible_timer = 0.0
        self.eaten_timers = {
            "blinky": 0.0,
            "pinky": 0.0,
            "inky": 0.0,
            "clyde": 0.0,
        }

    def update(self, gamestate: GameStateDT, dt: float) -> None:
        """Update ghost timers, edible status, and execute movement steps."""
        # count the time for the edible state.
        if self.edible_timer > 0:
            self.edible_timer -= dt

            if self.edible_timer <= 3:
                for ghost in gamestate.ghosts:
                    if (ghost.state != GhostState.EATEN 
                            and ghost.state != GhostState.NORMAL):

                        ghost.state = GhostState.FLASHING
            if self.edible_timer <= 0:
                for ghost in gamestate.ghosts:
                    if ghost.state != GhostState.EATEN:
                        ghost.state = GhostState.NORMAL

        for ghost in gamestate.ghosts:
            # check if a ghost was eaten and it go back to spawn position
            if ghost.state == GhostState.EATEN:
                self.eaten_timers[ghost.id] -= dt

                if self.eaten_timers[ghost.id] <= 0.0:
                    self.eaten_timers[ghost.id] = 0.0

                    if (
                        ghost.grid_x,
                        ghost.grid_y,
                    ) == self._get_spawn_position(ghost):
                        ghost.state = GhostState.NORMAL

        # to control the moving so not a step every frame.
        # Normal ghosts move faster.
        self.move_timer += dt
        self.edible_move_timer += dt

        if self.move_timer >= 0.4:
            for ghost in gamestate.ghosts:
                if ghost.state in (GhostState.NORMAL, GhostState.EATEN):
                    self._move_ghost(ghost, gamestate)

            self.move_timer = 0.0

        if self.edible_move_timer >= 0.7:
            for ghost in gamestate.ghosts:
                if ghost.state in (GhostState.EDIBLE, GhostState.FLASHING):
                    self._move_ghost(ghost, gamestate)

            self.edible_move_timer = 0.0

        return

    def _get_spawn_position(self, ghost: SpriteDT) -> Tuple[int, int]:
        """Return home spawn corner coordinates for a ghost."""
        width = self.maze.width
        height = self.maze.height

        if ghost.id == "blinky":
            return 0, 0
        elif ghost.id == "pinky":
            return width - 1, 0
        elif ghost.id == "inky":
            return 0, height - 1
        elif ghost.id == "clyde":
            return width - 1, height - 1

        return ghost.grid_x, ghost.grid_y

    def _move_ghost(self, ghost: SpriteDT,
                    gamestate: GameStateDT) -> None:
        """Advance ghost position based on AI profile and current state."""

        start = (ghost.grid_x, ghost.grid_y)

        if ghost.state == GhostState.EATEN:
            target = self._get_spawn_position(ghost)
            next_cell = self._bfs_next_step(start, target)

        elif ghost.state in (GhostState.EDIBLE, GhostState.FLASHING):
            target = self._get_flee_target(ghost, gamestate)
            next_cell = self._bfs_next_step(start, target)

        else:
            pacman = gamestate.pacman

            if ghost.id == "blinky":
                target = (pacman.grid_x, pacman.grid_y)
                next_cell = self._bfs_next_step(start, target)

            elif ghost.id == "pinky":
                next_cell = self._random_next_step(ghost)

            elif ghost.id == "inky":
                next_cell = self._get_predicted_cell(gamestate, start)

            else:  # "clyde"
                algorithms = ["bfs", "random", "prediction"]

                algorithm = random.choice(algorithms)
                if algorithm == "bfs":
                    target = (pacman.grid_x, pacman.grid_y)
                    next_cell = self._bfs_next_step(start, target)
                elif algorithm == "random":
                    next_cell = self._random_next_step(ghost)
                elif algorithm == "prediction":
                    next_cell = self._get_predicted_cell(gamestate, start)

        if next_cell is None:
            return

        next_x, next_y = next_cell

        if next_x > ghost.grid_x:
            ghost.direction = Direction.RIGHT
        elif next_x < ghost.grid_x:
            ghost.direction = Direction.LEFT
        elif next_y > ghost.grid_y:
            ghost.direction = Direction.DOWN
        elif next_y < ghost.grid_y:
            ghost.direction = Direction.UP

        ghost.grid_x = next_x
        ghost.grid_y = next_y

    def _get_valid_directions(self, ghost: SpriteDT) -> list[Direction]:
        """Return directions the ghost can move from its current cell."""
        valid_directions = []

        for direction in Direction:
            if self.maze.can_move(
                ghost.grid_x,
                ghost.grid_y,
                direction,
            ):
                valid_directions.append(direction)

        return valid_directions

    def make_edible(self, gamestate: GameStateDT) -> None:
        """Transition all active ghosts into edible frightened state."""
        self.edible_timer = 8.0

        for ghost in gamestate.ghosts:
            if ghost.state != GhostState.EATEN:
                ghost.state = GhostState.EDIBLE

    def _bfs_next_step(self, start: Tuple[int, int],
                       target: Tuple[int, int]) -> Tuple[int, int] | None:
        """Return the next cell toward the target using BFS."""
        queue = deque([start])
        visited = {start}
        parent: Dict[Tuple[int, int], Tuple[int, int]] = {}

        while queue:
            current = queue.popleft()

            if current == target:
                break

            x, y = current

            for neighbor in self.maze.get_neighbors(x, y):
                if neighbor in visited:
                    continue

                visited.add(neighbor)
                parent[neighbor] = current
                queue.append(neighbor)

        if target not in visited:
            return None

        current = target

        while parent.get(current) != start:
            if current not in parent:
                return None

            current = parent[current]

        return current

    def _random_next_step(self, ghost: SpriteDT) -> Tuple[int, int] | None:
        """Move forward, choose randomly when blocked."""
        x = ghost.grid_x
        y = ghost.grid_y

        if self.maze.can_move(x, y, ghost.direction):
            if ghost.direction == Direction.UP:
                return x, y - 1
            if ghost.direction == Direction.DOWN:
                return x, y + 1
            if ghost.direction == Direction.LEFT:
                return x - 1, y
            if ghost.direction == Direction.RIGHT:
                return x + 1, y

        neighbors = self.maze.get_neighbors(x, y)

        if not neighbors:
            return None

        return random.choice(neighbors)

    def _get_predicted_cell(self, gamestate: GameStateDT,
                            start: Tuple[int, int]) -> Tuple[int, int] | None:
        """Return a cell up to 5 steps ahead of Pac-Man."""
        pacman = gamestate.pacman

        x = pacman.grid_x
        y = pacman.grid_y

        for _ in range(5):
            if not self.maze.can_move(x, y, pacman.direction):
                break

            if pacman.direction == Direction.UP:
                y -= 1
            elif pacman.direction == Direction.DOWN:
                y += 1
            elif pacman.direction == Direction.LEFT:
                x -= 1
            elif pacman.direction == Direction.RIGHT:
                x += 1

        target = x, y
        next_cell = self._bfs_next_step(start, target)
        return next_cell

    def reset(self, maze: MazeAdapter) -> None:
        """Reset ghost timers and maze reference for a new level."""
        self.maze = maze
        self.move_timer = 0.0
        self.edible_timer = 0.0
        self.edible_move_timer = 0.0
        for ghost_id in self.eaten_timers:
            self.eaten_timers[ghost_id] = 0.0

    def _get_flee_target(self, ghost: SpriteDT,
                         gamestate: GameStateDT,) -> Tuple[int, int]:
        """Return target cell maximizing Manhattan distance to Pac-Man."""
        pacman = gamestate.pacman

        best_cell = (ghost.grid_x, ghost.grid_y)
        best_distance = -1

        for y in range(self.maze.height):
            for x in range(self.maze.width):
                if not self.maze.is_walkable(x, y):
                    continue

                distance = (
                    abs(x - pacman.grid_x)
                    + abs(y - pacman.grid_y)
                )

                if distance > best_distance:
                    best_distance = distance
                    best_cell = (x, y)

        return best_cell
