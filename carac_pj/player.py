import random
from map import Map
from Fight import fight
from monster import Monster
import tkinter as tk

class player:
    def __init__(self, classe):
        self.allClasse = {0: "guerrier", 1: "archer", 2: "sorcier"}
        self.player_collision = False
        self.view_distance = 100
        self.classe = classe
        self.level = 0
        self.xp = 0
        self.map = Map()
        self.character_x = self.map.cooSpawnX
        self.character_y = self.map.cooSpawnY

        if classe == 0:
            self.life_point = 120
            self.max_life_point = self.life_point
            self.mana = 20
            self.damage = 30
            self.knight = tk.PhotoImage(file="C:/Users/jules/Desktop/01Knight.png")
        elif classe == 1:
            self.life_point = 80
            self.max_life_point = self.life_point
            self.mana = 30
            self.range = 10
            self.damage = 10
        elif classe == 2:
            self.life_point = 100
            self.max_life_point = self.life_point
            self.mana = 50
            self.range = 5
            self.damage = 20

    def generatePlayer(self, window, generate):
        
        self.areaPlay = tk.Canvas(window, width=1000, height=700)

        self.map.generateMap(window, self.areaPlay)
        self.map.generateKey(self.areaPlay)
        self.map.generateSalle(window, self.areaPlay)
        self.map.generateFirstSalle(self.areaPlay)
        print(self.map.CaseNoire)
        print(self.map.centreCaseNoire)
        self.character_id = self.areaPlay.create_rectangle(self.character_x, self.character_y, self.character_x + 27, self.character_y + 27, fill="", outline="")
        self.character_pic = self.areaPlay.create_image((self.character_x + self.character_x + 27)/2, (self.character_y+self.character_y+27)/2, image=self.knight)
        self.update_view()
        self.number_monsters = random.randint(5, 7)
        self.generateMonsters(self.number_monsters)
        self.move_monster_periodically()

        self.areaPlay.pack()
        window.bind("<KeyPress>", self.move_character)

    def startFight(self):
        Fight = fight()
        print("Loading...")
        Fight.FightPage()

    def generateMonsters(self, num_monsters):
        self.monsters = []  # Liste pour stocker les monstres
        min_x = 0
        max_x = 720
        min_y = 0
        max_y = 520

        for _ in range(num_monsters):
            monster = Monster(self.map.level)  # Crée une instance de monstre


            # Vérifie si les coordonnées du monstre se trouvent dans le champ de vision
            
            emplacement = False
            emplacementOK = True
            while not emplacement:
                x1 = random.randint(0, 720)
                y1 = random.randint(0, 520)
                while self.checkMonsterInView(x1, y1):
                    x1 = random.randint(min_x, max_x)
                    y1 = random.randint(min_y, max_y)
                for cle, valeur in self.map.CaseNoire.items():
                    if (
                        x1 + 30 > valeur[0]
                        and y1 + 30 > valeur[1]
                        and x1 < valeur[2]
                        and y1 < valeur[3]
                    ):
                        emplacementOK = False
                if emplacementOK:
                    emplacement = True
                emplacementOK = True
            print(x1, y1, x1 + 30, y1 + 30)

            # Génère le carré noir du monstre dans l'areaPlay à la position aléatoire
            monster.generateMonster(self.areaPlay, x1, y1)

            self.monsters.append(monster)  # Ajoute le monstre à la liste
    
    def checkMonsterInView(self, monster_x, monster_y):
        if (
            monster_x >= self.view_x1
            and monster_x <= self.view_x2
            and monster_y >= self.view_y1
            and monster_y <= self.view_y2
        ):
            return True
        return False

    def move_monster_periodically(self):
        #self.monster.moveMonster(self.areaPlay, self.view_x1, self.view_y1, self.view_x2, self.view_y2, self.character_x, self.character_y, self.character_x2, self.character_x1, self.character_y2, self.character_y1)
        if self.player_collision == False:
            for monster in self.monsters:
                monster.moveMonster(
                    self.areaPlay, self.view_x1, self.view_y1, self.view_x2, self.view_y2,
                    self.character_x, self.character_y, self.character_x2, self.character_x1,
                    self.character_y2, self.character_y1, self, self.map
                )
            self.areaPlay.after(800, self.move_monster_periodically)
        #self.areaPlay.after(800, self.move_monster_periodically)


    def move_character(self, event):
        key = event.keysym
        if self.player_collision != True:
            dx, dy = 0, 0  # Valeurs de déplacement initiales

            if key == "Right":
                if self.character_x2 + 10 > 768:
                    return
                dx = 10  # Déplacement vers la droite

            elif key == "Left":
                if self.character_x1 - 10 < 0:
                    return
                dx = -10  # Déplacement vers la gauche

            elif key == "Up":
                if self.character_y1 - 10 < 0:
                    return
                dy = -10  # Déplacement vers le haut

            elif key == "Down":
                if self.character_y2 + 10 > 576:
                    return
                dy = 10  # Déplacement vers le bas

            new_x1 = self.character_x1 + dx
            new_y1 = self.character_y1 + dy
            new_x2 = self.character_x2 + dx
            new_y2 = self.character_y2 + dy

            for cle, valeur in self.map.CaseNoire.items():
                if (
                    new_x2 > valeur[0]
                    and new_y2 > valeur[1]
                    and new_x1 < valeur[2]
                    and new_y1 < valeur[3]
                ):
                    return  # Collision détectée, arrêter le déplacement

            self.areaPlay.move(self.character_id, dx, dy)  # Déplacer le personnage
            self.areaPlay.move(self.character_pic, dx, dy)
            self.update_view()


    def update_view(self):
        character_coords = self.areaPlay.coords(self.character_id)
        self.character_x = (character_coords[0] + character_coords[2]) / 2  # Coordonnée x du centre du rectangle rouge
        self.character_y = (character_coords[1] + character_coords[3]) / 2  # Coordonnée y du centre du rectangle rouge

        self.character_x1 = character_coords[0]
        self.character_y1 = character_coords[1]
        self.character_x2 = character_coords[2]
        self.character_y2 = character_coords[3]

        self.areaPlay.delete("view")  # Supprimer les anciennes zones de vision

        # Dessiner une nouvelle zone de vision
        self.view_x1 = self.character_x - self.view_distance
        self.view_y1 = self.character_y - self.view_distance
        self.view_x2 = self.character_x + self.view_distance
        self.view_y2 = self.character_y + self.view_distance

        print("Player : x1 : ",self.view_x1," y1 : ",self.view_x2," x2 : ",self.view_x2," y2 : ",self.view_y2)

        self.areaPlay.create_rectangle(self.view_x1, self.view_y1, self.view_x2, self.view_y2, fill="", outline="white", tag="view")


    def displayPJ(self):
        if self.classe == 0:
            return "Classe : "+ str(self.allClasse[self.classe])+ "Life point : "+ str(self.life_point)+ "Damage : "+str(self.damage)
        elif self.classe == 1:
            return "Classe : "+str(self.allClasse[self.classe])+ "Life point : "+ str(self.life_point)+ "Damage : "+str(self.damage)+ "Range : "+str(self.range)
        elif self.classe == 2:
            return "Classe : "+str(self.allClasse[self.classe])+ "Life point : "+str(self.life_point) +"Damage : "+str(self.damage)+ "Range : "+str(self.range)+ "Mana : "+str(self.mana)
        