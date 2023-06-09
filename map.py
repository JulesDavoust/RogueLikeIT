import tkinter as tk
import random

from windowParameters import WindowParameter


class Map:
    def __init__(self) -> None:
        self.level = 1

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
               
                areaPlay.create_rectangle(x1, y1, x2, y2, fill=fill_color)

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