import tkinter as tk
import random
from PIL import Image, ImageTk
from tkinter.constants import *
import mazeMap

from windowParameters import WindowParameter



class Map:
    maze = None
    def __init__(self) -> None:
        self.level = 0
        self.CaseNoire = {}
        self.centreCaseNoire = {}
        self.dicoC = {}
        self.indexDico = 0
        self.indexDicoC = 0
        self.spawnX = 0
        self.spawnY = 0
        self.maze = None

    def generateMap(self, areaPlay):
        self.map_width = WindowParameter.mapWidth
        self.map_height = WindowParameter.mapHeight
        case_size = WindowParameter.tileSize
        x_tile = WindowParameter.mapTileCol
        y_tile = WindowParameter.mapTileRow
        num_remove_walls = 50

        # Image assests import
        wall_image = Image.open("./sprites/wall_mid.png").convert("P")
        wall_image = wall_image.resize((case_size, case_size), Image.ANTIALIAS)
        self.wall_photo = ImageTk.PhotoImage(wall_image)

        floor_image = Image.open("./sprites/floor_1.png").convert("P")
        floor_image = floor_image.resize((case_size, case_size), Image.ANTIALIAS)
        self.floor_photo = ImageTk.PhotoImage(floor_image)

        # maze generation The number of wall can be modified(removed)
        self.maze = mazeMap.generate_maze(x_tile, y_tile)
        wall_list = mazeMap.detect_walls(self.maze)
        for i in range(num_remove_walls):
            remove_index = random.choice(wall_list)
            self.maze = mazeMap.delete_wall(self.maze, remove_index[0], remove_index[1])
            wall_list = mazeMap.detect_walls(self.maze)

        #print("Maze after delete walls:")
        #for row in self.maze:
            #print(" ".join(row))
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

        areaPlay.create_rectangle(self.x1R, self.y1R, self.x2R, self.y2R, fill="red")

        cooG = random.randint(0, len(list(self.dicoC.keys())))
        """self.xGreen = random.randint(0, (self.map_width-50)// case_size)
        self.yGreen = random.randint(0, (self.map_height-50)// case_size)"""
        while cooG == cooR:
            cooG = random.randint(0, len(list(self.dicoC.keys())))
            # self.yGreen = random.randint(0, (self.map_height-50)//case_size)
        x1G = self.dicoC[cooG][0]
        y1G = self.dicoC[cooG][1]
        x2G = self.dicoC[cooG][2]
        y2G = self.dicoC[cooG][3]
        areaPlay.create_rectangle(x1G, y1G, x2G, y2G, fill="green")

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
        # #print(self.CaseNoire)

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
        a_width = self.dicoC[cooM][2] - x1
        a_height = self.dicoC[cooM][3] - y1
        b_width = a_width * 0.5
        b_height = a_height * 0.5
        b_x1 = x1 + (a_width - b_width) / 2
        b_y1 = y1 + (a_height - b_height) / 2
        b_x2 = b_x1 + b_width
        b_y2 = b_y1 + b_height
        self.keyX1 = x1
        self.keyY1 = y1
        self.keyX2 = x1 + 6
        self.keyY2 = y1 + 6
        self.key = areaPlay.create_rectangle(b_x1, b_y1, b_x2, b_y2, fill="yellow")

    def player_info(self, areaPlay, player):
        map_width = WindowParameter.mapWidth
        map_height = WindowParameter.mapHeight
        screen_width = WindowParameter.screenWidth
        x1 = map_width
        x2 = screen_width
        y2 = screen_width

        # Barre de vie
        player_image = Image.open("./sprites/knight_f_idle_anim_f0.png").convert("P")
        pImage_width, pImage_height = player_image.size
        player_image = player_image.resize(
            (
                pImage_width * WindowParameter.SCALE,
                pImage_height * WindowParameter.SCALE,
            )
        )
        self.player_photo = ImageTk.PhotoImage(player_image)
        areaPlay.create_rectangle(
            x1, 0, x2, y2, fill="black", outline="red", dash=(3, 5)
        )
        areaPlay.create_image(
            map_width + 50, WindowParameter.tileSize +10, image=self.player_photo
        )
        areaPlay.create_rectangle(map_width + 80, WindowParameter.tileSize, map_width + 300, WindowParameter.tileSize + 30, fill="red")
        
        # Inventory information
        invento_string = ""
        for item in player.inventory.items():
            invento_string += f"{item[0]} : {item[1]} \n"
        # print(invento_string)
        # invento_info = tk.Label(areaPlay, text= invento_string, fg = "White", bg= "Black")
        # invento_info.place(x= WindowParameter.mapWidth + 30, y=100)
        areaPlay.create_text(WindowParameter.mapWidth + 50, WindowParameter.tileSize * 3, text= invento_string, fill="white", anchor = "w")



    def hp_update(self,player,areaPlay,monster):
        hp_max = player.max_life_point
        current_hp = player.life_point

        areaPlay.create_rectangle(
            WindowParameter.mapWidth + 80,
            50,
            WindowParameter.mapWidth + (hp_max * 3),
            80,
            fill="grey",
        )
        areaPlay.create_rectangle(
            WindowParameter.mapWidth + 80,
            50,
            WindowParameter.mapWidth + (current_hp * 3),
            80,
            fill="red",
        )

    """def numberMonster(self, maplevel):
        #print(maplevel)
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
