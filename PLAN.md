# Pac-Man: Master Architecture, Contract & Development Roadmap

> **Single Source of Truth for Development**  
> 42 Curriculum — *Pac-Man: Ghosts! More ghosts! (v1.4)*  
> Team Organization: Two Developers (**Person A: Front-End / Presentation** & **Person B: Back-End / Logic Core**)

---

## 1. Project Understanding

### 1.1 Context & Core Objective
The objective is to build a complete, playable, robust **Pac-Man** arcade game in **Python 3.10+** adhering to object-oriented principles, using **Pygame-ce** as the graphical library, integrating an external maze generation package, enforcing strict 42 coding standards (`flake8`, `mypy`), and producing a standalone packaged release for demonstration (Itch.io / Steam).

### 1.2 Mandatory Requirements & Constraints
| Category | Requirement | Specification Details |
| :--- | :--- | :--- |
| **CLI & Invocation** | `python3 pac-man.py config.json` | Exactly 1 CLI argument. Any error (missing file, invalid JSON, missing key) must produce a clean error message—**never a Python traceback**. |
| **Configuration** | JSON with `#` comments | Lines starting with `#` are comments. Missing or invalid values must clamp to safe defaults with clear log messages; unknown keys ignored. |
| **Maze Generator** | External `A-Maze-ing` package | Must use the assigned wheel (`mazegenerator`) **as-is**. The adapter must set `perfect=False` to generate Pac-Man corridor loops. Handled gracefully if it fails. |
| **Grid Placement** | Deterministic Spawns | Pac-Man in the center; 4 ghosts in 4 corners; 4 Super-pacgums in 4 corners; regular Pacgums in corridor cells. |
| **Player Mechanics** | Classic Pac-Man | 4-way movement (WASD/Arrows) confined strictly to corridors (no wall passing). 3 initial lives. Respawns in center upon life loss. Game over on 0 lives. |
| **Ghost AI** | 3-State Machine | **CHASE**: Autonomously tracks player through corridors.<br>**EDIBLE**: Triggered by Super-pacgum; ghosts turn vulnerable and flee.<br>**EATEN**: Defeated ghost returns to corner and respawns after 5–10s. |
| **Scoring & Progression** | Monotonic Score | +X per Pacgum, +Y per Super-pacgum, +Z per eaten ghost. 10 levels minimum with countdown timer (e.g. 90s). Score and lives persist across levels. |
| **Evaluation Cheats** | Review Facilitation | Invincibility, Level Skip, Freeze Ghosts, Extra Lives, Speed Boost. |
| **User Interface** | 5 Screens + HUD | Main Menu, In-Game HUD, Pause Menu, Game Over Screen, Victory Screen. Top 10 highscores with player names (max 10 alphanumeric chars). |
| **Code Standards** | 42 Norm | Python 3.10+, flake8 clean, strict mypy type hints (`--disallow-untyped-defs`), PEP 257 docstrings on all functions and classes, zero unhandled exceptions. |
| **Project Management** | Documentation Evidence | Dedicated directory documenting Timeline, Kanban, Risk Matrix, Acceptance Tests, and Team Work Breakdown (Ch. VIII). |
| **Packaging** | Standalone Executable | Root PyInstaller spec, unlisted public release on Itch.io/Steam with minimal in-package user instructions. |

---

## 2. Current Repository Analysis

### 2.1 File Audit & Implementation Status

