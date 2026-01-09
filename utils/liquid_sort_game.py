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