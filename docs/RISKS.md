# 42 Pac-Man: Risk Management Matrix

This document tracks identified architectural, algorithmic, and operational risks, assessing their potential impact and establishing verified mitigation strategies.

---

## Risk Assessment Matrix

| Risk                              | Simple Fix                                 | Status  |
| --------------------------------- | ------------------------------------------ | ------- |
| Game logic depends on Pygame      | Separated game logic from graphics         | ✅ Fixed |
| Many screens read events          | One main event loop handles events         | ✅ Fixed |
| Bad highscore file can crash game | Validate the file before using it          | ✅ Fixed |
| Bad CLI input can show traceback  | Catch errors and show a simple message     | ✅ Fixed |
| Game can lag                      | Cache the maze and limit ghost pathfinding | ✅ Fixed |
| Type checking can fail            | Added type hints and checked with `mypy`   | ✅ Fixed |
| Ghosts make the game too hard                 | Give each ghost different movement logic                       | ✅ Fixed        |
| Cheats disappear after changing level         | Keep active cheats between levels                              | ✅ Fixed        |
| Level changes happen too suddenly             | Freeze the game for 1 second before next level                 | ✅ Fixed        |
| Maze package may have a different API         | Keep all package-specific code inside `MazeAdapter`            | ✅ Mitigated    |