| File | Intended Role | Current Status | Issues & Bugs Identified |
| :--- | :--- | :--- | :--- |
| `pac-man.py` | CLI Entry Point | **Broken** | Ignores `sys.argv[1]`; does not parse config; directly instantiates `Renderer()`; lacks try/except wrapper to suppress tracebacks. |
| `Makefile` | Build & Task Runner | **Functional** | Has `install`, `run`, `debug`, `clean`, `lint`, `lint-strict`. Uses `uv` (fallback to standard `python3`/`pip` recommended). |
| `pyproject.toml` | Project Dependencies | **Functional** | Declares `pygame-ce`, `flake8`, `mypy`, `pyinstaller`. |
| `src/parser.py` | Config Parser | **Partially Implemented** | Strips only leading `#` lines (fails on indented or inline comments); writes a new config to disk on missing file instead of memory fallback; no clamping log messages. |
| `src/scores_manager.py` | Highscore Persistence | **Partially Implemented** | Validates name (10 chars, alphanumeric + space); crashes with unhandled `HighscoreManagerError` on missing or malformed file instead of creating default list. |
| `src/maze.py` | A-Maze-ing Adapter | **Critically Broken** | 1. Inverted coordinate indexing: uses `maze[x][y]` instead of `maze[y][x]`.<br>2. Inverted bitmask interpretation: bit 1 in `MazeGenerator` means **wall present**, but code treated 1 as open path.<br>3. Does not pass `perfect=False`. |
| `src/models/player.py` | Player Domain Model | **Usable** | Clean coordinates, lives, score, and state. |
| `src/models/ghost.py` | Ghost Domain Model | **Incomplete** | Basic coordinates, lacks state transitions, corner detection, and pathfinding. |
| `src/models/pacgum.py` | Pellet Domain Model | **Usable** | Clean coordinates and super-pellet boolean flag. |
| `src/sprites/pacman.py` | Pac-Man Sprite | **Architectural Flaw** | Inherits from both `pygame.sprite.Sprite` and `Player`. Tightly couples Pygame rendering to pure game logic. |
| `src/sprites/ghost.py` | Ghost Sprite | **Broken** | Crashes on init (`self.assets = self.right` where `self.right` is not defined). |
| `src/sprites/pacgum.py` | Pellet Sprite | **Broken** | Empty constructor calls `Sprite.__init__()` and `Pacgum.__init__()` with missing arguments. |
| `src/sprites/crosshair.py` | Mouse Crosshair | **Unnecessary** | Unrelated gun cursor and sound effect (`crosshair.mp3`); not part of Pac-Man. |
| `src/rendering/maze_renderer.py`| Maze Wall Surface | **Partially Working** | Renders bitmask walls to a cached surface. Works, but hardcodes tile size and seed (45). |
| `src/ui/hud.py` | In-game HUD overlay | **Working** | Renders boards from `assets/images/boards/` for score, lives, level, timer. |
| `src/screens/main_menu.py` | Main Menu UI | **Incomplete** | Only displays the crosshair sprite; missing buttons for Start, Highscores, Help, and Exit. |
| `src/screens/ingame_screen.py` | In-game screen loop | **Incomplete** | Renders static 0 values; does not update sprites; contains duplicate `pygame.display.flip()`. |
| `src/screens/game_over_screen.py`| Game Over screen | **Empty Stub** | Only handles a quit event; missing score summary and highscore name input. |
| `src/game_manager.py` | Screen Coordinator | **Broken** | Crashes with `AttributeError` on `GAME_OVER` (`self.game_over` uninitialized); passes mismatched arguments to `MainMenu`. |
| `src/renderer.py` | Window & Main Loop | **Broken** | Forces `pygame.FULLSCREEN` (breaks headless/windowed setups); calls `flip()` while child screens also call `flip()`; no delta-time calculation. |
| `src/test.py` | Loose Test Script | **Unnecessary** | Scrap file in `src/`. Should be replaced with pytest tests in `tests/`. |
| `README.md` | Mandatory 42 Doc | **Missing** | Empty (0 bytes). |

---

## 3. Current Problems / Risks

1. **Coupled Model-View Inheritance:**
   `src/sprites/pacman.py` and `pacgum.py` mix pure entity data with Pygame rendering. This prevents headless automated unit tests (tests fail if Pygame video is uninitialized) and introduces fragile superclass initializers.
