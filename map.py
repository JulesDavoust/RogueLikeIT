import tkinter as tk
import random
from PIL import Image, ImageTk
from tkinter.constants import *
import mazeMap

from windowParameters import WindowParameter



class Map:
    maze = None
    levelStatic = 0
    def __init__(self) -> None:
        Map.levelStatic += 1
        self.CaseNoire = {}
        self.centreCaseNoire = {}
        self.dicoC = {}
        self.indexDico = 0
        self.indexDicoC = 0
        self.spawnX = 0
        self.spawnY = 0

    def generateMap(self, areaPlay, existMap):
        self.map_width = WindowParameter.mapWidth
        self.map_height = WindowParameter.mapHeight
        case_size = WindowParameter.tileSize
        x_tile = WindowParameter.mapTileCol
        y_tile = WindowParameter.mapTileRow

        # Image assests import
        wall_image = Image.open("./sprites/wall_mid.png").convert("P")
        wall_image = wall_image.resize((case_size, case_size), Image.ANTIALIAS)
        self.wall_photo = ImageTk.PhotoImage(wall_image)

        floor_image = Image.open("./sprites/floor_1.png").convert("P")
        floor_image = floor_image.resize((case_size, case_size), Image.ANTIALIAS)
        self.floor_photo = ImageTk.PhotoImage(floor_image)

        if(existMap == None):
            random_loto = random.randint(0,50)
            if(random_loto < 10):
                num_remove_walls = random.randint(0,10)
            elif(random_loto >= 10 and random_loto < 30):
                num_remove_walls = random.randint(40, 60)
            elif(random_loto >= 30 and random_loto < 45):
                num_remove_walls = random.randint(20,50)
            else:
                num_remove_walls = 80

            # maze generation The number of wall can be modified(removed)
            self.maze = mazeMap.generate_maze(x_tile, y_tile)
            wall_list = mazeMap.detect_walls(self.maze)
            for i in range(num_remove_walls):
                remove_index = random.choice(wall_list)
                self.maze = mazeMap.delete_wall(self.maze, remove_index[0], remove_index[1])
                wall_list = mazeMap.detect_walls(self.maze)
        else:
            self.maze = existMap

        
        # Dessine les cases V2.0
        for y in range(len(self.maze)):
            for x in range(len(self.maze[y])):
                if self.maze[y][x] == "W":
                    areaPlay.create_image(
                        x * case_size, y * case_size, anchor="nw", image=self.wall_photo
                    )
                    self.CaseNoire[self.indexDico] = [
                        x * case_size,
                        y * case_size,
                        (x + 1) * case_size,
                        (y + 1) * case_size,
                    ]
                    self.centreCaseNoire[self.indexDico] = [
                        (x * case_size + (x + 1) * case_size) / 2,
                        (y * case_size + (y + 1) * case_size) / 2,
                    ]
                    self.indexDico += 1
                elif self.maze[y][x] == "C":
                    self.dicoC[self.indexDicoC] = [
                        x * case_size,
                        y * case_size,
                        (x + 1) * case_size,
                        (y + 1) * case_size,
                    ]
                    areaPlay.create_image(
                        x * case_size,
                        y * case_size,
                        anchor="nw",
                        image=self.floor_photo,
                    )
                    self.indexDicoC += 1

        cooR = random.randint(0, len(list(self.dicoC.keys())))
        yRed = random.randint(0, (self.map_height - 50) // case_size)

        self.x1R = self.dicoC[cooR][0]
        self.y1R = self.dicoC[cooR][1]
        self.x2R = self.dicoC[cooR][2]
        self.y2R = self.dicoC[cooR][3]

        #Exit
        areaPlay.create_rectangle(self.x1R, self.y1R, self.x2R, self.y2R, fill="")
        image_item = Image.open("./sprites/exit.png").convert("P")
        image_item = image_item.resize((WindowParameter.tileSize, WindowParameter.tileSize))
        self.image_exit = ImageTk.PhotoImage(image_item)
        areaPlay.create_image(
           self.x1R, self.y1R, image=self.image_exit , anchor = "nw"
        )



        cooG = random.randint(0, len(list(self.dicoC.keys()))-1)
        """self.xGreen = random.randint(0, (self.map_width-50)// case_size)
        self.yGreen = random.randint(0, (self.map_height-50)// case_size)"""
        while cooG == cooR:
            cooG = random.randint(0, len(list(self.dicoC.keys()))-1)
            # self.yGreen = random.randint(0, (self.map_height-50)//case_size)
        x1G = self.dicoC[cooG][0]
        y1G = self.dicoC[cooG][1]
        x2G = self.dicoC[cooG][2]
        y2G = self.dicoC[cooG][3]

        #Spawn point
        areaPlay.create_rectangle(x1G, y1G, x2G, y2G, fill="")
        image_item = Image.open("./sprites/spawn.png").convert("P")
        image_item = image_item.resize((WindowParameter.tileSize, WindowParameter.tileSize))
        self.image_spawn = ImageTk.PhotoImage(image_item)
        areaPlay.create_image(
           x1G, y1G, image=self.image_spawn , anchor = "nw"
        )


        KeyfindG = -1
        KeyfindR = -1
        for cle, valeur in self.CaseNoire.items():
            if (
                x1G == valeur[0]
                and y1G == valeur[1]
                and x2G == valeur[2]
                and y2G == valeur[3]
            ):
                KeyfindG = cle
            if (
                self.x1R == valeur[0]
                and self.y1R == valeur[1]
                and self.x2R == valeur[2]
                and self.y2R == valeur[3]
            ):
                KeyfindR = cle
        if KeyfindG != -1:
            self.CaseNoire.pop(KeyfindG)
            self.centreCaseNoire.pop(KeyfindG)
        if KeyfindR != -1:
            self.CaseNoire.pop(KeyfindR)
            self.centreCaseNoire.pop(KeyfindR)
        self.spawnX = x1G
        self.spawnY = y1G
        # ####print(self.CaseNoire)

    def generateKey(self, areaPlay):
        emplacement = False
        emplacementOK = True
        case_size = WindowParameter.tileSize
        while emplacement == False:
            cooM = random.randint(0, len(list(self.dicoC)) - 1)
            x1 = self.dicoC[cooM][0]
            y1 = self.dicoC[cooM][1]
            """x1 = random.randint(0, (self.map_width-50))
            y1 = random.randint(0, (self.map_height-50))"""
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

        image_item = Image.open("./sprites/key_1.png").convert("P")
        image_item = image_item.resize((WindowParameter.tileSize, WindowParameter.tileSize))
        self.image_key = ImageTk.PhotoImage(image_item)
        self.key = areaPlay.create_image(
           x1, y1, image=self.image_key , anchor = "nw"
        )

        # self.key = areaPlay.create_rectangle(b_x1, b_y1, b_x2, b_y2)

    
