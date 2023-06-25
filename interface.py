from carac_pj.classePJ import classePJ
from carac_pj.player import player
import tkinter as tk
import json
import os
import equipements

from windowParameters import WindowParameter

class Interface:
    def __init__(self):
        self.clickChoose = False
        self.newGameVar = False
        self.cont = False
        self.size = WindowParameter.screenSize
        self.window = tk.Tk()
        #self.window.overrideredirect(True)
        self.window.minsize(WindowParameter.screenWidth,WindowParameter.screenHeight)
        self.window.maxsize(WindowParameter.screenWidth,WindowParameter.screenHeight)

        # Obtention des dimensions de l'écran
        self.screen_width = self.window.winfo_screenwidth()
        self.screen_height = self.window.winfo_screenheight()

        # Calcul des coordonnées x et y pour centrer la fenêtre
        self.x = (self.screen_width - WindowParameter.screenWidth) // 2
        self.y = (self.screen_height - WindowParameter.screenHeight) // 2-20


    def select_guerrier(self):
        self.player = player(0, self)
        self.clickChoose = True
        self.MainMenu()


    def GenerateGame(self):
        if self.cont == False:
            with open('save.json', 'w') as fichier:
                fichier.truncate(0)
        self.main_menu.pack_forget()
        self.player.generatePlayer(self.window)
        self.player.areaPlay.focus_set()

    def newGame(self):
        self.newGameVar = True
        self.select_guerrier()
        

    def MainMenu(self):
        self.generate.pack_forget()
        self.fight.pack_forget()
        self.menu.pack_forget()
        self.main_menu.pack()

        title = tk.Label(self.main_menu, text="Rogue Like", font=("Press Start 2P", 24))
        title.pack()

        if self.clickChoose:
            self.GenerateGame()
        else:
            new_game_button = tk.Button(self.main_menu, text="New Game", command=self.newGame)
            new_game_button.pack()

            continue_button = tk.Button(self.main_menu, text="Continue", command=self.ContinueGame)
            continue_button.pack()

            quit_button = tk.Button(self.main_menu, text="Quit", command=self.quit)
            quit_button.pack()

    def quit(self):
        self.window.destroy()

    def on_closing(self):
        if self.clickChoose == True:
            self.save = tk.Toplevel(self.window)
            self.save.overrideredirect(True)
            self.save.geometry("150x100")

            window_width = self.window.winfo_width()
            window_height = self.window.winfo_height()
            x = self.window.winfo_rootx() + (window_width - self.save.winfo_width()) // 2 -75
            y = self.window.winfo_rooty() + (window_height - self.save.winfo_height()) // 2 - 200

            self.save.geometry("+{}+{}".format(x, y))
        
            self.save.focus_set()
            self.save.grab_set()
            
            textSave = tk.Label(self.save, text="Do you want to save ?")
            textSave.place(x=150 / 2, y=100/2 -20, anchor="center")

            buttonYes = tk.Button(self.save, text="No", command=self.quit)
            buttonYes.place(x=100, y=55, anchor="center")

            buttonNo = tk.Button(self.save, text="Yes", command=self.saveGame)
            buttonNo.place(x=50, y=55, anchor="center")

            
        else:
            self.quit()

    def saveGame(self):
        with open('save.json', 'w') as fichier:
        # Créer une structure de données avec les données souhaitées
            dataPlayer = {
                'level' : self.player.PlayerLevel,
                'xp' : self.player.xp,
                'class': self.player.classe,
                'gold': self.player.gold,
                'life_point': self.player.life_point,
                'max_life_point':self.player.max_life_point,
                'mana': self.player.mana,
                'max_mana': self.player.max_mana,
                'damage': equipements.Equipements.equipement_stats[self.player.weapon],
                'damageSpell' : self.player.damageSpell,
                'armor': self.player.armor,
                'weapon': self.player.weapon,
                'defense':equipements.Equipements.equipement_stats[self.player.armor],
                'inventory': self.player.inventory,
                'map': self.player.map.maze
            }
        
            # Écrire les données dans le fichier JSON
            json.dump(dataPlayer, fichier)
        self.save.destroy()
        self.quit()


    def ContinueGame(self):
        # Code pour charger une partie existante
        if self.is_json_file_empty():
            self.windowImpossible = tk.Toplevel(self.window)
            self.windowImpossible.geometry("200x200")
            self.windowImpossible.focus_set()
            self.message = tk.Label(self.windowImpossible, text="Vous n'avez aucune sauvegarde")
            self.message.place(x=200/2, y=200/ 2, anchor="center")

            window_width = self.window.winfo_width()
            window_height = self.window.winfo_height()
            x = self.window.winfo_rootx() + (window_width - self.windowImpossible.winfo_width()) // 2 -75
            y = self.window.winfo_rooty() + (window_height - self.windowImpossible.winfo_height()) // 2 - 200


            # Définition des coordonnées de la fenêtre
            self.windowImpossible.geometry("+{}+{}".format(x, y))
            
            self.windowImpossible.focus_set()
            self.windowImpossible.grab_set()
        else:
            self.cont = True
            with open('save.json', 'r') as file:
                data = json.load(file)
                # Exemple d'accès aux informations dans un objet JSON
                ##print(data)
                if data['class'] == 0:
                    self.select_guerrier()
                # Continuez à extraire les informations selon vos besoins...


    def backtomenu(self):
        self.player = None
        self.clickChoose = False
        self.start()

    def start(self):
        self.cont = False
        self.newGameVar = False
        self.window.geometry(f"+{self.x}+{self.y}")
        self.menu = tk.Frame(self.window)
        self.generate = tk.Frame(self.window)
        self.fight = tk.Frame(self.window)
        self.main_menu = tk.Frame(self.window)
        self.MainMenu()
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
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