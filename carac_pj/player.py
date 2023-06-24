import random
from map import Map
from monster import Monster
from pnj import PNJ
from windowParameters import WindowParameter
import tkinter as tk
from PIL import Image, ImageTk
import mazeMap
from equipements import Equipements, Items

import json
from escape import Escape

#from items import Items


class player:
    def __init__(self, classe, interface):
        #self.items = Items()
        self.interface = interface
        classe = 0
        self.classe = classe
        self.potion_pv = "potion_PV"
        self.potion_mp = "potion_MP"
        

        print("initiate player")
        if not self.interface.is_json_file_empty():
            print("Le fichier JSON n'est pas vide.")
            with open('save.json', 'r') as file:
                data = json.load(file)
                self.PlayerLevel = data['level']
                self.xp = data['xp']
                self.gold = data['gold']
                self.life_point = data['life_point']
                self.max_life_point = data['max_life_point']
                self.mana = data['mana']
                self.max_mana = data['max_mana']
                self.damageSpell = data['damageSpell']
                self.inventory = data['inventory']
                self.weapon = data['weapon']
                self.armor = data['armor']
                self.damage = data['damage']
                self.defense = data['defense']
        else:
            self.PlayerLevel = 0
            self.xp = 0
            self.inventory = {self.potion_pv: 1, self.potion_mp: 0}
            self.gold = 30
            if classe == 0:
                self.life_point = 75
                self.armor = 0
                self.max_life_point = self.life_point
                self.mana = 20
                self.damage = 30
                self.damageSpell = 20
                self.max_mana = 20
                self.weapon = "blade_0"
                self.armor = "ring_0"
                self.damage = Equipements.equipement_stats[self.weapon]
                self.defense = Equipements.equipement_stats[self.armor]
                # self.knight = tk.PhotoImage(file="./sprites/knight_f_idle_anim_f0.png")
            elif classe == 1:
                self.life_point = 75
                self.armor = 0
                self.max_life_point = self.life_point
                self.mana = 30
                self.range = 10
                self.damage = 10
                self.damageSpell = 20
                self.max_mana = 30
            elif classe == 2:
                self.life_point = 95
                self.armor = 0
                self.max_life_point = self.life_point
                self.mana = 50
                self.range = 5
                self.damage = 20
                self.damageSpell = 30
                self.max_mana = 50
        # add the other items in case we have time, like bomb
        # Each item is saved as dict in the list of inventory, in this way we can know the storage directly
        
        

        self.hasExitKey = False

        self.pnjCooDico = {}
        self.monsterDico = {}
        self.moved_m_index = 0

        self.indexDico = 0
        self.indexMonster = 0

        self.fullMonster = {"n": [], "e": [], "s": [], "w": []}
        self.lengthFullMonster = 0
        self.maxLengthFullMonster = 3

        self.monsterAttack = []
        
        self.text = "Monster :"

        self.escape = Escape()
        self.map = Map()
        self.view_distance = 100
        self.character_x = 0
        self.character_y = 0
        self.playerDied = False
        self.player_collision = False
        self.pause = False
        self.collPNJ = False
        self.cooldown_active = False
        self.gonext = False
        self.tourPlayer = True

        self.EJ = False
        self.E = False
        self.EA = False

        self.eventNrVar = False
        self.eventKVar = False
        self.eventMWVar = False
        self.eventMWalked = False

        self.eventMAVar = False

        self.countTourActivate = False
        self.countTourActivateSort = False
        self.countTour = 0

        self.attackDirection = "Right"

        self.numPNJ = 0

        # The distance of mouvement for player and monster
        self.moveDistance = WindowParameter.tileSize
            
        

    def generatePlayer(self, window):
        self.window = window
        self.areaPlay = tk.Canvas(
            window,
            width=WindowParameter.screenWidth,
            height=WindowParameter.screenWidth,
        )
        self.createAll()
        self.areaPlay.pack()
        window.bind("<KeyPress>", self.move_character)

    


    def reset(self):
        if self.classe == 0:
                self.life_point = 75
                self.armor = 0
                self.max_life_point = self.life_point
                self.mana = 20
                self.damage = 30
                self.damageSpell = 20
                self.max_mana = 20
                self.weapon = "blade_0"
                self.armor = "ring_0"
                self.damage = Equipements.equipement_stats[self.weapon]
                self.defense = Equipements.equipement_stats[self.armor]
                # self.knight = tk.PhotoImage(file="./sprites/knight_f_idle_anim_f0.png")
        elif self.classe == 1:
                self.life_point = 75
                self.armor = 0
                self.max_life_point = self.life_point
                self.mana = 30
                self.range = 10
                self.damage = 10
                self.damageSpell = 20
                self.max_mana = 30
        elif self.classe == 2:
                self.life_point = 95
                self.armor = 0
                self.max_life_point = self.life_point
                self.mana = 50
                self.range = 5
                self.damage = 20
                self.damageSpell = 30
                self.max_mana = 50
        self.inventory = {self.potion_pv: 1, self.potion_mp: 0}
        self.hasExitKey = False
        self.tourPlayer = True
        self.playerDied = False
        self.PlayerLevel = 0
        self.xp = 0

        self.gold = 30

        self.hasExitKey = False

        self.pnjCooDico = {}
        self.monsterDico = {}
        self.moved_m_index = 0

        self.indexDico = 0
        self.indexMonster = 0

        self.fullMonster = {"n": [], "e": [], "s": [], "w": []}
        self.lengthFullMonster = 0
        self.maxLengthFullMonster = 3

        self.monsterAttack = []
        
        self.text = "Monster :"
        
        self.view_distance = 100
        self.character_x = 0
        self.character_y = 0
        self.playerDied = False
        self.player_collision = False
        self.pause = False
        self.collPNJ = False
        self.cooldown_active = False
        self.gonext = False
        self.tourPlayer = True

        self.EJ = False
        self.E = False
        self.EA = False

        self.eventNrVar = False
        self.eventKVar = False
        self.eventMWVar = False
        self.eventMWalked = False

        self.eventMAVar = False

        self.countTourActivate = False
        self.countTourActivateSort = False
        self.countTour = 0

        self.attackDirection = "Right"

        self.numPNJ = 0
        self.life_point = self.max_life_point

    def createAll(self):
        
        self.map = Map()
        self.map.generateMap(self.areaPlay)
        self.map.level = self.map.level + 1
        self.levelMap = self.map.level
        self.map.generateKey(self.areaPlay)
        self.player_info()
        self.hp_update(False)
        self.mana_update(False)
        # print("map level : ", self.levelMap)
        # """#print(self.map.CaseNoire)
        # #print(self.map.centreCaseNoire)"""

        self.character_x = self.map.spawnX
        self.character_y = self.map.spawnY

        player_image = Image.open("./sprites/knight_f_idle_anim_f0.png").convert("P")
        
        pImage_width, pImage_height = player_image.size
        player_image = player_image.resize(
            (
                pImage_width * WindowParameter.SCALE,
                pImage_height * WindowParameter.SCALE,
            )
        )
        self.player_photo = ImageTk.PhotoImage(player_image)

        self.character_id = self.areaPlay.create_rectangle(
            self.character_x,
            self.character_y,
            self.character_x + WindowParameter.tileSize - 1,
            self.character_y + WindowParameter.tileSize - 1,
            outline="",
        )
        self.sprite = self.areaPlay.create_image(
            self.character_x, self.character_y, image=self.player_photo, anchor="nw"
        )

        self.update_view()
        number_monsters = self.numberMonsters()
        self.generateMonsters(number_monsters)
        self.generatePNJs()

    def start_moving_monsters(self):
        self.move_monster_periodically()
        self.tourPlayer = True

    def numberMonsters(self):
        if self.levelMap == 1:
            return random.randint(6, 8)
        elif self.levelMap == 2:
            return random.randint(9, 11)
        elif self.levelMap == 3:
            return random.randint(12, 14)
        elif self.levelMap == 4:
            return random.randint(12, 18)
        elif self.levelMap >= 5:
            return random.randint(19, 25)

    def generatePNJs(self):
        self.pnjs = []
        self.shops = []
        min_x = 0
        max_x = self.map.map_width - 50
        min_y = 0
        max_y = self.map.map_height - 50
        placeable_cell_list = mazeMap.three_walls_cells(self.map.maze)
        number_pnj = random.randint(1, 3)
        if number_pnj > len(placeable_cell_list):
            number_pnj = len(placeable_cell_list)

        for _ in range(number_pnj):
            pnj = PNJ()  # Crée une instance de pnj

            # PNJ generation V2.0
            randomPNJ = random.choice(placeable_cell_list)
            placeable_cell_list.remove(randomPNJ)
            x1 = randomPNJ[1]
            y1 = randomPNJ[0]

            # # Vérifie si les coordonnées du monstre se trouvent dans le champ de vision
            # randomPNJ = random.randint(0, len(list(self.map.CaseNoire.keys()))-1)
            # emplacement = False
            # emplacementOK = True
            # cooCaseNoire = self.map.CaseNoire[randomPNJ]
            # x1 = cooCaseNoire[0]
            # y1 = cooCaseNoire[1]
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
            """##print(x1, y1, x1 + 30, y1 + 30)"""

            # ##print(f"In generatePNJs:\n X: {x1*WindowParameter.tileSize} Y: {y1*WindowParameter.tileSize}")
            # self.areaPlay.create_image(x1*WindowParameter.tileSize, y1*WindowParameter.tileSize, anchor="nw", image=self.map.floor_photo)
            self.map.indexDico += 1
            self.map.CaseNoire[self.map.indexDico] = [
                x1 + 1,
                y1 + 1,
                x1 + WindowParameter.tileSize - 1,
                y1 + WindowParameter.tileSize - 1,
            ]
            self.pnjCooDico[self.indexDico] = [
                x1 + 1,
                y1 + 1,
                x1 + WindowParameter.tileSize - 1,
                y1 + WindowParameter.tileSize - 1,
            ]
            self.indexDico += 1
            pnj.generateShop(self.areaPlay, x1, y1)
            self.shops.append(pnj.shop)
            self.pnjs.append(pnj)

            ##print("pnj : ", self.pnjCooDico)
            ##print("CaseNoire : ", self.map.CaseNoire)

            # self.map.CaseNoire.pop(randomPNJ)
        ###print(self.shops)
        # for i in range(0, len(self.pnjs)):
        ###print(self.areaPlay.coords(self.pnjs[i].pnj))

    def generateMonsters(self, num_monsters):
        self.monsters = []  # Liste pour stocker les monstres
        min_x = 0
        max_x = self.map.map_width - 50
        min_y = 0
        max_y = self.map.map_height - 50

        for _ in range(num_monsters):
            monster = Monster(self.levelMap)  # Crée une instance de monstre

            emplacement = False
            emplacementOK = True
            while not emplacement:
                cooM = random.randint(0, len(list(self.map.dicoC)) - 1)
                ###print(self.map.dicoC)
                ###print(cooM)
                x1 = self.map.dicoC[cooM][0]
                y1 = self.map.dicoC[cooM][1]
                while self.checkMonsterInView(x1, y1):
                    cooM = random.randint(0, len(list(self.map.dicoC)))
                    x1 = self.map.dicoC[cooM][0]
                    y1 = self.map.dicoC[cooM][1]
                for cle, valeur in self.map.CaseNoire.items():
                    if (
                        x1 + +WindowParameter.characterSize > valeur[0]
                        and y1 + WindowParameter.characterSize > valeur[1]
                        and x1 < valeur[2]
                        and y1 < valeur[3]
                    ):
                        emplacementOK = False
                if emplacementOK:
                    emplacement = True
                emplacementOK = True
            """##print(x1, y1, x1 + 30, y1 + 30)"""

            # Génère le carré noir du monstre dans l'areaPlay à la position aléatoire
            monster.generateMonster(self.areaPlay, x1, y1)
            self.monsterDico[self.indexMonster] = [
                x1,
                y1,
                x1 + WindowParameter.tileSize - 1,
                y1 + WindowParameter.tileSize - 1,
            ]
            self.indexMonster += 1
            self.monsters.append(monster)  # Ajoute le monstre à la liste
        ###print("coo ===========",self.monsterDico)

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
        self.monsterDico = {}
        self.moved_m_index = 0
        # self.monster.moveMonster(self.areaPlay, self.view_x1, self.view_y1, self.view_x2, self.view_y2, self.character_x, self.character_y, self.character_x2, self.character_x1, self.character_y2, self.character_y1)
        if self.player_collision == False:
            # print("continue ?")
            for monster in self.monsters:
                monster.moveMonster(
                    self.areaPlay,
                    self.view_x1,
                    self.view_y1,
                    self.view_x2,
                    self.view_y2,
                    self.character_x,
                    self.character_y,
                    self.character_x2,
                    self.character_x1,
                    self.character_y2,
                    self.character_y1,
                    self,
                    self.map,
                )
                if self.playerDied == True :
                    break
                monster_coords = self.areaPlay.coords(monster.monster)
                self.monsterDico[self.moved_m_index] = [
                    monster_coords[0],
                    monster_coords[1],
                    monster_coords[2],
                    monster_coords[3],
                ]
                self.moved_m_index += 1
                

        # self.areaPlay.after(800, self.move_monster_periodically)

    def checkPNJCollision(self, i, dx, dy):
        self.cooPNJ = self.areaPlay.coords(self.pnjs[i].pnj)
        self.pnj_x = (
            self.cooPNJ[0] + self.cooPNJ[2]
        ) / 2  # Coordonnée x du centre du rectangle rouge
        self.pnj_y = (
            self.cooPNJ[1] + self.cooPNJ[3]
        ) / 2  # Coordonnée y du centre du rectangle rouge

        self.pnj_x1 = self.cooPNJ[0]
        self.pnj_y1 = self.cooPNJ[1]
        self.pnj_x2 = self.cooPNJ[2]
        self.pnj_y2 = self.cooPNJ[3]
        if (
            self.character_x1 + dx < self.pnj_x2
            and self.character_x2 + dx > self.pnj_x1
        ) and (
            self.character_y1 + dy < self.pnj_y2
            and self.character_y2 + dy > self.pnj_y1
        ):
            ###print("open shop")
            self.numPNJ = i
            self.collPNJ = True
            ###print("pnj num : ", self.numPNJ)
            self.eventJoueur("Shop open")
            self.pnjs[i].openShop(self.window, self, self.collPNJ)
            return True
        else:
            return False

    def checkMonsterCollision(self, i, dx, dy):
        self.monsterCOO = self.areaPlay.coords(self.monsters[i].monster)
        self.monster_x = (
            self.monsterCOO[0] + self.monsterCOO[2]
        ) / 2  # Coordonnée x du centre du rectangle rouge
        self.monster_y = (
            self.monsterCOO[1] + self.monsterCOO[3]
        ) / 2  # Coordonnée y du centre du rectangle rouge

        self.monster_x1 = self.monsterCOO[0]
        self.monster_y1 = self.monsterCOO[1]
        self.monster_x2 = self.monsterCOO[2]
        self.monster_y2 = self.monsterCOO[3]
        if (
            self.character_x1 + dx < self.monster_x2
            and self.character_x2 + dx > self.monster_x1
        ) and (
            self.character_y1 + dy < self.monster_y2
            and self.character_y2 + dy > self.monster_y1
        ):
            return True
        else:
            return False
        
            
