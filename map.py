import tkinter as tk
import random

from windowParameters import WindowParameter


class Map:
    def __init__(self) -> None:
        self.level = 1
        self.CaseNoire = {}
        self.indexDico = 0
        self.cooSpawnX = 0
        self.cooSpawnY = 0

    def generateMap(self, window, areaPlay):
        map_width = WindowParameter.mapWidth
        map_height = WindowParameter.mapHeight
        case_size = WindowParameter.tileSize
        # Dessine les cases
        for x in range(map_width // case_size):
            for y in range(map_height // case_size):
                if x == 11 and y == 8:
                     # Coin inferieur droit (fin du niveau)
                     fill_color = "red"
                elif x == 0 and y == 0:
                     # Coin superieur gauche (entrée du donjon)
                     fill_color = "green"
                else:
                     # Cases aléatoires (noir ou blanc)
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
                    self.indexDico += 1
                areaPlay.create_rectangle(x1, y1, x2, y2, fill=fill_color)

    def generateKey(self,areaPlay):
        emplacement = False
        emplacementOK = True
        case_size = WindowParameter.tileSize
        while not emplacement:
            x1 = random.randint(0, 720)
            y1 = random.randint(0, 520)
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
        print(x1, y1, x1 + case_size, y1 + case_size)
        self.key = areaPlay.create_rectangle(x1, y1, x1+20, y1+20, fill="yellow")

    def refreshMap(self,areaPlay):
        print("salut")

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