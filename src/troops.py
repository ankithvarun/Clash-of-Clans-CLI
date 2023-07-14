import src.colors as Colors

class troop:
    def __init__(self, name, health, strength, speed, x, y):
        self.name = name
        self.health = health
        self.max_health = health
        self.strength = strength
        self.speed = speed
        self.alive = True
        self.x = x
        self.y = y
        self.width = 1
        self.height = 1

    def get_health(self):
        return self.health

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y
    
    def move():
        pass

    def distance(self, building):
        return min(abs(self.x - building.x) + abs(self.y - building.y), abs(self.x - building.x - building.width + 1) + abs(self.y - building.y), abs(self.x - building.x - building.width + 1) + abs(self.y - building.y - building.height + 1), abs(self.x - building.x) + abs(self.y - building.y - building.height + 1))
    
    def direction(self, building):
        # Get direction pointing to building
        direction = {"x": 0, "y": 0}
        if self.x < building.x:
            direction["x"] = 1
        elif self.x > building.x + building.width - 1:
            direction["x"] = -1
        if self.y < building.y:
            direction["y"] = 1
        elif self.y > building.y + building.height - 1:
            direction["y"] = -1

        return direction

    def attack(self, obj, map):
        if obj == None:
            return

        obj.health -= self.strength
        if obj.health <= 0:
            for y in range(obj.height):
                for x in range(obj.width):
                    if map.get(obj.x + x, obj.y + y) != "O":
                        map.set(obj.x + x, obj.y + y, " ")
            map.buildings[obj.type].remove(obj)
            if self.type == "O":
                self.underTile = " "

    def check_collision(self, map, dir):
        for i in range(1, self.speed + 1):
            x = self.x + dir["x"] * i
            y = self.y + dir["y"] * i
            if map.get(x, y) != " ":
                return True
        else:
            return False
    
    def die(self):
        self.alive = False


class barbarian(troop):
    maxBarbs = 20
    numBarbs = 0
    
    def __init__(self, name, health, strength, speed, x, y):
        super().__init__(name, health, strength, speed, x, y)
        self.type = "B"
        barbarian.numBarbs += 1

    # def distance(self, building):
    #     return min(abs(self.x - building.x) + abs(self.y - building.y), abs(self.x - building.x - building.width) + abs(self.y - building.y), abs(self.x - building.x - building.width) + abs(self.y - building.y - building.height), abs(self.x - building.x) + abs(self.y - building.y - building.height))

    # def direction(self, building):
    #     # Get direction pointing to building
    #     direction = {"x": 0, "y": 0}
    #     if self.x < building.x:
    #         direction["x"] = 1
    #     elif self.x > building.x + building.width - 1:
    #         direction["x"] = -1
    #     if self.y < building.y:
    #         direction["y"] = 1
    #     elif self.y > building.y + building.height - 1:
    #         direction["y"] = -1

    #     return direction

    def get_nearest_building(self, map):
        building = None
        for key, value in map.buildings.items():
            if value == []:
                continue
            elif building is None:
                building = value[0]
            else:
                if key != ".":
                    for elem in value:
                        if self.distance(elem) < self.distance(building):
                            building = elem

        return building

    def move(self, map):
        dir = self.direction(self.get_nearest_building(map))
        x = self.x + dir["x"]
        y = self.y + dir["y"]

        if(not self.check_collision(map, dir)):
            map.set(self.get_x(), self.get_y(), " ")
            map.set(x, y, "B")
            self.x = x
            self.y = y
        else:
            if map.get(x, y) != "B" and map.get(x, y) != "A":
                self.attack(map.get_building(x, y), map)

    def alive(self):
        if self.health <= 0:
            self.alive = False
            print(f"{self.name} is dead")
        else:
            print(f"{self.name} is alive")

