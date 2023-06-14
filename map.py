import tkinter as tk
import random
from PIL import Image,ImageTk
from tkinter.constants import *
import mazeMap


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
        self.map_width = WindowParameter.mapWidth
        self.map_height = WindowParameter.mapHeight
        case_size = WindowParameter.tileSize
        x_tile = WindowParameter.mapTileCol
        y_tile = WindowParameter.mapTileRow
        maze = mazeMap.generate_maze(x_tile,y_tile)

        wall_image = Image.open(".\sprites\wall_mid.png").convert("P")
        wall_image = wall_image.resize((case_size, case_size), Image.ANTIALIAS)
        self.wall_photo = ImageTk.PhotoImage(wall_image)

        floor_image = Image.open("./sprites/floor_1.png").convert("P")
        floor_image= floor_image.resize((case_size, case_size), Image.ANTIALIAS)
        self.floor_photo = ImageTk.PhotoImage(floor_image)

        #Dessine les cases V2.0
        for y in range(len(maze)):
            for x in range(len(maze[y])):
                if(maze[y][x] == 'W'):
                    areaPlay.create_image(x * case_size, y * case_size, anchor="nw", image=self.wall_photo)
                    self.CaseNoire[self.indexDico] = [x * case_size, y * case_size, (x + 1) * case_size, (y + 1) * case_size]
                    self.centreCaseNoire[self.indexDico] = [(x * case_size + (x + 1) * case_size) / 2, (y * case_size + (y + 1) * case_size) / 2]
                    self.indexDico += 1
                elif(maze[y][x] == 'C'):
                    areaPlay.create_image(x * case_size, y * case_size, anchor="nw", image=self.floor_photo)
    
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
        print(self.CaseNoire)


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
        self.key = areaPlay.create_rectangle(x1, y1, x1+WindowParameter.objectSize, y1+WindowParameter.objectSize, fill="yellow")

                
    def player_info(self,areaPlay):
        map_width = WindowParameter.mapWidth
        map_height = WindowParameter.mapHeight
        screen_width = WindowParameter.screenWidth
        x1 = map_width
        x2 = screen_width
        y2 = screen_width
        p_image = Image.open(".\sprites\knight_f_idle_anim_f0.png").convert("P")
        p_image = p_image.resize((32,56))
        self.player_photo = ImageTk.PhotoImage(p_image)

        areaPlay.create_rectangle(x1, 0, x2, y2, fill="black", outline="red", dash=(3,5))
        areaPlay.create_image(map_width + 50,50,image=self.player_photo)
        areaPlay.create_rectangle(map_width+80,50,map_width+300,80,fill="red")
        areaPlay.create_rectangle(x1 + 20,400,x1 + 310,y2-50,fill="grey",outline="white")


    
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

