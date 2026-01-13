import heapq
import time

from utils.node import Node
from utils.liquid_sort_game import Beaker, check_game


def a_star(problem):
    metrics = {
        'time': 0.0,
        'expanded': 0,
        'generated': 0,
        'cost': 0,
        'solved': False
    }
    node = Node(problem, None, None, 0)
    frontier = []
    heapq.heappush(frontier, (node.cost + node.heuristic(), node)) # holds generated but not explored nodes
    explored = set() # holds explored state
    start = time.time()
    while frontier:
        # get the node with the highest priority (lowest eval)
        f_cur, current = heapq.heappop(frontier)
        # check if node.state is a solution
        if check_game(current.state):
            metrics['time'] = time.time() - start
            metrics['expanded'] = len(explored)
            metrics['generated'] = len(frontier)
            metrics['cost'] = current.cost
            metrics['solved'] = True
            return current.generate_solution(), metrics

        explored.add(tuple(beaker.to_tuple() for beaker in current.state))
        for a in current.generate_actions():
            new = Node(current.generate_state(a), current, a)
            print("New state generated:", new)
            if (tuple(beaker.to_tuple() for beaker in new.state) not in explored
                    and new.state not in [couple[1].state for couple in frontier]):
                heapq.heappush(frontier, (new.eval, new))
            else:
                handle_duplicates(new, frontier)
    return False, metrics

def handle_duplicates(new, frontier) -> None:
    """
    Checks for the presence of duplicate states with greater cost than the new generated node.
    If so, modifies the frontier, switching the two nodes.
    :param new: New generated node, with the state that is being checked in the frontier.
    :param frontier: A min-heap of not yet explored states (nodes).
    :return: None
    """
    for val in list(frontier):
        if new.state == val[1].state and new.cost < val[1].cost:
            frontier.remove(val)
            frontier.append((new.eval, new))
            heapq.heapify(frontier)
            break

if __name__ == '__main__':
    initial_state = [
        Beaker(capacity=4, content=[0, 1, 2, 3]),
        Beaker(capacity=4, content=[1, 0, 4, 1]),
        Beaker(capacity=4, content=[0, 3, 0, 2]),
        Beaker(capacity=4, content=[4, 3, 1, 4]),
        Beaker(capacity=4, content=[2, 4, 3, 2]),
        Beaker(capacity=4, content=[]),
        Beaker(capacity=4, content=[])
    ]

    solution = a_star(initial_state)
    print()

    for i in range(len(solution)):
        print("State ", i + 1, ": ", solution[i])

""" VARIOUS STARTING STATE
============= EASY STARTING STATES =======================
        Beaker(capacity=2, content=[0, 1]),
        Beaker(capacity=2, content=[1, 0]),
        Beaker(capacity=2, content=[])
        
........................................................................

        Beaker(capacity=4, content=[0, 1, 2, 3]),
        Beaker(capacity=4, content=[3, 0, 1, 2]),
        Beaker(capacity=4, content=[2, 3, 0, 1]),
        Beaker(capacity=4, content=[1, 2, 3, 0]),
        Beaker(capacity=4, content=[]),
        Beaker(capacity=4, content=[])
        
============= DOABLE STARTING STATES ======================================
        
        Beaker(capacity=4, content=[0, 1, 1, 0]),
        Beaker(capacity=4, content=[2, 2, 1, 3]),
        Beaker(capacity=4, content=[4, 1, 0, 3]),
        Beaker(capacity=4, content=[2, 5, 4, 4]),
        Beaker(capacity=4, content=[5, 3, 4, 3]),
        Beaker(capacity=4, content=[0, 2, 5, 5]),
        Beaker(capacity=4, content=[]),
        Beaker(capacity=4, content=[])
        
.............................................................................

        Beaker(capacity=4, content=[0, 0, 1, 2]),
        Beaker(capacity=4, content=[3, 2, 4, 5]),
        Beaker(capacity=4, content=[0, 5, 6, 6]),
        Beaker(capacity=4, content=[5, 6, 0, 4]),
        Beaker(capacity=4, content=[1, 3, 6, 3]),
        Beaker(capacity=4, content=[5, 1, 1, 3]),
        Beaker(capacity=4, content=[2, 2, 4, 4]),
        Beaker(capacity=4, content=[]),
        Beaker(capacity=4, content=[])

============= STATE SPACE EXPLODES (many duplicates at greater depths, longer execution, initial configuration dependant) ======================================

        Beaker(capacity=4, content=[0, 1, 2, 3]),
        Beaker(capacity=4, content=[1, 0, 4, 1]),
        Beaker(capacity=4, content=[0, 3, 0, 2]),
        Beaker(capacity=4, content=[4, 3, 1, 4]),
        Beaker(capacity=4, content=[2, 4, 3, 2]),
        Beaker(capacity=4, content=[]),       
        Beaker(capacity=4, content=[])
        
...........................................................
        
        Beaker(capacity=4, content=[0, 1, 2, 3]),
        Beaker(capacity=4, content=[0, 2, 4, 2]),
        Beaker(capacity=4, content=[1, 5, 5, 4]),
        Beaker(capacity=4, content=[0, 1, 3, 4]),
        Beaker(capacity=4, content=[4, 3, 5, 5]),
        Beaker(capacity=4, content=[1, 3, 0, 2]),
        Beaker(capacity=4, content=[]),
        Beaker(capacity=4, content=[])
        
............................................................

        Beaker(capacity=4, content=[0, 0, 1, 2]),
        Beaker(capacity=4, content=[3, 4, 4, 5]),
        Beaker(capacity=4, content=[2, 3, 1, 2]),
        Beaker(capacity=4, content=[0, 3, 4, 4]),
        Beaker(capacity=4, content=[3, 0, 5, 1]),
        Beaker(capacity=4, content=[5, 1, 5, 2]),
        Beaker(capacity=4, content=[]),
        Beaker(capacity=4, content=[])
        
"""