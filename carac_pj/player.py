import random
from map import Map
from Fight import fight
from monster import Monster
from pnj import PNJ
from windowParameters import WindowParameter
import tkinter as tk
from PIL import Image,ImageTk

class player:
    def __init__(self, classe):
        
        
        self.allClasse = {0: "guerrier", 1: "archer", 2: "sorcier"}
        self.classe = classe
        self.PlayerLevel = 0
        self.xp = 0
        self.inventory = {"key":0}
        self.gold = 30

        self.map = Map()

        self.view_distance = 100
        self.character_x = 0
        self.character_y = 0

        self.player_collision = False
        self.pause = False
        self.collPNJ = False
        self.cooldown_active = False
        
        self.attackDirection = "Right"

        self.numPNJ = 0

        # The distance of mouvement for player and monster
        self.moveDistance = WindowParameter.tileSize
        

        if classe == 0:
            self.life_point = 100
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
        self.areaPlay = tk.Canvas(window, width=WindowParameter.screenWidth, height=WindowParameter.screenWidth)

        self.map.generateMap(self.areaPlay)
        self.map.level = self.map.level + 1
        self.levelMap = self.map.level
        self.map.generateKey(self.areaPlay)
        self.map.player_info(self.areaPlay)
        print("map level : ", self.levelMap)
        # """print(self.map.CaseNoire)
        # print(self.map.centreCaseNoire)"""

        self.character_x = self.map.spawnX
        self.character_y = self.map.spawnY

        player_image = Image.open("./sprites/knight_f_idle_anim_f0.png").convert("P")
        pImage_width,pImage_height = player_image.size
        player_image = player_image.resize((pImage_width * WindowParameter.SCALE,pImage_height* WindowParameter.SCALE))
        self.player_photo = ImageTk.PhotoImage(player_image)
        
        # Changer le couleur de character_id à transparent 
        self.character_id = self.areaPlay.create_rectangle(self.character_x + 1, self.character_y + 1, self.character_x + WindowParameter.characterSize, self.character_y + WindowParameter.characterSize, fill="red", outline="")
        self.sprite = self.areaPlay.create_image(self.character_x, self.character_y, image=self.player_photo, anchor="nw")

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
            randomPNJ = random.randint(0, len(list(self.map.CaseNoire.keys()))-1)
            emplacement = False
            emplacementOK = True
            cooCaseNoire = self.map.CaseNoire[randomPNJ]
            x1 = cooCaseNoire[0]
            y1 = cooCaseNoire[1]

            """while not emplacement:
                x1 = random.randint(0, self.map.map_width-50)
                y1 = random.randint(0, self.map.map_height-50)
                for cle, valeur in self.map.CaseNoire.items():
                    if (
                        x1 + WindowParameter.characterSize > valeur[0]
                        and y1 + WindowParameter.characterSize > valeur[1]
                        and x1 < valeur[2]
                        and y1 < valeur[3]
                    ):
                        emplacementOK = False
                if emplacementOK:
                    emplacement = True
                emplacementOK = True"""
            """print(x1, y1, x1 + 30, y1 + 30)"""
            self.areaPlay.create_image(x1*WindowParameter.tileSize, y1*WindowParameter.tileSize, anchor="nw", image=self.map.floor_photo)
            pnj.generateShop(self.areaPlay, x1, y1)
            self.shops.append(pnj.shop)
            self.pnjs.append(pnj)
            self.map.CaseNoire.pop(randomPNJ)
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
                        x1 + + WindowParameter.characterSize > valeur[0]
                        and y1 + WindowParameter.characterSize > valeur[1]
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

    def checkPNJCollision(self, i, dx, dy):
        self.cooPNJ = self.areaPlay.coords(self.pnjs[i].pnj)
        self.pnj_x = (self.cooPNJ[0] + self.cooPNJ[2]) / 2  # Coordonnée x du centre du rectangle rouge
        self.pnj_y = (self.cooPNJ[1] + self.cooPNJ[3]) / 2  # Coordonnée y du centre du rectangle rouge

        self.pnj_x1 = self.cooPNJ[0]
        self.pnj_y1 = self.cooPNJ[1]
        self.pnj_x2 = self.cooPNJ[2]
        self.pnj_y2 = self.cooPNJ[3]
        if (self.character_x1+dx < self.pnj_x2 and self.character_x2+dx > self.pnj_x1) and (self.character_y1+dy < self.pnj_y2 and self.character_y2+dy > self.pnj_y1):
            print("open shop")
            self.numPNJ = i
            self.collPNJ = True
            print("pnj num : ", self.numPNJ)
            self.pnjs[i].openShop(self.window, self, self.collPNJ)
            return True
        else:
            return False

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

    def reset_cooldown(self):
        self.cooldown_active = False

    def Fight(self, attackRect):
        print("fonction fight")
        attack = self.areaPlay.coords(attackRect)
        attack_x1 = attack[0]
        attack_y1 = attack[1]
        attack_x2 = attack[2]
        attack_y2 = attack[3]
        i = 0
        pop = False
        while i < len(self.monsters) and pop == False:
            print("for loop")
            monsterCOO = self.areaPlay.coords(self.monsters[i].monster)

            monster_x1 = monsterCOO[0]
            monster_y1 = monsterCOO[1]
            monster_x2 = monsterCOO[2]
            monster_y2 = monsterCOO[3]
            if (attack_x2 >= monster_x1 
                and attack_x1 <= monster_x2 
                and attack_y2 >= monster_y1 
                and attack_y1 <= monster_y2):
                print(self.monsters[i].life_points_monster)
                self.monsters[i].life_points_monster = self.monsters[i].life_points_monster - self.damage
                print(self.monsters[i].life_points_monster)
                if(self.monsters[i].life_points_monster <= 0):
                    self.areaPlay.delete(self.monsters[i].monster)
                    self.monsters.pop(i)
                    pop = True
                else:
                    if(self.attackDirection == "Right"):
                        self.areaPlay.move(self.monsters[i].monster, +8, 0)
                    elif(self.attackDirection == "Left"):
                        self.areaPlay.move(self.monsters[i].monster, -8, 0)
                    elif(self.attackDirection == "Up"):
                        self.areaPlay.move(self.monsters[i].monster, 0, -8)
                    elif(self.attackDirection == "Down"):
                        self.areaPlay.move(self.monsters[i].monster, 0, +8)

            i += 1



    def move_character(self, event):
        
        key = event.keysym
        if not self.cooldown_active:
            if event.char == "a":
                if self.attackDirection == "Right":
                    print("direction attack right")
                    taille_cote = 10  # Taille du côté du carré principal
                    taille_secondaire = 6  # Taille du côté du carré secondaire

                    x1 = self.character_x2  # Coordonnée x1 du carré secondaire
                    y1 = self.character_y1 + (taille_cote - taille_secondaire) / 2  # Coordonnée y1 du carré secondaire
                    x2 = x1 + taille_secondaire  # Coordonnée x2 du carré secondaire
                    y2 = y1 + taille_secondaire  # Coordonnée y2 du carré secondaire

                    attackRect = self.areaPlay.create_rectangle(x1, y1, x2+3, y2, fill="blue")
                    self.Fight(attackRect)
                    self.window.after(100, lambda: self.areaPlay.delete(attackRect))
                    self.cooldown_active = True
                    self.window.after(3000, self.reset_cooldown)  # Désactive le cooldown après 2000 millisecondes (2 secondes)
            
            if event.char == "a":
                if self.attackDirection == "Left":
                    print("direction attack Left")
                    taille_cote = 10  # Taille du côté du carré principal
                    taille_secondaire = 6  # Taille du côté du carré secondaire

                    x2 = self.character_x1  # Coordonnée x1 du carré secondaire
                    y1 = self.character_y1 + (taille_cote - taille_secondaire) / 2  # Coordonnée y1 du carré secondaire
                    x1 = x2 - taille_secondaire  # Coordonnée x2 du carré secondaire
                    y2 = y1 + taille_secondaire  # Coordonnée y2 du carré secondaire

                    attackRect = self.areaPlay.create_rectangle(x1-3, y1, x2, y2, fill="blue")
                    self.Fight(attackRect)
                    self.window.after(100, lambda: self.areaPlay.delete(attackRect))
                    self.cooldown_active = True
                    self.window.after(3000, self.reset_cooldown)  # Désactive le cooldown après 2000 millisecondes (2 secondes)
                    
            if event.char == "a":
                if self.attackDirection == "Up":
                    print("direction attack Up")
                    taille_cote = 10  # Taille du côté du carré principal
                    taille_secondaire = 6  # Taille du côté du carré secondaire

                    x1 = self.character_x1 + (taille_cote - taille_secondaire) / 2
                    x2 = x1 + taille_secondaire
                    y2 = self.character_y1 # Coordonnée y2 du carré secondaire
                    y1 = y2 - taille_secondaire
                    

                    attackRect = self.areaPlay.create_rectangle(x1, y1-3, x2, y2, fill="blue")
                    self.Fight(attackRect)
                    self.window.after(100, lambda: self.areaPlay.delete(attackRect))
                    self.cooldown_active = True
                    self.window.after(3000, self.reset_cooldown)  # Désactive le cooldown après 2000 millisecondes (2 secondes)
                    
            if event.char == "a":
                if self.attackDirection == "Down":
                    print("direction attack Down")
                    taille_cote = 10  # Taille du côté du carré principal
                    taille_secondaire = 6  # Taille du côté du carré secondaire

                    x1 = self.character_x1 + (taille_cote - taille_secondaire) / 2 # Coordonnée x1 du carré secondaire
                    y1 = self.character_y2  # Coordonnée y1 du carré secondaire
                    x2 = x1 + taille_secondaire  # Coordonnée x2 du carré secondaire
                    y2 = y1 + taille_secondaire  # Coordonnée y2 du carré secondaire

                    attackRect = self.areaPlay.create_rectangle(x1, y1, x2, y2+3, fill="blue")
                    self.Fight(attackRect)
                    self.window.after(100, lambda: self.areaPlay.delete(attackRect))
                    self.cooldown_active = True
                    self.window.after(3000, self.reset_cooldown)  # Désactive le cooldown après 2000 millisecondes (2 secondes)

            
        

        #Player
        if self.player_collision != True:
                if(len(self.pnjs) > 0 and self.pnjs[self.numPNJ].collPNJ == False):
                    self.collPNJ = False
                if(self.collPNJ == False):
                    dx, dy = 0, 0  # Valeurs de déplacement initiales
                    if key == "Right":
                        if self.character_x2 + self.moveDistance > WindowParameter.mapWidth:
                            return
                        dx = self.moveDistance  # Déplacement vers la droite
                        self.attackDirection = "Right"

                    elif key == "Left":
                        if self.character_x1 - self.moveDistance < 0:
                            return
                        dx = -self.moveDistance  # Déplacement vers la gauche
                        self.attackDirection = "Left"

                    elif key == "Up":
                        if self.character_y1 - self.moveDistance < 0:
                            return
                        dy = -self.moveDistance  # Déplacement vers le haut
                        self.attackDirection = "Up"

                    elif key == "Down":
                        if self.character_y2 + self.moveDistance > WindowParameter.mapHeight:
                            return
                        dy = self.moveDistance  # Déplacement vers le bas
                        self.attackDirection = "Down"

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
                    i = 0
                    checkPNJ = False
                    while i < len(self.pnjs) and checkPNJ == False:
                        checkPNJ = self.checkPNJCollision(i, dx, dy)
                        i = i + 1
                    if(checkPNJ == True):
                        return
                    """for i in range(0, len(self.pnjs)):
                        if(self.checkPNJCollision(i, dx, dy)) : return"""
                    for i in range(0, len(self.monsters)):
                        if(self.checkMonsterCollision(i, dx, dy)): return
                    self.getKey()
                    self.goNextRoom()
                    self.areaPlay.move(self.character_id, dx, dy)  # Déplacer le personnage
                    self.areaPlay.move(self.sprite, dx, dy)
                    self.update_view()
        

    def attackPlayer(self):
        print("attack")

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

        #print("Player : x1 : ",self.view_x1," y1 : ",self.view_x2," x2 : ",self.view_x2," y2 : ",self.view_y2)

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
        