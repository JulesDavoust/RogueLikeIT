import random
from map import Map
from Fight import fight
from monster import Monster
from pnj import PNJ
from windowParameters import WindowParameter
import tkinter as tk

class player:
    def __init__(self, classe):
        self.allClasse = {0: "guerrier", 1: "archer", 2: "sorcier"}
        self.player_collision = False
        self.view_distance = 100
        self.classe = classe
        self.PlayerLevel = 0
        self.xp = 0
        self.map = Map()
        self.character_x = 0
        self.character_y = 0
        self.pause = False

        self.inventory = {"key":1}

        if classe == 0:
            self.life_point = 120
            self.max_life_point = self.life_point
            self.mana = 20
            self.damage = 30
            #self.knight = tk.PhotoImage(file="./sprites/knight_f_idle_anim_f0.png")
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

    def generatePlayer(self, window):
        self.window = window
        self.areaPlay = tk.Canvas(window, width=1000, height=700)

        self.map.generateMap(self.areaPlay)
        self.map.level = self.map.level + 1
        self.levelMap = self.map.level
        self.map.generateKey(self.areaPlay)
        self.map.generateSalle(window, self.areaPlay)
        self.map.generateFirstSalle(self.areaPlay)
        print("map level : ", self.levelMap)
        """print(self.map.CaseNoire)
        print(self.map.centreCaseNoire)"""
        self.character_x = self.map.spawnX
        self.character_y = self.map.spawnY
        self.character_id = self.areaPlay.create_rectangle(self.character_x, self.character_y, self.character_x + 10, self.character_y + 10, fill="red", outline="")
        #self.character_id = self.areaPlay.create_rectangle(self.character_x, self.character_y, self.character_x + WindowParameter.tileSize, self.character_y + WindowParameter.tileSize, fill="red", outline="")
        #self.character_pic = self.areaPlay.create_image((self.character_x + self.character_x + 27)/2, (self.character_y+self.character_y+27)/2, image=self.knight)
        self.update_view()
        number_monsters = self.numberMonsters()
        self.generateMonsters(number_monsters)
        number_pnj = random.randint(0,3)
        self.generatePNJs(number_pnj)
        self.start_moving_monsters()
        self.areaPlay.pack()
        window.bind("<KeyPress>", self.move_character)

    def start_moving_monsters(self):
        self.move_monster_periodically()
        self.areaPlay.after(900, self.start_moving_monsters)

    def numberMonsters(self):
        if(self.levelMap == 1):
            return random.randint(6,8)
        elif(self.levelMap == 2):
            return random.randint(9,11)
        elif(self.levelMap == 3):
            return random.randint(12,14)
        elif(self.levelMap == 4):
            return random.randint(12,18)
        elif(self.levelMap >= 5):
            return random.randint(19,25)

    def startFight(self):
        Fight = fight()
        print("Loading...")
        Fight.FightPage()

    def generatePNJs(self, number_pnj):
        self.pnjs = []
        self.shops = []
        min_x = 0
        max_x = self.map.map_width-50
        min_y = 0
        max_y = self.map.map_height-50
        for _ in range(number_pnj):
            print(_)
            pnj = PNJ()  # Crée une instance de pnj


            # Vérifie si les coordonnées du monstre se trouvent dans le champ de vision
            
            emplacement = False
            emplacementOK = True
            while not emplacement:
                x1 = random.randint(0, self.map.map_width-50)
                y1 = random.randint(0, self.map.map_height-50)
                for cle, valeur in self.map.CaseNoire.items():
                    if (
                        x1 + 10 > valeur[0]
                        and y1 + 10 > valeur[1]
                        and x1 < valeur[2]
                        and y1 < valeur[3]
                    ):
                        emplacementOK = False
                if emplacementOK:
                    emplacement = True
                emplacementOK = True
            """print(x1, y1, x1 + 30, y1 + 30)"""
            pnj.generateShop(self.areaPlay, x1, y1)
            self.shops.append(pnj.shop)
            self.pnjs.append(pnj)
        print(self.shops)
        for i in range(0, len(self.pnjs)):
            print(self.areaPlay.coords(self.pnjs[i].pnj))

    def generateMonsters(self, num_monsters):
        self.monsters = []  # Liste pour stocker les monstres
        min_x = 0
        max_x = self.map.map_width-50
        min_y = 0
        max_y = self.map.map_height-50

        for _ in range(num_monsters):
            monster = Monster(self.levelMap)  # Crée une instance de monstre


            # Vérifie si les coordonnées du monstre se trouvent dans le champ de vision
            
            emplacement = False
            emplacementOK = True
            while not emplacement:
                x1 = random.randint(0, self.map.map_width-50)
                y1 = random.randint(0, self.map.map_height-50)
                while self.checkMonsterInView(x1, y1):
                    x1 = random.randint(min_x, max_x)
                    y1 = random.randint(min_y, max_y)
                for cle, valeur in self.map.CaseNoire.items():
                    if (
                        x1 + 10 > valeur[0]
                        and y1 + 10 > valeur[1]
                        and x1 < valeur[2]
                        and y1 < valeur[3]
                    ):
                        emplacementOK = False
                if emplacementOK:
                    emplacement = True
                emplacementOK = True
            """print(x1, y1, x1 + 30, y1 + 30)"""

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
                print("continue ?")
                for monster in self.monsters:
                    monster.moveMonster(
                        self.areaPlay, self.view_x1, self.view_y1, self.view_x2, self.view_y2,
                        self.character_x, self.character_y, self.character_x2, self.character_x1,
                        self.character_y2, self.character_y1, self, self.map
                    )
            #self.areaPlay.after(800, self.move_monster_periodically)


    def checkPNJCollision(self, i):
        self.cooPNJ = self.areaPlay.coords(self.pnjs[i].pnj)
        self.pnj_x = (self.cooPNJ[0] + self.cooPNJ[2]) / 2  # Coordonnée x du centre du rectangle rouge
        self.pnj_y = (self.cooPNJ[1] + self.cooPNJ[3]) / 2  # Coordonnée y du centre du rectangle rouge

        self.pnj_x1 = self.cooPNJ[0]
        self.pnj_y1 = self.cooPNJ[1]
        self.pnj_x2 = self.cooPNJ[2]
        self.pnj_y2 = self.cooPNJ[3]
        if (self.character_x1 < self.pnj_x2 and self.character_x2 > self.pnj_x1) and (self.character_y1 < self.pnj_y2 and self.character_y2 > self.pnj_y1):
            print("open shop")

    def checkMonsterCollision(self, i, dx, dy):
        self.monsterCOO = self.areaPlay.coords(self.monsters[i].monster)
        self.monster_x = (self.monsterCOO[0] + self.monsterCOO[2]) / 2  # Coordonnée x du centre du rectangle rouge
        self.monster_y = (self.monsterCOO[1] + self.monsterCOO[3]) / 2  # Coordonnée y du centre du rectangle rouge

        self.monster_x1 = self.monsterCOO[0]
        self.monster_y1 = self.monsterCOO[1]
        self.monster_x2 = self.monsterCOO[2]
        self.monster_y2 = self.monsterCOO[3]
        if (self.character_x1 + dx < self.monster_x2 and self.character_x2 + dx > self.monster_x1) and (self.character_y1 + dy < self.monster_y2 and self.character_y2 + dy > self.monster_y1):
            return True
        else:
            return False

    def move_character(self, event):
        key = event.keysym

        if self.player_collision != True:
            
                dx, dy = 0, 0  # Valeurs de déplacement initiales

                if key == "Right":
                    if self.character_x2 + 3 > WindowParameter.mapWidth:
                        return
                    dx = 3  # Déplacement vers la droite

                elif key == "Left":
                    if self.character_x1 - 3 < 0:
                        return
                    dx = -3  # Déplacement vers la gauche

                elif key == "Up":
                    if self.character_y1 - 3 < 0:
                        return
                    dy = -3  # Déplacement vers le haut

                elif key == "Down":
                    if self.character_y2 + 3 > WindowParameter.mapHeight:
                        return
                    dy = 3  # Déplacement vers le bas

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
                for i in range(0, len(self.pnjs)):
                    self.checkPNJCollision(i)
                for i in range(0, len(self.monsters)):
                    if(self.checkMonsterCollision(i, dx, dy)): return
                self.getKey()
                self.goNextRoom()
                self.areaPlay.move(self.character_id, dx, dy)  # Déplacer le personnage
            #self.areaPlay.move(self.character_pic, dx, dy)
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

    def goNextRoom(self):
        print("nextRoom ?")
        if(self.inventory["key"] >= 1 and self.character_x1 >= self.map.x1R and self.character_x2 <= self.map.x2R and self.character_y2 <= self.map.y2R and self.character_y1 >= self.map.y1R):
            print("Yes !")
            self.generateNewMap()

    def getKey(self):
        if (self.character_x1 < self.map.keyX2 and self.character_x2 > self.map.keyX1) and (self.character_y1 < self.map.keyY2 and self.character_y2 > self.map.keyY1):
            self.inventory["key"] = +1
            self.areaPlay.delete(self.map.key)
            print(self.inventory)

    def generateNewMap(self):
        # Supprime les éléments de la carte actuelle
        self.areaPlay.delete("all")

        # Génère une nouvelle carte
        self.map = Map()
        self.map.generateMap(self.areaPlay)
        self.map.level = self.levelMap + 1
        self.levelMap = self.map.level
        print(self.map.level)
        self.map.generateKey(self.areaPlay)

        # Met à jour les coordonnées du personnage
        self.character_x = self.map.spawnX
        self.character_y = self.map.spawnY
        self.character_id = self.areaPlay.create_rectangle(
            self.character_x, self.character_y, self.character_x + 10, self.character_y + 10, fill="red", outline=""
        )

        # Génère les monstres pour la nouvelle carte
        self.update_view()
        number_monsters = self.numberMonsters()
        self.generateMonsters(number_monsters)
        number_pnj = random.randint(0,3)
        self.generatePNJs(number_pnj)
        self.move_monster_periodically()

    def displayPJ(self):
        if self.classe == 0:
            return "Classe : "+ str(self.allClasse[self.classe])+ "Life point : "+ str(self.life_point)+ "Damage : "+str(self.damage)
        elif self.classe == 1:
            return "Classe : "+str(self.allClasse[self.classe])+ "Life point : "+ str(self.life_point)+ "Damage : "+str(self.damage)+ "Range : "+str(self.range)
        elif self.classe == 2:
            return "Classe : "+str(self.allClasse[self.classe])+ "Life point : "+str(self.life_point) +"Damage : "+str(self.damage)+ "Range : "+str(self.range)+ "Mana : "+str(self.mana)
        