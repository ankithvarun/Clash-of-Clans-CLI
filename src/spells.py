class spell:
    def __init__(self, name, duration, startFrame):
        self.name = name
        self.duration = duration
        self.startFrame = startFrame

class rage(spell):
    def __init__(self, name, duration, startFrame):
        super().__init__(name, duration, startFrame)

    def activate(self, map):
        map.isRage = True
        map.timeout = 0.1
        map.troops["K"][0].strength *= 2
        for troop in map.troops["B"]:
            troop.strength *= 2

    def deactivate(self, map):
        map.isRage = False
        map.timeout = 0.5
        map.troops["K"][0].strength /= 2
        for troop in map.troops["B"]:
            troop.strength /= 2

class heal(spell):
    def __init__(self, name, duration, startFrame):
        super().__init__(name, duration, startFrame)
        self.isActivated = False

    def activate(self, map):
        self.isActivated = True
        map.troops["K"][0].health = map.troops["K"][0].max_health
        for troop in map.troops["B"]:
            troop.health = troop.max_health