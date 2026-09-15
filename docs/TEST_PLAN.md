# 42 Pac-Man: Verification & Test Plan

Comprehensive test specification covering automated unit testing, manual acceptance test procedures, and peer defense verification checklists.

---

## 1. Automated Verification Suite

### 1.1 Linting & Type Safety

The codebase must pass all static analysis checks with zero warnings or errors:

```bash
# Standard linting and typing
make lint

# Strict verification mode
make lint-strict
```

- **Flake8**: Validates PEP 8 styling, naming conventions, import ordering, and line lengths.
- **Mypy**: Validates static type coverage across all 29 source files (`--disallow-untyped-defs`, `--check-untyped-defs`, `--warn-return-any`).

### 1.2 Core Domain Headless Tests (`tests/`)

Tests in `tests/` execute against the pure Python core without initializing graphical display surfaces:

- **`test_config.py`**:
  - Missing file creates default configuration.
  - Lines starting with `#` are stripped cleanly.
  - Missing or invalid keys clamp to default values with warnings.
  - Rejection of non-JSON extensions and multi-argument CLI invocations.
- **`test_highscores.py`**:
  - Missing file initializes empty score list.
  - Sorting orders entries in descending score order.
  - List strictly clamps to top 10 records.
  - Name validation rejects strings > 10 characters or containing symbols.
- **`test_maze_adapter.py`**:
  - Validates 4-bit wall bitmasks for North, East, South, West.
  - Confirms solid obstacles (`15`) are impassable.
  - Verifies corridor graph adjacency (`get_neighbors`).
- **`test_engine.py`**:
  - Pac-Man grid movement and corridor collision checks.
  - Pellet consumption, score accrual, and level clearing.
  - Life deduction on ghost collision and game over trigger.
  - Cheat code toggles and state mutations.

---

## 2. Manual Acceptance Test Matrix

|  Test ID  | Feature Area       | Test Scenario / Input                         | Expected Result                                                  | Pass/Fail |
| :-------: | :----------------- | :-------------------------------------------- | :--------------------------------------------------------------- | :-------: |
| **TC-01** | **CLI Launch**     | `python pac-man.py` (no args)                 | Gracefully exits with error message; no raw traceback.           |   PASS    |
| **TC-02** | **CLI Launch**     | `python pac-man.py invalid.txt`               | Rejects non-JSON extension with error message.                   |   PASS    |
| **TC-03** | **CLI Launch**     | `python pac-man.py config.json`               | Launches window in 1920x1080 resolution at 60 FPS.               |   PASS    |
| **TC-04** | **Config Parser**  | Modify `config.json` with invalid `lives: -5` | Emits stdout warning; clamps lives to default `3`.               |   PASS    |
| **TC-05** | **Config Parser**  | Add `# comment line` inside `config.json`     | Strips comment cleanly and parses valid JSON.                    |   PASS    |
| **TC-06** | **Movement**       | Press `W`/`Up` into an open corridor          | Pac-Man smoothly turns and moves upward.                         |   PASS    |
| **TC-07** | **Movement**       | Press `D`/`Right` into a solid wall           | Pac-Man continues in current direction; no clipping.             |   PASS    |
| **TC-08** | **Pellets**        | Pac-Man enters tile containing Pacgum         | Pellet disappears; score increases by `points_per_pacgum`.       |   PASS    |
| **TC-09** | **Super-Pacgum**   | Pac-Man consumes corner Super-pacgum          | Ghosts turn blue (Edible state) for 8.0s; evade Pac-Man.         |   PASS    |
| **TC-10** | **Ghost Eat**      | Pac-Man touches edible ghost                  | Ghost turns to eyes; returns to base; awards `points_per_ghost`. |   PASS    |
| **TC-11** | **Ghost Touch**    | Pac-Man touches normal ghost                  | Pac-Man dies; lives decrement by 1; death animation plays.       |   PASS    |
| **TC-12** | **Game Over**      | Lives decrement to 0                          | Transitions to Save Score modal; prompts for name input.         |   PASS    |
| **TC-13** | **Pause Modal**    | Press `P` key during gameplay                 | Gameplay freezes; screen blurs; pause modal appears.             |   PASS    |
| **TC-14** | **Cheats**         | Press `K` (Skip Level)                        | Clears current level; advances to next procedural maze.          |   PASS    |
| **TC-15** | **Cheats**         | Press `L` (Speed Boost)                       | Pac-Man moves twice as fast (0.10s step delay).                  |   PASS    |
| **TC-16** | **Cheats**         | Press `H` (Unlimited lives)                   | Ghost contact causes zero damage to Pac-Man.                     |   PASS    |
| **TC-17** | **Cheats**         | Press `J` (Freeze Ghosts)                     | All ghosts freeze in place while Pac-Man moves freely.           |   PASS    |
| **TC-18** | **Highscore Save** | Enter 10-char name on Save Score screen       | Record saved to `highscores.json`; viewable in Leaderboard.      |   PASS    |
| **TC-19** | **Victory**        | Clear all 10 levels                           | Victory screen displays congratulations and final score.         |   PASS    |
