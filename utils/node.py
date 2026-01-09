class Node:
    def __init__(self, state, parent, action, cost=None):
        self.state = state
        self.parent = parent
        self.action = action
        self.cost = cost if cost else self.parent.cost + 1 # each move in the game has unitary cost

    def generate_state(self, action):
        """
        Generate a state
        :param action: A tuple (idx_from, idx_to) that pour the liquid from a beaker to another beaker
        :return: A list of beakers that represent a new state
        """
        new_state = self.state.deepcopy()
        no_error = new_state[action[0]].pour_to(new_state[action[1]])
        if no_error:
            return new_state
        return None

