import heapq
from utils.node import Node
from utils.liquid_sort_game import Beaker, check_game


def a_star(problem):
    node = Node(problem, None, None, 0)
    frontier = []
    heapq.heappush(frontier, (node.cost + node.heuristic(), node)) # holds generated but not explored nodes
    explored = set() # holds explored state
    while frontier:
        # get the node with the highest priority (lowest eval)
        f_cur, current = heapq.heappop(frontier)
        # check if node.state is a solution
        if check_game(current.state): return current.generate_solution()

        explored.add(tuple(beaker.to_tuple() for beaker in current.state))
        for a in current.generate_actions():
            new = Node(current.generate_state(a), current, a)
            if (tuple(beaker.to_tuple() for beaker in new.state) not in explored
                    and new.state not in [couple[1].state for couple in frontier]):
                heapq.heappush(frontier, (new.eval, new))
            else:
                handle_duplicates(new, frontier)
    return False

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
        Beaker(capacity=2, content=[0, 1]),
        Beaker(capacity=2, content=[1, 0]),
        Beaker(capacity=2, content=[])
    ]

    solution = a_star(initial_state)

    for i in range(len(solution)):
        print("Stato ", i + 1, ": ", solution[i])

