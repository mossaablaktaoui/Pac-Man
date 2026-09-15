# 42 Pac-Man: Kanban Board

This document tracks task progression, work-in-progress (WIP) allocations, and sprint milestones across the development cycle.

---

## Board Overview

| Backlog                          | To Do                         | In Progress                                 | In Review / Verification          | Done                              |
| :------------------------------- | :---------------------------- | :------------------------------------------ | :-------------------------------- | :-------------------------------- |
| • Online multiplayer sync        | • Sound effect variations     | • Standalone AppImage build                 | • Strict lint & mypy validation   | • Decoupled Engine Architecture   |
| • Custom maze theme skins        | • Joystick controller mapping | • Performance profiling on low-end hardware | • Defense rehearsal & recode prep | • A-Maze-ing Wheel Integration    |
| • Dynamic ghost difficulty curve | • Achievement trophy system   |                                             |                                   | • 4 Ghost AI Personalities (BFS)  |
|                                  |                               |                                             |                                   | • 60 FPS Sub-Tile Interpolation   |
|                                  |                               |                                             |                                   | • In-game HUD & Dashboard         |
|                                  |                               |                                             |                                   | • Screen State Flow (Menu to Win) |
|                                  |                               |                                             |                                   | • Developer Cheat Suite           |
|                                  |                               |                                             |                                   | • JSON Highscore Persistence      |
|                                  |                               |                                             |                                   | • Configuration Parser with '#'   |

---

## Detailed Task Breakdown by Phase

### Phase 1: Environment & Decoupled Foundation

- [x] **Task 1.1 (mlaktaou)**: Configuration parser with `#` comment stripping and default clamping.
- [x] **Task 1.2 (alaktaou)**: Centralized 1920x1080 windowed display with single event loop.
- [x] **Task 1.3 (mlaktaou)**: CLI entry point argument parsing and traceback-free error catching.
- [x] **Task 1.4 (Both)**: Repository cleanup, deleting obsolete assets and temporary files.
- **Milestone 1**: Clean CLI boot without crash; windowed display ready.

### Phase 2: Maze Logic & Wall Rendering

- [x] **Task 2.1 (mlaktaou)**: Integrate `mazegenerator` wheel and resolve 4-bit wall bitmask orientation.
- [x] **Task 2.2 (alaktaou)**: Implement cached dual-tone surface renderer with coordinate mapping.
- [x] **Task 2.3 (mlaktaou)**: Build corridor adjacency graph (`get_neighbors`, `can_move`).
- **Milestone 2**: Real maze from `A-Maze-ing` package renders accurately on screen with open corridors.

### Phase 3: Entities & Core Movement

- [x] **Task 3.1 (mlaktaou)**: Grid navigation, input buffering (`next_direction`), and pellet eating.
- [x] **Task 3.2 (alaktaou)**: Directional sprite animation and sub-tile linear motion interpolation.
- [x] **Task 3.3 (mlaktaou)**: Score updating, life deduction, and dead state timers.
- **Milestone 3**: Pac-Man moves smoothly through corridors and eats pellets with real-time score updates.

### Phase 4: Ghost AI & State Machine

- [x] **Task 4.1 (mlaktaou)**: Breadth-First Search (BFS) shortest-path navigation solver.
- [x] **Task 4.2 (mlaktaou)**: 4 distinct ghost personalities:
  - Blinky (Direct BFS Hunter)
  - Pinky & Clyde (Corridor exploration & junction choices)
  - Inky (20-tile lookahead projection & BFS interception)
- [x] **Task 4.3 (mlaktaou)**: Frightened / Edible state with maximum Manhattan distance fleeing.
- [x] **Task 4.4 (alaktaou)**: Ghost sprite states (Normal, Edible Blue, Flashing, Eaten Eyes).
- [x] **Task 4.5 (Both)**: Ghost touch collision matrix and eaten respawn timer.
- **Milestone 4**: Complete ghost chase dynamics with power pellet vulnerability and respawning eyes.

### Phase 5: Progression, UI Modals & Highscores

- [x] **Task 5.1 (mlaktaou)**: 10-level loop progression, level countdown timer, and reset logic.
- [x] **Task 5.2 (mlaktaou)**: HighscoreManager persistence (JSON storage, top 10 sorting, name sanitization).
- [x] **Task 5.3 (alaktaou)**: Screen flows (`MainMenu`, `InGame`, `Pause`, `GameOver`, `Victory`, `Highscores`, `Instructions`).
- [x] **Task 5.4 (alaktaou)**: Real-time box-blur background snapshot for modal overlays.
- [x] **Task 5.5 (alaktaou)**: 10-character alphanumeric name input dialog.
- **Milestone 5**: Complete end-to-end game loop from Main Menu to Victory/Defeat to Highscore registration.

### Phase 6: Cheats, Quality Gates & Packaging

- [x] **Task 6.1 (mlaktaou)**: Developer cheat suite (`SKIP_LEVEL`, `SPEED`, `UNLIMITED_LIFE`, `FREEZE_GHOSTS`).
- [x] **Task 6.2 (mlaktaou)**: Headless unit test suite in `tests/`.
- [x] **Task 6.3 (Both)**: Strict linting verification (`flake8`, `mypy --strict`).
- [x] **Task 6.4 (alaktaou)**: Complete 42-compliant `README.md` and documentation suite.
- **Milestone 6**: Standalone executable, passing lint/mypy, ready for 42 evaluation defense.