2. **Fatal Wall Collision Bug in `MazeAdapter`:**
   In the external `mazegenerator.py`:
   - `bit 0 (& 1)`: North Wall
   - `bit 1 (& 2)`: East Wall
   - `bit 2 (& 4)`: South Wall
   - `bit 3 (& 8)`: West Wall
   - `1` = **Wall Present**, `0` = **Open Corridor**.
   `src/maze.py` inverted this logic and reversed binary indices, making walls passable and corridors solid.
3. **Double `pygame.display.flip()` and Event Conflicts:**
   `Renderer.run()` has an outer event loop and calls `flip()`, while sub-screens (`MainMenu.run()`, `InGame.run()`) also call `pygame.event.get()` and `flip()`. This causes dropped keyboard inputs, black flickers, and unresponsive windows.
4. **Forced Fullscreen & Unresponsive Display:**
   Forcing `pygame.FULLSCREEN` freezes window managers or fails in dual-screen / evaluation setups. A windowed 1280x720 display with dynamic scaling is required.
5. **CLI & Specification Non-Compliance:**
   `pac-man.py` does not take `sys.argv[1]`, does not pass parsed configuration to the game engine, and does not catch exceptions to prevent Python tracebacks.
6. **Missing Evaluation Features:**
   No cheat engine, no pause screen, no victory screen, no name-input dialog for highscores, and no highscore browser on the main menu.

---

## 4. Recommended Architecture

The project will use a **Decoupled Engine-Renderer Pattern (Pure Logic vs. Presentation)**:

```
+-------------------------------------------------------------------------+
|                              CLI ENTRY                                  |
|                             pac-man.py                                  |
|         - Validates sys.argv[1] via ConfigParser                        |
|         - Catches uncaught exceptions gracefully (no tracebacks)        |
+------------------------------------+------------------------------------+
                                     |
                                     v
+-------------------------------------------------------------------------+
|                       CORE ENGINE / CONTROLLER                          |
|                       (Person B - Back-End)                             |
|                                                                         |
|   +-----------------------+     +-----------------------------------+   |
|   |   GameEngine (Logic)  | <-> |       GameStateDTO (Data DTO)     |   |
|   | - Tick loop (fixed dt)|     | - Grid coordinates (col, row)     |   |
|   | - Pacman navigation   |     | - Ghost states & directions       |   |
|   | - Ghost AI (BFS/Chase)|     | - Active pacgums / super-pacgums  |   |
|   | - Pellet eating       |     | - Score, Lives, Level, Time       |   |
|   | - Cheat manager       |     | - Highscore records               |   |
|   | - Level transitions   |     +-----------------------------------+   |
|   +-----------+-----------+                                             |
|               |                                                         |
|   +-----------v-----------+     +-----------------------------------+   |
|   |     MazeAdapter       |     |        HighscoreManager           |   |
|   | (Adapts A-Maze-ing)   |     | (Loads/saves top 10 JSON)         |   |
|   +-----------------------+     +-----------------------------------+   |
+------------------------------------+------------------------------------+
                                     | Passes Read-Only GameStateDTO
                                     v
+-------------------------------------------------------------------------+
|                      PRESENTATION & UI LAYER                            |
|                       (Person A - Front-End)                            |
|                                                                         |
|   +-----------------------------------------------------------------+   |
|   |                       Window & AppLoop                          |   |
|   |  - Single pygame.event.get() event pump                         |   |
|   |  - Delta-time clock tick (60 FPS)                               |   |
|   |  - Screen Router: MENU | PLAYING | PAUSED | GAMEOVER | VICTORY  |   |
|   +--------------------------------+--------------------------------+   |
|                                    |                                    |
|         +--------------------------+--------------------------+         |
|         |                          |                          |         |
|         v                          v                          v         |
|  +--------------+          +---------------+          +---------------+ |
|  |  MenuViews   |          | InGameView    |          | DialogViews   | |
|  | - Main Menu  |          | - Maze render |          | - Pause menu  | |
|  | - Highscores |          | - Sprite anim |          | - Name entry  | |
|  | - Rules/Help |          | - HUD boards  |          | - Victory     | |
|  +--------------+          +---------------+          +---------------+ |
+-------------------------------------------------------------------------+
```

