# 42 Pac-Man: Team Organization & Work Breakdown

Comprehensive team charter, architectural division of responsibilities, contract-first specifications, and collaboration workflows for **Pac-Man: Ghosts! More ghosts!**.

---

## 1. Team Members & Roles

The project was engineered collaboratively by two developers adhering to an **Agile pair-programming framework** and strict domain separation:

| Developer | Handle | Primary Role | Domain Ownership |
| :--- | :--- | :--- | :--- |
| **Abdelfatah Laktaoui** | `alaktaou` | **Front-End & Presentation Lead** (Person A) | Pygame display window, 60 FPS clock, screen state machine, sprite animations, sub-tile interpolation, HUD rendering, modal blur shaders, and packaging. |
| **Mossaab Laktaoui** | `mlaktaou` | **Back-End & Core Logic Lead** (Person B) | Pure Python simulation engine, A-Maze-ing maze adapter, BFS ghost AI pathfinding, collision detection, config parser, highscores persistence, and automated unit tests. |

---

## 2. Architectural Boundaries & Code Ownership

To prevent merge conflicts and maintain clean separation of concerns, the codebase is partitioned into distinct functional boundaries:

```
                               42 PAC-MAN
                                   │
         ┌─────────────────────────┴─────────────────────────┐
         ▼                                                   ▼
FRONT-END / PRESENTATION (Person A)                BACK-END / CORE LOGIC (Person B)
    `src/views/` & `assets/`                             `src/core/` & `tests/`
─────────────────────────────────────             ─────────────────────────────────────
• `src/views/renderer.py`                         • `src/core/engine.py`
• `src/views/maze_view.py`                        • `src/core/maze_adapter.py`
• `src/views/sprite_view.py`                      • `src/core/ghost.py`
• `src/views/hud_view.py`                         • `src/core/config.py`
• `src/views/screens/*.py`                        • `src/core/highscores.py`
• `assets/images/`, `assets/fonts/`               • `src/core/cheats.py`
• CLI Entry: `pac-man.py`, `src/app.py`           • Automated Unit Tests: `tests/`
                                   ▲
                                   │ Shared Contract
                                   ▼
                   `src/core/entities.py` (DTO Boundary)
                   • GameStateDT, SpriteDT, PacgumDT
                   • Direction, GhostState, CheatCode
```

### Collaboration Protocol
1. **Contract-First Agreement**: The data contracts defined in `src/core/entities.py` cannot be modified unilaterally. Any schema change requires joint approval by both developers.
2. **Pure Logic Isolation**: `src/core/` and `tests/` must remain completely free of graphical dependencies (`pygame`), enabling headless automated testing without an active X11 display.
3. **One-Way Data Flow**: The presentation layer treats `GameStateDT` as immutable and read-only. All player inputs (movement, pause, cheats) are communicated to the engine via explicit command methods.

---

## 3. Parallel Work Breakdown (Phase-by-Phase)

| Phase | Person A (Front-End Presentation) | Person B (Back-End Core Logic) | Joint Verification Milestone |
| :--- | :--- | :--- | :--- |
| **Phase 1: Environment & Foundation** | • Refactor display into windowed 1920x1080 mode.<br>• Centralize event loop into a single `pygame.event.get()`.<br>• Remove legacy crosshairs and scrap files. | • Build `Config` parser with `#` comment stripping and default clamping.<br>• Implement `pac-man.py` CLI parser with traceback-free error handling. | **M1**: `python pac-man.py config.json` starts a clean window with settings from config without crashing. |
| **Phase 2: Maze Logic & Rendering** | • Implement `MazeRenderer` with coordinate conversion (`grid_to_pixel`).<br>• Create cached dual-tone surface renderer with glowing wall strokes. | • Integrate `mazegenerator` wheel in `MazeAdapter`.<br>• Decode 4-bit wall bitmasks (`1=N, 2=E, 4=S, 8=W, 15=solid`).<br>• Implement corridor graph traversal (`get_neighbors`, `can_move`). | **M2**: Real maze from `A-Maze-ing` package renders accurately on screen with open corridor loops. |
| **Phase 3: Movement & Physics** | • Build `SpriteView` for animated directional Pac-Man sprites.<br>• Implement 60 FPS sub-tile linear motion interpolation (`_get_interpolated_pixel`). | • Implement grid coordinate updates and input queue (`next_direction`).<br>• Implement pellet and super-pacgum collection and score accrual. | **M3**: Player controls Pac-Man through corridors, eating pellets with fluid motion and updating score in real time. |
| **Phase 4: Ghost AI & State Machine** | • Add sprite rendering for 4 ghost colors, frightened flashing state, and eaten eyes state.<br>• Integrate intermission ready countdown banners. | • Implement Breadth-First Search (BFS) corridor pathfinder.<br>• Build 4 ghost AI personalities (Blinky, Pinky, Inky, Clyde).<br>• Implement frightened evasion and respawn return logic. | **M4**: Playable game with intelligent ghost chase, power pellet vulnerability, and respawning eyes. |
| **Phase 5: Progression & UI Screens** | • Implement screen controllers: `MainMenu`, `Pause`, `GameOver`, `Victory`, `Highscores`, `Instructions`.<br>• Implement 10-character name-input text modal.<br>• Real-time box-blur background snapshot shader. | • Implement 10-level campaign loop, countdown timer, and reset logic.<br>• Build `HighscoreManager` JSON persistence with validation and top 10 sorting. | **M5**: Complete game loop from Main Menu -> 10 Levels -> Victory/Defeat -> Name Input -> Highscore save. |
| **Phase 6: Quality Gates & Polish** | • Polish UI layout, typography, and button hover states.<br>• Conduct manual acceptance matrix tests (TC-01 to TC-19).<br>• Verify packaging and defense readiness. | • Implement developer cheat suite (`K`, `L`, `H`, `J`).<br>• Build automated test suite in `tests/` (39 unit tests).<br>• Enforce strict static typing (`make lint-strict`). | **M6**: All tests pass in `0.02s`; strict linting and typing pass 100% green; defense-ready submission. |

---

## 4. Front-End ↔ Back-End Integration Contract

| Feature Area | Front-End (Person A) Needs | Back-End (Person B) Provides |
| :--- | :--- | :--- |
| **Configuration** | Validated parameters to initialize window, boards, and timers. | `Config.load()` returning sanitized parameters with reliable default fallbacks and comment stripping. |
| **Maze Generation** | 2D matrix of wall bitmasks to draw onto the cached surface. | `MazeAdapter.maze` (15x15 matrix) and `engine.get_wall_matrix()`. |
| **Movement** | Entity coordinates `(grid_x, grid_y)` and `direction` for sprite blitting. | Buffered direction changes, corridor wall collision verification, and pellet consumption. |
| **Ghost AI** | Entity states (`NORMAL`, `EDIBLE`, `EATEN`) and coordinates. | FSM state transitions, BFS shortest-path steps, and lookahead targeting. |
| **HUD & Timers** | Real-time score, remaining lives, level number, countdown time, and cheat flags. | Continuous `engine.update(dt)` countdown, level clearing detection, and `GameStateDT` snapshots. |
| **Highscores** | Top 10 leaderboard list and a method to persist player names. | `HighscoreManager.add_score(name, score)` with 10-char alphanumeric sanitization and JSON persistence. |
| **Developer Cheats** | Hotkey triggers during active gameplay (`K`, `L`, `H`, `J`). | `engine.toggle_cheat(code)` modifying game physics, speed, life deduction, and ghost ticks. |

---

## 5. Development & Testing Workflow

### Independent Testing Strategy
1. **Back-End Headless Testing (Person B)**:
   - Person B executes unit tests in `tests/` completely headlessly:
     ```bash
     make test  # uv run python -m unittest discover -s tests -v
     ```
   - Validates configuration, highscores, maze bitmasks, and engine physics without initializing Pygame display surfaces.

2. **Front-End Mocking (Person A)**:
   - Person A verified rendering and UI transitions independently using static mock `GameStateDT` snapshots before full engine integration.

### Code Quality Gates
Before any code was merged or submitted:
```bash
make clean        # Remove caches and pyc artifacts
make lint         # Flake8 style compliance & Mypy static analysis
make lint-strict  # Strict Mypy type-checking (0 errors across 30 source files)
make test         # 39 automated unit tests passing in 0.02s
```

---

## 6. Git Branching & Review Strategy

- **`main`**: Deployable production branch.
- **`newer`**: Active integration and development branch.
- **Commit Convention**: Semantic scoped commit messages (e.g., `feat(maze): ...`, `fix(ghost): ...`, `test(engine): ...`, `docs(team): ...`).
- **Peer Code Review**: Both brothers reviewed every change before merging to ensure mutual mastery of the entire codebase for the 42 peer defense recode evaluation.
