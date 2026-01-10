from queue import PriorityQueue
from utils.node import Node
from utils.liquid_sort_game import Beaker, check_game

if __name__ == '__main__':
    # TODO: create an initial state


    # TODO: invoke A* on initial state (problem)

def a_star(problem):
    node = Node(problem, None, None, 0)
    frontier = PriorityQueue()
    frontier.put((node.cost + node.heuristic(), node)) # holds generated but not explored nodes
    explored = set() # holds explored state
    while not frontier.empty():
        f_cur, current = frontier.get()
        if check_game(current.state): return current.generate_solution()
        explored.add(current.state)
        for a in current.generate_actions():
            new = Node(current.generate_state(a), current, a)
            if new.state not in explored and new.state not in [node[1].state for node in frontier]:
                frontier.put((new.cost + new.heuristic(), new))
            elif :
    return False
