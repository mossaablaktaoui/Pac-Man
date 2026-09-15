_This project was created as part of the 42 curriculum by alaktaou and mlaktaou._

# Pac-Man: Ghosts! More Ghosts!

[![Language](https://img.shields.io/badge/Language-Python%203.10%2B-blue.svg)](https://www.python.org/)
[![Engine](https://img.shields.io/badge/Engine-Pygame--ce-green.svg)](https://pyga.me/)
[![Type Checker](https://img.shields.io/badge/Type%20Check-mypy%20strict-brightgreen.svg)](https://mypy-lang.org/)
[![Linter](https://img.shields.io/badge/Linter-flake8-yellow.svg)](https://flake8.pycqa.org/)

An arcade-accurate recreation of **Pac-Man** featuring procedural maze generation, distinct ghost AI behaviors, 10-level progression, evaluation cheats, and a decoupled Model-View-Controller architecture.

---

## 1. Description

This project recreates the classic arcade game **Pac-Man** using **Python 3.10+** and **Pygame-ce**. 

Instead of a fixed board, the game generates procedural 15x15 mazes for each level using the external `mazegenerator` wheel. The player navigates corridors, eats pellets and super-pellets, and avoids 4 distinct ghost AI personalities (**Blinky**, **Pinky**, **Inky**, and **Clyde**).

---

## 2. Instructions

### Prerequisites
- **Python 3.10+**
- **uv** (recommended) or standard `pip` / `venv`

### Installation & Run

```bash
# Clone and enter repository
git clone <repository_url>
cd Pac-man

# Install dependencies and the A-Maze-ing wheel
make install

# Launch the game with default config
make run

# Or launch directly via CLI (requires exactly 1 JSON argument)
python3 pac-man.py config.json
```

### Controls & Cheats

| Key | Action |
| :--- | :--- |
| **`W` / `Up`** | Move Up |
| **`S` / `Down`** | Move Down |
| **`A` / `Left`** | Move Left |
| **`D` / `Right`** | Move Right |
| **`P`** | Pause / Resume |
| **`R`** | Restart Game |
| **`Q`** | Return to Menu |
| **`ESC`** | Quit Game |
| **`K`** | **Cheat:** Skip Level |
| **`L`** | **Cheat:** 2x Speed Boost |
| **`H`** | **Cheat:** Unlimited Lives |
| **`J`** | **Cheat:** Freeze Ghosts |

---

## 3. Resources & AI Usage

- **References**: Classic Pac-Man dossier and official Pygame-ce documentation.
- **AI Disclosure**: Used AI tools for debugging, code review, structuring documentation, and Pygame animation techniques.

---

## 4. Configuration

The game accepts a `.json` configuration file via CLI. Lines starting with `#` are treated as comments. Missing or invalid values automatically fall back to safe defaults without crashing.

| Key | Default | Description |
| :--- | :---: | :--- |
| `highscore_filename` | `"highscores.json"` | Path to save highscores |
| `lives` | `3` | Initial lives |
| `pacgum` | `42` | Pellet count (min 4 for super pellets) |
| `points_per_pacgum` | `120` | Points per normal pellet |
| `points_per_super_pacgum` | `50` | Points per super pellet |
| `points_per_ghost` | `200` | Points per eaten ghost |
| `seed` | `42` | Random seed for Level 1 maze |
| `level_max_time` | `120` | Level countdown timer (seconds) |

---

## 5. Highscores

Persistent top-10 leaderboard saved to `highscores.json`:
- **Validation**: Names are limited to 10 alphanumeric characters.
- **Resilience**: If the file is missing or corrupted, the game initializes an empty leaderboard instead of crashing.

---

## 6. Maze Generation

The game wraps the external `mazegenerator` wheel through `MazeAdapter` (`src/core/maze_adapter.py`):
- **Wall Bitmasks**: Each cell is an integer (1=North, 2=East, 4=South, 8=West, 15=Solid Block).
- **Levels**: Level 1 uses the configured `seed`; levels 2–10 generate fresh random mazes.

---

## 7. Ghost AI & Mechanics

All ghosts operate on a 4-state machine (**NORMAL**, **EDIBLE**, **FLASHING**, **EATEN**):
- **Blinky (Red)**: Chases Pac-Man using shortest-path BFS.
- **Pinky & Clyde**: Roam corridors and make pseudo-random turns at intersections.
- **Inky (Cyan)**: Intercepts by targeting points ahead of Pac-Man.
- **Edible / Fleeing**: Triggered by super-pellets; ghosts flee away from Pac-Man at reduced speed.
- **Eaten (Eyes)**: Returns to corner spawn point before reforming.

---

## 8. Architecture

The codebase strictly decouples game logic from graphics:
- **`src/core/` (Back-End)**: Pure Python logic (movement, collisions, AI, highscores). Contains zero Pygame code, enabling fast, headless unit tests.
- **`src/views/` (Front-End)**: Pygame-ce presentation layer (window management, 60 FPS clock, sub-tile motion interpolation, sprite animations, HUD, and screen routing).
- **Data Boundary**: Engine communicates state to views using read-only Data Transfer Objects (`GameStateDT`).

---

## 9. Project Management

Work was divided between **`alaktaou`** (Front-End / Presentation) and **`mlaktaou`** (Back-End / Core Logic) using an Agile/Kanban workflow.

Complete evidence, timelines, test matrices, and risk plans are documented in the **[`docs/`](docs/)** directory:
- 📋 [docs/KANBAN.md](docs/KANBAN.md) - Work breakdown and task status
- ⏱️ [docs/TIMELINE.md](docs/TIMELINE.md) - Project schedule and milestones
- 🛡️ [docs/RISKS.md](docs/RISKS.md) - Risk analysis and mitigations
- 👥 [docs/TEAM.md](docs/TEAM.md) - Team organization and responsibilities