### Core Responsibilities
- **Person B (Back-End Core):** Pure Python domain logic with **zero Pygame dependencies**. Owns grid coordinates, collision detection, ghost pathfinding algorithms, maze generation adapter, config parsing, highscores persistence, and cheat flags. Exposes a clean, typed `IGameEngine` interface.
- **Person A (Front-End Presentation):** Pygame lifecycle owner. Owns window management, event polling, key translation, sprite animations, sound effects, HUD drawing, screen navigation, and PyInstaller packaging.

---

## 5. Clean Project Structure

### 5.1 Proposed Directory Layout

```
pacman-project/
├── .gitignore
├── Makefile
├── pyproject.toml
├── pac-man.spec                     # Standalone packaging spec
├── pac-man.py                       # Main CLI entry point
├── config.json                      # Default configuration
├── highscores.json                  # Persistent highscores file
├── README.md                        # Ch. IX compliant documentation
│
├── docs/                            # Project Management Evidence (Ch. VIII)
│   ├── TIMELINE.md                  # Milestone planning & schedule
│   ├── KANBAN.md                    # Work division & task status
│   ├── RISKS.md                     # Risk analysis & mitigations
│   └── TEST_PLAN.md                 # Acceptance test protocols
│
├── assets/                          # Static media assets
│   ├── fonts/
│   │   └── pacfont.ttf
│   ├── sounds/
│   │   ├── chomp.wav
│   │   ├── death.wav
│   │   ├── eat_ghost.wav
│   │   └── power_pellet.wav
│   └── images/
│       ├── backgrounds/
│       │   └── general_background.jpg
│       ├── boards/
│       │   ├── scoreboard.png
│       │   ├── livesboard.png
│       │   ├── timerboard.png
│       │   └── levelboard.png
│       ├── pacman/                  # Directional & death frame sequences
│       └── ghosts/                  # Ghost directional, scared, and flashing sprites
│
├── src/                             # Source Package
│   ├── __init__.py
│   ├── core/                        # BACK-END: Pure Game Logic (Person B)
│   │   ├── __init__.py
│   │   ├── config.py                # ConfigParser with comment stripping & clamping
│   │   ├── highscores.py            # HighscoreManager (top 10, name validation)
│   │   ├── maze_adapter.py          # A-Maze-ing wrapper (bitmask & perfect=False)
│   │   ├── entities.py              # Pure data models (Player, Ghost, Pacgum, DTOs)
│   │   ├── ghost_ai.py              # BFS / Chase / Flee algorithms
│   │   ├── cheats.py                # Cheat controller (invincible, skip, freeze, speed)
│   │   └── engine.py                # GameEngine coordinating rules, score, timers
│   │
│   ├── views/                       # FRONT-END: Pygame UI & Rendering (Person A)
│   │   ├── __init__.py
│   │   ├── window.py                # Window manager, resolution scaling, frame-rate
│   │   ├── maze_view.py             # Optimized wall surface builder & cache
│   │   ├── sprite_view.py           # Animated sprite drawer (Pacman, Ghosts, Pellets)
│   │   ├── hud_view.py              # In-game stats boards & text overlay
│   │   └── screens/                 # State screens
│   │       ├── __init__.py
│   │       ├── base_screen.py       # Abstract BaseScreen interface
│   │       ├── menu_screen.py       # Main menu (Start, Scores, Help, Exit)
│   │       ├── game_screen.py       # Active gameplay screen
│   │       ├── pause_screen.py      # Pause menu modal
│   │       ├── highscore_screen.py  # Top 10 leaderboard display
│   │       ├── game_over_screen.py  # Defeat screen with name entry input
│   │       └── victory_screen.py    # Victory screen with name entry input
│   │
│   └── app.py                       # Application Orchestrator / Game Controller
│
└── tests/                           # Unit and Integration Tests (pytest)
    ├── test_config.py               # Config parsing & faulty JSON tests
    ├── test_highscores.py           # Highscores loading, sorting, validation
    ├── test_maze_adapter.py         # Bitmask corridor & boundary tests
    └── test_engine.py               # Collision, scoring, and cheat tests
```

