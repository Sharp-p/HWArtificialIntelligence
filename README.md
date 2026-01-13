# AI Homework - Water Sort Puzzle Solver

This repository contains the implementation of two AI techniques to solve the Water Sort Puzzle, as part of the Artificial Intelligence course (AY 2025-26).

## Project Structure

*   **`src/`**: Contains the source code.
    *   `a_star.py`: **Task 2.1** - Custom A* implementation in Python.
    *   `task2_2.py`: **Task 2.2** - Orchestrator for PDDL generation and Fast Downward execution.
    *   `problem_generator.py`: Generates the `problem.pddl` file dynamically from a game state.
    *   `experiments.py`: **Task 3** - Runs benchmarks on both algorithms and saves data to CSV.
    *   `plot_results.py`: Generates visualization plots from the CSV data.
    *   `pddl/domain.pddl`: The PDDL domain definition (Chunking model).
*   **`utils/`**: Helper classes (Node, Beaker) for game logic.
*   **`result/`**: Contains the output metrics (`.csv`) and plots (`.png`).

## Prerequisites

1.  **Python 3.8+**
2.  **Fast Downward Planner**: You must have Fast Downward installed or built on your machine. [Official Instructions](https://www.fast-downward.org/ObtainingAndRunning).
3.  **Python Libraries**:
    ```bash
    pip install pandas matplotlib seaborn
    ```

## Configuration

**Crucial Step:** Before running the code, you must tell the script where your Fast Downward executable is located.

1.  Open `src/task2_2.py`.
2.  Find the `PLANNER_EXE` variable.
3.  Change the path to your local `fast-downward.py` file.

Example:
```python
# src/task2_2.py
PLANNER_EXE = "/home/your_username/fast_downward/fast-downward.py"
