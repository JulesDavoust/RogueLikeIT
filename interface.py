from carac_pj.classePJ import classePJ
from carac_pj.player import player
from map import Map
import tkinter as tk

class interface:

    def __init__(self):
        #Unit interface size
        originTileSize = 16
        #A changer par player apres
        SCALE = 3

        tileSize= originTileSize*SCALE

        screenTileCol = 16
        screenTileRow = 12
        screenWidth = tileSize * screenTileCol
        screenHeight = tileSize * screenTileRow
        screenSize = f"{screenWidth}x{screenHeight}"
        print(screenSize)

        self.clickChoose = False
        self.size = screenSize
        self.window = tk.Tk()
        self.window.minsize(screenWidth,screenHeight)
        self.window.maxsize(screenWidth,screenHeight)

    def select_guerrier(self):
        self.player = player(0)
        self.clickChoose = True
        self.MenuClass()

    def select_archer(self):
        self.player = player(1)
        self.clickChoose = True
        self.MenuClass()

    def select_sorcier(self):
        self.player = player(2)
        self.clickChoose = True
        self.MenuClass()

    def GenerateGame(self):
        self.menu.pack_forget()
        self.player.generatePlayer(self.window)
        self.player.areaPlay.focus_set()

    def MenuClass(self):
        self.generate.pack_forget()
        self.menu.pack()

        if self.clickChoose:
            self.GenerateGame()
        else:
            guerrier = tk.Label(self.menu, text="Classe : Guerrier")
            buttonGuerrier = tk.Button(self.menu, text="Choisir", command=self.select_guerrier)

            archer = tk.Label(self.menu, text="Classe : Archer")
            buttonArcher = tk.Button(self.menu, text="Choisir", command=self.select_archer)

            sorcier = tk.Label(self.menu, text="Classe : Sorcier")
            buttonSorcier = tk.Button(self.menu, text="Choisir", command=self.select_sorcier)

            guerrier.pack()
            buttonGuerrier.pack()
            archer.pack()
            buttonArcher.pack()
            sorcier.pack()
            buttonSorcier.pack()

    def start(self):
        self.window.geometry(self.size)
        self.menu = tk.Frame(self.window)
        self.generate = tk.Frame(self.window)
        self.MenuClass()
        self.window.mainloop()