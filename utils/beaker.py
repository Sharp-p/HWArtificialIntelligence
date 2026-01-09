
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
            return

        remain = self.remove()
        if not remain: return
        completed = target.add(remain)
        if not completed:
            self.add(remain)