class archer(troop):
    maxArchs = 20
    numArchs = 0
    
    def __init__(self, name, health, strength, speed, x, y):
        super().__init__(name, health, strength, speed, x, y)
        self.type = "A"
        self.range = 6
        archer.numArchs += 1

    # def distance(self, building):
    #     return min(abs(self.x - building.x) + abs(self.y - building.y), abs(self.x - building.x - building.width) + abs(self.y - building.y), abs(self.x - building.x - building.width) + abs(self.y - building.y - building.height), abs(self.x - building.x) + abs(self.y - building.y - building.height))

    # def direction(self, building):
    #     # Get direction pointing to building
    #     direction = {"x": 0, "y": 0}
    #     if self.x < building.x:
    #         direction["x"] = 1
    #     elif self.x > building.x + building.width - 1:
    #         direction["x"] = -1
    #     if self.y < building.y:
    #         direction["y"] = 1
    #     elif self.y > building.y + building.height - 1:
    #         direction["y"] = -1

    #     return direction

    def get_nearest_building(self, map):
        building = None
        for key, value in map.buildings.items():
            if value == []:
                continue
            elif building is None:
                building = value[0]
            else:
                if key != ".":
                    for elem in value:
                        if self.distance(elem) < self.distance(building):
                            building = elem

        return building

    def move(self, map):
        building = self.get_nearest_building(map)
        dir = self.direction(building)
        x = self.x + dir["x"] * self.speed
        y = self.y + dir["y"] * self.speed

        if self.distance(building) <= self.range:
            self.attack(building, map)
        elif(not self.check_collision(map, dir)):
            map.set(self.get_x(), self.get_y(), " ")
            map.set(x, y, "A")
            self.x = x
            self.y = y
        else:
            for i in range(1, self.speed + 1):
                temp_x = self.x + dir["x"] * i
                temp_y = self.y + dir["y"] * i
                if map.get(temp_x, temp_y) != "A" and map.get(temp_x, temp_y) != 'B' and map.get(temp_x, temp_y) != 'K' and map.get(temp_x, temp_y) != ' ':
                    self.attack(map.get_building(temp_x, temp_y), map)
                    break

    def alive(self):
        if self.health <= 0:
            self.alive = False
            print(f"{self.name} is dead")
        else:
            print(f"{self.name} is alive")

class balloon(troop):
    maxLoons = 5
    numLoons = 0
    
    def __init__(self, name, health, strength, speed, x, y):
        super().__init__(name, health, strength, speed, x, y)
        self.type = "O"
        self.range = 1
        self.underTile = " "
        balloon.numLoons += 1

    # def distance(self, building):
    #     return min(abs(self.x - building.x) + abs(self.y - building.y), abs(self.x - building.x - building.width) + abs(self.y - building.y), abs(self.x - building.x - building.width) + abs(self.y - building.y - building.height), abs(self.x - building.x) + abs(self.y - building.y - building.height))

    # def direction(self, building):
    #     # Get direction pointing to building
    #     direction = {"x": 0, "y": 0}
    #     if self.x < building.x:
    #         direction["x"] = 1
    #     elif self.x > building.x + building.width - 1:
    #         direction["x"] = -1
    #     if self.y < building.y:
    #         direction["y"] = 1
    #     elif self.y > building.y + building.height - 1:
    #         direction["y"] = -1

    #     return direction

    def get_nearest_def_building(self, map):
        building = None

        if map.buildings["C"] != [] or map.buildings["W"] != []:
            
            if map.buildings["C"] != []:
                building = map.buildings["C"][0]
            else:
                building = map.buildings["W"][0]

            for cannon in map.buildings["C"]:
                if self.distance(cannon) <= self.distance(building):
                    building = cannon
            for tower in map.buildings["W"]:
                if self.distance(tower) <= self.distance(building):
                    building = tower

        else:
            for key, value in map.buildings.items():
                if value == []:
                    continue
                elif building is None:
                    building = value[0]
                else:
                    if key != ".":
                        for elem in value:
                            if self.distance(elem) < self.distance(building):
                                building = elem

        return building

    def move(self, map):
        building = self.get_nearest_def_building(map)
        dir = self.direction(building)
        x = self.x + dir["x"] * self.speed
        y = self.y + dir["y"] * self.speed

        if self.distance(building) == 0:
            self.underTile = " "
            self.attack(building, map)
        elif map.get(x,y) != "O":
            map.set(self.get_x(), self.get_y(), self.underTile)
            if map.get(x, y) != "A" and map.get(x, y) != 'B' and map.get(x, y) != 'K' and map.get(x, y) != 'Q':
                self.underTile = map.get(x, y)
            map.set(x, y, "O")
            self.x = x
            self.y = y

    def alive(self):
        if self.health <= 0:
            self.alive = False
            print(f"{self.name} is dead")
        else:
            print(f"{self.name} is alive")

