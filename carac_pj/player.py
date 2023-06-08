import random
from map import Map
import tkinter as tk

class player:
    def __init__(self, classe):
        self.allClasse = {0: "guerrier", 1: "archer", 2: "sorcier"}
        self.view_distance = 100
        self.classe = classe
        self.level = 0
        self.xp = 0

        if classe == 0:
            self.life_point = 120
            self.max_life_point = self.life_point
            self.damage = 30
        elif classe == 1:
            self.life_point = 80
            self.max_life_point = self.life_point
            self.range = 10
            self.damage = 10
        elif classe == 2:
            self.life_point = 100
            self.max_life_point = self.life_point
            self.mana = 50
            self.range = 5
            self.damage = 20

    def generatePlayer(self, window):
        map = Map()
        self.areaPlay = tk.Canvas(window, width=1000, height=700)
        map.generateMap(window, self.areaPlay)
        map.generateSalle(window, self.areaPlay)
        map.generateFirstSalle(self.areaPlay)
        self.character_id = self.areaPlay.create_rectangle(100, 100, 130, 130, fill="red")
        self.update_view()
        self.areaPlay.pack()
        window.bind("<KeyPress>", self.move_character)
        


    def move_character(self, event):
        key = event.keysym
        if key == "Right":
            self.areaPlay.move(self.character_id, 10, 0)  # Déplacement vers la droite de 10 pixels
        elif key == "Left":
            self.areaPlay.move(self.character_id, -10, 0)  # Déplacement vers la gauche de 10 pixels
        elif key == "Up":
            self.areaPlay.move(self.character_id, 0, -10)  # Déplacement vers le haut de 10 pixels
        elif key == "Down":
            self.areaPlay.move(self.character_id, 0, 10)  # Déplacement vers le bas de 10 pixels

        self.update_view()

    def update_view(self):
        character_coords = self.areaPlay.coords(self.character_id)
        character_x = (character_coords[0] + character_coords[2]) / 2  # Coordonnée x du centre du rectangle rouge
        character_y = (character_coords[1] + character_coords[3]) / 2  # Coordonnée y du centre du rectangle rouge

        self.areaPlay.delete("view")  # Supprimer les anciennes zones de vision

        # Dessiner une nouvelle zone de vision
        view_x1 = character_x - self.view_distance
        view_y1 = character_y - self.view_distance
        view_x2 = character_x + self.view_distance
        view_y2 = character_y + self.view_distance

        self.areaPlay.create_rectangle(view_x1, view_y1, view_x2, view_y2, fill="", outline="white", tag="view")


    def displayPJ(self):
        if self.classe == 0:
            return "Classe : "+ str(self.allClasse[self.classe])+ "Life point : "+ str(self.life_point)+ "Damage : "+str(self.damage)
        elif self.classe == 1:
            return "Classe : "+str(self.allClasse[self.classe])+ "Life point : "+ str(self.life_point)+ "Damage : "+str(self.damage)+ "Range : "+str(self.range)
        elif self.classe == 2:
            return "Classe : "+str(self.allClasse[self.classe])+ "Life point : "+str(self.life_point) +"Damage : "+str(self.damage)+ "Range : "+str(self.range)+ "Mana : "+str(self.mana)
        