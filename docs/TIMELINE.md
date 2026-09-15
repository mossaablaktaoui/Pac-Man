# 42 Pac-Man: Project Timeline & Roadmap

The actual 8-day development timeline executed collaboratively by **Abdelfatah Laktaoui (`alaktaou`)** and **Mossaab Laktaoui (`mlaktaou`)**.

---

## Gantt / Real Schedule Overview

```
Day:       1       2       3       4       5       6       7       8 (Today)
         ┌───────┬───────┬───────┬───────┬───────┬───────┬───────┬───────┐
M1       ████████                                                        │ M1: Env & Foundation (Day 1)
M2       ████████████████                                                │ M2: Maze Logic & Adapter (Days 1–2)
M3 & M4                  ████████████████                                │ M3/M4: Movement, Ghost AI & Cheats (Days 3–4)
M5       ████████████████████████████████████████████████████████████████│ M5: UI Screens & Highscores (Iterative Days 1–8)
Integr.                                  ████████                        │ Back-end & Front-end Integration (Day 5)
Bugfix                                           ████████████████        │ Logic Bugfixes & Missing Rules (Days 6–7)
Polish                                                           ████████│ Final Logic Fixes & Tests (Day 8 - Today)
Linting  ════════════════════════════════════════════════════════════════│ Continuous Linting (Every commit)
         └───────┴───────┴───────┴───────┴───────┴───────┴───────┴───────┘
```

---

## Detailed Chronological Log

### Day 1: Milestone 1 & Early UI Scaffolding

- **Milestone 1 Completed in 1 Day**:
  - `pac-man.py` CLI parser accepting single JSON config argument with graceful exception handling.
  - Custom `Config` class supporting `#` comment stripping, default clamping, and automatic config creation on missing files.
  - Initial 1920x1080 windowed Pygame display setup with centralized clock and event loop.
- **Milestone 5 (UI Screens) Kickoff**:
  - Started foundational screen routing and menu scaffolding on Day 1, laying the groundwork for iterative daily UI enhancements.

### Days 1–2: Milestone 2 — Maze Logic & Wall Rendering

- **Integration of A-Maze-ing Wheel**:
  - Installed and wrapped `mazegenerator` wheel using `MazeAdapter`.
  - Inverted and decoded 4-bit wall bitmasks (`1=N, 2=E, 4=S, 8=W, 15=solid`).
  - Implemented cached dual-tone maze surface renderer (`MazeRenderer`) for 60 FPS wall blitting.
  - Established open corridor graph traversal (`get_neighbors`, `can_move`).

### Days 3–4: Milestones 3 & 4 — Core Movement, Ghost AI & Developer Cheats

- **Milestone 3 (Entities & Movement)**:
  - Discrete grid coordinate tracking for Pac-Man with input queuing (`next_direction`).
  - Pellet and super-pacgum placement and collection logic.
  - Directional animated sprites and sub-tile linear motion interpolation (`_get_interpolated_pixel`).
- **Milestone 4 (Ghost AI & State Machine)**:
  - Implementation of Breadth-First Search (BFS) corridor navigation solver.
  - 4 specialized ghost AI personalities:
    - **Blinky**: Direct BFS hunter targeting Pac-Man's exact cell.
    - **Pinky & Clyde**: Corridor wandering with random turns at junctions.
    - **Inky**: 20-tile lookahead trajectory projection with BFS interception.
  - Super-pacgum consumption triggering Edible / Frightened state (Manhattan distance evasion) for 8.0s.
  - Eaten eyes returning to corner base spawns via BFS before reforming.
- **Developer Cheat Suite**:
  - Implemented real-time cheat toggles (`K` Skip Level, `L` Speed Boost, `H` Unlimited lives / God Mode, `J` Freeze Ghosts).
- **Ongoing UI Iterations (Milestone 5)**:
  - Added HUD boards for score, lives, timer, and active cheat badges.

### Day 5: Front-End & Back-End Integration

- **Bridging the Decoupled Architecture**:
  - Connected the pure Python logic core (`src/core/`) to the Pygame presentation layer (`src/views/`) via immutable Data Transfer Objects (`GameStateDT`).
  - Synchronized screen transitions: `MainMenu` ➔ `InGame` ➔ `Pause` ➔ `GameOver` / `Victory` ➔ `SaveScore` ➔ `Highscores`.
  - Integrated frosted glass real-time box-blur background snapshot for modals.

### Days 6–7: Logic Bug Squashing & Edge Cases

- **Confronting Real Gameplay & Edge-Case Bugs**:
  - **Ghost Spacing / Stacking Fix**: Enforced collision check so active non-eaten ghosts cannot occupy the same cell, while allowing dead/eaten eyes to pass through each other freely (`commit 5024d09`, `d16f1be`).
  - **Pac-Man Death Timer**: Added 1.3s death delay timer (`dead_timer`) to allow the death animation to play before resetting entity positions (`commit 33caf13`).
  - **Maze Re-rendering on Level Advance**: Fixed level transition logic so fresh procedural mazes are correctly re-rendered upon clearing pacgums (`commit 7f094d1`).
  - **Smooth Movement & Ready Intermission Screen**: Tuned sub-tile interpolation and added a 4-second "Level X / Ready!" banner countdown (`commit 3694c06`).
  - **Highscore Board & Name Input**: Built the 10-character alphanumeric name-saving input dialog and leaderboard display with score preservation (`commit 88f8b07`, `aca89ed`, `288185c`).

### Day 8 (Today): Final Logic Refinements, Test Suite & Documentation

- **Current Status**:
  - Fine-tuning remaining subtle logic edge cases in entity behaviors.
  - Comprehensive automated unit test suite in `tests/` (39 passing unit tests covering config, highscores, maze adapter, and engine rules).
  - Project documentation finalized (`docs/` and `README.md`).
  - Verification with `make test` and `make lint`.

---

## Quality Control: Continuous Linting Strategy

Unlike traditional workflows where code formatting is delayed until the end:

- **Continuous Linting**: Both developers ran `flake8` and `mypy` continuously during daily coding sessions and before feature merges (`commit 4e7eb8b`, `ccd05f2`).
- **Clean Type Annotations**: Maintained clean PEP 484 type hints across all source and test modules throughout development.
