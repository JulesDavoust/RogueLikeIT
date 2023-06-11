import tkinter as tk
import random


from windowParameters import WindowParameter


class Map:
    def __init__(self) -> None:
        self.level = 0
        self.CaseNoire = {}
        self.centreCaseNoire = {}
        self.indexDico = 0
        self.spawnX = 0
        self.spawnY = 0

    def generateMap(self, areaPlay):
        map_width = WindowParameter.mapWidth
        map_height = WindowParameter.mapHeight
        case_size = WindowParameter.tileSize
        x_tile = map_width // case_size
        y_tile = map_height // case_size
        print(x_tile)
        print(y_tile)

        # Dessine les cases
        for x in range(x_tile):
            for y in range(y_tile):
                if x == x_tile - 1 and y == y_tile - 1 :
                     # Coin inferieur droit (fin du niveau)
                     fill_color = "red"
                elif x == 0 and y == 0:
                     # Coin superieur gauche (entrée du donjon)
                     fill_color = "green"
        for x in range(self.map_width // case_size):
            for y in range(self.map_height // case_size):
                if random.random() < 0.335:  # Changer la probabilité selon vos besoins
                    fill_color = "black"  # Mur
                else:
                    fill_color = "white"  # Libre passage
                x1 = x * case_size
                y1 = y * case_size
                x2 = x1 + case_size
                y2 = y1 + case_size
                if fill_color == "black":
                        self.CaseNoire[self.indexDico] = [x1, y1, x2, y2]
                        self.centreCaseNoire[self.indexDico] = [(x1+x2)/2, (y1+y2)/2]
                        self.indexDico += 1
                areaPlay.create_rectangle(x1, y1, x2, y2, fill=fill_color)
        xRed = random.randint(0, (self.map_width-50)// case_size)
        yRed = random.randint(0, (self.map_height-50)// case_size)
        self.x1R = xRed * case_size
        self.y1R = yRed * case_size
        self.x2R = self.x1R + case_size
        self.y2R = self.y1R + case_size
        areaPlay.create_rectangle(self.x1R, self.y1R, self.x2R, self.y2R, fill="red")

        self.xGreen = random.randint(0, (self.map_width-50)// case_size)
        self.yGreen = random.randint(0, (self.map_height-50)// case_size)
        while self.xGreen == xRed and yRed == self.yGreen:
            self.xGreen = random.randint(0, (self.map_width-50)//case_size)
            self.yGreen = random.randint(0, (self.map_height-50)//case_size)
        x1G = self.xGreen * case_size
        y1G = self.yGreen * case_size
        x2G = x1G + case_size
        y2G = y1G + case_size
        areaPlay.create_rectangle(x1G, y1G, x2G, y2G, fill="green")
        KeyfindG = -1
        KeyfindR = -1
        for cle, valeur in self.CaseNoire.items():
            if(x1G == valeur[0] and y1G == valeur[1] and x2G == valeur[2] and y2G == valeur[3]):
                KeyfindG = cle
            if(self.x1R == valeur[0] and self.y1R == valeur[1] and self.x2R == valeur[2] and self.y2R == valeur[3]):
                KeyfindR = cle
        if KeyfindG != -1:
            self.CaseNoire.pop(KeyfindG)
            self.centreCaseNoire.pop(KeyfindG)
        if KeyfindR != -1:
            self.CaseNoire.pop(KeyfindR)
            self.centreCaseNoire.pop(KeyfindR)
        self.spawnX = x1G + (case_size - 10) // 2
        self.spawnY = y1G + (case_size - 10) // 2


    def generateKey(self,areaPlay):
        emplacement = False
        emplacementOK = True
        case_size = WindowParameter.tileSize
        while emplacement == False:
            x1 = random.randint(0, (self.map_width-50))
            y1 = random.randint(0, (self.map_height-50))
            for cle, valeur in self.CaseNoire.items():
                if (
                    x1 + case_size > valeur[0]
                    and y1 + case_size > valeur[1]
                    and x1 < valeur[2]
                    and y1 < valeur[3]
                ):
                    emplacementOK = False
            if emplacementOK:
                emplacement = True
            emplacementOK = True
        self.keyX1 = x1
        self.keyY1 = y1
        self.keyX2 = x1 + 6
        self.keyY2 = y1 + 6
        self.key = areaPlay.create_rectangle(x1, y1, x1+6, y1+6, fill="yellow")

    def refreshMap(self,areaPlay,player):
        map_width = WindowParameter.mapWidth
        map_height = WindowParameter.mapHeight
        case_size = WindowParameter.tileSize
        x_tile = map_width // case_size
        y_tile = map_height // case_size
        print(x_tile)
        print(y_tile)

        #Parcours les cases et change la map
        for x in range(x_tile):
            for y in range(y_tile):
                if player.x == 3:
                    return True
                
    def generateFirstSalle(self, areaPlay):
        print("salutGENERATEfirstSALLE")
        # x1, y1 = 150, 150
        # x2, y2 = 300, 150
        # x3, y3 = 300, 300
        # x4, y4 = 150, 300
        # areaPlay.create_line(x1, y1, x2, y2, fill="brown", width=WindowParameter.tileSize)
        # areaPlay.create_line(x2, y2, x3, y3, fill="brown", width=WindowParameter.tileSize)
        # areaPlay.create_line(x3, y3, x4, y4, fill="brown", width=WindowParameter.tileSize)
        # areaPlay.create_line(x4, y4, x1, y1, fill="brown", width=WindowParameter.tileSize)
        

    def generateSalle(self, window, areaPlay):
        print("salutGENERATESALLE")
        # areaPlay.create_line(100, 450, 100, 350, fill="brown", width=4)

    """def numberMonster(self, maplevel):
        print(maplevel)
        if(maplevel == 1):
            return random.randint(5, 7)
        elif(maplevel == 2 and maplevel <=4):
            return random.randint(8,10)
        elif(maplevel == 5 and maplevel <= 7):
            return random.randint(11,13)
        elif(maplevel == 8 and maplevel <= 10):
            return random.randint(14, 16)
        elif(maplevel > 10):
            return random.randint(17, 25)"""

