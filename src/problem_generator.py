import os

from utils.liquid_sort_game import Beaker


def generate_problem_pddl(beakers: list[Beaker], problem_name="liquidsort_task"):
    """
    Generates a problem.pddl file from the init state of beakers.
    """

    if not beakers:
        raise ValueError("Empty list of beakers passed.")

    # every beaker has the same capacity (as per standard rules)
    capacity = beakers[0].capacity
    num_beakers = len(beakers)

    # finding all the different colors
    unique_colors = set()
    for b in beakers:
        for color_code in b.content:
            unique_colors.add(color_code)

    # sorting them to make the output deterministic
    sorted_colors = sorted(list(unique_colors))

    # --- DEFINTION OF PDDL NAMES ---
    # Beakers: b0, b1, ...
    # Livelli: l0 (fondo), l1, l2, ..., l_capacity
    # Colori: c0, c1, ... (based on the actual value in the content)

    beaker_names = [f"b{i}" for i in range(num_beakers)]
    level_names = [f"l{i}" for i in range(capacity + 1)]  # from l0 to l4

    # starting the construction of the pddl string
    pddl = f"(define (problem {problem_name})\n"
    pddl += "  (:domain LiquidSort)\n"

    # defining :objects
    pddl += "  (:objects\n"
    pddl += "    " + " ".join(beaker_names) + " - beaker\n"

    # converting the colors in strings for each color c0, c1...
    color_names = [f"c{c}" for c in sorted_colors]
    pddl += "    " + " ".join(color_names) + " - color\n"

    pddl += "    " + " ".join(level_names) + " - level\n"
    pddl += "  )\n\n"

    # 4. defining :init
    pddl += "  (:init\n"
    pddl += "    ; --- Geometry of the game (static) ---\n"
    pddl += "    (is-bottom l0)\n"
    for i in range(capacity):
        pddl += f"    (succ l{i} l{i + 1})\n"

    pddl += "\n    ; --- Defining initial state of the beakers ---\n"

    for i, beaker in enumerate(beakers):
        b_name = f"b{i}"
        current_height = len(beaker.content)

        # Mapping:
        # Python list index 0 -> PDDL l1
        # Python list index 1 -> PDDL l2
        for lvl_idx, color_val in enumerate(beaker.content):
            pddl_level = f"l{lvl_idx + 1}"
            color_name = f"c{color_val}"
            pddl += f"    (has-color {b_name} {pddl_level} {color_name})\n"

        # defining the top
        # top is the len of the content of beaker
        top_lvl = f"l{current_height}"
        pddl += f"    (top {b_name} {top_lvl})\n"

    pddl += "  )\n\n"

    # defining :goal
    # logic: for all color there must exist a full beaker of that color.
    pddl += "  (:goal (and\n"

    for color_val in sorted_colors:
        c_name = f"c{color_val}"
        pddl += f"    ; Goal for color {c_name}\n"
        pddl += "    (or\n"

        # generate the or clause for each beaker with color color_val
        for b_name in beaker_names:
            conditions = []
            # adding a fullness condition to every level of the beaker
            for k in range(1, capacity + 1):
                conditions.append(f"(has-color {b_name} l{k} {c_name})")

            # unite the conditions for this beaker and color
            beaker_goal = "      (and " + " ".join(conditions) + ")"
            pddl += f"{beaker_goal}\n"

        pddl += "    )\n"

    pddl += "  ))\n"
    pddl += ")"

    return pddl


if __name__ == "__main__":
    # example from "DOABLE STARTING STATES" (look at a_star.py)
    test_problem = [
        Beaker(capacity=4, content=[0, 1, 1, 0]),
        Beaker(capacity=4, content=[2, 2, 1, 3]),
        Beaker(capacity=4, content=[4, 1, 0, 3]),
        Beaker(capacity=4, content=[2, 5, 4, 4]),
        Beaker(capacity=4, content=[5, 3, 4, 3]),
        Beaker(capacity=4, content=[0, 2, 5, 5]),
        Beaker(capacity=4, content=[]),
        Beaker(capacity=4, content=[])
    ]

    # generating
    try:
        pddl_content = generate_problem_pddl(test_problem)

        # saving in file
        filename = "problem.pddl"
        path = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(path, "..", "pddl", filename)
        with open(path, "w") as f:
            f.write(pddl_content)

        #print(f"File '{filename}' generated.")

    except Exception as e:
        print(f"Error: {e}")

