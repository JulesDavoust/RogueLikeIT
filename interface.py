from carac_pj.classePJ import classePJ
from carac_pj.player import player
from map import Map
import tkinter as tk
import GameMap
import json
import os

from windowParameters import WindowParameter

class Interface:
    def __init__(self):
        self.clickChoose = False
        self.size = WindowParameter.screenSize
        self.window = tk.Tk()
        self.window.minsize(WindowParameter.screenWidth,WindowParameter.screenHeight)
        self.window.maxsize(WindowParameter.screenWidth,WindowParameter.screenHeight)

    def select_guerrier(self):
        self.player = player(0, self)
        self.clickChoose = True
        self.MenuClass()

    def select_archer(self):
        self.player = player(1, self)
        self.clickChoose = True
        self.MenuClass()

    def select_sorcier(self):
        self.player = player(2, self)
        self.clickChoose = True
        self.MenuClass()

    def GenerateGame(self):
        with open('save.json', 'w') as fichier:
            fichier.truncate(0)
        self.menu.pack_forget()
        self.player.generatePlayer(self.window)
        self.player.areaPlay.focus_set()

    def MainMenu(self):
        self.generate.pack_forget()
        self.fight.pack_forget()
        self.menu.pack_forget()
        self.main_menu.pack()

        title = tk.Label(self.main_menu, text="Rogue Like", font=("Press Start 2P", 24))
        title.pack()

        new_game_button = tk.Button(self.main_menu, text="New Game", command=self.MenuClass)
        new_game_button.pack()

        continue_button = tk.Button(self.main_menu, text="Continue", command=self.ContinueGame)
        continue_button.pack()

    def MenuClass(self):
        with open('save.json', 'w') as fichier:
            fichier.truncate(0)
        self.generate.pack_forget()
        self.fight.pack_forget()
        self.main_menu.pack_forget()
        self.menu.pack()

        if self.clickChoose:
            self.GenerateGame()
        else:
            guerrier = tk.Label(self.menu, text="Classe : Guerrier")
            buttonGuerrier = tk.Button(self.menu, text="Choisir", command=self.select_guerrier)

            guerrier.pack()
            buttonGuerrier.pack()

    def ContinueGame(self):
        # Code pour charger une partie existante
        if self.is_json_file_empty():
            self.windowImpossible = tk.Toplevel(self.window)
            self.windowImpossible.geometry("200x200")
            self.windowImpossible.focus_set()
            self.message = tk.Label(self.windowImpossible, text="Vous n'avez aucune sauvegarde")
            self.message.place(x=200/2, y=200/ 2, anchor="center")
        else:
            with open('save.json', 'r') as file:
                data = json.load(file)

                # Exemple d'accès aux informations dans un objet JSON
                print(data)
                if data['class'] == 0:
                    self.select_guerrier()
                elif data['class'] == 1:
                    self.select_archer()
                elif data['class'] == 2:
                    self.select_sorcier()
                # Continuez à extraire les informations selon vos besoins...


    def backtomenu(self):
        self.player = None
        self.clickChoose = False
        self.start()

    def start(self):
        self.window.geometry(self.size)
        self.menu = tk.Frame(self.window)
        self.generate = tk.Frame(self.window)
        self.fight = tk.Frame(self.window)
        self.main_menu = tk.Frame(self.window)
        self.MainMenu()
        self.window.mainloop()
    
    def is_json_file_empty(self):
        if not os.path.isfile('save.json'):
            return True
    
        # Vérifier si le fichier est vide
        if os.stat('save.json').st_size == 0:
            return True
        
        # Ouvrir le fichier JSON en mode lecture
        with open('save.json', 'r') as file:
            try:
                # Charger le contenu JSON
                data = json.load(file)
            except json.JSONDecodeError:
                # Erreur de décodage JSON, le fichier ne contient pas de valeur JSON valide
                return True
        
        # Vérifier si le contenu JSON est vide
        if not data:
            return True
        
        return False