##########################################################################
# Item functions
# Why they are here? Because implenting from another class within inputs has
# conflicts with bind_tag click ¯\_(ツ)_/¯
    def healthRestore_potion(self,event):
        if(self.inventory[self.potion_pv] > 0):
            self.life_point += Items.healthAmount
            if(self.life_point > self.max_life_point):
                self.life_point = self.max_life_point
            self.inventory[self.potion_pv] -= 1
        else:
            pass

##########################################################################

    def player_info(self):
        map_width = WindowParameter.mapWidth
        map_height = WindowParameter.mapHeight
        screen_width = WindowParameter.screenWidth
        x1 = map_width
        x2 = screen_width
        y2 = screen_width

        # Barre de vie
        player_imageI = Image.open("./sprites/knight_f_idle_anim_f0.png").convert("P")
        pImage_width, pImage_height = player_imageI.size
        player_imageI = player_imageI.resize(
            (
                pImage_width * WindowParameter.SCALE,
                pImage_height * WindowParameter.SCALE,
            )
        )
        self.player_photoI = ImageTk.PhotoImage(player_imageI)
        self.areaPlay.create_rectangle(
            x1, 0, x2, y2, fill="black", outline="red", dash=(3, 5)
        )
        self.areaPlay.create_image(
            map_width + 50, WindowParameter.tileSize + 10, image=self.player_photoI
        )

        

        # Money / XP / Lv
        self.areaPlay.create_rectangle(x1 + 20, 100, x1 + 310, 140, fill="white")
        self.areaPlay.create_rectangle(
            x1 + 20, 100, x1 + 123, 140, fill="black", outline="white"
        )

        gold_image = Image.open("./sprites/roguelikeitems.png").convert("P")
        gImage_width, gImage_height = gold_image.size
        gold_image = gold_image.resize(
            (
                gImage_width * WindowParameter.SCALE,
                gImage_height * WindowParameter.SCALE,
            )
        )
        self.gold_photo = ImageTk.PhotoImage(gold_image)

        self.areaPlay.create_image(x1 + 48, 120, image=self.gold_photo)
        self.areaPlay.create_text(
            x1 + 70,
            125,
            text=self.gold,
            fill="white",
            font=("Press Start 2P", 12),
            anchor="w"
        )

        self.areaPlay.create_rectangle(
            x1 + 127, 100, x1 + 230, 140, fill="black", outline="white"
        )
        self.areaPlay.create_text(
            x1 + 140,
            125,
            text="XP:",
            fill="white",
            font=("Press Start 2P", 12),
            anchor="w"
        )
        self.areaPlay.create_text(
            x1 + 190,
            125,
            text=self.xp,
            fill="white",
            font=("Press Start 2P", 12),
            anchor="w"
        )

        self.areaPlay.create_rectangle(
            x1 + 234, 100, x1 + 337, 140, fill="black", outline="white"
        )
        self.areaPlay.create_text(
            x1 + 240,
            125,
            text="LVL:",
            fill="white",
            font=("Press Start 2P", 12),
            anchor="w"
        )
        self.areaPlay.create_text(
            x1 + 305,
            125,
            text=self.PlayerLevel,
            fill="white",
            font=("Press Start 2P", 12),
            anchor="w"
        )

        # Monsters infos
        self.areaPlay.create_text(x1 + 45, 195, text="North", fill="white", font=("Press Start 2P", 11))
        self.areaPlay.create_rectangle(x1 + 3, 200, x1 + 88, 340, fill="")
        self.areaPlay.create_rectangle(
            x1 + 3, 200, x1 + 88, 250, fill="", outline="white"
        )
        self.areaPlay.create_rectangle(
            x1 + 3, 250, x1 + 88, 295, fill="", outline="white"
        )
        self.areaPlay.create_rectangle(
            x1 + 3, 295, x1 + 88, 340, fill="", outline="white"
        )
        
        self.areaPlay.create_text(x1 + 131, 195, text="East", fill="white", font=("Press Start 2P", 11))
        self.areaPlay.create_rectangle(x1 + 89, 200, x1 + 174, 340, fill="")
        self.areaPlay.create_rectangle(
            x1 + 89, 200, x1 + 174, 250, fill="", outline="white"
        )
        self.areaPlay.create_rectangle(
            x1 + 89, 250, x1 + 174, 295, fill="", outline="white"
        )
        self.areaPlay.create_rectangle(
            x1 + 89, 295, x1 + 174, 340, fill="", outline="white"
        )

        self.areaPlay.create_text(x1 + 217, 195, text="South", fill="white", font=("Press Start 2P", 11))
        self.areaPlay.create_rectangle(x1 + 175, 200, x1 + 260, 340, fill="")
        self.areaPlay.create_rectangle(
            x1 + 175, 200, x1 + 260, 250, fill="", outline="white"
        )
        self.areaPlay.create_rectangle(
            x1 + 175, 250, x1 + 260, 295, fill="", outline="white"
        )
        self.areaPlay.create_rectangle(
            x1 + 175, 295, x1 + 260, 340, fill="", outline="white"
        )

        self.areaPlay.create_text(x1 + 306, 195, text="West", fill="white", font=("Press Start 2P", 11))
        self.areaPlay.create_rectangle(x1 + 261, 200, x1 + 346, 340, fill="")
        self.areaPlay.create_rectangle(
            x1 + 261, 200, x1 + 346, 250, fill="", outline="white"
        )
        self.areaPlay.create_rectangle(
            x1 + 261, 250, x1 + 346, 295, fill="", outline="white"
        )
        self.areaPlay.create_rectangle(
            x1 + 261, 295, x1 + 346, 340, fill="", outline="white"
        )
        # the low border of the monster information: X: x1 + 3   Y: 340
        #                                            X: x1 + 346 Y:

        # The battle information
        self.areaPlay.create_rectangle(x1 + 3, 380, x1+346, 495, fill="", outline="white")
        # TBC

        # The storage of items
        # Start at Y :  WindowParameter.screenHeight - 150
        # End at Y : y_item_top_aera + 100

        map_width = WindowParameter.mapWidth
        map_height = WindowParameter.mapHeight
        screen_width = WindowParameter.screenWidth
        x1 = map_width
        x2 = screen_width
        y2 = screen_width
        lineX = x1 + 3
        max_x = x1 + 346
        item_grid_size = 70
        item_image_size = 64
        y_item_top_aera = WindowParameter.screenHeight - 150

        self.areaPlay.create_rectangle(
            x1 + 3, y_item_top_aera, x1 + 346, y_item_top_aera + 100, fill="", outline="white"
        )
        # The square for display items
        for i in range(lineX, max_x, item_grid_size):
            self.areaPlay.create_line(
                i, y_item_top_aera, i, y_item_top_aera + 100, fill="white", width=3
            )

        # First slot for potion PV
        image_item = Image.open("./sprites/potion_PV.png").convert("P")
        image_item = image_item.resize((item_grid_size, item_grid_size))
        self.image_potion_pv = ImageTk.PhotoImage(image_item)
        self.areaPlay.create_image(
            lineX, y_item_top_aera, image=self.image_potion_pv , anchor = "nw"
        )
        # Second slot for potion MP
        image_item = Image.open("./sprites/potion_MP.png").convert("P")
        image_item = image_item.resize((item_grid_size, item_grid_size))
        self.image_potion_mp = ImageTk.PhotoImage(image_item)
        self.areaPlay.create_image(
            lineX + item_grid_size * 1, y_item_top_aera, image=self.image_potion_mp , anchor = "nw"
        )

        # The square for showing the storage of the items
        # for i in range(2):
        #     self.areaPlay.create_rectangle(
        #         lineX + i * item_grid_size, y_item_top_aera, lineX + i * item_grid_size + 20, y_item_top_aera + 20, outline="white"
        #     )

        #Storage potion PV
        self.areaPlay.create_text(
            lineX +5,
            y_item_top_aera+5,
            text=self.inventory[self.potion_pv],
            fill="white",
            font=("Press Start 2P", 10),
            anchor="nw"
        )
        #Storage potion MP
        self.areaPlay.create_text(
            lineX + item_grid_size + 5,
            y_item_top_aera + 5,
            text=self.inventory[self.potion_mp],
            fill="white",
            font=("Press Start 2P", 10),
            anchor="nw"
        )