---

## 6. Front-end ↔ Back-end Contract

### 6.1 Shared Data Structures (`src/core/entities.py`)

```python
from dataclasses import dataclass
from enum import Enum
from typing import List

class Direction(str, Enum):
    UP = "UP"
    DOWN = "DOWN"
    LEFT = "LEFT"
    RIGHT = "RIGHT"
    NONE = "NONE"

class GhostState(str, Enum):
    CHASE = "CHASE"
    EDIBLE = "EDIBLE"
    FLASHING = "FLASHING"
    EATEN = "EATEN"

@dataclass(frozen=True)
class EntityDTO:
    id: str                          # "pacman", "blinky", "pinky", "inky", "clyde"
    grid_x: int                      # Current column in maze
    grid_y: int                      # Current row in maze
    pixel_offset_x: float            # Interpolated sub-tile offset [0.0, 1.0)
    pixel_offset_y: float            # Interpolated sub-tile offset [0.0, 1.0)
    direction: Direction
    state: str                       # e.g. "ALIVE", "DEAD", or GhostState

@dataclass(frozen=True)
class PacgumDTO:
    grid_x: int
    grid_y: int
    is_super: bool

@dataclass(frozen=True)
class GameStateDTO:
    level: int
    score: int
    lives: int
    time_remaining: float
    is_paused: bool
    is_game_over: bool
    is_victory: bool
    is_level_cleared: bool
    pacman: EntityDTO
    ghosts: List[EntityDTO]
    pacgums: List[PacgumDTO]
    grid_width: int
    grid_height: int
    active_cheats: List[str]
```

### 6.2 Back-end Engine API (`src/core/engine.py`)

```python
class IGameEngine:
    def load_config(self, config_data: dict) -> None:
        """Initialize engine settings from validated config."""
        ...

    def start_new_game(self) -> None:
        """Reset scores, lives, level count, and spawn entities."""
        ...

    def update(self, dt: float) -> None:
        """Advance game physics and timers by delta-time (dt in seconds)."""
        ...

    def set_player_direction(self, direction: Direction) -> None:
        """Queue the next intended direction for Pac-Man."""
        ...

    def toggle_pause(self) -> bool:
        """Toggle paused state; returns new pause status."""
        ...

    def trigger_cheat(self, cheat_code: str) -> None:
        """Toggle cheat features: 'INVINCIBILITY', 'SKIP_LEVEL', 'FREEZE_GHOSTS', 'ADD_LIFE', 'SPEED'."""
        ...

    def get_state(self) -> GameStateDTO:
        """Return an immutable snapshot of current game state for rendering."""
        ...

    def get_wall_matrix(self) -> List[List[int]]:
        """Return 2D grid of 4-bit wall bitmasks for the current level."""
        ...
```

---

## 7. Feature-by-Feature Integration Plan

### Feature 1: Configuration Loading & CLI Launch
- **Front-end needs:** Validated config parameters to initialize window and HUD.
- **Back-end provides:** `ConfigParser.load(filepath) -> dict` returning sanitized parameters with fallback defaults.
- **Error Handling:** Missing or malformed config logs a clear explanation, applies safe defaults, and runs without a traceback.
- **Order:** Person B implements parser + unit tests; Person A connects it to `pac-man.py`.

### Feature 2: Maze Generation & Wall Rendering
- **Front-end needs:** 2D grid of wall bitmasks to draw walls onto a cached surface.
- **Back-end provides:** `MazeAdapter` wrapping `mazegenerator.MazeGenerator(size=(w, h), seed=s, perfect=False)`.
- **Bitmask Definition:**
  - `bit 0 (& 1)`: North Wall
  - `bit 1 (& 2)`: East Wall
  - `bit 2 (& 4)`: South Wall
  - `bit 3 (& 8)`: West Wall
  - `1` = Wall / Blocked; `0` = Corridor / Walkable.
