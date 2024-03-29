import tkinter as tk
import json
import windowParameters
import equipements
from map import Map

class Escape:

    def __init__(self) -> None:
        pass

    def createEscap(self,window, selfP):
        self.selfplayer = selfP
        self.windowEsc = tk.Toplevel(window)

        # #Remove window decorations (Top-right)
        # self.windowEsc.overrideredirect(True)

        # # Get the width and height of the Toplevel window
        # window_width = self.windowEsc.winfo_reqwidth()
        # window_height = self.windowEsc.winfo_reqheight()

        # # Calculate the position of the window based on the dimensions of the parent window
        # position_top = int(window.winfo_y() + (window.winfo_height() / 2) - (window_height / 2))
        # position_right = int(window.winfo_x() + (window.winfo_width() / 2) - (window_width / 2))

        # # Set the geometry of the window with the calculated position
        # self.windowEsc.geometry("+{}+{}".format(position_right, position_top))

        #############################################
        self.windowEsc.overrideredirect(True)
        self.windowEsc.geometry("150x300")

        window_width = window.winfo_width()
        window_height = window.winfo_height()
        x = window.winfo_rootx() + (window_width - self.windowEsc.winfo_width()) // 2 -75
        y = window.winfo_rooty() + (window_height - self.windowEsc.winfo_height()) // 2 - 200


        # Définition des coordonnées de la fenêtre
        self.windowEsc.geometry("+{}+{}".format(x, y))
        
        self.windowEsc.focus_set()
        self.windowEsc.grab_set()

        buttonContinue = tk.Label(self.windowEsc, text="Menu")
        buttonContinue.place(x=150 / 2, y=(300/2)-130 , anchor="center")
        ###########################################


        buttonContinue = tk.Button(self.windowEsc, text="Continue", command=self.closeEsc)
        buttonContinue.place(x=150 / 2, y=150/2 -20, anchor="center")

        buttonSave = tk.Button(self.windowEsc, text="Save and Quit", command=self.save)
        buttonSave.place(x=150 / 2, y=150/2 + 20, anchor="center")

        buttonQuit = tk.Button(self.windowEsc, text="Quit", command=self.quit)
        buttonQuit.place(x=150 / 2, y=(300 / 2) + 40, anchor="center")

    def quit(self):

        self.selfplayer.areaPlay.delete("all")
        self.selfplayer.areaPlay.unbind("<KeyPress>")
        self.windowEsc.destroy()
        self.selfplayer.areaPlay.delete("all")
        self.selfplayer.areaPlay.destroy()
        self.selfplayer.interface.backtomenu()

    def save(self):
        self.selfplayer.areaPlay.delete("all")
        self.selfplayer.areaPlay.unbind("<KeyPress>")
        with open('save.json', 'w') as fichier:
        # Créer de la save
            dataPlayer = {
                'level' : self.selfplayer.PlayerLevel,
                'xp' : self.selfplayer.xp,
                'class': self.selfplayer.classe,
                'gold': self.selfplayer.gold,
                'life_point': self.selfplayer.life_point,
                'max_life_point':self.selfplayer.max_life_point,
                'mana': self.selfplayer.mana,
                'max_mana': self.selfplayer.max_mana,
                'damage': equipements.Equipements.equipement_stats[self.selfplayer.weapon],
                'damageSpell' : self.selfplayer.damageSpell,
                'armor': self.selfplayer.armor,
                'weapon': self.selfplayer.weapon,
                'defense':equipements.Equipements.equipement_stats[self.selfplayer.armor],
                'inventory': self.selfplayer.inventory,
                'map': self.selfplayer.map.maze,
                'levelMap': self.selfplayer.levelMap
            }
        
            # Écrire les données dans le fichier JSON
            json.dump(dataPlayer, fichier)
        
        self.windowEsc.destroy()
        self.selfplayer.areaPlay.delete("all")
        self.selfplayer.areaPlay.destroy()
        self.selfplayer.interface.backtomenu()

    def closeEsc(self):
        ##print("destroy")
        self.selfplayer.collPNJ = False
        self.windowEsc.destroy()