#################################################################################################################

        # Third slot for weapon
        text = f"./sprites/{self.weapon}.png"
        image_item = Image.open(text).convert("P")
        image_item = image_item.resize((item_grid_size, item_grid_size))
        self.image_weapon = ImageTk.PhotoImage(image_item)
        self.areaPlay.create_image(
            lineX + item_grid_size * 2, y_item_top_aera, image=self.image_weapon , anchor = "nw"
        )


        # Fourth slot for armor
        text = f"./sprites/{self.armor}.png"
        image_item = Image.open(text).convert("P")
        image_item = image_item.resize((item_grid_size, item_grid_size))
        self.image_armor = ImageTk.PhotoImage(image_item)
        self.areaPlay.create_image(
            lineX + item_grid_size * 3, y_item_top_aera, image=self.image_armor , anchor = "nw"
        )
#################################################################################################################
        # Last slot for key
        # X: lineX + item_grid_size * 4
        if(self.hasExitKey):
            image_item = Image.open("./sprites/key_1.png").convert("P")
        else:
            image_item = Image.open("./sprites/key_1_empty.png").convert("P")
        
        image_item = image_item.resize((item_image_size, item_image_size))
        self.image_key = ImageTk.PhotoImage(image_item)
        self.areaPlay.create_image(
            lineX + item_grid_size * 4, y_item_top_aera, image=self.image_key, anchor = "nw"
        )
        