- **Order:** Person B fixes `src/maze.py`; Person A builds cached `maze_view.py`.

### Feature 3: Player Movement & Pellet Eating
- **Front-end needs:** Pac-Man grid position, sub-tile offset, and direction for sprite animation.
- **Back-end provides:** Direction queuing, corridor check (`can_move`), pellet collision, and score updates.
- **Order:** Person B writes pure movement logic; Person A maps keyboard events (WASD / Arrows).

### Feature 4: Ghost AI State Machine & Frightened Mode
- **Front-end needs:** Entity positions and states (`CHASE`, `EDIBLE`, `FLASHING`, `EATEN`) to render the correct sprite.
- **Back-end provides:**
  - BFS corridor chase towards player.
  - Vulnerable state on Super-pacgum collection (7s edible + 3s flashing).
  - Life loss and respawn on normal collision; ghost defeat and corner respawn on edible collision.
- **Order:** Person B implements AI state machine; Person A draws ghost sprites and handles audio triggers.

### Feature 5: In-Game HUD, Level Progression & Timers
- **Front-end needs:** Score, lives, level number, countdown timer.
- **Back-end provides:** Level timer decrement in `update(dt)`. Level transition on all pellets consumed (advancing up to level 10+).
- **Order:** Person B manages multi-level loop; Person A wires `hud_view.py` to `GameStateDTO`.

### Feature 6: Highscores & UI Screens
- **Front-end needs:** Top 10 leaderboard data and text input box for name entry on victory/defeat.
- **Back-end provides:** `HighscoreManager` loading/saving `highscores.json`, name validation (max 10 alphanumeric chars), and sorting.
- **Order:** Person B implements file manager; Person A implements Menu, Pause, Game Over, and Victory screens.

### Feature 7: Cheat Mode
- **Front-end needs:** Hotkeys bound during gameplay (`I` = Invincible, `L` = Level Skip, `F` = Freeze Ghosts, `+` = Extra Life, `S` = Speed Boost).
- **Back-end provides:** `engine.trigger_cheat(code)` toggling active cheat states.
- **Order:** Person B adds cheat flags to engine; Person A captures keystrokes and displays cheat status in HUD.

---

## 8. Development Roadmap

```
[Phase 1: Foundations & Architecture] (Days 1-2)
  ├── Task 1.1: Fix ConfigParser & CLI (Person B)
  ├── Task 1.2: Clean Display & App Skeleton (Person A)
  └── MILESTONE 1: Clean CLI boot without crash, windowed display ready

[Phase 2: Maze Logic & Wall Rendering] (Days 3-4)
  ├── Task 2.1: Correct MazeAdapter Bitmasks (Person B)
  ├── Task 2.2: Dynamic Maze Surface Renderer (Person A)
  └── MILESTONE 2: Correct maze rendered on screen with 'perfect=False'

[Phase 3: Entities & Core Movement] (Days 5-6)
  ├── Task 3.1: Grid Movement & Pellet Collision (Person B)
  ├── Task 3.2: Animated Sprites & Direction Controls (Person A)
  └── MILESTONE 3: Pac-Man moves smoothly through corridors and eats pacgums

[Phase 4: Ghost AI & Power Mechanics] (Days 7-8)
  ├── Task 4.1: Ghost State Machine & Pathfinding (Person B)
  ├── Task 4.2: Ghost Sprites (Normal, Scared, Eyes) (Person A)
  └── MILESTONE 4: Ghosts chase, turn edible on Super-pacgum, can be eaten

[Phase 5: Progression, UI Screens & Highscores] (Days 9-10)
  ├── Task 5.1: 10-Level Loop, Timer, Highscores (Person B)
  ├── Task 5.2: Screens (Menu, Pause, GameOver, Victory) (Person A)
  └── MILESTONE 5: Complete game loop from Menu to Win/Loss to Highscores

[Phase 6: Cheats, Packaging & Polish] (Days 11-12)
  ├── Task 6.1: Cheat Mode & Unit Test Suite (Person B)
  ├── Task 6.2: PyInstaller Packaging & Documentation (Person A)
  └── MILESTONE 6: Standalone executable, passing lint/mypy, ready for defense
```

