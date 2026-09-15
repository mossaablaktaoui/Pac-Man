# 42 Pac-Man: Risk Management Matrix

This document tracks identified architectural, algorithmic, and operational risks, assessing their potential impact and establishing verified mitigation strategies.

---

## Risk Assessment Matrix

| # | Risk Description | Severity | Likelihood | Impact Area | Mitigation Strategy | Status |
| :-: | :--- | :---: | :---: | :--- | :--- | :---: |
| **R1** | **Inverted Maze Bitmasks**<br>The external `mazegenerator` wheel uses bit 0 for North and 1 for wall present, which can be easily misinterpreted. | **Critical** | High | Collision & Navigation | Validated bitmask logic in `src/core/maze_adapter.py`. Mapped 4-bit string directly (`bin_str[3]`=Up, `bin_str[2]`=Right, `bin_str[1]`=Down, `bin_str[0]`=Left). | **Resolved** |
| **R2** | **Coupled Model-View Inheritance**<br>Sprites inheriting from both `pygame.sprite.Sprite` and domain entities prevents headless testing. | **High** | High | Testing & Architecture | Created pure Python dataclasses (`GameStateDT`, `SpriteDT`, `PacgumDT`). Stripped all Pygame imports from `src/core/`. | **Resolved** |
| **R3** | **Pygame Event Loop Contention**<br>Multiple sub-screens calling `pygame.event.get()` and `flip()` drops keystrokes and causes flicker. | **High** | Medium | Window & Input | Centralized event loop in `Renderer.run()`. Screens only implement `handle_event(event)` and `draw()`. | **Resolved** |
| **R4** | **Corrupted Highscore Files**<br>Modified, truncated, or invalid highscore JSON crashing the application on startup. | **Medium** | High | Persistence | Implemented defensive validation in `HighscoreManager`. Validates types, non-negative scores, 10-char names, and handles missing files gracefully. | **Resolved** |
| **R5** | **CLI Tracebacks on Bad Input**<br>Invalid arguments or non-existent files raising unhandled Python exceptions during evaluation. | **Medium** | High | CLI & Grading | Wrapped entrypoint in `pac-man.py` with custom `ConfigError` handling to print clean messages without stack traces. | **Resolved** |
| **R6** | **Ghost Congestion & Trapping**<br>Multiple ghosts piling up in the same corridor cell or corner, blocking entity paths. | **Medium** | Medium | Gameplay & AI | Enforced collision check preventing active non-eaten ghosts from entering occupied cells, while allowing eaten eyes to pass. | **Resolved** |
| **R7** | **Frame Rate Jitter & Stutter**<br>Recalculating maze walls or running BFS every single frame causing framerate dips below 60 FPS. | **Medium** | Low | Performance | Pre-rendered maze onto a cached `pygame.Surface`. Throttled ghost BFS updates to discrete timer ticks (0.4s / 0.7s). | **Resolved** |
| **R8** | **Strict Mypy Typing Failures**<br>Dynamic Pygame surfaces or missing types causing `mypy --strict` to fail during evaluation. | **Low** | Medium | Code Quality | Comprehensive type hints across all 29 source files using modern Python typing (`pygame.Surface`, DTOs, Enums). | **Resolved** |