#################################################################################################################
        # Lower Slot
        # Y: y_item_top_aera + item_grid_size
        self.areaPlay.create_line(
            lineX, y_item_top_aera + item_grid_size,
            max_x, y_item_top_aera + item_grid_size,
            fill="white",
            width=3
        )

        
        # First lower slot: potion PV

        # self.areaPlay.create_rectangle(
        #     lineX,
        #     y_item_top_aera + item_grid_size,
        #     lineX + item_grid_size,
        #     y_item_top_aera + item_grid_size + 30,
        #     fill="black"
        # )

        use_btn_pv = self.areaPlay.create_text(
            lineX + 10,
            y_item_top_aera + item_grid_size + 20,
            text="USE",
            fill="white",
            font=("Press Start 2P", 12),
            anchor="w"
        )

        self.areaPlay.tag_bind(use_btn_pv, '<Button-1>', self.healthRestore_potion)

        # Second lower slot: potion PV
        self.areaPlay.create_text(
            lineX + item_grid_size + 10,
            y_item_top_aera + item_grid_size + 20,
            text="USE",
            fill="white",
            font=("Press Start 2P", 12),
            anchor="w"
        )
#################################################################################################################
        # Third lower slot: weapon
        self.areaPlay.create_text(
            lineX + item_grid_size * 2 + 10,
            y_item_top_aera + item_grid_size + 20,
            text="ATK",
            fill="white",
            font=("Press Start 2P", 12),
            anchor="w"
        )

        # Fourth lower slot: armor
        self.areaPlay.create_text(
            lineX + item_grid_size * 3 + 10,
            y_item_top_aera + item_grid_size + 20,
            text="DEF",
            fill="white",
            font=("Press Start 2P", 12),
            anchor="w"
        )

        # Last lower slot: KEY
        self.areaPlay.create_text(
            lineX + item_grid_size * 4 + 10,
            y_item_top_aera + item_grid_size + 20,
            text="KEY",
            fill="white",
            font=("Press Start 2P", 12),
            anchor="w"
        )


    def hp_update(self, textThere):
        print(self.life_point)

        if self.life_point <= 25:
            self.areaPlay.delete(self.text_health)
            self.areaPlay.delete(self.health_bar)
            self.text_health = self.areaPlay.create_text(WindowParameter.mapWidth + 83,  WindowParameter.tileSize+17, text=(str(0)), fill="white", font=("Press Start 2P", 12))
            print("Dead")
            
            self.dead()
        else:
            if textThere == True:
                self.areaPlay.delete(self.text_health)
                self.areaPlay.delete(self.health_bar)
            self.health_percent = self.life_point/self.max_life_point
            self.bar_width = self.health_percent * 300
            self.health_bar = self.areaPlay.create_rectangle(WindowParameter.mapWidth + 80,  WindowParameter.tileSize, WindowParameter.mapWidth+ self.bar_width, WindowParameter.tileSize + 30, fill="red")
            self.text_health = self.areaPlay.create_text(WindowParameter.mapWidth + self.bar_width+20,  WindowParameter.tileSize+17, text=(str(self.life_point-25)), fill="white", font=("Press Start 2P", 12))
        
    def mana_update(self, textThere):
        print(self.mana)
        if self.mana >= 5:
            if textThere == True:
                self.areaPlay.delete(self.text_mana)
                self.areaPlay.delete(self.mana_bar)
            self.mana_percent = self.mana/self.max_mana
            self.bar_mana_width = self.mana_percent * 300
            self.mana_bar = self.areaPlay.create_rectangle(WindowParameter.mapWidth + 80,  WindowParameter.tileSize + 40, WindowParameter.mapWidth+ self.bar_mana_width, WindowParameter.tileSize + 50, fill="blue")
            self.text_mana = self.areaPlay.create_text(WindowParameter.mapWidth + self.bar_mana_width+20,  WindowParameter.tileSize+50, text=(str(self.mana)), fill="white", font=("Press Start 2P", 12))
        else:
            self.text_mana = self.areaPlay.create_text(WindowParameter.mapWidth + 80,  WindowParameter.tileSize+50, text=(str(0)), fill="white", font=("Press Start 2P", 12))
        
    def dead(self):
        self.reset()
        with open('save.json', 'w') as fichier:
            fichier.truncate(0)
        self.areaPlay.unbind("<KeyPress>")
        self.playerDied = True
        self.blackScreen = self.areaPlay.create_rectangle(0, 0, WindowParameter.screenWidth, WindowParameter.screenHeight, outline="black")
        """self.died = self.areaPlay.create_text(WindowParameter.screenWidth / 2, WindowParameter.screenHeight / 2, text="You died", fill="Red", font=("Press Start 2P", 16), anchor="center")
        self.buttonNewG = tk.Button(self.window, text="New Game", command=self.newGame)"""

        self.text = tk.Label(self.window, text="You died", font=("Press Start 2P", 16), fg="red", bg="black")
        self.text.place(x=WindowParameter.screenWidth / 2, y=WindowParameter.screenHeight / 2, anchor="center")
        
        # Création du bouton
        self.button = tk.Button(self.window, text="New Game", command=self.newGame)
        self.button.place(x=WindowParameter.screenWidth / 2, y=WindowParameter.screenHeight / 2 + 30, anchor="center")

        self.menuButton = tk.Button(self.window, text="Menu", command=self.menu)
        self.menuButton.place(x=WindowParameter.screenWidth / 2, y=WindowParameter.screenHeight / 2 + 60, anchor="center")

    def menu(self):
        self.text.destroy()
        self.button.destroy()
        self.menuButton.destroy()
        self.areaPlay.delete("all")
        self.areaPlay.destroy()
        self.reset()
        print("test1")
        self.interface.backtomenu()
        print("test2")

    def newGame(self):
        self.text.destroy()
        # Pour supprimer le bouton
        self.button.destroy()
        self.menuButton.destroy()
        self.areaPlay.delete("all")
        self.reset()
        self.createAll()

    def eventJoueur(self, text):
        if self.EJ == True:
            self.areaPlay.delete(self.eventJoueurtxt)
            self.EJ = False
        map_width = WindowParameter.mapWidth
        map_height = WindowParameter.mapHeight
        screen_width = WindowParameter.screenWidth
        x1 = map_width
        x2 = screen_width
        y2 = screen_width

        self.eventJoueurtxt = self.areaPlay.create_text(x1 + 9, 395, text=text, fill="white",font=("Press Start 2P", 9),  anchor="w")
        self.EJ = True

    def eventMonster(self, text):
        if self.E == True:
            self.areaPlay.delete(self.eventMonstertxt)
            self.E = False
        map_width = WindowParameter.mapWidth
        map_height = WindowParameter.mapHeight
        screen_width = WindowParameter.screenWidth
        x1 = map_width
        x2 = screen_width
        y2 = screen_width

        self.eventMonstertxt = self.areaPlay.create_text(x1 + 9, 410, text=text, fill="white",font=("Press Start 2P", 9),  anchor="nw")
        self.E = True

    def eventMonsterAttack(self, direction):
        self.eventMAVar = True
        if self.EA == True:
            self.areaPlay.delete(self.eventMonsterAttacktxt)
            self.EA = False
        if self.E == True:
            self.areaPlay.delete(self.eventMonstertxt)
            self.E = False
        map_width = WindowParameter.mapWidth
        map_height = WindowParameter.mapHeight
        screen_width = WindowParameter.screenWidth
        x1 = map_width
        x2 = screen_width
        y2 = screen_width

        if direction == "n":
            self.text = self.text+"\n"+"\t-Attack from north"
            #print( self.text)
        if direction == "e":
            self.text = self.text+"\n"+"\t-Attack from east"
            #print( self.text)
        if direction == "s":
            self.text = self.text+"\n"+"\t-Attack from south"
            #print( self.text)
        if direction == "w":
            self.text = self.text+"\n"+"\t-Attack from west"
            #print( self.text)

        self.eventMonsterAttacktxt = self.areaPlay.create_text(x1 + 9, 410, text= self.text, fill="white",font=("Press Start 2P", 9),  anchor="nw")
        self.EA = True

    def update_infoPN(self):
        #print(self.fullMonster)
        map_width = WindowParameter.mapWidth
        map_height = WindowParameter.mapHeight
        screen_width = WindowParameter.screenWidth
        x1 = map_width
        x2 = screen_width
        y2 = screen_width

        monsterN_image = Image.open(self.fullMonster["n"][0]).convert("P")
        mNImage_width,mNImage_height = monsterN_image.size
        monsterN_image = monsterN_image.resize((mNImage_width,mNImage_height))
        self.monsterN_photo = ImageTk.PhotoImage(monsterN_image)
        self.areaPlay.create_image(x1 + 47, 220, image = self.monsterN_photo)
        self.areaPlay.create_text(x1 + 47, 275, text=self.fullMonster["n"][1], fill="white",font=("Press Start 2P", 12), anchor="w")
        self.areaPlay.create_text(x1 + 47, 320, text=self.fullMonster["n"][2], fill="white",font=("Press Start 2P", 12), anchor="w")

    def update_infoPE(self):
        #print(self.fullMonster)
        map_width = WindowParameter.mapWidth
        map_height = WindowParameter.mapHeight
        screen_width = WindowParameter.screenWidth
        x1 = map_width
        x2 = screen_width
        y2 = screen_width

        monsterE_image = Image.open(self.fullMonster["e"][0]).convert("P")
        mEImage_width,mEImage_height = monsterE_image.size
        monsterE_image = monsterE_image.resize((mEImage_width ,mEImage_height))
        self.monsterE_photo = ImageTk.PhotoImage(monsterE_image)
        self.areaPlay.create_image(x1 + 133, 220, image = self.monsterE_photo)
        self.areaPlay.create_text(x1 + 133, 275, text=self.fullMonster["e"][1], fill="white",font=("Press Start 2P", 12), anchor="w")
        self.areaPlay.create_text(x1 + 133, 320, text=self.fullMonster["e"][2], fill="white",font=("Press Start 2P", 12), anchor="w")

    def update_infoPS(self):
        #print(self.fullMonster)
        map_width = WindowParameter.mapWidth
        map_height = WindowParameter.mapHeight
        screen_width = WindowParameter.screenWidth
        x1 = map_width
        x2 = screen_width
        y2 = screen_width

        monsterS_image = Image.open(self.fullMonster["s"][0]).convert("P")
        mSImage_width,mSImage_height = monsterS_image.size
        monsterS_image = monsterS_image.resize((mSImage_width,mSImage_height))
        self.monsterS_photo = ImageTk.PhotoImage(monsterS_image)
        self.areaPlay.create_image(x1 + 219, 220, image = self.monsterS_photo)
        self.areaPlay.create_text(x1 + 219, 275, text=self.fullMonster["s"][1], fill="white",font=("Press Start 2P", 12), anchor="w")
        self.areaPlay.create_text(x1 + 219, 320, text=self.fullMonster["s"][2], fill="white",font=("Press Start 2P", 12), anchor="w")
        
    def update_infoPW(self):
        #print(self.fullMonster)
        map_width = WindowParameter.mapWidth
        map_height = WindowParameter.mapHeight
        screen_width = WindowParameter.screenWidth
        x1 = map_width
        x2 = screen_width
        y2 = screen_width

        monsterW_image = Image.open(self.fullMonster["w"][0]).convert("P")
        mWImage_width,mWImage_height = monsterW_image.size
        monsterW_image = monsterW_image.resize((mWImage_width,mWImage_height))
        self.monsterW_photo = ImageTk.PhotoImage(monsterW_image)
        self.areaPlay.create_image(x1 + 305, 220, image = self.monsterW_photo)
        self.areaPlay.create_text(x1 + 305, 275, text=self.fullMonster["w"][1], fill="white",font=("Press Start 2P", 12), anchor="w")
        self.areaPlay.create_text(x1 + 305, 320, text=self.fullMonster["w"][2], fill="white",font=("Press Start 2P", 12), anchor="w")

    def Fight(self):
        #print("Event joueur : Le joueur attaque")
        
        attack = self.areaPlay.coords(self.attackRect)
        attack_x1 = attack[0]
        attack_y1 = attack[1]
        attack_x2 = attack[2]
        attack_y2 = attack[3]
        i = 0
        pop = False
        while i < len(self.monsters) and pop == False:
            monsterCOO = self.areaPlay.coords(self.monsters[i].monster)
            monster_x1 = monsterCOO[0]
            monster_y1 = monsterCOO[1]
            monster_x2 = monsterCOO[2]
            monster_y2 = monsterCOO[3]
            if (
                attack_x2 >= monster_x1
                and attack_x1 <= monster_x2
                and attack_y2 >= monster_y1
                and attack_y1 <= monster_y2
            ):
                self.monsters[i].life_points_monster = (
                    self.monsters[i].life_points_monster - self.damage
                )

                if self.monsters[i].life_points_monster <= 0:
                    self.areaPlay.delete(self.monsters[i].health_bar)
                    self.areaPlay.delete(self.monsters[i].monster)

                    self.xp = self.xp + (self.monsters[i].xp - self.PlayerLevel * 2)
                    if self.xp <= 0:
                        self.xp = self.xp + 1
                    if self.xp >= 50:
                        self.PlayerLevel = self.PlayerLevel + 1
                        self.life_point = self.life_point + 3
                        self.damage = self.damage + 3
                        self.xp = 0
                    self.gold = self.monsters[i].xp + self.gold
                    pop = True
                    self.monsters.pop(i)
                else:
                    self.monsters[i].update_healthBar(
                        self.areaPlay, monster_x1, monster_y1
                    )

            i += 1
    
    def Sort(self):
        #print("Event joueur : Le joueur attaque")
        self.mana = self.mana - 5
        self.mana_update(True)
        if self.mana < 0:
            self.mana = 0
        attackR = self.areaPlay.coords(self.attackRectR)
        attack_x1R = attackR[0]
        attack_y1R = attackR[1]
        attack_x2R = attackR[2]
        attack_y2R = attackR[3]
        attackL = self.areaPlay.coords(self.attackRectL)
        attack_x1L = attackL[0]
        attack_y1L = attackL[1]
        attack_x2L = attackL[2]
        attack_y2L = attackL[3]
        attackU = self.areaPlay.coords(self.attackRectU)
        attack_x1U = attackU[0]
        attack_y1U = attackU[1]
        attack_x2U = attackU[2]
        attack_y2U = attackU[3]
        attackD = self.areaPlay.coords(self.attackRectD)
        attack_x1D = attackD[0]
        attack_y1D = attackD[1]
        attack_x2D = attackD[2]
        attack_y2D = attackD[3]
        i = 0
        pop = False
        while i < len(self.monsters) and pop == False:
            monsterCOO = self.areaPlay.coords(self.monsters[i].monster)
            monster_x1 = monsterCOO[0]
            monster_y1 = monsterCOO[1]
            monster_x2 = monsterCOO[2]
            monster_y2 = monsterCOO[3]
            if (
                attack_x2R >= monster_x1
                and attack_x1R <= monster_x2
                and attack_y2R >= monster_y1
                and attack_y1R <= monster_y2
            ) or (
                attack_x2L >= monster_x1
                and attack_x1L <= monster_x2
                and attack_y2L >= monster_y1
                and attack_y1L <= monster_y2
            ) or (
                attack_x2U >= monster_x1
                and attack_x1U <= monster_x2
                and attack_y2U >= monster_y1
                and attack_y1U <= monster_y2
            )or (
                attack_x2D >= monster_x1
                and attack_x1D <= monster_x2
                and attack_y2D >= monster_y1
                and attack_y1D <= monster_y2
            ):
                ###print(self.monsters[i].life_points_monster)
                self.monsters[i].life_points_monster = (
                    self.monsters[i].life_points_monster - self.damageSpell
                )

                ###print(self.monsters[i].life_points_monster)

                if self.monsters[i].life_points_monster <= 0:
                    self.areaPlay.delete(self.monsters[i].health_bar)
                    self.areaPlay.delete(self.monsters[i].monster)

                    self.xp = self.xp + (self.monsters[i].xp - self.PlayerLevel * 2)
                    if self.xp <= 0:
                        self.xp = self.xp + 1
                    if self.xp >= 50:
                        self.PlayerLevel = self.PlayerLevel + 1
                        self.life_point = self.life_point + 3
                        self.damage = self.damage + 3
                        self.damageSpell = self.damageSpell + 2
                        self.xp = 0
                    self.gold = self.monsters[i].xp + self.gold
                    pop = True
                    # #print("Level : ", self.PlayerLevel)
                    # #print("Xp : ", self.xp)
                    # #print("Gold : ", self.gold)
                    self.monsters.pop(i)
                else:
                    self.monsters[i].update_healthBar(
                        self.areaPlay, monster_x1, monster_y1
                    )

            i += 1
    

    def collisionWithMonster(self):
        tolerance = 6
        ci = self.areaPlay.coords(self.character_id)
        for i in range(len(self.monsters)):
            monsterCOO = self.areaPlay.coords(self.monsters[i].monster)
            if ci[2] + tolerance >= monsterCOO[0] and ci[0] <= monsterCOO[2] + tolerance:
                if ci[3] + tolerance >= monsterCOO[1] and ci[1] <= monsterCOO[3] + tolerance:
                    #print("Collision avec le monstre", i)
                    if ci[0] > monsterCOO[2] and ci[0] > monsterCOO[2] and ci[1] == monsterCOO[1] and ci[3] == monsterCOO[3]:
                        #print("W")
                        self.fullMonster["w"] = ["./sprites/monster_1.png", self.monsters[i].life_points_monster, self.monsters[i].damage]
                    elif ci[2] < monsterCOO[0] and ci[2] < monsterCOO[2] and ci[1] == monsterCOO[1] and ci[3] == monsterCOO[3]:
                        #print("E")
                        self.fullMonster["e"] = ["./sprites/monster_1.png", self.monsters[i].life_points_monster, self.monsters[i].damage]
                    elif ci[0] == monsterCOO[0] and ci[2] == monsterCOO[2] and ci[1] > monsterCOO[1] and ci[1] > monsterCOO[3]:
                        #print("N")
                        self.fullMonster["n"] = ["./sprites/monster_1.png", self.monsters[i].life_points_monster, self.monsters[i].damage]
                    elif ci[0] == monsterCOO[0] and ci[2] == monsterCOO[2] and ci[3] < monsterCOO[1] and ci[3] < monsterCOO[3]:
                        #print("S")
                        self.fullMonster["s"] = ["./sprites/monster_1.png", self.monsters[i].life_points_monster, self.monsters[i].damage]


    def move_character(self, event):
        eventJoueur = False
        self.countTourActivate = False
        self.countTourActivateSort = False
        key = event.keysym
        if key == "Escape" and not self.collPNJ:
            self.collPNJ = True
            self.escape.createEscap(self.window,self)

        elif (self.playerDied == False) and (not self.collPNJ):
            if self.tourPlayer :
                if key == "a":
                        if self.attackDirection == "Right":
                            ##print("direction attack right")
                            taille_cote = WindowParameter.characterSize  # Taille du côté du carré principal
                            taille_secondaire = 8  # Taille du côté du carré secondaire

                            x1 = self.character_x2  # Coordonnée x1 du carré secondaire
                            y1 = self.character_y1 + (taille_cote - taille_secondaire) / 2  # Coordonnée y1 du carré secondaire
                            x2 = x1 + taille_secondaire  # Coordonnée x2 du carré secondaire
                            y2 = y1 + taille_secondaire  # Coordonnée y2 du carré secondaire

                            self.attackRect = self.areaPlay.create_rectangle(x1, y1, x2+8, y2, fill="blue")
                            self.Fight()
                            self.window.after(100, lambda: self.areaPlay.delete(self.attackRect))

                            self.countTourActivate = True
                            
                        elif self.attackDirection == "Left":
                            ##print("direction attack Left")
                            taille_cote = WindowParameter.characterSize  # Taille du côté du carré principal
                            taille_secondaire = 8  # Taille du côté du carré secondaire

                            x2 = self.character_x1  # Coordonnée x1 du carré secondaire
                            y1 = self.character_y1 + (taille_cote - taille_secondaire) / 2  # Coordonnée y1 du carré secondaire
                            x1 = x2 - taille_secondaire  # Coordonnée x2 du carré secondaire
                            y2 = y1 + taille_secondaire  # Coordonnée y2 du carré secondaire

                            self.attackRect = self.areaPlay.create_rectangle(x1-8, y1, x2, y2, fill="blue")
                            self.Fight()
                            self.window.after(100, lambda: self.areaPlay.delete(self.attackRect))

                            self.countTourActivate = True  # Désactive le cooldown après 2000 millisecondes (2 secondes)
                            
                        elif self.attackDirection == "Up":
                            ##print("direction attack Up")
                            taille_cote = WindowParameter.characterSize  # Taille du côté du carré principal
                            taille_secondaire = 8  # Taille du côté du carré secondaire

                            x1 = self.character_x1 + (taille_cote - taille_secondaire) / 2
                            x2 = x1 + taille_secondaire
                            y2 = self.character_y1 # Coordonnée y2 du carré secondaire
                            y1 = y2 - taille_secondaire
                            

                            self.attackRect = self.areaPlay.create_rectangle(x1, y1-8, x2, y2, fill="blue")
                            self.Fight()
                            self.window.after(100, lambda: self.areaPlay.delete(self.attackRect))
                            
                            self.countTourActivate = True
                        
                        elif self.attackDirection == "Down":
                            ##print("direction attack Down")
                            taille_cote = WindowParameter.characterSize  # Taille du côté du carré principal
                            taille_secondaire = 8  # Taille du côté du carré secondaire

                            x1 = self.character_x1 + (taille_cote - taille_secondaire) / 2 # Coordonnée x1 du carré secondaire
                            y1 = self.character_y2  # Coordonnée y1 du carré secondaire
                            x2 = x1 + taille_secondaire  # Coordonnée x2 du carré secondaire
                            y2 = y1 + taille_secondaire  # Coordonnée y2 du carré secondaire

                            self.attackRect = self.areaPlay.create_rectangle(x1, y1, x2, y2+8, fill="blue")
                            self.Fight()
                            self.window.after(100, lambda: self.areaPlay.delete(self.attackRect))
                            
                            self.countTourActivate = True
                        self.window.after(200, self.start_moving_monsters)

                elif key == "s" and self.mana >= 5:
                            ##print("direction attack right")
                            taille_cote = WindowParameter.characterSize  # Taille du côté du carré principal
                            taille_secondaire = 8  # Taille du côté du carré secondaire

                            x1R = self.character_x2  # Coordonnée x1 du carré secondaire
                            y1R = self.character_y1 + (taille_cote - taille_secondaire) / 2  # Coordonnée y1 du carré secondaire
                            x2R = x1R + taille_secondaire  # Coordonnée x2 du carré secondaire
                            y2R = y1R + taille_secondaire  # Coordonnée y2 du carré secondaire

                            x2L = self.character_x1  # Coordonnée x1 du carré secondaire
                            y1L = self.character_y1 + (taille_cote - taille_secondaire) / 2  # Coordonnée y1 du carré secondaire
                            x1L = x2L - taille_secondaire  # Coordonnée x2 du carré secondaire
                            y2L = y1L + taille_secondaire  # Coordonnée y2 du carré secondaire

                            x1U = self.character_x1 + (taille_cote - taille_secondaire) / 2
                            x2U = x1U + taille_secondaire
                            y2U = self.character_y1 # Coordonnée y2 du carré secondaire
                            y1U = y2U - taille_secondaire

                            x1D = self.character_x1 + (taille_cote - taille_secondaire) / 2 # Coordonnée x1 du carré secondaire
                            y1D = self.character_y2  # Coordonnée y1 du carré secondaire
                            x2D = x1D + taille_secondaire  # Coordonnée x2 du carré secondaire
                            y2D = y1D + taille_secondaire  # Coordonnée y2 du carré secondaire

                            self.attackRectR = self.areaPlay.create_rectangle(x1R, y1R, x2R+8, y2R, fill="red")
                            self.attackRectL = self.areaPlay.create_rectangle(x1L-8, y1L, x2L, y2L, fill="red")
                            self.attackRectU = self.areaPlay.create_rectangle(x1U, y1U-8, x2U, y2U, fill="red")
                            self.attackRectD = self.areaPlay.create_rectangle(x1D, y1D, x2D, y2D+8, fill="red")
                            self.Sort()

                            self.window.after(100, lambda: self.areaPlay.delete(self.attackRectR))
                            self.window.after(100, lambda: self.areaPlay.delete(self.attackRectL))
                            self.window.after(100, lambda: self.areaPlay.delete(self.attackRectU))
                            self.window.after(100, lambda: self.areaPlay.delete(self.attackRectD))

                            self.countTourActivateSort = True
                            
                            self.window.after(200, self.start_moving_monsters)
       

                #Player
                elif self.player_collision != True:
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
                                if(self.checkMonsterCollision(i, dx, dy)):
                                    return
                            self.getKey()
                            
                            if not self.gonext:
                                eventJoueur = True
                                self.areaPlay.move(self.character_id, dx, dy)  # Déplacer le personnage
                                self.areaPlay.move(self.sprite, dx, dy)
                                self.update_view()
                            self.goNextRoom()
                        self.window.after(100, self.start_moving_monsters)
            
            self.tourPlayer = False
            print("in p ",self.fullMonster)
            self.player_info()
            self.hp_update(True)
            self.mana_update(True)
            if self.eventNrVar == True:
                text =  "Player go to the next room"
                self.eventJoueur(text)
                self.eventNrVar = False
            elif self.eventKVar == True:
                text =  "Player get the key"
                print(text)
                self.eventJoueur(text)
                self.eventKVar = False
            elif eventJoueur == True:
                text = "Player walks"
                self.eventJoueur(text)
            elif self.countTourActivate == True:
                text = "Player attacks"
                self.eventJoueur(text)
            elif self.countTourActivateSort == True:
                text = "Player casts a spell"
                self.eventJoueur(text)
            print(self.text)
            self.eventMWalked = False
            self.eventMAVar = False
            self.text = "Monster :"
        
        

        
            
        

    def update_view(self):
        character_coords = self.areaPlay.coords(self.character_id)
        self.character_x = (
            character_coords[0] + character_coords[2]
        ) / 2  # Coordonnée x du centre du rectangle rouge
        self.character_y = (
            character_coords[1] + character_coords[3]
        ) / 2  # Coordonnée y du centre du rectangle rouge

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

        ###print("Player : x1 : ",self.view_x1," y1 : ",self.view_x2," x2 : ",self.view_x2," y2 : ",self.view_y2)

        self.areaPlay.create_rectangle(
            self.view_x1,
            self.view_y1,
            self.view_x2,
            self.view_y2,
            fill="",
            outline="white",
            tag="view",
        )

    def goNextRoom(self):
        ###print("nextRoom ?")
        if self.gonext:
            self.gonext = False
        elif (
            self.hasExitKey
            and self.character_x1 >= self.map.x1R
            and self.character_x2 <= self.map.x2R
            and self.character_y2 <= self.map.y2R
            and self.character_y1 >= self.map.y1R
        ):
            self.gonext = True
            #print("Event : Le joueur passe au prochain étage")
            self.eventNrVar = True
            ###print("Yes !")
            self.generateNewMap()

    def getKey(self):
        if (
            self.character_x1 < self.map.keyX2 and self.character_x2 > self.map.keyX1
        ) and (
            self.character_y1 < self.map.keyY2 and self.character_y2 > self.map.keyY1
        ):
            self.hasExitKey = True
            #print("Event : Le joueur ramasse la clé")
            self.eventKVar = True
            self.areaPlay.delete(self.map.key)
            ###print(self.inventory)

    def generateNewMap(self):
        # Supprime les éléments de la carte actuelle
        self.areaPlay.delete("all")

        # Génère une nouvelle carte
        self.createAll()

    def displayPJ(self):
        if self.classe == 0:
            return (
                "Classe : "
                + str(self.allClasse[self.classe])
                + "Life point : "
                + str(self.life_point)
                + "Damage : "
                + str(self.damage)
            )
        elif self.classe == 1:
            return (
                "Classe : "
                + str(self.allClasse[self.classe])
                + "Life point : "
                + str(self.life_point)
                + "Damage : "
                + str(self.damage)
                + "Range : "
                + str(self.range)
            )
        elif self.classe == 2:
            return (
                "Classe : "
                + str(self.allClasse[self.classe])
                + "Life point : "
                + str(self.life_point)
                + "Damage : "
                + str(self.damage)
                + "Range : "
                + str(self.range)
                + "Mana : "
                + str(self.mana)
            )