---

## 9. Parallel Work Plan for Two Developers

| Phase | Person A (Front-end / Presentation) | Person B (Back-end / Logic Core) | Joint Verification Milestone |
| :--- | :--- | :--- | :--- |
| **Phase 1** | • Refactor `src/renderer.py` into windowed 1280x720 display with 60 FPS clock.<br>• Unify event loop into single `pygame.event.get()`.<br>• Remove `crosshair.py` and extraneous assets. | • Rewrite `src/parser.py` (comment stripping, default clamping, validation logging).<br>• Wire `pac-man.py` with `sys.argv[1]` and traceback-free error handling. | **M1:** `python3 pac-man.py config.json` starts a clean window with settings from config. |
| **Phase 2** | • Update `maze_renderer.py` to render variable grid sizes dynamically.<br>• Implement `grid_to_pixel()` coordinate mapping and sub-tile interpolation. | • Fix `src/maze.py`: correct `[y][x]` indexing, invert bitmask checks, add `perfect=False`.<br>• Write unit tests verifying corridor traversability and boundaries. | **M2:** Real maze from `A-Maze-ing` package renders accurately on screen with open corridor loops. |
| **Phase 3** | • Build `src/views/sprite_view.py` for animated directional Pac-Man sprites.<br>• Capture WASD/Arrow keys in main event loop and forward to engine. | • Implement `Player` entity logic and queued direction turning in `src/core/engine.py`.<br>• Implement Pacgum and Super-pacgum grid placement and consumption logic. | **M3:** Player controls Pac-Man through corridors, eating pellets, updating score in real-time. |
| **Phase 4** | • Add rendering for 4 distinct ghost colors, frightened flashing state, and eaten eyes state.<br>• Integrate audio triggers for chomp, ghost eaten, and death. | • Implement `GhostAI` with BFS corridor navigation.<br>• Implement 3-state machine (`CHASE`, `EDIBLE`, `EATEN`).<br>• Implement touch collision and respawn timer. | **M4:** Playable game with full ghost chase, power pellet vulnerability, and respawning. |
| **Phase 5** | • Implement `MainMenu`, `PauseMenu`, `GameOverScreen`, `VictoryScreen`, and `HighscoreScreen`.<br>• Build name-input text field (10 alphanumeric chars). | • Implement 10-level progression and level countdown timer.<br>• Fix `HighscoreManager` to prevent crashes on missing/corrupted files. | **M5:** Complete game loop: Main Menu -> Start -> 10 Levels -> Victory/Defeat -> Name Input -> Highscore save. |
| **Phase 6** | • Create `pac-man.spec` for PyInstaller.<br>• Test standalone executable build.<br>• Format `README.md` to Ch. IX specification. | • Implement cheat mode toggles (`I`, `L`, `F`, `+`, `S`).<br>• Write test suite in `tests/` covering config, highscores, and engine. | **M6:** `make lint` and `make lint-strict` pass 100% green; executable uploads cleanly to Itch.io. |

---

## 10. Git Workflow

### 10.1 Branch Strategy
- **`main`**: Production-ready, deployable, passes `make lint`. Direct pushes are blocked.
- **`develop`**: Integration branch for combining feature branches.
- **Feature Branches**:
  - `feat/fe-window-loop` (Person A)
  - `feat/be-config-parser` (Person B)
  - `feat/be-maze-adapter` (Person B)
  - `feat/fe-screens-ui` (Person A)
  - `feat/be-ghost-ai` (Person B)
  - `feat/fe-packaging` (Person A)

