from liquid_sort_game import check_action
import copy

class Node:
    def __init__(self, state, parent, action, cost=None):
        self.state = state
        self.parent = parent
        self.action = action
        self.cost = cost if cost is not None else self.parent.cost + 1 # each move in the game has unitary cost
        self.eval = # TODO: add evaluation of node UPDATE a_star.py

    def heuristic(self):
        color_distribution = {} # numer of beakers a color has been found in for each color
        for beaker in self.state:
            color_beaker = {}
            for color in beaker.content:
                if not color in color_beaker:
                    color_beaker[color] = True
                    if color in color_distribution:
                        color_distribution[color] += 1
                    else:
                        color_distribution[color] = 1
        # calculating the absolute minor numer of moves necessary to unite all different colors
        cost = 0
        for color, qnt in color_distribution.items():
            cost += qnt - 1

        return cost

    def generate_state(self, action):
        """
        Generate a state
        :param action: A tuple (idx_from, idx_to) that pour the liquid from a beaker to another beaker
        :return: A list of beakers that represent a new state
        """
        new_state = copy.deepcopy(self.state)
        no_error = new_state[action[0]].pour_to(new_state[action[1]])
        if no_error:
            return new_state
        return None

    def generate_solution(self):
        """
        Generate a solution, i.e. a list of nodes from root to self, a path
        :return: A list of nodes from root to self
        """
        path = [self]
        current = self
        while current.parent is not None:
            current = current.parent
            path.append(current)
        path.reverse()
        return path

    def generate_actions(self):
        """
        Generate every legal action in the current state
        :return: A list of actions
        """
        actions = [] # Ma che cazzp hp fatto non esiste .beaker state è una lista
        for i in range(len(self.state) - 1):
            for j in range(i + 1, len(self.state)):
                if check_action(self.state, (i, j)):
                    actions.append((i, j))
                if check_action(self.state, (j, i)):
                    actions.append((j, i))

        return actions

    def check_duplicate(self, frontier):

        for priority, node in frontier.items():

