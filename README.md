_This project has been created as part of the 42 curriculum by alaktaou and mlaktaou._

# Pac-Man: Ghosts! More Ghosts!

[![Language](https://img.shields.io/badge/Language-Python%203.10%2B-blue.svg)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/Engine-Pygame--ce%202.5.8%2B-green.svg)](https://pyga.me/)
[![Type Checker](https://img.shields.io/badge/Type%20Check-mypy%20strict-brightgreen.svg)](https://mypy-lang.org/)
[![Linter](https://img.shields.io/badge/Linter-flake8-yellow.svg)](https://flake8.pycqa.org/)

A full-featured, arcade-accurate recreation of **Pac-Man** featuring procedural maze integration, four distinct ghost artificial intelligence profiles, dynamic difficulty scaling across 10 levels, developer debug cheats, persistent high scores, and a strict decoupled Model-View-Controller architecture.

---

## Table of Contents

- [1. Description](#1-description)
- [2. Instructions](#2-instructions)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Execution](#execution)
  - [Controls & Hotkeys](#controls--hotkeys)
  - [Development Tasks (Makefile)](#development-tasks-makefile)
- [3. Resources & AI Usage](#3-resources--ai-usage)
  - [Classic References](#classic-references)
  - [AI Usage Disclosure](#ai-usage-disclosure)
- [4. Configuration](#4-configuration)
  - [File Structure & Comment Support](#file-structure--comment-support)
  - [Supported Configuration Keys](#supported-configuration-keys)
  - [Validation, Clamping & Fallback Logic](#validation-clamping--fallback-logic)
  - [Example Configuration](#example-configuration)
- [5. Highscore](#5-highscore)
  - [Persistence System Architecture](#persistence-system-architecture)
  - [Storage Format & File Handling](#storage-format--file-handling)
  - [Validation & Sanitization Logic](#validation--sanitization-logic)
  - [Justification of Design Decisions](#justification-of-design-decisions)
- [6. Maze Generation](#6-maze-generation)
  - [A-Maze-ing Wheel Integration](#a-maze-ing-wheel-integration)
  - [Wall Bitmask Specification](#wall-bitmask-specification)
  - [Corridor Graph & Neighbor Traversal](#corridor-graph--neighbor-traversal)
  - [Procedural Progression Across Levels](#procedural-progression-across-levels)
- [7. Implementation](#7-implementation)
  - [Game Loop & Timing Architecture](#game-loop--timing-architecture)
  - [Movement Physics & Sub-Tile Motion Interpolation](#movement-physics--sub-tile-motion-interpolation)
  - [Collision Handling Matrix](#collision-handling-matrix)
  - [Ghost AI Personalities & State Machine](#ghost-ai-personalities--state-machine)
  - [Visual Effects & Shaders](#visual-effects--shaders)
- [8. General Software Architecture](#8-general-software-architecture)
  - [Architectural Overview](#architectural-overview)
  - [Module & Class Breakdown](#module--class-breakdown)
  - [Data Transfer Object (DTO) Boundary](#data-transfer-object-dto-boundary)
- [9. Project Management](#9-project-management)
  - [Methodology & Team Breakdown](#methodology--team-breakdown)
  - [Direct Link to Project Management Documentation](#direct-link-to-project-management-documentation)

---

## 1. Description

The goal of this project is to build a robust, modular, and extensible desktop recreation of the legendary arcade title **Pac-Man** using **Python 3.10+** and **Pygame-ce** as prescribed by the 42 curriculum (_Pac-Man: Ghosts! More ghosts!_).

Rather than simply rendering a static pre-defined maze, the game integrates with the 42 **A-Maze-ing** procedural maze generator to generate dynamic, complex 15x15 labyrinthine grids for each level. The player must navigate the labyrinth, consume all pellets (**pacgums**) and energized power pellets (**super-pacgums**), while evading four distinct spectral pursuers (**Blinky**, **Pinky**, **Inky**, and **Clyde**), each exhibiting specialized behavior.

### Key Highlights

- **Strict Decoupled Architecture**: A pure Python core engine (`src/core/`) isolated from graphics and audio, communicating via read-only Data Transfer Objects (`GameStateDT`). The engine has zero Pygame dependencies, making it 100% testable headlessly.
- **Dynamic Procedural Mazes**: Native integration of the `mazegenerator` wheel, decoding 4-bit directional wall bitmasks into an traversable corridor graph.
- **Authentic Ghost Artificial Intelligence**:
  - **Blinky (Red)**: The relentless hunter using Breadth-First Search (BFS) shortest-path navigation targeting Pac-Man directly.
  - **Pinky (Pink) & Clyde (Orange)**: Explorers roaming corridors and making pseudo-random junction turns.
  - **Inky (Cyan)**: Tactical ambusher computing a 20-tile lookahead projection along Pac-Man's trajectory vector.
  - **Frightened / Edible**: Dynamic evasion state calculating the maximum Manhattan distance away from Pac-Man.
  - **Eaten / Eyes**: Defeated ghosts pathfind back to their origin corner before reforming.
- **Fluid Sub-Tile Rendering**: 60 FPS coordinate interpolation converting discrete grid steps into silky-smooth continuous pixel motion.
- **10-Level Campaign**: Level progression with per-level timer countdowns, ready intermission banners, and persistent score accumulation.
- **Developer Cheat Suite**: Real-time hotkeys to skip levels, boost speed, freeze enemies, and enable invulnerability for grading and testing.
- **Hardened Highscore Persistence**: JSON-backed storage with strict schema validation, alphanumeric name sanitization, and corruption recovery.

---

## 2. Instructions

### Prerequisites

- **Python**: Version `3.10` or higher (`3.13` recommended).
- **Package Manager**: [`uv`](https://github.com/astral-sh/uv) (recommended) or standard `pip` / `venv`.
- **System Dependencies**: Standard audio/video drivers required by Pygame (SDL2 libraries on Linux).

### Installation

#### Method A: Using `uv` and `Makefile` (Recommended)

The repository includes a ready-to-use `Makefile` preconfigured with `uv`:

```bash
# Clone the repository
git clone <repository_url>
cd Pac-ma

# Install project dependencies and the external A-Maze-ing wheel
make install
```

#### Method B: Manual Installation via standard `pip` and `venv`

If `uv` is not installed on your system, you can use standard Python tooling:

```bash
# Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies from pyproject.toml
pip install "pygame-ce>=2.5.8" "flake8>=7.3.0" "mypy>=2.3.1" "pyinstaller>=6.22.2"

# Install the external A-Maze-ing maze generator wheel
pip install mazegenerator-00001-py3-none-any.whl
```

### Execution

The game entry point is `pac-man.py`, which requires the path to a JSON configuration file as its single argument:

```bash
# Via Makefile (runs with default config.json)
make run

# Or directly via CLI with custom or default configuration
python pac-man.py config.json
```

> **CLI Validation Note**: The CLI strictly requires exactly one argument ending with `.json`. Passing missing files, improper extensions, or invalid syntax triggers graceful error messages without raw Python stack traces.

### Controls & Hotkeys

| Key Binding           | Category       | Description                                                                |
| :-------------------- | :------------- | :------------------------------------------------------------------------- |
| **`Up`** / **`W`**    | Movement       | Move Pac-Man Up                                                            |
| **`Down`** / **`S`**  | Movement       | Move Pac-Man Down                                                          |
| **`Left`** / **`A`**  | Movement       | Move Pac-Man Left                                                          |
| **`Right`** / **`D`** | Movement       | Move Pac-Man Right                                                         |
| **`P`**               | Game Flow      | Pause / Resume gameplay with blurred overlay                               |
| **`R`**               | Game Flow      | Restart / Replay current game                                              |
| **`Q`**               | Game Flow      | Return to Main Menu                                                        |
| **`ESC`**             | Application    | Quit the application cleanly                                               |
| **`K`**               | **Cheat Code** | **Skip Level**: Instantly completes the current level and advances         |
| **`L`**               | **Cheat Code** | **Speed Boost**: Doubles Pac-Man's movement speed (0.1s step delay)        |
| **`H`**               | **Cheat Code** | **Unlimited Lives**: Grants Unlimited lives invulnerability against ghosts |
| **`J`**               | **Cheat Code** | **Freeze Ghosts**: Freezes all ghost AI updates in place                   |

### Development Tasks (Makefile)

The `Makefile` defines standard targets for linting, typing, debugging, and housekeeping:

```bash
make run          # Launch the game with uv and config.json
make debug        # Run the game inside the Python PDB debugger
make lint         # Run flake8 style checks and mypy static type checking
make lint-strict  # Run flake8 and mypy in strict verification mode
make clean        # Remove __pycache__, .pyc files, and .mypy_cache
```

---

## 3. Resources & AI Usage

### Classic References

1. **The Pac-Man Dossier** by _Jamey Pittman_:
   - Detailed analysis of original 1980 arcade ROM logic, tile-based navigation, ghost targeting routines, corner scatter behavior, and speed timers.
   - Reference URL: [https://www.gamedeveloper.com/design/the-pac-man-dossier](https://www.gamedeveloper.com/design/the-pac-man-dossier)
2. **Pygame-ce (Community Edition) Documentation**:
   - Reference guide for SDL2 windowing, alpha surfaces, coordinate blitting, event queue consumption, and box-blur shaders (`pygame.transform.box_blur`).
   - Reference URL: [https://pyga.me/docs/](https://pyga.me/docs/)
3. **Introduction to Algorithms (CLRS) - Graph Search & BFS**:
   - Algorithmic foundations for grid graph representation, unweighted shortest-path Breadth-First Search, and queue-based neighbor expansion.
4. **Game Programming Patterns** by _Robert Nystrom_:
   - Patterns applied: Game Loop, State Pattern (Ghost states, screen states), Component/DTO Decoupling, and Spatial Graph Partitioning.
   - Reference URL: [https://gameprogrammingpatterns.com/](https://gameprogrammingpatterns.com/)
5. **Python Typing (PEP 484, PEP 544, PEP 585, PEP 604)**:
   - Modern type annotation standards enabling strict static analysis via `mypy`.

### AI Usage Disclosure

In compliance with the 42 curriculum guidelines (p. 18), the exact usage of Artificial Intelligence during project conception, engineering, and documentation is disclosed below:

- stillllll

---

## 4. Configuration

### File Structure & Comment Support

The game configuration is provided as a JSON file via the command-line interface.

In addition to standard JSON syntax, our custom configuration parser in `src/core/config.py` supports **line comments starting with `#`**. Lines with leading `#` (and surrounding whitespace) are automatically stripped before passing the payload to Python's `json.loads()`.

Furthermore, if the file specified on the CLI does not exist, the game **automatically generates a fresh configuration file** pre-populated with standard default values via `create_config()`.

### Supported Configuration Keys

The following table documents every supported key, expected type, validation boundaries, and fallback default values:

| Key                       | Type  |    Default Value    | Validation Constraints     | Description                                                                                    |
| :------------------------ | :---: | :-----------------: | :------------------------- | :--------------------------------------------------------------------------------------------- |
| `highscore_filename`      | `str` | `"highscores.json"` | Must be a non-empty string | Path to the persistent JSON file where highscores are stored and loaded.                       |
| `lives`                   | `int` |         `3`         | `int >= 0`                 | Initial number of lives allocated to Pac-Man at the start of a game.                           |
| `pacgum`                  | `int` |        `42`         | `int >= 4`                 | Total number of pellets distributed across the maze (minimum 4 to place corner Super-pacgums). |
| `points_per_pacgum`       | `int` |        `120`        | `int >= 0`                 | Score points awarded when Pac-Man consumes a standard pellet.                                  |
| `points_per_super_pacgum` | `int` |        `50`         | `int >= 0`                 | Score points awarded when Pac-Man consumes an energizing Super-pacgum.                         |
| `points_per_ghost`        | `int` |        `200`        | `int >= 0`                 | Base score points awarded for devouring a frightened ghost.                                    |
| `seed`                    | `int` |        `42`         | `int >= 0`                 | Seed integer passed to `MazeGenerator` for initial procedural generation.                      |
| `level_max_time`          | `int` |        `120`        | `int >= 0`                 | Time limit in seconds allowed to complete each level before game over.                         |

### Validation, Clamping & Fallback Logic

The configuration loader enforces robust defensive programming:

1. **Type Strictness**: Boolean values (`True`/`False`) are explicitly rejected for numeric fields (since `isinstance(True, int)` evaluates to `True` in Python).
2. **Missing Key Handling**: If a key is missing from the JSON file, the parser emits an informative warning:
   ```text
   Warning: missing '<key>', using default value
   ```
3. **Invalid Value Handling**: If a key contains an invalid type, negative integer, or out-of-range constraint (e.g., `pacgum < 4`), the parser emits:
   ```text
   Warning: invalid '<key>', using default value
   ```
4. **Zero-Crash Policy**: The game never terminates due to missing or ill-formed configuration keys; it gracefully clamps all invalid settings to their reliable defaults.

### Example Configuration

```json
# ==========================================
# 42 Pac-Man Runtime Configuration
# Lines starting with '#' are ignored comments
# ==========================================
{
    "highscore_filename": "highscores.json",
    "lives": 3,
    "pacgum": 42,
    "points_per_pacgum": 120,
    "points_per_super_pacgum": 50,
    "points_per_ghost": 200,
    "seed": 42,
    "level_max_time": 120
}
```

---

## 5. Highscore

### Persistence System Architecture

Highscore persistence is handled by the `HighscoreManager` class located in `src/core/highscores.py`. It operates as a self-contained persistence module decoupled from both graphics rendering and game simulation.

```
Game Completion (Victory / Game Over)
               │
               ▼
   ScrSaveScore (Name Input Modal)
               │ (player_name, score)
               ▼
HighscoreManager.add_score(name, score)
               │
               ├─► validate_name() & score verification
               ├─► Appends & sorts descending by score
               ├─► Clamps list to top 10 entries
               ▼
HighscoreManager.save_scores()
               │
               ▼
Writes formatted JSON to disk (highscores.json)
```

### Storage Format & File Handling

Scores are serialized in human-readable JSON format, indented by 4 spaces for transparency and ease of auditing:

```json
[
  {
    "name": "ALAKTAOU",
    "score": 135200
  },
  {
    "name": "MLAKTAOU",
    "score": 38480
  }
]
```

- **Absence Resilience**: If the highscore file does not exist upon game launch (`FileNotFoundError`), `HighscoreManager` initializes an empty leaderboard (`self.scores = []`) rather than crashing.
- **Top 10 Clamping**: The list automatically discards scores beyond rank 10 using Python slicing `self.scores[:10]`.
- **Atomic Operations**: Saving is executed immediately upon score submission to prevent data loss on unexpected exits.

### Validation & Sanitization Logic

The persistence engine enforces strict validation before accepting any record:

1. **Name Validation (`validate_name`)**:
   - **Length Limit**: Must be strictly between 1 and 10 characters (`0 < len(name) <= 10`).
   - **Character Whitelist**: Only alphanumeric characters (`a-z`, `A-Z`, `0-9`) and spaces (` `) are permitted (`all(char.isalnum() or char == " " for char in name)`).
   - **Security**: Prevents buffer overflows, format string vulnerabilities, and UI distortion in leaderboard menus.
2. **Score Validation**:
   - Score must be a positive integer (`isinstance(score, int) and score >= 0`).
3. **Corrupted File Detection**:
   - If the JSON file contains corrupted data, non-list root structures, or modified invalid entries, a `HighscoreManagerError` is raised with a clear explanatory error message.

### Justification of Design Decisions

- **Why JSON?**: JSON is human-readable, cross-platform, natively supported by Python's standard library (`json`), and does not require third-party relational databases (like SQLite) or fragile binary serialization (like `pickle`), which poses security risks.
- **Decoupled Architecture**: By keeping `HighscoreManager` purely in `src/core/`, score storage logic can be verified with automated headless unit tests without initializing Pygame display surfaces.
- **Whitelist Filtering**: Limiting names to 10 alphanumeric characters mirrors authentic arcade hardware constraints and ensures clean, uniform typography on the HUD and leaderboard screens.

---

## 6. Maze Generation

### A-Maze-ing Wheel Integration

The game integrates the assigned external **`mazegenerator`** package (provided via the wheel file `mazegenerator-00001-py3-none-any.whl`).

Integration is orchestrated through the `MazeAdapter` class (`src/core/maze_adapter.py`), which acts as an **Adapter Pattern** wrapper around the third-party `MazeGenerator` class:

```python
from mazegenerator import MazeGenerator

class MazeAdapter:
    SIZE = (15, 15)

    def __init__(self, seed: int):
        self.mazegenerator = MazeGenerator(size=self.SIZE, seed=seed)
        self.maze: list[list[int]] = self.mazegenerator.maze
        self.width = self.SIZE[0]
        self.height = self.SIZE[1]
```

### Wall Bitmask Specification

The external library outputs the maze as a two-dimensional grid of integers (`maze[y][x]`). Each integer is a **4-bit bitmask** encoding the presence or absence of walls surrounding that cell:

|    Bit Position    | Value | Binary Mask |     Direction      |      Meaning When Bit is `1`       | Meaning When Bit is `0` |
| :----------------: | :---: | :---------: | :----------------: | :--------------------------------: | :---------------------: |
|  **Bit 0 (LSB)**   |  `1`  |   `0001`    |   **North (Up)**   |            Wall Present            |      Open Corridor      |
|     **Bit 1**      |  `2`  |   `0010`    |  **East (Right)**  |            Wall Present            |      Open Corridor      |
|     **Bit 2**      |  `4`  |   `0100`    |  **South (Down)**  |            Wall Present            |      Open Corridor      |
|  **Bit 3 (MSB)**   |  `8`  |   `1000`    |  **West (Left)**   |            Wall Present            |      Open Corridor      |
| **Solid Obstacle** | `15`  |   `1111`    | **All Directions** | Fully enclosed solid obstacle cell |    Impassable block     |

In `MazeAdapter.can_move(x, y, direction)`, the cell value is converted into a 4-bit binary representation (`bin_str = f"{cell_value:04b}"`):

- `Direction.UP`: checks `bin_str[3] == "0"` (Bit 0)
- `Direction.RIGHT`: checks `bin_str[2] == "0"` (Bit 1)
- `Direction.DOWN`: checks `bin_str[1] == "0"` (Bit 2)
- `Direction.LEFT`: checks `bin_str[0] == "0"` (Bit 3)

### Corridor Graph & Neighbor Traversal

To support pathfinding for the ghost artificial intelligence, `MazeAdapter` transforms the raw bitmask matrix into a navigable corridor graph:

- **`is_inside(x, y)`**: Validates coordinate boundaries (`0 <= x < 15 and 0 <= y < 15`).
- **`is_walkable(x, y)`**: Rejects solid obstacle blocks (`maze[y][x] != 15`).
- **`get_neighbors(x, y)`**: Evaluates all 4 cardinal directions using `can_move()` and returns valid, open adjacent cell coordinates `(nx, ny)`.
- **`get_random_cell()`**: Samples safe, walkable corridors to place entities and pellets without trapping them in obstacles.

### Procedural Progression Across Levels

- **Level 1 (Deterministic)**: Initialized with the `seed` key configured in `config.json` (`MazeGenerator(size=(15, 15), seed=seed)`), guaranteeing reproducible evaluation setups.
- **Levels 2 through 10 (Procedural)**: On each level transition (`start_next_level()`), `MazeAdapter.create_random_maze()` invokes `MazeGenerator` with fresh procedural randomness, providing 10 unique maze layouts per campaign run.

---

## 7. Implementation

### Game Loop & Timing Architecture

The runtime is governed by a **fixed 60 FPS clock** managed in `Renderer.run()`:

```python
dt = self.clock.tick(60) / 1000.0  # Delta-time in seconds
```

- **Single Event Loop**: All window and keyboard events are processed in a unified `pygame.event.get()` loop, delegating to active screen handlers (`main`, `ingame`, `pause`, etc.). This eliminates event swallowing, dropped inputs, and window manager freezes.
- **Independent Engine Ticks**: Pure game simulation updates on discrete accumulators rather than rendering frame rate:
  - **Pac-Man Movement**: Moves every `0.20s` (or `0.10s` under the `SPEED` cheat).
  - **Normal Ghost Movement**: Moves every `0.40s`.
  - **Edible Ghost Movement**: Moves every `0.70s` (simulating sluggish vulnerability).
  - **Level Countdown**: Decrements `time_remaining` continuously by `dt`.
  - **Ready Intermission**: Holds a 4.0-second ready delay at the beginning of each level.

### Movement Physics & Sub-Tile Motion Interpolation

Although the logical engine evaluates collisions on discrete grid coordinates `(grid_x, grid_y)`, the presentation layer (`src/views/sprite_view.py`) achieves arcade-grade fluid motion via **sub-tile linear interpolation**:

```python
# Progress fraction over move duration
progress = track["timer"] / duration  # Clamped to [0.0, 1.0]

# Linear interpolation formula
interp_x = track["prev_x"] + (track["curr_x"] - track["prev_x"]) * progress
interp_y = track["prev_y"] + (track["curr_y"] - track["prev_y"]) * progress

# Pixel translation to screen coordinates
px = int(xoffset + MARGIN + interp_x * TILE_SIZE + TILE_SIZE // 2)
py = int(yoffset + MARGIN + interp_y * TILE_SIZE + TILE_SIZE // 2)
```

- **Input Buffering**: Player directional key presses are buffered in `next_direction`. Pac-Man smoothly executes the requested turn the exact moment a corridor opening appears.

### Collision Handling Matrix

| Interacting Entities                | Condition            | Outcome / State Transition                                                                                                                       |
| :---------------------------------- | :------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------- |
| **Pac-Man vs Pellet**               | Same grid coordinate | Pellet consumed; score increases by `points_per_pacgum`. If pellets reach 0, level is cleared.                                                   |
| **Pac-Man vs Super-Pacgum**         | Same grid coordinate | Super-pacgum consumed; score increases by `points_per_super_pacgum`. Triggers `make_edible(8.0s)` on all non-eaten ghosts.                       |
| **Pac-Man vs Edible Ghost**         | Same grid coordinate | Ghost is devoured; awards `points_per_ghost`; ghost switches to `GhostState.EATEN` (eyes) for 5.0s.                                              |
| **Pac-Man vs Normal Ghost**         | Same grid coordinate | Pac-Man dies; lives decrease by 1; triggers death animation (`dead_timer = 1.3s`); resets entity positions. If `lives == 0`, triggers Game Over. |
| **Pac-Man vs Eaten Ghost**          | Same grid coordinate | Ignored; floating eyes do not harm Pac-Man.                                                                                                      |
| **Pac-Man (Unlimited lives Cheat)** | Any ghost contact    | Ghost cannot harm Pac-Man; collision damage bypassed.                                                                                            |
| **Ghost vs Ghost**                  | Intended next cell   | Active non-eaten ghosts cannot occupy the same cell, preventing sprite stacking and encouraging corridor spread. Eaten eyes can pass freely.     |

### Ghost AI Personalities & State Machine

Every ghost operates within a 4-state finite state machine:

```
         ┌───────────────────┐
         │      NORMAL       │◄─────────────────┐
         └─────────┬─────────┘                  │
                   │ Super-pacgum               │ Reached spawn
                   ▼ consumed                   │ corner
         ┌───────────────────┐                  │
         │      EDIBLE       │                  │
         └─────────┬─────────┘                  │
                   │ Devoured by                │
                   ▼ Pac-Man                    │
         ┌───────────────────┐                  │
         │       EATEN       │──────────────────┘
         └───────────────────┘
```

1. **Blinky (Red - Direct Chaser)**:
   - **Target**: Pac-Man's exact tile `(pacman.grid_x, pacman.grid_y)`.
   - **Algorithm**: Unweighted Breadth-First Search (BFS) computing the globally optimal shortest path across open corridors.
2. **Pinky (Pink) & Clyde (Orange - Corridor Patrollers)**:
   - **Target**: Roam corridors dynamically.
   - **Algorithm**: Continues forward along its current heading. If an obstacle or intersection is reached, chooses randomly among all available open neighbor cells via `random.choice(neighbors)`.
3. **Inky (Cyan - Tactical Ambusher)**:
   - **Target**: Projected intercept tile ahead of Pac-Man.
   - **Algorithm**: Computes a forward vector ray up to 20 tiles ahead of Pac-Man along his current direction vector until encountering a wall, then pathfinds to that lookahead point via BFS.
4. **Frightened / Edible State**:
   - **Behavior**: All active ghosts turn blue and flee.
   - **Evasion Heuristic**: Evaluates all reachable corridor cells in the maze and selects the cell that maximizes Manhattan distance to Pac-Man:
     $$ ext{dist} = |x - ext{pac_x}| + |y - ext{pac_y}|$$
   - Moves along the shortest BFS path toward this evasion target at reduced speed (0.7s per step).
5. **Eaten / Eyes State**:
   - **Behavior**: Upon being eaten, the ghost becomes a pair of disembodied eyes.
   - **Algorithm**: Computes the shortest BFS path back to its dedicated corner spawn base:
     - Blinky: Top-Left `(0, 0)`
     - Pinky: Top-Right `(width - 1, 0)`
     - Inky: Bottom-Left `(0, height - 1)`
     - Clyde: Bottom-Right `(width - 1, height - 1)`
   - Once it reaches the spawn coordinate, it instantly reforms into `NORMAL` state.

### Visual Effects & Shaders

- **Dual-Tone Maze Surface**: Wall boundaries are pre-rendered once onto an off-screen `pygame.Surface` with a dark blue primary stroke and a glowing light-blue highlight stroke, ensuring optimal 60 FPS rendering without CPU overhead.
- **Hardware-Accelerated Box Blur**: When switching to the Pause or Save Highscore screens, the game captures the active frame buffer and applies a real-time 8-pixel box blur (`pygame.transform.box_blur(screen, 8)`), creating a sleek frosted glass effect behind the modal.
- **Directional Animated Sprites**: 4-frame animated sprite loops for Pac-Man and ghosts, automatically flipped and oriented based on the current movement vector.

---

## 8. General Software Architecture

### Architectural Overview

The system follows a strict **Decoupled Engine-Renderer Pattern (Pure Logic vs. Presentation)**:

```
+───────────────────────────────────────────────────────────────────────────+
│                                CLI ENTRY                                  │
│                               pac-man.py                                  │
│         - Validates CLI argument (config.json)                            │
│         - Instantiates Renderer and handles uncaught exceptions           │
+─────────────────────────────────────┬─────────────────────────────────────+
                                      │
                                      ▼
+───────────────────────────────────────────────────────────────────────────+
│                       PRESENTATION LAYER (src/views/)                     │
│                            (Pygame-ce Frontend)                           │
│                                                                           │
│   +───────────────────────────+     +─────────────────────────────────+   │
│   │         Renderer          │     │          SpriteView             │   │
│   │ - Window & 60 FPS Clock   │     │ - Sub-tile linear interpolation │   │
│   │ - Centralized event loop  │     │ - 4-frame sprite animations     │   │
│   │ - Screen State Machine    │     │ - Directional asset flipping    │   │
│   +─────────────┬─────────────+     +─────────────────────────────────+   │
│                 │                                                         │
│                 ▼ Delegates rendering & UI events                         │
│   +───────────────────────────────────────────────────────────────────+   │
│   │  Screens: SrcMainMenu | SrcInGame | ScrPause | ScrHighscores      │   │
│   │           ScrVictory  | ScrGameOver | ScrInstructions | SaveScore │   │
│   +───────────────────────────┬───────────────────────────────────────+   │
│                               │                                           │
│   +───────────────────────────┴─+   +─────────────────────────────────+   │
│   │        MazeRenderer         │   │            HUD View             │   │
│   │ - Dual-tone cached walls    │   │ - Score, Lives, Level, Timer    │   │
│   │ - Bitmask cell rendering    │   │ - Active Cheat Badges           │   │
│   +─────────────────────────────+   +─────────────────────────────────+   │
+─────────────────────────────────────▲─────────────────────────────────────+
                                      │ Read-Only GameStateDT
                                      │
+─────────────────────────────────────┴─────────────────────────────────────+
│                         CORE ENGINE (src/core/)                           │
│                         (Pure Python Logic Core)                          │
│                                                                           │
│   +───────────────────────────+     +─────────────────────────────────+   │
│   │        GameEngine         │ <───┤             Config              │   │
│   │ - Master simulation clock │     │ - Argument parsing & JSON load  │   │
│   │ - Entity collision rules  │     │ - '#' Comment stripping         │   │
│   │ - Level progression (1-10)│     │ - Validation & safe defaults    │   │
│   +───────┬───────────┬───────+     +─────────────────────────────────+   │
│           │           │                                                   │
│           ▼           ▼             +─────────────────────────────────+   │
│   +───────────────+ +───────────────┤        HighscoreManager         │   │
│   │ GhostManager  │ │    Cheats     │ - Persistent JSON top 10 list   │   │
│   │ - BFS Solver  │ │ - SKIP_LEVEL  │ - Alphanumeric name validation  │   │
│   │ - AI behaviors│ │ - SPEED       │ - Safe fallback on missing file │   │
│   │ - 4-state FSM │ │ - GOD_MODE    +─────────────────────────────────+   │
│   +───────┬───────+ │ - FREEZE_GHOST│                                     │
│           │         +───────────────+                                     │
│           ▼                                                               │
│   +───────────────────────────+     +─────────────────────────────────+   │
│   │        MazeAdapter        │ <───┤       mazegenerator.whl         │   │
│   │ - 15x15 grid adapter      │     │ (External A-Maze-ing Package)   │   │
│   │ - Bitmask wall decoding   │     +─────────────────────────────────+   │
│   │ - Graph neighbor queries  │                                           │
│   +───────────────────────────+                                           │
+───────────────────────────────────────────────────────────────────────────+
```

### Module & Class Breakdown

#### 1. Core Logic Modules (`src/core/`)

- **`engine.py` (`GameEngine`)**: The central coordinator. Manages simulation time, advances level state, tests collision rules, processes buffered movement inputs, spawns entities, and generates `GameStateDT`.
- **`config.py` (`Config`)**: Handles command-line arguments, strips hash comments (`#`), deserializes JSON, validates constraints, and provides defaults.
- **`highscores.py` (`HighscoreManager`)**: Loads, validates, sorts, and persists top 10 player records to disk.
- **`maze_adapter.py` (`MazeAdapter`)**: Wraps the external `MazeGenerator` class, translates 4-bit wall bitmasks, and resolves corridor adjacency.
- **`ghost.py` (`GhostManager`)**: Implements ghost state transitions (`NORMAL`, `EDIBLE`, `EATEN`), BFS graph search, lookahead targeting, and fleeing heuristics.
- **`cheats.py` (`Cheats`)**: Manages real-time toggling of developer debug cheat modes (`SKIP_LEVEL`, `FREEZE_GHOSTS`, `UNLIMITED_LIFE`, `SPEED`).
- **`entities.py`**: Declares immutable data transfer classes (`SpriteDT`, `PacgumDT`, `GameStateDT`) and enumerations (`Direction`, `GhostState`, `CheatCode`).

#### 2. Presentation Layer Modules (`src/views/`)

- **`renderer.py` (`Renderer`)**: Manages the Pygame display window, runs the 60 FPS clock, executes the top-level event loop, captures snapshot blurs, and switches active screens.
- **`maze_view.py` (`MazeRenderer`)**: Generates the static cached surface displaying glowing maze walls based on bitmask flags.
- **`sprite_view.py` (`SpriteView`)**: Loads directional sprite sequences and applies sub-tile linear interpolation for smooth motion rendering.
- **`hud_view.py` (`HUD`)**: Renders player score, remaining lives, level badges, countdown timers, and active cheat badges.
- **`screens/`**: Encapsulated UI state controllers for `SrcMainMenu`, `SrcInGame`, `ScrPause`, `ScrGameOver`, `ScrVictory`, `ScrHighscores`, `ScrInstructions`, and `ScrSaveScore`.

### Data Transfer Object (DTO) Boundary

To maintain complete decoupling between game logic and the user interface, the engine communicates with the view solely through read-only **Data Transfer Objects (DTOs)**:

- **`SpriteDT`**: `id`, `grid_x`, `grid_y`, `direction`, `state`.
- **`PacgumDT`**: `grid_x`, `grid_y`, `is_super`.
- **`GameStateDT`**: Encapsulates the entire frame snapshot (level, score, lives, time remaining, entity lists, cheat list, flags).

The presentation layer **never mutates game entities directly**. All player inputs (movement requests, pause toggles, cheat hotkeys) are forwarded to the engine via explicit command methods (`set_player_direction`, `toggle_pause`, `toggle_cheat`).

---

## 9. Project Management

### Methodology & Team Breakdown

The project was executed by **Abdelfatah Laktaoui (`alaktaou`)** and **Mossaab Laktaoui (`mlaktaou`)** using an **Agile / Kanban pair-programming framework**.

To maximize development velocity while avoiding merge conflicts, the codebase was partitioned into two strict functional domains:

```
                  ┌──────────────────────────────────────────────┐
                  │                 42 PAC-MAN                   │
                  └──────────────────────┬───────────────────────┘
                                         │
             ┌───────────────────────────┴───────────────────────────┐
             ▼                                                       ▼
   FRONT-END / PRESENTATION                                BACK-END / CORE LOGIC
         (alaktaou)                                              (mlaktaou)
   • Window & 60 FPS Event Loop                           • Config Parser & Hash Comments
   • Dual-Tone Maze Surface Renderer                      • MazeAdapter Bitmask Decoding
   • Animated Directional Sprites                         • Pure GameEngine Simulation
   • Sub-Tile Motion Interpolation                        • Ghost AI (BFS, Lookahead, Flee)
   • HUD & Screen State Modals                            • Highscore Persistence & Validation
   • Real-Time Frosted Blur Shaders                       • Developer Cheat Suite
   • PyInstaller Packaging                                • Headless Unit Test Suite
```

### Direct Link to Project Management Documentation

Complete project management records, tracking boards, risk matrices, acceptance criteria, and scheduling timelines are maintained in our dedicated documentation directory:

🔗 **[Dedicated Project Management Directory (docs/)](docs/)**

Direct links to specific project management artifacts:

- 📋 **[docs/KANBAN.md](docs/KANBAN.md)**: Sprint task backlog, work-in-progress limits, and completed feature cards.
- ⏱️ **[docs/TIMELINE.md](docs/TIMELINE.md)**: 12-day milestone roadmap and delivery schedule.
- 🛡️ **[docs/RISKS.md](docs/RISKS.md)**: Risk assessment matrix, failure mode effects analysis, and mitigation strategies.
- 🧪 **[docs/TEST_PLAN.md](docs/TEST_PLAN.md)**: Comprehensive verification strategy, manual test matrix, and acceptance criteria.
- 👥 **[docs/TEAM.md](docs/TEAM.md)**: Team organization, architectural ownership, parallel work breakdown, and developer contracts.
- 📐 **[PLAN.md](PLAN.md)**: Master architectural plan and developer contract specifications.

---

_Enjoy playing Pac-Man! For inquiries or evaluation defense, refer to the project repository and documentation._