### 10.2 Commit Rules
Conventional commits with scope:
- `feat(parser): support hash comments and default fallback clamping`
- `fix(maze): correct bitmask interpretation and y-x coordinate indexing`
- `feat(ui): implement pause menu overlay and resume action`
- `docs(project): update kanban board and risk mitigation matrix`

### 10.3 Integration & Conflict Avoidance Rules
1. **Directory Boundary**: Person B works in `src/core/` and `tests/`; Person A works in `src/views/` and `assets/`.
2. **Contract-First Agreement**: Interface signatures in `src/core/entities.py` cannot be modified without mutual agreement.
3. **Pre-Merge Checklist**:
   ```bash
   make clean
   make lint
   pytest
   ```
4. **Peer Review**: Both brothers must review and approve every PR to prepare for the 42 evaluation recode test.

---

## 11. Testing & Integration Strategy

### 11.1 Independent Headless Tests (Person B)
```bash
pytest tests/
```
- `tests/test_config.py`: Missing file, malformed syntax, comment handling, default clamping.
- `tests/test_highscores.py`: Missing JSON, corrupted data, sorting, 10-character name validation.
- `tests/test_maze_adapter.py`: Validates wall bitmask logic, ensuring walls are impassable and corridors open.
- `tests/test_engine.py`: Tests movement rules, life deduction, score increments, and cheat toggles.

### 11.2 Independent Front-end Mocking (Person A)
Person A tests rendering components using a static mock `GameStateDTO` without waiting for engine completion:
```python
mock_state = GameStateDTO(
    level=1, score=1200, lives=3, time_remaining=85.0,
    is_paused=False, is_game_over=False, is_victory=False, is_level_cleared=False,
    pacman=EntityDTO("pacman", 10, 10, 0.0, 0.0, Direction.RIGHT, "ALIVE"),
    ghosts=[EntityDTO("blinky", 1, 1, 0.0, 0.0, Direction.LEFT, GhostState.CHASE)],
    pacgums=[PacgumDTO(5, 5, False), PacgumDTO(1, 1, True)],
    grid_width=20, grid_height=20, active_cheats=[]
)
```

---

## 12. Critical Path

1. **Fix `src/maze.py`**: Everything depends on a working maze. Entities cannot navigate until walls and corridors are correctly identified.
2. **Decouple Models from Pygame**: Remove `pygame.sprite.Sprite` inheritance from `Player` and `Pacgum` so Person B can build pure movement logic and unit tests.
3. **Establish Single Event Loop**: Eliminate duplicate `flip()` and `pygame.event.get()` calls in sub-screens.
4. **Core Gameplay Loop**: Pac-Man movement, pellet eating, and Ghost AI chase.
5. **UI & Progression**: Menu navigation, countdown timer, highscore registration, and cheat hotkeys.
6. **Packaging**: PyInstaller `.spec` build and `README.md` completion.

---

## 13. Immediate Next Steps

1. **Delete obsolete artifacts:**
   - Remove `src/sprites/crosshair.py`, `assets/sounds_effect/crosshair.mp3`, and `src/test.py`.
2. **Fix `src/maze.py`:**
   - Pass `perfect=False` to `MazeGenerator`.
   - Access grid via `self.maze[y][x]`.
   - Check wall bitmasks directly where `1` = Wall (`if direction == "UP": return not bool(cell & 1)`).
3. **Decouple Entities in `src/models/`:**
   - Make `Player`, `Ghost`, and `Pacgum` pure Python dataclasses.
4. **Refactor Main Loop in `src/renderer.py`:**
   - Replace fullscreen with a 1280x720 window; centralize `clock.tick(60)` and `pygame.display.flip()`.
5. **Initialize Project Management Folder:**
   - Create `docs/KANBAN.md` and `docs/TIMELINE.md` to satisfy Chapter VIII.
