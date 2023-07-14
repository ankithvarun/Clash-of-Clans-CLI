import src.building as Building
import src.troops as Troops
import src.colors as Colors
import src.spells as Spells

class map:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.map = [[0 for i in range(width)] for j in range(height)]
        self.spawnPoints = [[1,20],[98,1],[75,38]]
        self.buildings = {"T": [Building.building("Town Hall", 47, 19, 4, 3, 100, "T")], "H": [], "C": [], "W": [], ".": []}
        self.troops = {"B": [], "K": [], "Q": [], "A": [], "O": []}
        self.numTroops = {"B": 20, "A": 20, "O": 5, "K": 0, "Q": 0}
        self.springTraps = []
        self.gameState = "Playing"
        self.timeout = 0.5
        self.isRage = False
        self.curFrame = 0
        self.isLeviathan = False
        self.create_border()

    # Destructor
    def __del__(self):
       return 

    def set(self, x, y, value):
        self.map[y][x] = value

    def get(self, x, y):
        return self.map[y][x]

    def get_building(self, x, y):
        if self.get(x, y) in self.buildings.keys():
            for elem in self.buildings[str(self.get(x, y))]:
                if (x >= elem.x and x < elem.x + elem.width) and (y >= elem.y and y < elem.y + elem.height):
                    return elem        
        else:
            return None

    def get_troop(self, x, y):
        if self.get(x, y) in self.troops.keys():
            for elem in self.troops[str(self.get(x, y))]:
                if x == elem.x and y == elem.y:
                    return elem
        else:
            return None

    def get_color(self, obj, x ,y):
        if obj == None:
            return Colors.BLACK

        if obj.type == "C" or obj.type == "W":
            if obj.isShoot and x == obj.x and y == obj.y:
                return Colors.WHITE
        
        if obj.health / obj.max_health < 0.2:
            return Colors.RED
        elif obj.health / obj.max_health < 0.5:
            return Colors.YELLOW
        else:
            return Colors.GREEN       

    def display(self, level):
        disp = "Level " + str(level) + "\n\n"
        for y in range(self.height):
            for x in range(self.width):
                object = self.get_building(x, y)
                if object == None:
                    object = self.get_troop(x, y)
                disp += self.get_color(object, x, y) + self.get(x, y)
            disp += "\n"
                # print(self.get_color(object, x, y) + self.map[y][x], end="")
            # print()
        print(disp)

    def create_border(self):
        for y in range(self.height):
            for x in range(self.width):
                if (x == 0 or x == self.width - 1) and (y == 0 or y == self.height - 1):
                    self.set(x, y, '+')
                elif y == 0 or y == self.height - 1:
                    self.set(x, y, '-')
                elif x == 0 or x == self.width - 1:
                    self.set(x, y, '|')
                else:
                    self.set(x, y, ' ')

    def spawn_townhall(self):
        self.buildings["T"][0].spawn(self)

    def spawn_huts(self):
        for i in range(8):
            if i > 5:
                x = 48 + (-1) ** (i % 2) * 20
                y = 19 - (-1) ** (i % 2) * 10
            elif i > 3:
                x = 48 + (-1) ** (i % 2) * 20
                y = 19 + (-1) ** (i % 2) * 10
            elif i > 1:
                x = 48
                y = 19 + (-1) ** (i % 2) * 10
            else:
                x = 48 + (-1) ** (i % 2) * 20
                y = 19
            hut = Building.building("Hut", x, y, 2, 2, 10, "H")
            hut.spawn(self)
            self.buildings["H"].append(hut)

    def spawn_cannons(self, level):
        for i in range(4):
            if i > 1:
                x = 48 + (-1) ** (i % 2) * 10
                y = 19 + (-1) ** (i % 2) * 5
            else:
                x = 48 + (-1) ** (i % 2) * 10
                y = 19 - (-1) ** (i % 2) * 5
            cannon = Building.cannon("Cannon", x, y, 2, 2, 40, "C", 15, 1)
            cannon.spawn(self)
            self.buildings["C"].append(cannon)

        if level >= 2:
            for i in range(2):
                if i > 1:
                    x = 48 + (-1) ** (i % 2) * 10
                    y = 19 + (-1) ** (i % 2) * 10
                else:
                    x = 48 - (-1) ** (i % 2) * 10
                    y = 19 - (-1) ** (i % 2) * 10
                cannon = Building.cannon("Cannon", x, y, 2, 2, 40, "C", 15, 1)
                cannon.spawn(self)
                self.buildings["C"].append(cannon)

        if level >= 3:
            for i in range(2):
                if i > 1:
                    x = 48 + (-1) ** (i % 2) * 20
                    y = 19 - (-1) ** (i % 2) * 5
                else:
                    x = 48 - (-1) ** (i % 2) * 20
                    y = 19 + (-1) ** (i % 2) * 5
                cannon = Building.cannon("Cannon", x, y, 2, 2, 40, "C", 15, 1)
                cannon.spawn(self)
                self.buildings["C"].append(cannon)

    def spawn_wizTowers(self, level):
        for i in range(4):
            if i > 1:
                x = 48
                y = 19 + (-1) ** (i % 2) * 5
            else:
                x = 48 + (-1) ** (i % 2) * 10
                y = 19
            wiz = Building.wizTower("Wizard Tower", x, y, 2, 2, 40, "W", 15, 1)
            wiz.spawn(self)
            self.buildings["W"].append(wiz)

        if level >= 2:
            for i in range(2):
                if i > 1:
                    x = 48 + (-1) ** (i % 2) * 10
                    y = 19 - (-1) ** (i % 2) * 10
                else:
                    x = 48 - (-1) ** (i % 2) * 10
                    y = 19 + (-1) ** (i % 2) * 10
                wiz = Building.wizTower("Wizard Tower", x, y, 2, 2, 40, "W", 15, 1)
                wiz.spawn(self)
                self.buildings["W"].append(wiz)

        if level >= 3:
            for i in range(2):
                if i > 1:
                    x = 48 - (-1) ** (i % 2) * 20
                    y = 19 - (-1) ** (i % 2) * 5
                else:
                    x = 48 + (-1) ** (i % 2) * 20
                    y = 19 + (-1) ** (i % 2) * 5
                wiz = Building.wizTower("Wizard Tower", x, y, 2, 2, 40, "W", 15, 1)
                wiz.spawn(self)
                self.buildings["W"].append(wiz)

    def spawn_walls(self):
        # inner walls
        for i in range(44, 54):
            wall = Building.building("Wall", i, 17, 1, 1, 10, ".")
            wall.spawn(self)
            self.buildings["."].append(wall)

            wall = Building.building("Wall", i, 23, 1, 1, 10, ".")
            wall.spawn(self)
            self.buildings["."].append(wall)

        for j in range(18, 23):
            wall = Building.building("Wall", 44, j, 1, 1, 10, ".")
            wall.spawn(self)
            self.buildings["."].append(wall)

            wall = Building.building("Wall", 53, j, 1, 1, 10, ".")
            wall.spawn(self)
            self.buildings["."].append(wall)

        # outer walls
        for i in range(24, 74):
            wall = Building.building("Wall", i, 7, 1, 1, 10, ".")
            wall.spawn(self)
            self.buildings["."].append(wall)

            wall = Building.building("Wall", i, 32, 1, 1, 10, ".")
            wall.spawn(self)
            self.buildings["."].append(wall)

        for j in range(8, 32):
            wall = Building.building("Wall", 24, j, 1, 1, 10, ".")
            wall.spawn(self)
            self.buildings["."].append(wall)

            wall = Building.building("Wall", 73, j, 1, 1, 10, ".")
            wall.spawn(self)
            self.buildings["."].append(wall)

    def spawn_barbarian(self, ind):        
        x = self.spawnPoints[ind][0]
        y = self.spawnPoints[ind][1]
        barb = Troops.barbarian("Barbarian", 10, 2, 1, x, y)
        self.set(x, y, "B")
        self.troops["B"].append(barb)

    def move_barbarians(self):
        for barb in self.troops["B"]:
            if barb.health > 0:
                barb.move(self)
                if barb.get_health() <= 0:
                    self.set(barb.x, barb.y, " ")
                    self.troops["B"].remove(barb)
        if self.buildings["C"] == [] and self.buildings["T"] == [] and self.buildings["H"] == []:
            print(Colors.GREEN + "You win!")
            self.gameState = "Win"
            
    def spawn_archer(self, ind):        
        x = self.spawnPoints[ind][0]
        y = self.spawnPoints[ind][1]
        arch = Troops.archer("Archer", 5, 1, 2, x, y)
        self.set(x, y, "A")
        self.troops["A"].append(arch)

    def move_archers(self):
        for arch in self.troops["A"]:
            if arch.health > 0:
                arch.move(self)
                if arch.get_health() <= 0:
                    self.set(arch.x, arch.y, " ")
                    self.troops["A"].remove(arch)
        if self.buildings["C"] == [] and self.buildings["T"] == [] and self.buildings["H"] == []:
            print(Colors.GREEN + "You win!")
            self.gameState = "Win"

    def spawn_balloon(self, ind):        
        x = self.spawnPoints[ind][0]
        y = self.spawnPoints[ind][1]
        loon = Troops.balloon("Balloon", 5, 1, 2, x, y)
        self.set(x, y, "O")
        self.troops["O"].append(loon)

    def move_balloons(self):
        for loon in self.troops["O"]:
            if loon.health > 0:
                loon.move(self)
                if loon.get_health() <= 0:
                    self.set(loon.x, loon.y, " ")
                    self.troops["O"].remove(loon)
        if self.buildings["C"] == [] and self.buildings["T"] == [] and self.buildings["H"] == []:
            print(Colors.GREEN + "You win!")
            self.gameState = "Win"

    def spawn_king(self):
        king = Troops.king("King", 100, 8, 1, 1, 1)
        self.set(1, 1, "K")
        self.troops["K"].append(king)
        self.hero = "K"
        self.numTroops["K"] = 1

    def spawn_queen(self):
        queen = Troops.queen("Queen", 100, 4, 1, self.width - 2, self.height - 2)
        self.set(self.width - 2, self.height - 2, "Q")
        self.troops["Q"].append(queen)
        self.hero = "Q"
        self.numTroops["Q"] = 1

    def shoot_cannons(self):
        for cannon in self.buildings["C"]:
            if cannon.health > 0:
                cannon.attack(self)
        
        if self.numTroops[self.hero] + self.numTroops["B"] + self.numTroops["A"] + self.numTroops["O"] == 0:
            print(Colors.RED + "You lost!")
            self.gameState = "Lose"

    def shoot_wizTowers(self):
        for wiz in self.buildings["W"]:
            if wiz.health > 0:
                wiz.attack(self)
        
        if self.numTroops[self.hero] + self.numTroops["B"] + self.numTroops["A"] + self.numTroops["O"] == 0:
            print(Colors.RED + "You lost!")
            self.gameState = "Lose"

    def create_spells(self):
        self.rageSpell = Spells.rage("Rage", 80, self.curFrame)
        self.healSpell = Spells.heal("Heal", 40, self.curFrame)