class king(troop):
    def __init__(self, name, health, strength, speed, x, y):
        super().__init__(name, health, strength, speed, x, y)
        self.type = "K"
        self.attackdir = {"x": 0, "y": 0}
        self.leviathan = False
        self.leviathanRange = 10
        self.leviathanDuration = 30
        self.leviathanFrame = 0

    def move(self, map, dir):
        x = self.x + dir["x"]
        y = self.y + dir["y"]
        self.attackdir = dir

        if(not self.check_collision(map, dir)):
            map.set(self.get_x(), self.get_y(), " ")
            map.set(x, y, "K")
            self.x = x
            self.y = y        

    def prep_attack(self, map):
        if(self.leviathan):
           for key, buildings in map.buildings.items():
               if buildings != []:
                   for building in buildings:
                       if building.distance(self) <= self.leviathanRange:
                           self.attack(building, map) 
        else:
            x = self.x + self.attackdir["x"]
            y = self.y + self.attackdir["y"]

            building = map.get_building(x,y)
            if building is not None:
                self.attack(building, map)
    
    def alive(self):
        if self.health <= 0:
            self.alive = False
            print(f"{self.name} is dead")
        else:
            print(f"{self.name} is alive")

    def print_healthbar(self):
        healthbar = ""
        for i in range(self.health):
            healthbar += "█"
        for i in range(self.max_health - self.health):
            healthbar += " "
        health_frac = self.health / self.max_health
        if health_frac < 0.2:
            color = Colors.RED
        elif health_frac < 0.5:
            color = Colors.YELLOW
        else:
            color = Colors.GREEN
        print(f"{Colors.WHITE + self.name} {color + healthbar}")

class queen(troop):
    def __init__(self, name, health, strength, speed, x, y):
        super().__init__(name, health, strength, speed, x, y)
        self.type = "Q"
        self.attackdir = {"x": 0, "y": 0}

    def move(self, map, dir):
        x = self.x + dir["x"]
        y = self.y + dir["y"]
        self.attackdir = dir

        if(not self.check_collision(map, dir)):
            map.set(self.get_x(), self.get_y(), " ")
            map.set(x, y, "Q")
            self.x = x
            self.y = y        

    def prep_attack(self, map):
        x = self.x + self.attackdir["x"] * 8
        y = self.y + self.attackdir["y"] * 8

        self.aoe_attack(map, x, y)

    def aoe_attack(self, map, x, y):
        attackedBuildings = []
        for i in range(x - 2, x + 3):
            for j in range(y - 2, y + 3):
                if i >= 0 and i < map.width and j >= 0 and j < map.height:
                    building = map.get_building(i, j)
                    if building != None:
                        if building not in attackedBuildings:
                            self.attack(building, map)
                            attackedBuildings.append(building)
    
    def alive(self):
        if self.health <= 0:
            self.alive = False
            print(f"{self.name} is dead")
        else:
            print(f"{self.name} is alive")

    def print_healthbar(self):
        healthbar = ""
        for i in range(self.health):
            healthbar += "█"
        for i in range(self.max_health - self.health):
            healthbar += " "
        health_frac = self.health / self.max_health
        if health_frac < 0.2:
            color = Colors.RED
        elif health_frac < 0.5:
            color = Colors.YELLOW
        else:
            color = Colors.GREEN
        print(f"{Colors.WHITE + self.name} {color + healthbar}")
