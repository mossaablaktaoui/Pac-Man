from src.core.maze_adapter import MazeAdapter
from src.core.entities import GameStateDT, SpriteDT, Direction, GhostState
from collections import deque


class GhostManager:
    def __init__(self, maze: MazeAdapter) -> None:
        self.maze = maze
        self.move_timer = 0.0
        self.edible_timer = 0.0

    def update(self, gamestate: GameStateDT, dt: float) -> None:
        """Update ghost movement."""
        # count the time for the edible state.
        if self.edible_timer > 0:
            self.edible_timer -= dt

            if self.edible_timer <= 0:
                for ghost in gamestate.ghosts:
                    if ghost.state != GhostState.EATEN:
                        ghost.state = GhostState.NORMAL

        # to control the moving so not a step every frame.
        self.move_timer += dt
        if self.move_timer < 0.3:
            return

        self.move_timer = 0.0

        # move all ghosts when a step comes.
        for ghost in gamestate.ghosts:
            self._move_ghost(ghost, gamestate)

            # check if a ghost was eaten and it go back to spawn position
            if ghost.state == GhostState.EATEN:
                if ((ghost.grid_x, ghost.grid_y) ==
                        self._get_spawn_position(ghost)):
                    ghost.state = GhostState.NORMAL
        return

    def _get_spawn_position(self, ghost: SpriteDT) -> tuple[int, int]:
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
        if ghost.state == GhostState.EATEN:
            target = self._get_spawn_position(ghost)
        elif ghost.state == GhostState.EDIBLE:
            target = self._get_flee_target(ghost, gamestate)
        else:
            pacman = gamestate.pacman
            target = (pacman.grid_x, pacman.grid_y)

        next_cell = self._bfs_next_step(
            (ghost.grid_x, ghost.grid_y),
            target)

        if next_cell is None:
            return

        for other in gamestate.ghosts:
            if other is ghost:
                continue

            if (other.grid_x, other.grid_y) == next_cell:
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
        self.edible_timer = 8.0

        for ghost in gamestate.ghosts:
            if ghost.state != GhostState.EATEN:
                ghost.state = GhostState.EDIBLE

    def _bfs_next_step(self, start: tuple[int, int],
                       target: tuple[int, int]) -> tuple[int, int] | None:
        """Return the next cell toward the target using BFS."""
        queue = deque([start])
        visited = {start}
        parent: dict[tuple[int, int], tuple[int, int]] = {}

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

    def reset(self, maze: MazeAdapter) -> None:
        self.maze = maze
        self.move_timer = 0.0
        self.edible_timer = 0.0

    def _get_flee_target(self, ghost: SpriteDT,
                         gamestate: GameStateDT,) -> tuple[int, int]:
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
