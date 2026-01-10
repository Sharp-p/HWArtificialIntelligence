class Beaker:
    def __init__(self, capacity=5, content=None):
        self.content = content if content else []
        self.capacity = capacity

    def add(self, liquid=None):
        if not liquid:
            print("No liquid provided")
            return False

        if len(self.content+liquid) > self.capacity:
            print("Too many liquids")
            return False

        if self.content and liquid[-1] != self.content[-1]:
            print("Liquids do not match")
            return False

        self.content = self.content + liquid
        return True

    def remove(self):
        if not self.content:
            print("No liquid in the beaker")
            return False

        top_liq = self.content[-1]
        remain = []
        for i, e in reversed(list(enumerate(self.content))):
            if top_liq == e:
                remain.append(self.content.pop(i))
            else:
                return remain
        return remain

    def pour_to(self, target):
        if not isinstance(target, Beaker):
            print("Target is not a Beaker")
            return False

        remain = self.remove()
        if not remain: return False
        completed = target.add(remain)
        if not completed:
            self.add(remain)
        return True

def check_game(game_state):
    """
    Checks if a game as reached a win state.
    :param game_state: A game state, a list of Beaker objects
    :return: True if the game is reached a win state, False otherwise
    """
    end_state = True

    for beaker in game_state:
        if not check_beaker(beaker):
            end_state = False
            break
    return end_state

def check_beaker(beaker):
    completed = True
    if not beaker.content: return completed
    for i in range(len(beaker.content[1:])):
        if beaker.content[i] != beaker.content[i-1]:
            completed = False
            break
    return completed

def check_action(game_state, action):
    """
    Does all the checks performed in the pour_to() method, but without performing the action
    :param game_state: A game state, a list of Beaker objects
    :param action: A tuple (idx_from, idx_to) that pour the liquid from a beaker to another beaker
    :return: True if the action is valid, False otherwise
    """
    from_beaker = game_state[action[0]]
    to_beaker = game_state[action[1]]

    if ((not from_beaker.content) or
            (len(to_beaker + from_beaker) > to_beaker.capacity) or
            (to_beaker.content and from_beaker.content[-1] != to_beaker.content[-1])):
        return False

    return True