class building:
    def __init__(self, name, x, y, width, height, health, type):
        self.name = name
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.health = health
        self.max_health = health
        self.type = type

    def spawn(self, map):
        for y in range(self.y, self.y + self.height):
            for x in range(self.x, self.x + self.width):
                map.set(x, y, self.type)

    def remove(self, map):
        for y in range(self.y, self.y + self.height):
            for x in range(self.x, self.x + self.width):
                map.set(x, y, " ")
        map.objects[self.type].remove(self)
        if(map.objects[self.type] == []):
            del map.objects[self.type]
            
    def distance(self, troop):
        return ((troop.x - self.x - troop.width / 2)**2 + (troop.y - self.y - troop.height / 2)**2)**0.5

class cannon(building):
    def __init__(self, name, x, y, width, height, health, type, range, strength):
        super().__init__(name, x, y, width, height, health, type)
        self.range = range
        self.strength = strength
        self.isShoot = False

    
    def attack(self, map):
        for key, troops in map.troops.items():
            flag = False
            for troop in troops:
                if self.distance(troop) <= self.range and troop.type != 'O':
                    troop.health -= self.strength
                    self.isShoot = True
                    flag = True
                    if(troop.health <= 0):
                        if troop.type == 'K':
                            map.troops['K'][0].leviathan = False
                        map.numTroops[troop.type] -= 1
                        map.troops[troop.type].remove(troop)
                        map.set(troop.x, troop.y, " ")
                    break
                else:
                    self.isShoot = False
            if flag:
                break

class wizTower(building):
    def __init__(self, name, x, y, width, height, health, type, range, strength):
        super().__init__(name, x, y, width, height, health, type)
        self.range = range
        self.strength = strength
        self.isShoot = False
    
    def get_dir(self, troop):
        dir = {"x": 0, "y": 0}
        if troop.x > self.x:
            dir["x"] = 1
        elif troop.x < self.x:
            dir["x"] = -1
        if troop.y > self.y:
            dir["y"] = 1
        elif troop.y < self.y:
            dir["y"] = -1

        return dir

    def damage(self, troop, map):
        troop.health -= self.strength
        if(troop.health <= 0):
            if troop.type == 'K':
                map.troops['K'][0].leviathan = False
            map.numTroops[troop.type] -= 1
            map.troops[troop.type].remove(troop)
            map.set(troop.x, troop.y, " ")

    def aoe_attack(self, map, x, y, dir):
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                if i >= 0 and i < map.width and j >= 0 and j < map.height and i != x and j != y:
                    troop = map.get_troop(i, j)
                    if troop != None:
                        self.damage(troop, map)
    
    def attack(self, map):
        for key, troops in map.troops.items():
            flag = False
            for troop in troops:
                if self.distance(troop) <= self.range:
                    self.aoe_attack(map, troop.x, troop.y, self.get_dir(troop))
                    self.damage(troop, map)
                    self.isShoot = True
                    flag = True
                    break
                else:
                    self.isShoot = False
            if flag:
                break