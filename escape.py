import tkinter as tk
import json


class Escape:

    def __init__(self) -> None:
        pass

    def createEscap(self,window, selfP):
        self.selfplayer = selfP
        self.windowEsc = tk.Toplevel(window)
        self.windowEsc.geometry("150x300")
        self.windowEsc.focus_set()

        buttonContinue = tk.Button(self.windowEsc, text="Continue", command=self.closeEsc)
        buttonContinue.place(x=150 / 2, y=(300/2)-20 , anchor="center")

        buttonSave = tk.Button(self.windowEsc, text="Save and Quit", command=self.save)
        buttonSave.place(x=150 / 2, y=(300 / 2) + 10, anchor="center")


    def save(self):
        """self.selfplayer.areaPlay.delete("all")
        self.selfplayer.areaPlay.unbind("<KeyPress>")"""
        with open('save.json', 'w') as fichier:
        # Créer une structure de données avec les données souhaitées
            dataPlayer = {
                'level' : self.selfplayer.PlayerLevel,
                'xp' : self.selfplayer.xp,
                'class': self.selfplayer.classe,
                'gold': self.selfplayer.gold,
                'life_point': self.selfplayer.life_point,
                'max_life_point':self.selfplayer.max_life_point,
                'mana': self.selfplayer.mana,
                'damage': self.selfplayer.damage,
                'armor': self.selfplayer.armor,
                'inventory': self.selfplayer.inventory
            }
        
            # Écrire les données dans le fichier JSON
            json.dump(dataPlayer, fichier)
        
        """self.windowEsc.destroy()
        self.selfplayer.areaPlay.delete("all")
        self.selfplayer.areaPlay.destroy()
        self.selfplayer.interface.backtomenu()"""

    def closeEsc(self):
        print("destroy")
        self.selfplayer.collPNJ = False
        self.windowEsc.destroy()
