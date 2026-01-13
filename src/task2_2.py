import subprocess
import os
import shutil
import time
import re

from utils.liquid_sort_game import Beaker
from src.problem_generator import generate_problem_pddl

# --- CONFIG ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DOMAIN_DIR = os.path.join(BASE_DIR, "..", "pddl")
RESULT_DIR = os.path.join(BASE_DIR, "..", "result")

os.makedirs(DOMAIN_DIR, exist_ok=True)
os.makedirs(RESULT_DIR, exist_ok=True)

DOMAIN_FILE = "domain.pddl"
DOMAIN_PATH = os.path.join(DOMAIN_DIR, DOMAIN_FILE)

PROBLEM_FILE = "problem.pddl"
PROBLEM_PATH = os.path.join(DOMAIN_DIR, PROBLEM_FILE)

PLAN_FILE = "sas_plan"
PLAN_PATH = os.path.join(RESULT_DIR, PLAN_FILE)
# to update the path depending on your fast_downward.py location
PLANNER_EXE = "/home/sharpeii/fast_downward/fast-downward.py"
PLANNER_OPTIONS = ["--search", "astar(blind())"]



def solve_with_pddl(initial_state):
    """
    Generates the problem given the initial state and solve it using fast_downward.
    :param initial_state: A list of beakers objects.
    """
    metrics = {
        'time': 0.0,
        'expanded': 0,
        'generated': 0,
        'cost': 0,
        'solved': False
    }
    print("--- 1. Generating problem.pddl ---")
    try:
        pddl_str = generate_problem_pddl(initial_state)
        with open(PROBLEM_PATH, "w") as f:
            f.write(pddl_str)
        print(f"File '{PROBLEM_FILE}' created.")
    except Exception as e:
        print(f"[ERROR] Error in PDDL generation: {e}")
        return

    print("\n--- 2. Executing problem.pddl ---")

    # removing old files
    if os.path.exists(PLAN_PATH):
        os.remove(PLAN_PATH)
    if os.path.exists("sas_plan"):
        os.remove("sas_plan")

    # genereting command
    cmd = [PLANNER_EXE, DOMAIN_PATH, PROBLEM_PATH] + PLANNER_OPTIONS

    print(f"Executing: {' '.join(cmd)}")

    start_time = time.time() # starting timer
    try:
        # running the command
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True
        )

        end_time = time.time() # end timer
        """ 
        # running command with every output
        with subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True
        ) as p:
            # reads every output from the planner
            for line in p.stdout:
                print(line, end='')"""

        metrics['time'] = end_time - start_time
        output_log = result.stdout

        # --- Parsing Fast Downward log in search of data ---

        # searching expanded metric
        exp_match = re.search(r"Expanded (\d+) state\(s\)", output_log)
        if exp_match:
            metrics['expanded'] = int(exp_match.group(1))

        # searching generated metric
        gen_match = re.search(r"Generated (\d+) state\(s\)", output_log)
        if gen_match:
            metrics['generated'] = int(gen_match.group(1))

        # switch between p and result for the different outputs
        if result.returncode != 0:
            print(f"Planner has error code: {result.returncode}")
            # not return because it may have found the plan still depending on which error code

    except FileNotFoundError:
        print(f"[ERROR] Executable not found at {cmd[0]}")
        return metrics

    # moving the output from cwd to result dir
    if os.path.exists("sas_plan"):
        shutil.move("sas_plan", PLAN_PATH)
        metrics['solved'] = True


    print("\n--- 3. Reading the plan ---")
    if os.path.exists(PLAN_PATH):
        with open(PLAN_PATH, "r") as f:
            lines = f.readlines()

        step = 1
        for line in lines:
            if line.startswith(";"):
                print(f"Total cost of the plan: {line.strip()}")
                metrics['cost'] = int(line.split("=")[1].strip())
                continue

            # cleaning the action line
            clean_line = line.strip().replace("(", "").replace(")", "")
            parts = clean_line.split()
            action_name = parts[0]

            if "pour" in action_name:
                src = parts[1]
                dst = parts[2]
                color = parts[3]
                print(f"{step}. Pour {color} from {src} to {dst} ({action_name})")
                step += 1
            else:
                print(f"{step}. {clean_line}")
    else:
        print("No file generated. The problem is not resolvable or the planner has failed.")

    return metrics


if __name__ == "__main__":
    # the definition of the domain.pddl forces capacity=4
    initial_state = [
        Beaker(capacity=4, content=[0, 1, 2, 3]),
        Beaker(capacity=4, content=[1, 0, 4, 1]),
        Beaker(capacity=4, content=[0, 3, 0, 2]),
        Beaker(capacity=4, content=[4, 3, 1, 4]),
        Beaker(capacity=4, content=[2, 4, 3, 2]),
        Beaker(capacity=4, content=[]),
        Beaker(capacity=4, content=[])
    ]

    solve_with_pddl(initial_state)