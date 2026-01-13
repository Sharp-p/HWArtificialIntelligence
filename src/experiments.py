import os
import pandas as pd
from src.a_star import a_star
from src.task2_2 import solve_with_pddl
from utils.liquid_sort_game import Beaker

if __name__ == "__main__":
    # --- Defining test instances ---
    # same init state as in a_star.py
    test_cases = [
        {
            "name": "EASY_1",
            "state": [
                Beaker(capacity=4, content=[0, 0, 0]),
                Beaker(capacity=4, content=[0]),
            ]
        },
        {
            "name": "EASY_2",
            "state": [
                Beaker(capacity=2, content=[0, 1]),
                Beaker(capacity=2, content=[1, 0]),
                Beaker(capacity=2, content=[])
            ]
        },
        {
            "name": "EASY_3",
            "state": [
                Beaker(capacity=4, content=[0, 0]),
                Beaker(capacity=4, content=[1, 1, 1]),
                Beaker(capacity=4, content=[0, 0, 1]),
            ]
        },
        {
            "name": "EASY_4",
            "state": [
                Beaker(capacity=4, content=[0, 1, 2, 3]),
                Beaker(capacity=4, content=[3, 0, 1, 2]),
                Beaker(capacity=4, content=[2, 3, 0, 1]),
                Beaker(capacity=4, content=[1, 2, 3, 0]),
                Beaker(capacity=4, content=[]),
                Beaker(capacity=4, content=[])
            ]
        },
        {
            "name": "DOABLE_1",
            "state": [
                Beaker(capacity=4, content=[0, 1, 1, 0]),
                Beaker(capacity=4, content=[2, 3, 3, 2]),
                Beaker(capacity=4, content=[2, 1, 3, 0]),
                Beaker(capacity=4, content=[3, 1, 2, 0]),
                Beaker(capacity=4, content=[]),
                Beaker(capacity=4, content=[]),
            ]
        },
        {
            "name": "DOABLE_2",
            "state": [
                Beaker(capacity=4, content=[0, 0, 1, 2]),
                Beaker(capacity=4, content=[0, 3, 1, 2]),
                Beaker(capacity=4, content=[3, 2, 3, 1]),
                Beaker(capacity=4, content=[2, 3, 1, 0]),
                Beaker(capacity=4, content=[]),
                Beaker(capacity=4, content=[]),
            ]
        },
        {
            "name": "DOABLE_3",
            "state": [
                Beaker(capacity=4, content=[0, 1, 2, 2]),
                Beaker(capacity=4, content=[2, 3, 4, 1]),
                Beaker(capacity=4, content=[4, 0, 2, 0]),
                Beaker(capacity=4, content=[3, 4, 1, 0]),
                Beaker(capacity=4, content=[3, 1, 3, 4]),
                Beaker(capacity=4, content=[]),
                Beaker(capacity=4, content=[]),
            ]
        },
        {
            "name": "DOABLE_4",
            "state": [
                Beaker(capacity=4, content=[0, 1, 2, 3]),
                Beaker(capacity=4, content=[1, 3, 0, 4]),
                Beaker(capacity=4, content=[3, 0, 2, 2]),
                Beaker(capacity=4, content=[3, 4, 1, 4]),
                Beaker(capacity=4, content=[0, 1, 4, 2]),
                Beaker(capacity=4, content=[]),
                Beaker(capacity=4, content=[]),
            ]
        },
        {
            "name": "DOABLE_5",
            "state": [
                Beaker(capacity=4, content=[0, 1, 2, 3]),
                Beaker(capacity=4, content=[1, 0, 4, 1]),
                Beaker(capacity=4, content=[0, 3, 0, 2]),
                Beaker(capacity=4, content=[4, 3, 1, 4]),
                Beaker(capacity=4, content=[2, 4, 3, 2]),
                Beaker(capacity=4, content=[]),
                Beaker(capacity=4, content=[]),
            ]
        },

    ]

    data_records = []

    # Header for table
    print(f"\n{'=' * 95}")
    print(
        f"{'PROBLEM':<12} | {'ALG':<8} | {'SOLVED':<6} | {'TIME (s)':<10} | {'EXPANDED':<10} | {'GENERATED':<10} | {'COST':<5}")
    print(f"{'=' * 95}")

    for case in test_cases:
        problem_name = case["name"]
        initial_state = case["state"]

        # ---------------------------
        # 1. TEST PYTHON A* (Task 2.1)
        # ---------------------------
        print(f"Running A* on {problem_name}...", end="\r")

        # Executing A*
        try:
            solution, metrics_py = a_star(initial_state)

            # saving data
            data_records.append({
                "Problem": problem_name,
                "Algorithm": "Py A*",
                "Solved": metrics_py['solved'],
                "Time": metrics_py['time'],
                "Expanded": metrics_py['expanded'],
                "Generated": metrics_py['generated'],
                "Cost": metrics_py['cost']
            })

            print(f"{problem_name:<12} | {'Py A*':<8} | {str(metrics_py['solved']):<6} | "
                  f"{metrics_py['time']:<10.4f} | {metrics_py['expanded']:<10} | "
                  f"{metrics_py['generated']:<10} | {metrics_py['cost']:<5}")

        except Exception as e:
            print(f"{problem_name:<12} | {'Py A*':<8} | ERROR  | {str(e)}")

        # ---------------------------
        # 2. TEST PDDL PLANNER (Task 2.2)
        # ---------------------------
        print(f"Running PDDL on {problem_name}...", end="\r")

        metrics_pddl = solve_with_pddl(initial_state)

        # saving data
        data_records.append({
            "Problem": problem_name,
            "Algorithm": "PDDL",
            "Solved": metrics_pddl['solved'],
            "Time": metrics_pddl['time'],
            "Expanded": metrics_pddl['expanded'],
            "Generated": metrics_pddl['generated'],
            "Cost": metrics_pddl['cost']
        })

        print(f"{'':<12} | {'PDDL':<8} | {str(metrics_pddl['solved']):<6} | "
              f"{metrics_pddl['time']:<10.4f} | {metrics_pddl['expanded']:<10} | "
              f"{metrics_pddl['generated']:<10} | {metrics_pddl['cost']:<5}")

        print("-" * 95)

    # --- Generating CSV ---
    df = pd.DataFrame(data_records)
    csv_filename = "../result/experiment_results.csv"


    os.makedirs(os.path.dirname(csv_filename), exist_ok=True)

    df.to_csv(csv_filename, index=False)
    print(f"\nResults saved to {csv_filename}")

    print("\n--- SUMMARY ---")
    print(df.groupby(["Algorithm"])[["Time", "Expanded"]].mean())