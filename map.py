import tkinter as tk
import random

from windowParameters import WindowParameter


class Map:
    def __init__(self) -> None:
        self.level = 1

    def generateMap(self, window, areaPlay):
        areaPlay.create_rectangle(0, 0, WindowParameter.mapWidth, WindowParameter.mapHeight, fill="gray")  # Colorier l'aire en noir

    def generateFirstSalle(self, areaPlay):
        x1, y1 = 150, 150
        x2, y2 = 300, 150
        x3, y3 = 300, 300
        x4, y4 = 150, 300
        areaPlay.create_line(x1, y1, x2, y2, fill="brown", width=WindowParameter.tileSize)
        areaPlay.create_line(x2, y2, x3, y3, fill="brown", width=WindowParameter.tileSize)
        areaPlay.create_line(x3, y3, x4, y4, fill="brown", width=WindowParameter.tileSize)
        areaPlay.create_line(x4, y4, x1, y1, fill="brown", width=WindowParameter.tileSize)
        

    def generateSalle(self, window, areaPlay):
        areaPlay.create_line(100, 450, 100, 350, fill="brown", width=4)