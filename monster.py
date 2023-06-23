import math
import random
import tkinter as tk
from PIL import Image, ImageTk
import map
from windowParameters import WindowParameter

class Monster:
    
    def __init__(self, MapLevel) -> None:
        self.direction = [0, 1, 2, 3]
        self.monster_collision = False
        self.diag = False
        self.monster_positions = []  # Liste pour stocker les positions des monstres
        
        self.moveDistance = WindowParameter.tileSize

        if(MapLevel == 1):
            self.level = random.randint(1, 2)
        elif(MapLevel >= 2 and MapLevel <=4):
            self.level = random.randint(2,4)
        elif(MapLevel >= 5 and MapLevel <= 7):
            self.level = random.randint(5, 7)
        elif(MapLevel >= 8 and MapLevel <= 10):
            self.level = random.randint(8, 10)
        elif(MapLevel > 10):
            self.level = random.randint(10, 15)
        
        if(self.level <= 2):
            self.damage = 5
            self.life_points_monster_max = 50
            self.life_points_monster = 50
            self.xp = 10
            self.gold = 5
        elif(self.level <= 4 and self.level > 2):
            self.damage = 10
            self.life_points_monster_max = 70
            self.life_points_monster = 70
            self.xp = 10
            self.gold = 7
        elif(self.level <= 7 and self.level > 4):
            self.damage = 15
            self.life_points_monster_max = 90
            self.life_points_monster = 90
            self.xp = 10
            self.gold = 9
        elif(self.level <= 10 and self.level > 7):
            self.damage = 25
            self.life_points_monster_max = 100
            self.life_points_monster = 100
            self.xp = 10
            self.gold = 11
        elif(self.level > 10):
            self.damage = 30
            self.life_points_monster_max = 120
            self.life_points_monster = 120
            self.xp = 10
            self.gold = 12

    

    def generateMonster(self, areaPlay, x, y):
        self.monster = areaPlay.create_rectangle(x, y, x + WindowParameter.tileSize-1, y + WindowParameter.tileSize-1, fill="", outline = "")

        image_monster = Image.open("./sprites/monster_1.png").convert("P")
        image_monster = image_monster.resize((WindowParameter.tileSize, WindowParameter.tileSize))
        self.image_monster = ImageTk.PhotoImage(image_monster)
        self.monster_image = areaPlay.create_image(
           x, y, image = self.image_monster , anchor = "nw"
        )

        self.create_healthBar(areaPlay, x, y)
        self.monster_positions.append((x, y))  # Ajouter la position du monstre à la liste



    def create_healthBar(self, areaPlay, x, y):
        self.health_percent = self.life_points_monster/self.life_points_monster_max
        self.bar_width = self.health_percent * 31
        self.health_bar = areaPlay.create_rectangle(x, y+1, x + self.bar_width-1, y+4, fill="red")

    def update_healthBar(self, areaPlay, x, y):
        self.health_percent = self.life_points_monster/self.life_points_monster_max
        self.bar_width = self.health_percent * 31
        areaPlay.coords(self.health_bar, x, y+1, x + self.bar_width-1, y+4)

    def moveMonster(self, areaPlay, x1P, y1P, x2P, y2P, target_x, target_y, x2, x1, y2, y1, playerSelf, map):
        ci = areaPlay.coords(playerSelf.character_id)
        tolerance = 6
        self.antiInfinite = 0
        ok = False
        self.monster_coords = areaPlay.coords(self.monster)
        self.monster_x1 = self.monster_coords[0]
        self.monster_y1 = self.monster_coords[1]  
        self.monster_x2 = self.monster_coords[2]
        self.monster_y2 = self.monster_coords[3]
        ##print("Monster : x1 : ",self.monster_x1)
        

        self.current_x = (self.monster_coords[0] + self.monster_coords[2])/2
        self.current_y = (self.monster_coords[1] + self.monster_coords[3])/2

        black_center_x = (self.monster_x1 + self.monster_x2) // 2
        black_center_y = (self.monster_y1 + self.monster_y2) // 2
        red_center_x = (x1P + x2P) // 2
        red_center_y = (y1P + y2P) // 2

        if (red_center_x - black_center_x) != 0:
                slope = (red_center_y - black_center_y) / (red_center_x - black_center_x)
        else:
                slope = 0
        
        ##print(slope)
        dx = self.moveDistance
        dy = -self.moveDistance
        """if x1_rect1 < x2_rect2 and x2_rect1 > x1_rect2 and y1_rect1 < y2_rect2 and y2_rect1 > y1_rect2:"""
        if(self.monster_x1-3 <= x2 and self.monster_x2+3 >= x1 and self.monster_y1-3 <= y2 and self.monster_y2+3 >= y1 and playerSelf.player_collision == False):
            #playerSelf.player_collision = True
            self.monster_collision = True
            if self.current_x > target_x:
                        if slope < 0:
                                self.diag = True
                                dy = 1
                                dx = 0
                                new_x1 = self.monster_x1
                                new_y1 = self.monster_y1 + dy * self.moveDistance
                                new_x2 = self.monster_x2
                                new_y2 = self.monster_y2 + dy * self.moveDistance
                                if any(new_x2 > case[0] and new_y2 > case[1] and new_x1 < case[2] and new_y1 < case[3] for case in map.CaseNoire.values()):
                                    self.diage = False
                                    dx = -1
                                    dy = 0
                                    new_x1 = self.monster_x1 + dx * self.moveDistance
                                    new_y1 = self.monster_y1
                                    new_x2 = self.monster_x2 + dx * self.moveDistance
                                    new_y2 = self.monster_y2
                                    if any(new_x2 > case[0] and new_y2 > case[1] and new_x1 < case[2] and new_y1 < case[3] for case in map.CaseNoire.values()):
                                        return
                                for monster in playerSelf.monsterDico.values():
                                    if areaPlay.coords(monster) != areaPlay.coords(self.monster):
                                        if (new_x2 > monster[0] 
                                        and new_y2 > monster[1]
                                        and new_x1 < monster[2]
                                        and new_y1 < monster[3]):
                                            return
                                
                                if ci[2] + tolerance >= new_x1 and ci[0] <= new_x2 + tolerance:
                                    if ci[3] + tolerance >= new_y1 and ci[1] <= new_y2 + tolerance:
                                        print("Collision avec le monstre")
                                        if ci[0] > new_x2 and ci[0] > new_x2 and ci[1] == new_y1 and ci[3] == new_y2:
                                            print("W")
                                            playerSelf.fullMonster["w"] = ["./sprites/big_zombie_idle_anim_f0.png", self.life_points_monster, self.damage]
                                            playerSelf.update_infoPW()
                                            playerSelf.eventMonsterAttack("w")
                                            playerSelf.eventMAVar = True
                                        elif ci[2] < new_x1 and ci[2] < new_x2 and ci[1] == new_y1 and ci[3] == new_y2:
                                            print("E")
                                            playerSelf.fullMonster["e"] = ["./sprites/big_zombie_idle_anim_f0.png", self.life_points_monster, self.damage]
                                            playerSelf.update_infoPE()
                                            playerSelf.eventMonsterAttack("e")
                                            playerSelf.eventMAVar = True
                                        elif ci[0] == new_x1 and ci[2] == new_x2 and ci[1] > new_y1 and ci[1] > new_y2:
                                            print("N")
                                            playerSelf.fullMonster["n"] = ["./sprites/big_zombie_idle_anim_f0.png", self.life_points_monster, self.damage]
                                            playerSelf.update_infoPN()
                                            playerSelf.eventMonsterAttack("n")
                                            playerSelf.eventMAVar = True
                                        elif ci[0] == new_x1 and ci[2] == new_x2 and ci[3] < new_y1 and ci[3] < new_y2:
                                            print("S")
                                            playerSelf.fullMonster["s"] = ["./sprites/big_zombie_idle_anim_f0.png", self.life_points_monster, self.damage]
                                            playerSelf.update_infoPS()
                                            playerSelf.eventMonsterAttack("s")
                                            playerSelf.eventMAVar = True
                                playerSelf.eventMWVar = True
                                areaPlay.move(self.monster, dx * self.moveDistance, dy * self.moveDistance)
                                areaPlay.move(self.health_bar, dx * self.moveDistance, dy * self.moveDistance)
                                areaPlay.move(self.monster_image, dx * self.moveDistance, dy * self.moveDistance)
                        elif slope > 0:
                                self.diag = True
                                dy = -1
                                dx = 0
                                new_x1 = self.monster_x1
                                new_y1 = self.monster_y1 + dy * self.moveDistance
                                new_x2 = self.monster_x2
                                new_y2 = self.monster_y2 + dy * self.moveDistance
                                if any(new_x2 > case[0] and new_y2 > case[1] and new_x1 < case[2] and new_y1 < case[3] for case in map.CaseNoire.values()):
                                    dx = -1
                                    dy = 0
                                    self.diag = False
                                    new_x1 = self.monster_x1 + dx * self.moveDistance
                                    new_y1 = self.monster_y1
                                    new_x2 = self.monster_x2 + dx * self.moveDistance
                                    new_y2 = self.monster_y2
                                    if any(new_x2 > case[0] and new_y2 > case[1] and new_x1 < case[2] and new_y1 < case[3] for case in map.CaseNoire.values()):
                                        return
                                for monster in playerSelf.monsterDico.values():
                                    if areaPlay.coords(monster) != areaPlay.coords(self.monster):
                                        if (new_x2 > monster[0] 
                                        and new_y2 > monster[1]
                                        and new_x1 < monster[2]
                                        and new_y1 < monster[3]):
                                            return
                                if ci[2] + tolerance >= new_x1 and ci[0] <= new_x2 + tolerance:
                                    if ci[3] + tolerance >= new_y1 and ci[1] <= new_y2 + tolerance:
                                        print("Collision avec le monstre")
                                        if ci[0] > new_x2 and ci[0] > new_x2 and ci[1] == new_y1 and ci[3] == new_y2:
                                            print("W")
                                            playerSelf.fullMonster["w"] = ["./sprites/big_zombie_idle_anim_f0.png", self.life_points_monster, self.damage]
                                            playerSelf.update_infoPW()
                                            playerSelf.eventMonsterAttack("w")
                                            playerSelf.eventMAVar = True
                                        elif ci[2] < new_x1 and ci[2] < new_x2 and ci[1] == new_y1 and ci[3] == new_y2:
                                            print("E")
                                            playerSelf.fullMonster["e"] = ["./sprites/big_zombie_idle_anim_f0.png", self.life_points_monster, self.damage]
                                            playerSelf.update_infoPE()
                                            playerSelf.eventMonsterAttack("e")
                                            playerSelf.eventMAVar = True
                                        elif ci[0] == new_x1 and ci[2] == new_x2 and ci[1] > new_y1 and ci[1] > new_y2:
                                            print("N")
                                            playerSelf.fullMonster["n"] = ["./sprites/big_zombie_idle_anim_f0.png", self.life_points_monster, self.damage]
                                            playerSelf.update_infoPN()
                                            playerSelf.eventMonsterAttack("n")
                                            playerSelf.eventMAVar = True
                                        elif ci[0] == new_x1 and ci[2] == new_x2 and ci[3] < new_y1 and ci[3] < new_y2:
                                            print("S")
                                            playerSelf.fullMonster["s"] = ["./sprites/big_zombie_idle_anim_f0.png", self.life_points_monster, self.damage]
                                            playerSelf.update_infoPS()
                                            playerSelf.eventMonsterAttack("s")
                                            playerSelf.eventMAVar = True
                                playerSelf.eventMWVar = True
                                areaPlay.move(self.monster, dx * self.moveDistance, dy * self.moveDistance)
                                areaPlay.move(self.health_bar, dx * self.moveDistance, dy * self.moveDistance)
                                areaPlay.move(self.monster_image, dx * self.moveDistance, dy * self.moveDistance)
            elif self.current_x < target_x:
                        if slope < 0:
                            
                                self.diag = True
                                dy = -1
                                dx = 0
                                new_x1 = self.monster_x1
                                new_y1 = self.monster_y1 + dy * self.moveDistance
                                new_x2 = self.monster_x2
                                new_y2 = self.monster_y2 + dy * self.moveDistance
                                if any(new_x2 > case[0] and new_y2 > case[1] and new_x1 < case[2] and new_y1 < case[3] for case in map.CaseNoire.values()):
                                    self.diag = False
                                    dx = 1
                                    dy = 0
                                    new_x1 = self.monster_x1 + dx * self.moveDistance
                                    new_y1 = self.monster_y1
                                    new_x2 = self.monster_x2 + dx * self.moveDistance
                                    new_y2 = self.monster_y2
                                    if any(new_x2 > case[0] and new_y2 > case[1] and new_x1 < case[2] and new_y1 < case[3] for case in map.CaseNoire.values()):
                                        return
                                for monster in playerSelf.monsterDico.values():
                                    if areaPlay.coords(monster) != areaPlay.coords(self.monster):
                                        if (new_x2 > monster[0] 
                                        and new_y2 > monster[1]
                                        and new_x1 < monster[2]
                                        and new_y1 < monster[3]):
                                            return
                                if ci[2] + tolerance >= new_x1 and ci[0] <= new_x2 + tolerance:
                                    if ci[3] + tolerance >= new_y1 and ci[1] <= new_y2 + tolerance:
                                        print("Collision avec le monstre")
                                        if ci[0] > new_x2 and ci[0] > new_x2 and ci[1] == new_y1 and ci[3] == new_y2:
                                            print("W")
                                            playerSelf.fullMonster["w"] = ["./sprites/big_zombie_idle_anim_f0.png", self.life_points_monster, self.damage]
                                            playerSelf.update_infoPW()
                                            playerSelf.eventMonsterAttack("w")
                                            playerSelf.eventMAVar = True
                                        elif ci[2] < new_x1 and ci[2] < new_x2 and ci[1] == new_y1 and ci[3] == new_y2:
                                            print("E")
                                            playerSelf.fullMonster["e"] = ["./sprites/big_zombie_idle_anim_f0.png", self.life_points_monster, self.damage]
                                            playerSelf.update_infoPE()
                                            playerSelf.eventMonsterAttack("e")
                                            playerSelf.eventMAVar = True
                                        elif ci[0] == new_x1 and ci[2] == new_x2 and ci[1] > new_y1 and ci[1] > new_y2:
                                            print("N")
                                            playerSelf.fullMonster["n"] = ["./sprites/big_zombie_idle_anim_f0.png", self.life_points_monster, self.damage]
                                            playerSelf.update_infoPN()
                                            playerSelf.eventMonsterAttack("n")
                                            playerSelf.eventMAVar = True
                                        elif ci[0] == new_x1 and ci[2] == new_x2 and ci[3] < new_y1 and ci[3] < new_y2:
                                            print("S")
                                            playerSelf.fullMonster["s"] = ["./sprites/big_zombie_idle_anim_f0.png", self.life_points_monster, self.damage]
                                            playerSelf.update_infoPS()
                                            playerSelf.eventMonsterAttack("s")
                                            playerSelf.eventMAVar = True
                                playerSelf.eventMWVar = True
                                areaPlay.move(self.monster, dx * self.moveDistance, dy * self.moveDistance)
                                areaPlay.move(self.health_bar, dx * self.moveDistance, dy * self.moveDistance)
                                areaPlay.move(self.monster_image, dx * self.moveDistance, dy * self.moveDistance)
                            
                        elif slope > 0:
                            
                                self.diag = True
                                dy = 1
                                dx = 0
                                new_x1 = self.monster_x1
                                new_y1 = self.monster_y1 + dy * self.moveDistance
                                new_x2 = self.monster_x2
                                new_y2 = self.monster_y2 + dy * self.moveDistance
                                if any(new_x2 > case[0] and new_y2 > case[1] and new_x1 < case[2] and new_y1 < case[3] for case in map.CaseNoire.values()):
                                    self.diag = False
                                    dx = 1
                                    dy = 0
                                    new_x1 = self.monster_x1 + dx * self.moveDistance
                                    new_y1 = self.monster_y1
                                    new_x2 = self.monster_x2 + dx * self.moveDistance
                                    new_y2 = self.monster_y2
                                    if any(new_x2 > case[0] and new_y2 > case[1] and new_x1 < case[2] and new_y1 < case[3] for case in map.CaseNoire.values()):
                                        return
                                for monster in playerSelf.monsterDico.values():
                                    if areaPlay.coords(monster) != areaPlay.coords(self.monster):
                                        if (new_x2 > monster[0] 
                                        and new_y2 > monster[1]
                                        and new_x1 < monster[2]
                                        and new_y1 < monster[3]):
                                            return
                                if ci[2] + tolerance >= new_x1 and ci[0] <= new_x2 + tolerance:
                                    if ci[3] + tolerance >= new_y1 and ci[1] <= new_y2 + tolerance:
                                        print("Collision avec le monstre")
                                        if ci[0] > new_x2 and ci[0] > new_x2 and ci[1] == new_y1 and ci[3] == new_y2:
                                            print("W")
                                            playerSelf.fullMonster["w"] = ["./sprites/big_zombie_idle_anim_f0.png", self.life_points_monster, self.damage]
                                            playerSelf.update_infoPW()
                                            playerSelf.eventMonsterAttack("w")
                                            playerSelf.eventMAVar = True
                                        elif ci[2] < new_x1 and ci[2] < new_x2 and ci[1] == new_y1 and ci[3] == new_y2:
                                            print("E")
                                            playerSelf.fullMonster["e"] = ["./sprites/big_zombie_idle_anim_f0.png", self.life_points_monster, self.damage]
                                            playerSelf.update_infoPE()
                                            playerSelf.eventMonsterAttack("e")
                                            playerSelf.eventMAVar = True
                                        elif ci[0] == new_x1 and ci[2] == new_x2 and ci[1] > new_y1 and ci[1] > new_y2:
                                            print("N")
                                            playerSelf.fullMonster["n"] = ["./sprites/big_zombie_idle_anim_f0.png", self.life_points_monster, self.damage]
                                            playerSelf.update_infoPN()
                                            playerSelf.eventMonsterAttack("n")
                                            playerSelf.eventMAVar = True
                                        elif ci[0] == new_x1 and ci[2] == new_x2 and ci[3] < new_y1 and ci[3] < new_y2:
                                            print("S")
                                            playerSelf.fullMonster["s"] = ["./sprites/big_zombie_idle_anim_f0.png", self.life_points_monster, self.damage]
                                            playerSelf.update_infoPS()
                                            playerSelf.eventMonsterAttack("s")
                                            playerSelf.eventMAVar = True
                                playerSelf.eventMWVar = True
                                areaPlay.move(self.monster, dx * self.moveDistance, dy * self.moveDistance)
                                areaPlay.move(self.health_bar, dx * self.moveDistance, dy * self.moveDistance)
                                areaPlay.move(self.monster_image, dx * self.moveDistance, dy * self.moveDistance)
                            
           
            #playerSelf.startFight()
            ##print("collision with player")
            #self.diag = False # ==============> à voir si on doit mettre ou pas
            if ok == False:
                if ci[2] + tolerance >= self.monster_x1 and ci[0] <= self.monster_x2 + tolerance:
                    if ci[3] + tolerance >= self.monster_y1 and ci[1] <= self.monster_y2 + tolerance:
                        print("Collision avec le monstre")
                        if ci[0] > self.monster_x2 and ci[0] > self.monster_x2 and ci[1] == self.monster_y1 and ci[3] == self.monster_y2:
                                            print("W")
                                            playerSelf.fullMonster["w"] = ["./sprites/big_zombie_idle_anim_f0.png", self.life_points_monster, self.damage]
                                            playerSelf.update_infoPW()
                                            playerSelf.eventMonsterAttack("w")
                                            playerSelf.eventMAVar = True
                        elif ci[2] < self.monster_x1 and ci[2] < self.monster_x2 and ci[1] == self.monster_y1 and ci[3] == self.monster_y2:
                                            print("E")
                                            playerSelf.fullMonster["e"] = ["./sprites/big_zombie_idle_anim_f0.png", self.life_points_monster, self.damage]
                                            playerSelf.update_infoPE()
                                            playerSelf.eventMonsterAttack("e")
                                            playerSelf.eventMAVar = True
                        elif ci[0] == self.monster_x1 and ci[2] == self.monster_x2 and ci[1] > self.monster_y1 and ci[1] > self.monster_y2:
                                            print("N")
                                            playerSelf.fullMonster["n"] = ["./sprites/big_zombie_idle_anim_f0.png", self.life_points_monster, self.damage]
                                            playerSelf.update_infoPN()
                                            playerSelf.eventMonsterAttack("n")
                                            playerSelf.eventMAVar = True
                        elif ci[0] == self.monster_x1 and ci[2] == self.monster_x2 and ci[3] < self.monster_y1 and ci[3] < self.monster_y2:
                                            print("S")
                                            playerSelf.fullMonster["s"] = ["./sprites/big_zombie_idle_anim_f0.png", self.life_points_monster, self.damage]
                                            playerSelf.update_infoPS()
                                            playerSelf.eventMonsterAttack("s")
                                            playerSelf.eventMAVar = True
            print(playerSelf.fullMonster)    
            

        elif(self.monster_x1 < x2P and self.monster_x2 > x1P and self.monster_y1 < y2P and self.monster_y2 > y1P and playerSelf.player_collision == False and playerSelf.collPNJ == False):
          
            self.monster_collision = False
            ##print(self.current_x, self.current_y, target_x, target_y)
            ##print("slope", slope)
            intersec = False
            for case in map.CaseNoire.values():
                x3, y3, x4, y4 = case
                if self.intersect(self.current_x, self.current_y, target_x, target_y, x3, y3, x4, y4):
                    #return True
                    intersec = True

            #return False
            
            if intersec == False:
                ##print("intersec")
                if slope == 0 and target_x == self.current_x and self.current_y < target_y:
                    new_x2 = self.monster_x2
                    new_x1 = self.monster_x1
                    new_y1 = self.monster_y1 + self.moveDistance
                    new_y2 = self.monster_y2 + self.moveDistance
                    for monster in playerSelf.monsterDico.values():
                        if areaPlay.coords(monster) != areaPlay.coords(self.monster):
                            if (new_x2 > monster[0] 
                            and new_y2 > monster[1]
                            and new_x1 < monster[2]
                            and new_y1 < monster[3]):
                                return
                    if ci[2] + tolerance >= new_x1 and ci[0] <= new_x2 + tolerance:
                                    if ci[3] + tolerance >= new_y1 and ci[1] <= new_y2 + tolerance:
                                        print("Collision avec le monstre")
                                        if ci[0] > new_x2 and ci[0] > new_x2 and ci[1] == new_y1 and ci[3] == new_y2:
                                            print("W")
                                            playerSelf.fullMonster["w"] = ["./sprites/big_zombie_idle_anim_f0.png", self.life_points_monster, self.damage]
                                            playerSelf.update_infoPW()
                                            playerSelf.eventMonsterAttack("w")
                                            playerSelf.eventMAVar = True
                                        elif ci[2] < new_x1 and ci[2] < new_x2 and ci[1] == new_y1 and ci[3] == new_y2:
                                            print("E")
                                            playerSelf.fullMonster["e"] = ["./sprites/big_zombie_idle_anim_f0.png", self.life_points_monster, self.damage]
                                            playerSelf.update_infoPE()
                                            playerSelf.eventMonsterAttack("e")
                                            playerSelf.eventMAVar = True
                                        elif ci[0] == new_x1 and ci[2] == new_x2 and ci[1] > new_y1 and ci[1] > new_y2:
                                            print("N")
                                            playerSelf.fullMonster["n"] = ["./sprites/big_zombie_idle_anim_f0.png", self.life_points_monster, self.damage]
                                            playerSelf.update_infoPN()
                                            playerSelf.eventMonsterAttack("n")
                                            playerSelf.eventMAVar = True
                                        elif ci[0] == new_x1 and ci[2] == new_x2 and ci[3] < new_y1 and ci[3] < new_y2:
                                            print("S")
                                            playerSelf.fullMonster["s"] = ["./sprites/big_zombie_idle_anim_f0.png", self.life_points_monster, self.damage]
                                            playerSelf.update_infoPS()
                                            playerSelf.eventMonsterAttack("s")
                                            playerSelf.eventMAVar = True
                    playerSelf.eventMWVar = True
                    areaPlay.move(self.monster, 0, 1 * self.moveDistance)
                    areaPlay.move(self.health_bar, 0, 1 * self.moveDistance)
                    areaPlay.move(self.monster_image, 0, 1 * self.moveDistance)
                elif slope == 0 and target_x == self.current_x and self.current_y > target_y:
                    new_x2 = self.monster_x2 
                    new_x1 = self.monster_x1 
                    new_y1 = self.monster_y1 - self.moveDistance
                    new_y2 = self.monster_y2 - self.moveDistance
                    for monster in playerSelf.monsterDico.values():
                        if areaPlay.coords(monster) != areaPlay.coords(self.monster):
                            if (new_x2 > monster[0] 
                            and new_y2 > monster[1]
                            and new_x1 < monster[2]
                            and new_y1 < monster[3]):
                                return
                    if ci[2] + tolerance >= new_x1 and ci[0] <= new_x2 + tolerance:
                                    if ci[3] + tolerance >= new_y1 and ci[1] <= new_y2 + tolerance:
                                        print("Collision avec le monstre")
                                        if ci[0] > new_x2 and ci[0] > new_x2 and ci[1] == new_y1 and ci[3] == new_y2:
                                            print("W")
                                            playerSelf.fullMonster["w"] = ["./sprites/big_zombie_idle_anim_f0.png", self.life_points_monster, self.damage]
                                            playerSelf.update_infoPW()
                                            playerSelf.eventMonsterAttack("w")
                                            playerSelf.eventMAVar = True
                                        elif ci[2] < new_x1 and ci[2] < new_x2 and ci[1] == new_y1 and ci[3] == new_y2:
                                            print("E")
                                            playerSelf.fullMonster["e"] = ["./sprites/big_zombie_idle_anim_f0.png", self.life_points_monster, self.damage]
                                            playerSelf.update_infoPE()
                                            playerSelf.eventMonsterAttack("e")
                                            playerSelf.eventMAVar = True
                                        elif ci[0] == new_x1 and ci[2] == new_x2 and ci[1] > new_y1 and ci[1] > new_y2:
                                            print("N")
                                            playerSelf.fullMonster["n"] = ["./sprites/big_zombie_idle_anim_f0.png", self.life_points_monster, self.damage]
                                            playerSelf.update_infoPN()
                                            playerSelf.eventMonsterAttack("n")
                                            playerSelf.eventMAVar = True
                                        elif ci[0] == new_x1 and ci[2] == new_x2 and ci[3] < new_y1 and ci[3] < new_y2:
                                            print("S")
                                            playerSelf.fullMonster["s"] = ["./sprites/big_zombie_idle_anim_f0.png", self.life_points_monster, self.damage]
                                            playerSelf.update_infoPS()
                                            playerSelf.eventMonsterAttack("s")
                                            playerSelf.eventMAVar = True
                    playerSelf.eventMWVar = True
                    areaPlay.move(self.monster, 0, -1 * self.moveDistance)
                    areaPlay.move(self.health_bar, 0, -1 * self.moveDistance)
                    areaPlay.move(self.monster_image, 0, -1 * self.moveDistance)
                elif slope == -0.0 and target_y == self.current_y and self.current_x > target_x:
                    new_x2 = self.monster_x2 - self.moveDistance
                    new_x1 = self.monster_x1 - self.moveDistance
                    new_y1 = self.monster_y1
                    new_y2 = self.monster_y2
                    for monster in playerSelf.monsterDico.values():
                        if areaPlay.coords(monster) != areaPlay.coords(self.monster):
                            if (new_x2 > monster[0] 
                            and new_y2 > monster[1]
                            and new_x1 < monster[2]
                            and new_y1 < monster[3]):
                                return
                    if ci[2] + tolerance >= new_x1 and ci[0] <= new_x2 + tolerance:
                                    if ci[3] + tolerance >= new_y1 and ci[1] <= new_y2 + tolerance:
                                        print("Collision avec le monstre")
                                        if ci[0] > new_x2 and ci[0] > new_x2 and ci[1] == new_y1 and ci[3] == new_y2:
                                            print("W")
                                            playerSelf.fullMonster["w"] = ["./sprites/big_zombie_idle_anim_f0.png", self.life_points_monster, self.damage]
                                            playerSelf.update_infoPW()
                                            playerSelf.eventMonsterAttack("w")
                                            playerSelf.eventMAVar = True
                                        elif ci[2] < new_x1 and ci[2] < new_x2 and ci[1] == new_y1 and ci[3] == new_y2:
                                            print("E")
                                            playerSelf.fullMonster["e"] = ["./sprites/big_zombie_idle_anim_f0.png", self.life_points_monster, self.damage]
                                            playerSelf.update_infoPE()
                                            playerSelf.eventMonsterAttack("e")
                                            playerSelf.eventMAVar = True
                                        elif ci[0] == new_x1 and ci[2] == new_x2 and ci[1] > new_y1 and ci[1] > new_y2:
                                            print("N")
                                            playerSelf.fullMonster["n"] = ["./sprites/big_zombie_idle_anim_f0.png", self.life_points_monster, self.damage]
                                            playerSelf.update_infoPN()
                                            playerSelf.eventMonsterAttack("n")
                                            playerSelf.eventMAVar = True
                                        elif ci[0] == new_x1 and ci[2] == new_x2 and ci[3] < new_y1 and ci[3] < new_y2:
                                            print("S")
                                            playerSelf.fullMonster["s"] = ["./sprites/big_zombie_idle_anim_f0.png", self.life_points_monster, self.damage]
                                            playerSelf.update_infoPS()
                                            playerSelf.eventMonsterAttack("s")
                                            playerSelf.eventMAVar = True
                    playerSelf.eventMWVar = True
                    areaPlay.move(self.monster, -1 * self.moveDistance, 0)
                    areaPlay.move(self.health_bar, -1 * self.moveDistance, 0)
                    areaPlay.move(self.monster_image, -1 * self.moveDistance, 0)
                elif slope == 0.0 and target_y == self.current_y and self.current_x < target_x:
                    new_x2 = self.monster_x2 + self.moveDistance
                    new_x1 = self.monster_x1 + self.moveDistance
                    new_y1 = self.monster_y1 
                    new_y2 = self.monster_y2 
                    for monster in playerSelf.monsterDico.values():
                        if areaPlay.coords(monster) != areaPlay.coords(self.monster):
                            if (new_x2 > monster[0] 
                            and new_y2 > monster[1]
                            and new_x1 < monster[2]
                            and new_y1 < monster[3]):
                                return
                    if ci[2] + tolerance >= new_x1 and ci[0] <= new_x2 + tolerance:
                                    if ci[3] + tolerance >= new_y1 and ci[1] <= new_y2 + tolerance:
                                        print("Collision avec le monstre")
                                        if ci[0] > new_x2 and ci[0] > new_x2 and ci[1] == new_y1 and ci[3] == new_y2:
                                            print("W")
                                            playerSelf.fullMonster["w"] = ["./sprites/big_zombie_idle_anim_f0.png", self.life_points_monster, self.damage]
                                            playerSelf.update_infoPW()
                                            playerSelf.eventMonsterAttack("w")
                                            playerSelf.eventMAVar = True
                                        elif ci[2] < new_x1 and ci[2] < new_x2 and ci[1] == new_y1 and ci[3] == new_y2:
                                            print("E")
                                            playerSelf.fullMonster["e"] = ["./sprites/big_zombie_idle_anim_f0.png", self.life_points_monster, self.damage]
                                            playerSelf.update_infoPE()
                                            playerSelf.eventMonsterAttack("e")
                                            playerSelf.eventMAVar = True
                                        elif ci[0] == new_x1 and ci[2] == new_x2 and ci[1] > new_y1 and ci[1] > new_y2:
                                            print("N")
                                            playerSelf.fullMonster["n"] = ["./sprites/big_zombie_idle_anim_f0.png", self.life_points_monster, self.damage]
                                            playerSelf.update_infoPN()
                                            playerSelf.eventMonsterAttack("n")
                                            playerSelf.eventMAVar = True
                                        elif ci[0] == new_x1 and ci[2] == new_x2 and ci[3] < new_y1 and ci[3] < new_y2:
                                            print("S")
                                            playerSelf.fullMonster["s"] = ["./sprites/big_zombie_idle_anim_f0.png", self.life_points_monster, self.damage]
                                            playerSelf.update_infoPS()
                                            playerSelf.eventMonsterAttack("s")
                                            playerSelf.eventMAVar = True
                    playerSelf.eventMWVar = True
                    areaPlay.move(self.monster, 1 * self.moveDistance, 0)
                    areaPlay.move(self.health_bar, 1 * self.moveDistance, 0)
                    areaPlay.move(self.monster_image, 1 * self.moveDistance, 0)
                else:
                    if self.current_x > target_x:
                        if slope < 0:
                            if self.diag == False:
                                self.diag = True
                                dy = 1
                                dx = 0
                                new_x1 = self.monster_x1
                                new_y1 = self.monster_y1 + dy * self.moveDistance
                                new_x2 = self.monster_x2
                                new_y2 = self.monster_y2 + dy * self.moveDistance
                                if any(new_x2 > case[0] and new_y2 > case[1] and new_x1 < case[2] and new_y1 < case[3] for case in map.CaseNoire.values()):
                                    self.diage = False
                                    dx = -1
                                    dy = 0
                                new_x2 = self.monster_x2 + dx * self.moveDistance
                                new_x1 = self.monster_x1 + dx *self.moveDistance
                                new_y1 = self.monster_y1 + dy * self.moveDistance
                                new_y2 = self.monster_y2 + dy * self.moveDistance
                                for monster in playerSelf.monsterDico.values():
                                    if areaPlay.coords(monster) != areaPlay.coords(self.monster):
                                        if (new_x2 > monster[0] 
                                        and new_y2 > monster[1]
                                        and new_x1 < monster[2]
                                        and new_y1 < monster[3]):
                                            return
                                if ci[2] + tolerance >= new_x1 and ci[0] <= new_x2 + tolerance:
                                    if ci[3] + tolerance >= new_y1 and ci[1] <= new_y2 + tolerance:
                                        print("Collision avec le monstre")
                                        if ci[0] > new_x2 and ci[0] > new_x2 and ci[1] == new_y1 and ci[3] == new_y2:
                                            print("W")
                                            playerSelf.fullMonster["w"] = ["./sprites/big_zombie_idle_anim_f0.png", self.life_points_monster, self.damage]
                                            playerSelf.update_infoPW()
                                            playerSelf.eventMonsterAttack("w")
                                            playerSelf.eventMAVar = True
                                        elif ci[2] < new_x1 and ci[2] < new_x2 and ci[1] == new_y1 and ci[3] == new_y2:
                                            print("E")
                                            playerSelf.fullMonster["e"] = ["./sprites/big_zombie_idle_anim_f0.png", self.life_points_monster, self.damage]
                                            playerSelf.update_infoPE()
                                            playerSelf.eventMonsterAttack("e")
                                            playerSelf.eventMAVar = True
                                        elif ci[0] == new_x1 and ci[2] == new_x2 and ci[1] > new_y1 and ci[1] > new_y2:
                                            print("N")
                                            playerSelf.fullMonster["n"] = ["./sprites/big_zombie_idle_anim_f0.png", self.life_points_monster, self.damage]
                                            playerSelf.update_infoPN()
                                            playerSelf.eventMonsterAttack("n")
                                            playerSelf.eventMAVar = True
                                        elif ci[0] == new_x1 and ci[2] == new_x2 and ci[3] < new_y1 and ci[3] < new_y2:
                                            print("S")
                                            playerSelf.fullMonster["s"] = ["./sprites/big_zombie_idle_anim_f0.png", self.life_points_monster, self.damage]
                                            playerSelf.update_infoPS()
                                            playerSelf.eventMonsterAttack("s")
                                            playerSelf.eventMAVar = True
                                playerSelf.eventMWVar = True
                                areaPlay.move(self.monster, dx * self.moveDistance, dy * self.moveDistance)
                                areaPlay.move(self.health_bar, dx * self.moveDistance, dy * self.moveDistance)
                                areaPlay.move(self.monster_image, dx * self.moveDistance, dy * self.moveDistance)
                            else:
                                self.diag = False
                                dx = -1
                                dy = 0
                                new_x1 = self.monster_x1 + dx * self.moveDistance
                                new_y1 = self.monster_y1
                                new_x2 = self.monster_x2 + dx * self.moveDistance
                                new_y2 = self.monster_y2
                                if any(new_x2 > case[0] and new_y2 > case[1] and new_x1 < case[2] and new_y1 < case[3] for case in map.CaseNoire.values()):
                                    self.diag = True
                                    dx = 0
                                    dy = 1
                                new_x2 = self.monster_x2 + dx * self.moveDistance
                                new_x1 = self.monster_x1 + dx *self.moveDistance
                                new_y1 = self.monster_y1 + dy * self.moveDistance
                                new_y2 = self.monster_y2 + dy * self.moveDistance
                                for monster in playerSelf.monsterDico.values():
                                    if areaPlay.coords(monster) != areaPlay.coords(self.monster):
                                        if (new_x2 > monster[0] 
                                        and new_y2 > monster[1]
                                        and new_x1 < monster[2]
                                        and new_y1 < monster[3]):
                                            return
                                if ci[2] + tolerance >= new_x1 and ci[0] <= new_x2 + tolerance:
                                    if ci[3] + tolerance >= new_y1 and ci[1] <= new_y2 + tolerance:
                                        print("Collision avec le monstre")
                                        if ci[0] > new_x2 and ci[0] > new_x2 and ci[1] == new_y1 and ci[3] == new_y2:
                                            print("W")
                                            playerSelf.fullMonster["w"] = ["./sprites/big_zombie_idle_anim_f0.png", self.life_points_monster, self.damage]
                                            playerSelf.update_infoPW()
                                            playerSelf.eventMonsterAttack("w")
                                            playerSelf.eventMAVar = True
                                        elif ci[2] < new_x1 and ci[2] < new_x2 and ci[1] == new_y1 and ci[3] == new_y2:
                                            print("E")
                                            playerSelf.fullMonster["e"] = ["./sprites/big_zombie_idle_anim_f0.png", self.life_points_monster, self.damage]
                                            playerSelf.update_infoPE()
                                            playerSelf.eventMonsterAttack("e")
                                            playerSelf.eventMAVar = True
                                        elif ci[0] == new_x1 and ci[2] == new_x2 and ci[1] > new_y1 and ci[1] > new_y2:
                                            print("N")
                                            playerSelf.fullMonster["n"] = ["./sprites/big_zombie_idle_anim_f0.png", self.life_points_monster, self.damage]
                                            playerSelf.update_infoPN()
                                            playerSelf.eventMonsterAttack("n")
                                            playerSelf.eventMAVar = True
                                        elif ci[0] == new_x1 and ci[2] == new_x2 and ci[3] < new_y1 and ci[3] < new_y2:
                                            print("S")
                                            playerSelf.fullMonster["s"] = ["./sprites/big_zombie_idle_anim_f0.png", self.life_points_monster, self.damage]
                                            playerSelf.update_infoPS()
                                            playerSelf.eventMonsterAttack("s")
                                            playerSelf.eventMAVar = True
                                playerSelf.eventMWVar = True
                                areaPlay.move(self.monster, dx * self.moveDistance, dy * self.moveDistance)
                                areaPlay.move(self.health_bar, dx * self.moveDistance, dy * self.moveDistance)
                                areaPlay.move(self.monster_image, dx * self.moveDistance, dy * self.moveDistance)
                        elif slope > 0:
                            if self.diag == False:
                                self.diag = True
                                dy = -1
                                dx = 0
                                new_x1 = self.monster_x1
                                new_y1 = self.monster_y1 + dy * self.moveDistance
                                new_x2 = self.monster_x2
                                new_y2 = self.monster_y2 + dy * self.moveDistance
                                if any(new_x2 > case[0] and new_y2 > case[1] and new_x1 < case[2] and new_y1 < case[3] for case in map.CaseNoire.values()):
                                    dx = -1
                                    dy = 0
                                    self.diag = False
                                new_x2 = self.monster_x2 + dx * self.moveDistance
                                new_x1 = self.monster_x1 + dx *self.moveDistance
                                new_y1 = self.monster_y1 + dy * self.moveDistance
                                new_y2 = self.monster_y2 + dy * self.moveDistance
                                for monster in playerSelf.monsterDico.values():
                                    if areaPlay.coords(monster) != areaPlay.coords(self.monster):
                                        if (new_x2 > monster[0] 
                                        and new_y2 > monster[1]
                                        and new_x1 < monster[2]
                                        and new_y1 < monster[3]):
                                            return
                                if ci[2] + tolerance >= new_x1 and ci[0] <= new_x2 + tolerance:
                                    if ci[3] + tolerance >= new_y1 and ci[1] <= new_y2 + tolerance:
                                        print("Collision avec le monstre")
                                        if ci[0] > new_x2 and ci[0] > new_x2 and ci[1] == new_y1 and ci[3] == new_y2:
                                            print("W")
                                            playerSelf.fullMonster["w"] = ["./sprites/big_zombie_idle_anim_f0.png", self.life_points_monster, self.damage]
                                            playerSelf.update_infoPW()
                                            playerSelf.eventMonsterAttack("w")
                                            playerSelf.eventMAVar = True
                                        elif ci[2] < new_x1 and ci[2] < new_x2 and ci[1] == new_y1 and ci[3] == new_y2:
                                            print("E")
                                            playerSelf.fullMonster["e"] = ["./sprites/big_zombie_idle_anim_f0.png", self.life_points_monster, self.damage]
                                            playerSelf.update_infoPE()
                                            playerSelf.eventMonsterAttack("e")
                                            playerSelf.eventMAVar = True
                                        elif ci[0] == new_x1 and ci[2] == new_x2 and ci[1] > new_y1 and ci[1] > new_y2:
                                            print("N")
                                            playerSelf.fullMonster["n"] = ["./sprites/big_zombie_idle_anim_f0.png", self.life_points_monster, self.damage]
                                            playerSelf.update_infoPN()
                                            playerSelf.eventMonsterAttack("n")
                                            playerSelf.eventMAVar = True
                                        elif ci[0] == new_x1 and ci[2] == new_x2 and ci[3] < new_y1 and ci[3] < new_y2:
                                            print("S")
                                            playerSelf.fullMonster["s"] = ["./sprites/big_zombie_idle_anim_f0.png", self.life_points_monster, self.damage]
                                            playerSelf.update_infoPS()
                                            playerSelf.eventMonsterAttack("s")
                                            playerSelf.eventMAVar = True
                                playerSelf.eventMWVar = True
                                areaPlay.move(self.monster, dx * self.moveDistance, dy * self.moveDistance)
                                areaPlay.move(self.health_bar, dx * self.moveDistance, dy * self.moveDistance)
                                areaPlay.move(self.monster_image, dx * self.moveDistance, dy * self.moveDistance)
                            else:
                                self.diag = False
                                dx = -1
                                dy = 0
                                new_x1 = self.monster_x1 + dx * self.moveDistance
                                new_y1 = self.monster_y1
                                new_x2 = self.monster_x2 + dx * self.moveDistance
                                new_y2 = self.monster_y2
                                if any(new_x2 > case[0] and new_y2 > case[1] and new_x1 < case[2] and new_y1 < case[3] for case in map.CaseNoire.values()):
                                    self.diag = True
                                    dx = 0
                                    dy = -1
                                new_x2 = self.monster_x2 + dx * self.moveDistance
                                new_x1 = self.monster_x1 + dx *self.moveDistance
                                new_y1 = self.monster_y1 + dy * self.moveDistance
                                new_y2 = self.monster_y2 + dy * self.moveDistance
                                for monster in playerSelf.monsterDico.values():
                                    if areaPlay.coords(monster) != areaPlay.coords(self.monster):
                                        if (new_x2 > monster[0] 
                                        and new_y2 > monster[1]
                                        and new_x1 < monster[2]
                                        and new_y1 < monster[3]):
                                            return
                                if ci[2] + tolerance >= new_x1 and ci[0] <= new_x2 + tolerance:
                                    if ci[3] + tolerance >= new_y1 and ci[1] <= new_y2 + tolerance:
                                        print("Collision avec le monstre")
                                        if ci[0] > new_x2 and ci[0] > new_x2 and ci[1] == new_y1 and ci[3] == new_y2:
                                            print("W")
                                            playerSelf.fullMonster["w"] = ["./sprites/big_zombie_idle_anim_f0.png", self.life_points_monster, self.damage]
                                            playerSelf.update_infoPW()
                                            playerSelf.eventMonsterAttack("w")
                                            playerSelf.eventMAVar = True
                                        elif ci[2] < new_x1 and ci[2] < new_x2 and ci[1] == new_y1 and ci[3] == new_y2:
                                            print("E")
                                            playerSelf.fullMonster["e"] = ["./sprites/big_zombie_idle_anim_f0.png", self.life_points_monster, self.damage]
                                            playerSelf.update_infoPE()
                                            playerSelf.eventMonsterAttack("e")
                                            playerSelf.eventMAVar = True
                                        elif ci[0] == new_x1 and ci[2] == new_x2 and ci[1] > new_y1 and ci[1] > new_y2:
                                            print("N")
                                            playerSelf.fullMonster["n"] = ["./sprites/big_zombie_idle_anim_f0.png", self.life_points_monster, self.damage]
                                            playerSelf.update_infoPN()
                                            playerSelf.eventMonsterAttack("n")
                                            playerSelf.eventMAVar = True
                                        elif ci[0] == new_x1 and ci[2] == new_x2 and ci[3] < new_y1 and ci[3] < new_y2:
                                            print("S")
                                            playerSelf.fullMonster["s"] = ["./sprites/big_zombie_idle_anim_f0.png", self.life_points_monster, self.damage]
                                            playerSelf.update_infoPS()
                                            playerSelf.eventMonsterAttack("s")
                                            playerSelf.eventMAVar = True
                                playerSelf.eventMWVar = True
                                areaPlay.move(self.monster, dx * self.moveDistance, dy * self.moveDistance)
                                areaPlay.move(self.health_bar, dx * self.moveDistance, dy * self.moveDistance)
                                areaPlay.move(self.monster_image, dx * self.moveDistance, dy * self.moveDistance)
                    elif self.current_x < target_x:
                        if slope < 0:
                            if self.diag == False:
                                self.diag = True
                                dy = -1
                                dx = 0
                                new_x1 = self.monster_x1
                                new_y1 = self.monster_y1 + dy * self.moveDistance
                                new_x2 = self.monster_x2
                                new_y2 = self.monster_y2 + dy * self.moveDistance
                                if any(new_x2 > case[0] and new_y2 > case[1] and new_x1 < case[2] and new_y1 < case[3] for case in map.CaseNoire.values()):
                                    self.diag = False
                                    dx = 1
                                    dy = 0
                                new_x2 = self.monster_x2 + dx * self.moveDistance
                                new_x1 = self.monster_x1 + dx *self.moveDistance
                                new_y1 = self.monster_y1 + dy * self.moveDistance
                                new_y2 = self.monster_y2 + dy * self.moveDistance
                                for monster in playerSelf.monsterDico.values():
                                    if areaPlay.coords(monster) != areaPlay.coords(self.monster):
                                        if (new_x2 > monster[0] 
                                        and new_y2 > monster[1]
                                        and new_x1 < monster[2]
                                        and new_y1 < monster[3]):
                                            return
                                if ci[2] + tolerance >= new_x1 and ci[0] <= new_x2 + tolerance:
                                    if ci[3] + tolerance >= new_y1 and ci[1] <= new_y2 + tolerance:
                                        print("Collision avec le monstre")
                                        if ci[0] > new_x2 and ci[0] > new_x2 and ci[1] == new_y1 and ci[3] == new_y2:
                                            print("W")
                                            playerSelf.fullMonster["w"] = ["./sprites/big_zombie_idle_anim_f0.png", self.life_points_monster, self.damage]
                                            playerSelf.update_infoPW()
                                            playerSelf.eventMonsterAttack("w")
                                            playerSelf.eventMAVar = True
                                        elif ci[2] < new_x1 and ci[2] < new_x2 and ci[1] == new_y1 and ci[3] == new_y2:
                                            print("E")
                                            playerSelf.fullMonster["e"] = ["./sprites/big_zombie_idle_anim_f0.png", self.life_points_monster, self.damage]
                                            playerSelf.update_infoPE()
                                            playerSelf.eventMonsterAttack("e")
                                            playerSelf.eventMAVar = True
                                        elif ci[0] == new_x1 and ci[2] == new_x2 and ci[1] > new_y1 and ci[1] > new_y2:
                                            print("N")
                                            playerSelf.fullMonster["n"] = ["./sprites/big_zombie_idle_anim_f0.png", self.life_points_monster, self.damage]
                                            playerSelf.update_infoPN()
                                            playerSelf.eventMonsterAttack("n")
                                            playerSelf.eventMAVar = True
                                        elif ci[0] == new_x1 and ci[2] == new_x2 and ci[3] < new_y1 and ci[3] < new_y2:
                                            print("S")
                                            playerSelf.fullMonster["s"] = ["./sprites/big_zombie_idle_anim_f0.png", self.life_points_monster, self.damage]
                                            playerSelf.update_infoPS()
                                            playerSelf.eventMonsterAttack("s")
                                            playerSelf.eventMAVar = True
                                playerSelf.eventMWVar = True
                                areaPlay.move(self.monster, dx * self.moveDistance, dy * self.moveDistance)
                                areaPlay.move(self.health_bar, dx * self.moveDistance, dy * self.moveDistance)
                                areaPlay.move(self.monster_image, dx * self.moveDistance, dy * self.moveDistance)
                            else:
                                self.diag = False
                                dx = 1
                                dy = 0
                                new_x1 = self.monster_x1 + dx * self.moveDistance
                                new_y1 = self.monster_y1
                                new_x2 = self.monster_x2 + dx * self.moveDistance
                                new_y2 = self.monster_y2
                                if any(new_x2 > case[0] and new_y2 > case[1] and new_x1 < case[2] and new_y1 < case[3] for case in map.CaseNoire.values()):
                                    self.diag = True
                                    dx = 0
                                    dy = -1
                                new_x2 = self.monster_x2 + dx * self.moveDistance
                                new_x1 = self.monster_x1 + dx *self.moveDistance
                                new_y1 = self.monster_y1 + dy * self.moveDistance
                                new_y2 = self.monster_y2 + dy * self.moveDistance
                                for monster in playerSelf.monsterDico.values():
                                    if areaPlay.coords(monster) != areaPlay.coords(self.monster):
                                        if (new_x2 > monster[0] 
                                        and new_y2 > monster[1]
                                        and new_x1 < monster[2]
                                        and new_y1 < monster[3]):
                                            return
                                if ci[2] + tolerance >= new_x1 and ci[0] <= new_x2 + tolerance:
                                    if ci[3] + tolerance >= new_y1 and ci[1] <= new_y2 + tolerance:
                                        print("Collision avec le monstre")
                                        if ci[0] > new_x2 and ci[0] > new_x2 and ci[1] == new_y1 and ci[3] == new_y2:
                                            print("W")
                                            playerSelf.fullMonster["w"] = ["./sprites/big_zombie_idle_anim_f0.png", self.life_points_monster, self.damage]
                                            playerSelf.update_infoPW()
                                            playerSelf.eventMonsterAttack("w")
                                            playerSelf.eventMAVar = True
                                        elif ci[2] < new_x1 and ci[2] < new_x2 and ci[1] == new_y1 and ci[3] == new_y2:
                                            print("E")
                                            playerSelf.fullMonster["e"] = ["./sprites/big_zombie_idle_anim_f0.png", self.life_points_monster, self.damage]
                                            playerSelf.update_infoPE()
                                            playerSelf.eventMonsterAttack("e")
                                            playerSelf.eventMAVar = True
                                        elif ci[0] == new_x1 and ci[2] == new_x2 and ci[1] > new_y1 and ci[1] > new_y2:
                                            print("N")
                                            playerSelf.fullMonster["n"] = ["./sprites/big_zombie_idle_anim_f0.png", self.life_points_monster, self.damage]
                                            playerSelf.update_infoPN()
                                            playerSelf.eventMonsterAttack("n")
                                            playerSelf.eventMAVar = True
                                        elif ci[0] == new_x1 and ci[2] == new_x2 and ci[3] < new_y1 and ci[3] < new_y2:
                                            print("S")
                                            playerSelf.fullMonster["s"] = ["./sprites/big_zombie_idle_anim_f0.png", self.life_points_monster, self.damage]
                                            playerSelf.update_infoPS()
                                            playerSelf.eventMonsterAttack("s")
                                            playerSelf.eventMAVar = True
                                playerSelf.eventMWVar = True
                                areaPlay.move(self.monster, dx * self.moveDistance, dy * self.moveDistance)
                                areaPlay.move(self.health_bar, dx * self.moveDistance, dy * self.moveDistance)
                                areaPlay.move(self.monster_image, dx * self.moveDistance, dy * self.moveDistance)
                        elif slope > 0:
                            if self.diag == False:
                                self.diag = True
                                dy = 1
                                dx = 0
                                new_x1 = self.monster_x1
                                new_y1 = self.monster_y1 + dy * self.moveDistance
                                new_x2 = self.monster_x2
                                new_y2 = self.monster_y2 + dy * self.moveDistance
                                if any(new_x2 > case[0] and new_y2 > case[1] and new_x1 < case[2] and new_y1 < case[3] for case in map.CaseNoire.values()):
                                    self.diag = False
                                    dx = 1
                                    dy = 0
                                new_x2 = self.monster_x2 + dx * self.moveDistance
                                new_x1 = self.monster_x1 + dx *self.moveDistance
                                new_y1 = self.monster_y1 + dy * self.moveDistance
                                new_y2 = self.monster_y2 + dy * self.moveDistance
                                for monster in playerSelf.monsterDico.values():
                                    if areaPlay.coords(monster) != areaPlay.coords(self.monster):
                                        if (new_x2 > monster[0] 
                                        and new_y2 > monster[1]
                                        and new_x1 < monster[2]
                                        and new_y1 < monster[3]):
                                            return
                                if ci[2] + tolerance >= new_x1 and ci[0] <= new_x2 + tolerance:
                                    if ci[3] + tolerance >= new_y1 and ci[1] <= new_y2 + tolerance:
                                        print("Collision avec le monstre")
                                        if ci[0] > new_x2 and ci[0] > new_x2 and ci[1] == new_y1 and ci[3] == new_y2:
                                            print("W")
                                            playerSelf.fullMonster["w"] = ["./sprites/big_zombie_idle_anim_f0.png", self.life_points_monster, self.damage]
                                            playerSelf.update_infoPW()
                                            playerSelf.eventMonsterAttack("w")
                                            playerSelf.eventMAVar = True
                                        elif ci[2] < new_x1 and ci[2] < new_x2 and ci[1] == new_y1 and ci[3] == new_y2:
                                            print("E")
                                            playerSelf.fullMonster["e"] = ["./sprites/big_zombie_idle_anim_f0.png", self.life_points_monster, self.damage]
                                            playerSelf.update_infoPE()
                                            playerSelf.eventMonsterAttack("e")
                                            playerSelf.eventMAVar = True
                                        elif ci[0] == new_x1 and ci[2] == new_x2 and ci[1] > new_y1 and ci[1] > new_y2:
                                            print("N")
                                            playerSelf.fullMonster["n"] = ["./sprites/big_zombie_idle_anim_f0.png", self.life_points_monster, self.damage]
                                            playerSelf.update_infoPN()
                                            playerSelf.eventMonsterAttack("n")
                                            playerSelf.eventMAVar = True
                                        elif ci[0] == new_x1 and ci[2] == new_x2 and ci[3] < new_y1 and ci[3] < new_y2:
                                            print("S")
                                            playerSelf.fullMonster["s"] = ["./sprites/big_zombie_idle_anim_f0.png", self.life_points_monster, self.damage]
                                            playerSelf.update_infoPS()
                                            playerSelf.eventMonsterAttack("s")
                                            playerSelf.eventMAVar = True
                                playerSelf.eventMWVar = True
                                areaPlay.move(self.monster, dx * self.moveDistance, dy * self.moveDistance)
                                areaPlay.move(self.health_bar, dx * self.moveDistance, dy * self.moveDistance)
                                areaPlay.move(self.monster_image, dx * self.moveDistance, dy * self.moveDistance)
                            else:
                                self.diag = False
                                dx = 1
                                dy = 0
                                new_x1 = self.monster_x1 + dx * self.moveDistance
                                new_y1 = self.monster_y1
                                new_x2 = self.monster_x2 + dx * self.moveDistance
                                new_y2 = self.monster_y2
                                if any(new_x2 > case[0] and new_y2 > case[1] and new_x1 < case[2] and new_y1 < case[3] for case in map.CaseNoire.values()):
                                    self.diag = True
                                    dx = 0
                                    dy = 1
                                new_x2 = self.monster_x2 + dx * self.moveDistance
                                new_x1 = self.monster_x1 + dx *self.moveDistance
                                new_y1 = self.monster_y1 + dy * self.moveDistance
                                new_y2 = self.monster_y2 + dy * self.moveDistance
                                for monster in playerSelf.monsterDico.values():
                                    if areaPlay.coords(monster) != areaPlay.coords(self.monster):
                                        if (new_x2 > monster[0] 
                                        and new_y2 > monster[1]
                                        and new_x1 < monster[2]
                                        and new_y1 < monster[3]):
                                            return
                                if ci[2] + tolerance >= new_x1 and ci[0] <= new_x2 + tolerance:
                                    if ci[3] + tolerance >= new_y1 and ci[1] <= new_y2 + tolerance:
                                        print("Collision avec le monstre")
                                        if ci[0] > new_x2 and ci[0] > new_x2 and ci[1] == new_y1 and ci[3] == new_y2:
                                            print("W")
                                            playerSelf.fullMonster["w"] = ["./sprites/big_zombie_idle_anim_f0.png", self.life_points_monster, self.damage]
                                            playerSelf.update_infoPW()
                                            playerSelf.eventMonsterAttack("w")
                                            playerSelf.eventMAVar = True
                                        elif ci[2] < new_x1 and ci[2] < new_x2 and ci[1] == new_y1 and ci[3] == new_y2:
                                            print("E")
                                            playerSelf.fullMonster["e"] = ["./sprites/big_zombie_idle_anim_f0.png", self.life_points_monster, self.damage]
                                            playerSelf.update_infoPE()
                                            playerSelf.eventMonsterAttack("e")
                                            playerSelf.eventMAVar = True
                                        elif ci[0] == new_x1 and ci[2] == new_x2 and ci[1] > new_y1 and ci[1] > new_y2:
                                            print("N")
                                            playerSelf.fullMonster["n"] = ["./sprites/big_zombie_idle_anim_f0.png", self.life_points_monster, self.damage]
                                            playerSelf.update_infoPN()
                                            playerSelf.eventMonsterAttack("n")
                                            playerSelf.eventMAVar = True
                                        elif ci[0] == new_x1 and ci[2] == new_x2 and ci[3] < new_y1 and ci[3] < new_y2:
                                            print("S")
                                            playerSelf.fullMonster["s"] = ["./sprites/big_zombie_idle_anim_f0.png", self.life_points_monster, self.damage]
                                            playerSelf.update_infoPS()
                                            playerSelf.eventMonsterAttack("s")
                                            playerSelf.eventMAVar = True
                                playerSelf.eventMWVar = True
                                areaPlay.move(self.monster, dx * self.moveDistance, dy * self.moveDistance)
                                areaPlay.move(self.health_bar, dx * self.moveDistance, dy * self.moveDistance)
                                areaPlay.move(self.monster_image, dx * self.moveDistance, dy * self.moveDistance)

                    ##print("diag")
                
                ##print("not intersec")
            else:
                self.diag = False
                ##print("intersec")
                stop = False
                if self.monster_x2 + self.moveDistance > WindowParameter.mapWidth-WindowParameter.tileSize:
                    ##print("test1")
                    self.diag = False
                    ##print("x2")
                    #areaPlay.move(self.monster, -1*self.moveDistance, 0)
                    
                    dx = random.choice([-1, 0])
                    dy = random.choice([-1, 1]) if dx == 0 else 0  # Empêche les mouvements en diagonal
                    new_x1 = self.monster_x1 + dx * self.moveDistance
                    new_y1 = self.monster_y1 + dy * self.moveDistance
                    new_x2 = self.monster_x2 + dx * self.moveDistance
                    new_y2 = self.monster_y2 + dy * self.moveDistance
                    
                    for monster in playerSelf.monsterDico.values():
                        if areaPlay.coords(monster) != areaPlay.coords(self.monster):
                            if (new_x2 > monster[0] 
                            and new_y2 > monster[1]
                            and new_x1 < monster[2]
                            and new_y1 < monster[3]):
                                stop = True        
                    ##print(new_x1, new_y1, new_x2, new_y2)
                    while (new_x2 > WindowParameter.mapWidth or
                    any(new_x2 > case[0] and new_y2 > case[1] and new_x1 < case[2] and new_y1 < case[3] for case in map.CaseNoire.values()) or
                    any(new_x2 > monster[0] and new_y2 > monster[1] and new_x1 < monster[2] and new_y1 < monster[3] for monster in playerSelf.monsterDico.values()) or stop == True):
                        ##print("Whiletest1")
                        stop = False
                        for monster in playerSelf.monsterDico.values():
                            if areaPlay.coords(monster) != areaPlay.coords(self.monster):
                                if (new_x2 > monster[0] 
                                and new_y2 > monster[1]
                                and new_x1 < monster[2]
                                and new_y1 < monster[3]):
                                    stop = True
                        if self.antiInfinite > 150:
                             return
                        self.antiInfinite += 1
                        dx = random.choice([-1, 0])
                        dy = random.choice([-1, 1]) if dx == 0 else 0  # Empêche les mouvements en diagonal
                        new_x1 = self.monster_x1 + dx * self.moveDistance
                        new_y1 = self.monster_y1 + dy * self.moveDistance
                        new_x2 = self.monster_x2 + dx * self.moveDistance
                        new_y2 = self.monster_y2 + dy * self.moveDistance
                    playerSelf.eventMWVar = True
                    areaPlay.move(self.monster, dx * self.moveDistance, dy * self.moveDistance)
                    areaPlay.move(self.health_bar, dx * self.moveDistance, dy * self.moveDistance)
                    areaPlay.move(self.monster_image, dx * self.moveDistance, dy * self.moveDistance)
                elif self.monster_x1 - self.moveDistance < 0+WindowParameter.tileSize:
                            self.diag = False
                            dx = random.choice([0, 1])
                            dy = random.choice([-1, 1]) if dx == 0 else 0  # Empêche les mouvements en diagonal
                            new_x1 = self.monster_x1 + dx * self.moveDistance
                            new_y1 = self.monster_y1 + dy * self.moveDistance
                            new_x2 = self.monster_x2 + dx * self.moveDistance
                            new_y2 = self.monster_y2 + dy * self.moveDistance
                            for monster in playerSelf.monsterDico.values():
                                if areaPlay.coords(monster) != areaPlay.coords(self.monster):
                                    if (new_x2 > monster[0] 
                                    and new_y2 > monster[1]
                                    and new_x1 < monster[2]
                                    and new_y1 < monster[3]):
                                        stop = True
                            ##print(new_x1, new_y1, new_x2, new_y2)
                            while (new_x1 < 0 or
                            any(new_x2 > case[0] and new_y2 > case[1] and new_x1 < case[2] and new_y1 < case[3] for case in map.CaseNoire.values()) or
                            any(new_x2 > monster[0] and new_y2 > monster[1] and new_x1 < monster[2] and new_y1 < monster[3] for monster in playerSelf.monsterDico.values()) or stop == True):
                                ##print("Whiletest2")
                                stop = False
                                for monster in playerSelf.monsterDico.values():
                                    if areaPlay.coords(monster) != areaPlay.coords(self.monster):
                                        if (new_x2 > monster[0] 
                                        and new_y2 > monster[1]
                                        and new_x1 < monster[2]
                                        and new_y1 < monster[3]):
                                            stop = True
                                if self.antiInfinite > 150:
                                    return
                                self.antiInfinite += 1
                                dx = random.choice([0, 1])
                                dy = random.choice([-1, 1]) if dx == 0 else 0  # Empêche les mouvements en diagonal
                                new_x1 = self.monster_x1 + dx * self.moveDistance
                                new_y1 = self.monster_y1 + dy * self.moveDistance
                                new_x2 = self.monster_x2 + dx * self.moveDistance
                                new_y2 = self.monster_y2 + dy * self.moveDistance
                            playerSelf.eventMWVar = True
                            areaPlay.move(self.monster, dx * self.moveDistance, dy * self.moveDistance)
                            areaPlay.move(self.health_bar, dx * self.moveDistance, dy * self.moveDistance)
                            areaPlay.move(self.monster_image, dx * self.moveDistance, dy * self.moveDistance)
                elif self.monster_y2 + self.moveDistance > WindowParameter.mapHeight-WindowParameter.tileSize:
                            self.diag = False
                            ##print("test3")
                            ##print("y2")
                            #areaPlay.move(self.monster, 0, -1*self.moveDistance)
                            dy = random.choice([-1, 0])
                            dx = random.choice([-1, 1]) if dy == 0 else 0  # Empêche les mouvements en diagonal
                            new_x1 = self.monster_x1 + dx * self.moveDistance
                            new_y1 = self.monster_y1 + dy * self.moveDistance
                            new_x2 = self.monster_x2 + dx * self.moveDistance
                            new_y2 = self.monster_y2 + dy * self.moveDistance
                            for monster in playerSelf.monsterDico.values():
                                if areaPlay.coords(monster) != areaPlay.coords(self.monster):
                                    if (new_x2 > monster[0] 
                                    and new_y2 > monster[1]
                                    and new_x1 < monster[2]
                                    and new_y1 < monster[3]):
                                        stop = True
                            ##print(new_x1, new_y1, new_x2, new_y2)
                            while (new_y2 > WindowParameter.mapHeight or
                            any(new_x2 > case[0] and new_y2 > case[1] and new_x1 < case[2] and new_y1 < case[3] for case in map.CaseNoire.values()) or
                            any(new_x2 > monster[0] and new_y2 > monster[1] and new_x1 < monster[2] and new_y1 < monster[3] for monster in playerSelf.monsterDico.values()) or stop == True):
                                ##print("Whiletest3")
                                stop = False
                                for monster in playerSelf.monsterDico.values():
                                    if areaPlay.coords(monster) != areaPlay.coords(self.monster):
                                        if (new_x2 > monster[0] 
                                        and new_y2 > monster[1]
                                        and new_x1 < monster[2]
                                        and new_y1 < monster[3]):
                                            stop = True
                                if self.antiInfinite > 150:
                                    return
                                self.antiInfinite += 1
                                dy = random.choice([-1, 0])
                                dx = random.choice([-1, 1]) if dy == 0 else 0  # Empêche les mouvements en diagonal
                                new_x1 = self.monster_x1 + dx * self.moveDistance
                                new_y1 = self.monster_y1 + dy * self.moveDistance
                                new_x2 = self.monster_x2 + dx * self.moveDistance
                                new_y2 = self.monster_y2 + dy * self.moveDistance
                            playerSelf.eventMWVar = True
                            areaPlay.move(self.monster, dx * self.moveDistance, dy * self.moveDistance)
                            areaPlay.move(self.health_bar, dx * self.moveDistance, dy * self.moveDistance)
                            areaPlay.move(self.monster_image, dx * self.moveDistance, dy * self.moveDistance)
                            
                elif self.monster_y1 - self.moveDistance < 0+WindowParameter.tileSize:
                            self.diag = False
                            dy = random.choice([0, 1])
                            dx = random.choice([-1, 1]) if dy == 0 else 0  # Empêche les mouvements en diagonal
                            new_x1 = self.monster_x1 + dx * self.moveDistance
                            new_y1 = self.monster_y1 + dy * self.moveDistance
                            new_x2 = self.monster_x2 + dx * self.moveDistance
                            new_y2 = self.monster_y2 + dy * self.moveDistance
                            for monster in playerSelf.monsterDico.values():
                                if areaPlay.coords(monster) != areaPlay.coords(self.monster):
                                    if (new_x2 > monster[0] 
                                    and new_y2 > monster[1]
                                    and new_x1 < monster[2]
                                    and new_y1 < monster[3]):
                                        stop = True
                            ##print(new_x1, new_y1, new_x2, new_y2)
                            while (new_y1 < 0 or
                            any(new_x2 > case[0] and new_y2 > case[1] and new_x1 < case[2] and new_y1 < case[3] for case in map.CaseNoire.values()) or
                            any(new_x2 > monster[0] and new_y2 > monster[1] and new_x1 < monster[2] and new_y1 < monster[3] for monster in playerSelf.monsterDico.values()) or stop == True):
                                ##print("Whiletest4")
                                stop = False
                                for monster in playerSelf.monsterDico.values():
                                    if areaPlay.coords(monster) != areaPlay.coords(self.monster):
                                        if (new_x2 > monster[0] 
                                        and new_y2 > monster[1]
                                        and new_x1 < monster[2]
                                        and new_y1 < monster[3]):
                                            stop = True
                                if self.antiInfinite > 150:
                                    return
                                self.antiInfinite += 1
                                dy = random.choice([0, 1])
                                dx = random.choice([-1, 1]) if dy == 0 else 0  # Empêche les mouvements en diagonal
                                new_x1 = self.monster_x1 + dx * self.moveDistance
                                new_y1 = self.monster_y1 + dy * self.moveDistance
                                new_x2 = self.monster_x2 + dx * self.moveDistance
                                new_y2 = self.monster_y2 + dy * self.moveDistance
                            playerSelf.eventMWVar = True
                            areaPlay.move(self.monster, dx * self.moveDistance, dy * self.moveDistance)
                            areaPlay.move(self.health_bar, dx * self.moveDistance, dy * self.moveDistance)
                            #areaPlay.move(self.monster_pic, -20, 0)
                else:
                    self.diag = False
                    coll = False
                    index = list(map.CaseNoire.keys())
                    i = 0
                    dx = random.randint(-1, 1)
                    dy = random.choice([-1, 1]) if dx == 0 else 0  # Empêche les mouvements en diagonal
                    new_x1 = self.monster_x1 + dx * self.moveDistance
                    new_y1 = self.monster_y1 + dy * self.moveDistance
                    new_x2 = self.monster_x2 + dx * self.moveDistance
                    new_y2 = self.monster_y2 + dy * self.moveDistance
                    ##print("test5")
                    for monster in playerSelf.monsterDico.values():
                        if areaPlay.coords(monster) != areaPlay.coords(self.monster):
                            if (new_x2 > monster[0] 
                            and new_y2 > monster[1]
                            and new_x1 < monster[2]
                            and new_y1 < monster[3]):
                                stop = True
                    # Vérification de collision avec les murs (cases noires) et les carrés bleus
                    while (any(new_x2 > case[0] and new_y2 > case[1] and new_x1 < case[2] and new_y1 < case[3] for case in map.CaseNoire.values()) or
                        any(new_x2 > monster[0] and new_y2 > monster[1] and new_x1 < monster[2] and new_y1 < monster[3] for monster in playerSelf.monsterDico.values()) or stop == True):
                        ##print("Whiletest5")
                        stop = False
                        for monster in playerSelf.monsterDico.values():
                            if areaPlay.coords(monster) != areaPlay.coords(self.monster):
                                if (new_x2 > monster[0] 
                                and new_y2 > monster[1]
                                and new_x1 < monster[2]
                                and new_y1 < monster[3]):
                                    stop = True
                        if self.antiInfinite > 150:
                             return
                        self.antiInfinite += 1
                        dx = random.randint(-1, 1)
                        dy = random.choice([-1, 1]) if dx == 0 else 0  # Empêche les mouvements en diagonal
                        new_x1 = self.monster_x1 + dx * self.moveDistance
                        new_y1 = self.monster_y1 + dy * self.moveDistance
                        new_x2 = self.monster_x2 + dx * self.moveDistance
                        new_y2 = self.monster_y2 + dy * self.moveDistance
                    playerSelf.eventMWVar = True
                    areaPlay.move(self.monster, dx * self.moveDistance, dy * self.moveDistance)
                    areaPlay.move(self.health_bar, dx * self.moveDistance, dy * self.moveDistance)
                    areaPlay.move(self.monster_image, dx * self.moveDistance, dy * self.moveDistance)

                # #print(dx)
                # #print(dy)
                """if dx == 0 and dy < 0:
                    areaPlay.move(self.monster, 0, -1 * self.moveDistance)
                elif dx == 0 and dy > 0:
                    areaPlay.move(self.monster, 0, 1 * self.moveDistance)
                elif dx < 0 and dy == 0:
                    areaPlay.move(self.monster, -1 * self.moveDistance , 0)
                elif dx > 0 and dy == 0:
                    areaPlay.move(self.monster, +1 * self.moveDistance , 0)"""
            

        elif self.monster_x2 + self.moveDistance > WindowParameter.mapWidth-WindowParameter.tileSize:
                    ##print("test6")
                    self.monster_collision = False
                    self.diag = False
                    stop = False
                    ##print("x2")
                    #areaPlay.move(self.monster, -1*self.moveDistance, 0)

                    dx = random.choice([-1, 0])
                    dy = random.choice([-1, 1]) if dx == 0 else 0  # Empêche les mouvements en diagonal
                    new_x1 = self.monster_x1 + dx * self.moveDistance
                    new_y1 = self.monster_y1 + dy * self.moveDistance
                    new_x2 = self.monster_x2 + dx * self.moveDistance
                    new_y2 = self.monster_y2 + dy * self.moveDistance
                    for monster in playerSelf.monsterDico.values():
                            if areaPlay.coords(monster) != areaPlay.coords(self.monster):
                                if (new_x2 > monster[0] 
                                and new_y2 > monster[1]
                                and new_x1 < monster[2]
                                and new_y1 < monster[3]):
                                    stop = True
                    ##print(new_x1, new_y1, new_x2, new_y2)
                    while (new_x2 > WindowParameter.mapWidth or
                    any(new_x2 > case[0] and new_y2 > case[1] and new_x1 < case[2] and new_y1 < case[3] for case in map.CaseNoire.values()) or
                    any(new_x2 > monster[0] and new_y2 > monster[1] and new_x1 < monster[2] and new_y1 < monster[3] for monster in playerSelf.monsterDico.values()) or stop == True):
                        ##print("Whiletest6")
                        stop = False
                        for monster in playerSelf.monsterDico.values():
                            if areaPlay.coords(monster) != areaPlay.coords(self.monster):
                                if (new_x2 > monster[0] 
                                and new_y2 > monster[1]
                                and new_x1 < monster[2]
                                and new_y1 < monster[3]):
                                    stop = True
                        if self.antiInfinite > 150:
                             return
                        self.antiInfinite += 1
                        dx = random.choice([-1, 0])
                        dy = random.choice([-1, 1]) if dx == 0 else 0  # Empêche les mouvements en diagonal
                        new_x1 = self.monster_x1 + dx * self.moveDistance
                        new_y1 = self.monster_y1 + dy * self.moveDistance
                        new_x2 = self.monster_x2 + dx * self.moveDistance
                        new_y2 = self.monster_y2 + dy * self.moveDistance
                    playerSelf.eventMWVar = True
                    areaPlay.move(self.monster, dx * self.moveDistance, dy * self.moveDistance)
                    areaPlay.move(self.health_bar, dx * self.moveDistance, dy * self.moveDistance)
                    areaPlay.move(self.monster_image, dx * self.moveDistance, dy * self.moveDistance)
                    
        elif self.monster_x1 - self.moveDistance < 0+WindowParameter.tileSize:
                    self.monster_collision = False
                    self.diag = False
                    ##print("x1")
                    ##print("test7")
                    #areaPlay.move(self.monster, +1*self.moveDistance, 0)
                    dx = random.choice([0, 1])
                    dy = random.choice([-1, 1]) if dx == 0 else 0  # Empêche les mouvements en diagonal
                    new_x1 = self.monster_x1 + dx * self.moveDistance
                    new_y1 = self.monster_y1 + dy * self.moveDistance
                    new_x2 = self.monster_x2 + dx * self.moveDistance
                    new_y2 = self.monster_y2 + dy * self.moveDistance
                    stop = False
                    for monster in playerSelf.monsterDico.values():
                            if areaPlay.coords(monster) != areaPlay.coords(self.monster):
                                if (new_x2 > monster[0] 
                                and new_y2 > monster[1]
                                and new_x1 < monster[2]
                                and new_y1 < monster[3]):
                                    stop = True
                    ##print(new_x1, new_y1, new_x2, new_y2)
                    while (new_x1 < 0 or
                    any(new_x2 > case[0] and new_y2 > case[1] and new_x1 < case[2] and new_y1 < case[3] for case in map.CaseNoire.values()) or
                    any(new_x2 > monster[0] and new_y2 > monster[1] and new_x1 < monster[2] and new_y1 < monster[3] for monster in playerSelf.monsterDico.values()) or stop == True):
                        ##print("Whiletest7")
                        stop = False
                        for monster in playerSelf.monsterDico.values():
                            if areaPlay.coords(monster) != areaPlay.coords(self.monster):
                                if (new_x2 > monster[0] 
                                and new_y2 > monster[1]
                                and new_x1 < monster[2]
                                and new_y1 < monster[3]):
                                    stop = True
                        if self.antiInfinite > 150:
                             return
                        self.antiInfinite += 1
                        dx = random.choice([0, 1])
                        dy = random.choice([-1, 1]) if dx == 0 else 0  # Empêche les mouvements en diagonal
                        new_x1 = self.monster_x1 + dx * self.moveDistance
                        new_y1 = self.monster_y1 + dy * self.moveDistance
                        new_x2 = self.monster_x2 + dx * self.moveDistance
                        new_y2 = self.monster_y2 + dy * self.moveDistance
                    playerSelf.eventMWVar = True
                    areaPlay.move(self.monster, dx * self.moveDistance, dy * self.moveDistance)
                    areaPlay.move(self.health_bar, dx * self.moveDistance, dy * self.moveDistance)
                    areaPlay.move(self.monster_image, dx * self.moveDistance, dy * self.moveDistance)
                    #areaPlay.move(self.monster_pic, -20, 0)
        elif self.monster_y2 + self.moveDistance > WindowParameter.mapHeight-WindowParameter.tileSize:
                    self.monster_collision = False
                    self.diag = False
                    ##print("y2")
                    ##print("test8")
                    #areaPlay.move(self.monster, 0, -1*self.moveDistance)
                    dy = random.choice([-1, 0])
                    dx = random.choice([-1, 1]) if dy == 0 else 0  # Empêche les mouvements en diagonal
                    new_x1 = self.monster_x1 + dx * self.moveDistance
                    new_y1 = self.monster_y1 + dy * self.moveDistance
                    new_x2 = self.monster_x2 + dx * self.moveDistance
                    new_y2 = self.monster_y2 + dy * self.moveDistance
                    stop = False
                    for monster in playerSelf.monsterDico.values():
                            if areaPlay.coords(monster) != areaPlay.coords(self.monster):
                                if (new_x2 > monster[0] 
                                and new_y2 > monster[1]
                                and new_x1 < monster[2]
                                and new_y1 < monster[3]):
                                    stop = True
                    ##print(new_x1, new_y1, new_x2, new_y2)
                    while (new_y2 > WindowParameter.mapHeight or
                    any(new_x2 > case[0] and new_y2 > case[1] and new_x1 < case[2] and new_y1 < case[3] for case in map.CaseNoire.values()) or
                    any(new_x2 > monster[0] and new_y2 > monster[1] and new_x1 < monster[2] and new_y1 < monster[3] for monster in playerSelf.monsterDico.values()) or stop == True):
                        ##print("Whiletest8")
                        stop = False
                        for monster in playerSelf.monsterDico.values():
                            if areaPlay.coords(monster) != areaPlay.coords(self.monster):
                                if (new_x2 > monster[0] 
                                and new_y2 > monster[1]
                                and new_x1 < monster[2]
                                and new_y1 < monster[3]):
                                    stop = True
                        if self.antiInfinite > 150:
                             return
                        self.antiInfinite += 1
                        dy = random.choice([-1, 0])
                        dx = random.choice([-1, 1]) if dy == 0 else 0  # Empêche les mouvements en diagonal
                        new_x1 = self.monster_x1 + dx * self.moveDistance
                        new_y1 = self.monster_y1 + dy * self.moveDistance
                        new_x2 = self.monster_x2 + dx * self.moveDistance
                        new_y2 = self.monster_y2 + dy * self.moveDistance
                    playerSelf.eventMWVar = True
                    areaPlay.move(self.monster, dx * self.moveDistance, dy * self.moveDistance)
                    areaPlay.move(self.health_bar, dx * self.moveDistance, dy * self.moveDistance)
                    areaPlay.move(self.monster_image, dx * self.moveDistance, dy * self.moveDistance)
                    #areaPlay.move(self.monster_pic, -20, 0)
        elif self.monster_y1 - self.moveDistance < 0+WindowParameter.tileSize:
                    self.monster_collision = False
                    self.diag = False
                    ##print("test9")
                    ##print("y1")
                    #areaPlay.move(self.monster, 0, +1*self.moveDistance)
                    dy = random.choice([0, 1])
                    dx = random.choice([-1, 1]) if dy == 0 else 0  # Empêche les mouvements en diagonal
                    new_x1 = self.monster_x1 + dx * self.moveDistance
                    new_y1 = self.monster_y1 + dy * self.moveDistance
                    new_x2 = self.monster_x2 + dx * self.moveDistance
                    new_y2 = self.monster_y2 + dy * self.moveDistance
                    stop = False
                    for monster in playerSelf.monsterDico.values():
                            if areaPlay.coords(monster) != areaPlay.coords(self.monster):
                                if (new_x2 > monster[0] 
                                and new_y2 > monster[1]
                                and new_x1 < monster[2]
                                and new_y1 < monster[3]):
                                    stop = True
                    ##print(new_x1, new_y1, new_x2, new_y2)
                    while (new_y1 < 0 or
                    any(new_x2 > case[0] and new_y2 > case[1] and new_x1 < case[2] and new_y1 < case[3] for case in map.CaseNoire.values()) or
                    any(new_x2 > monster[0] and new_y2 > monster[1] and new_x1 < monster[2] and new_y1 < monster[3] for monster in playerSelf.monsterDico.values()) or stop == True):
                        ##print("Whiletest10")
                        stop = False
                        for monster in playerSelf.monsterDico.values():
                            if areaPlay.coords(monster) != areaPlay.coords(self.monster):
                                if (new_x2 > monster[0] 
                                and new_y2 > monster[1]
                                and new_x1 < monster[2]
                                and new_y1 < monster[3]):
                                    stop = True
                        if self.antiInfinite > 150:
                             return
                        self.antiInfinite += 1
                        dy = random.choice([0, 1])
                        dx = random.choice([-1, 1]) if dy == 0 else 0  # Empêche les mouvements en diagonal
                        new_x1 = self.monster_x1 + dx * self.moveDistance
                        new_y1 = self.monster_y1 + dy * self.moveDistance
                        new_x2 = self.monster_x2 + dx * self.moveDistance
                        new_y2 = self.monster_y2 + dy * self.moveDistance
                    playerSelf.eventMWVar = True
                    areaPlay.move(self.monster, dx * self.moveDistance, dy * self.moveDistance)
                    areaPlay.move(self.health_bar, dx * self.moveDistance, dy * self.moveDistance)
                    areaPlay.move(self.monster_image, dx * self.moveDistance, dy * self.moveDistance)
                    #areaPlay.move(self.monster_pic, -20, 0)
        elif(playerSelf.player_collision == False):
            self.monster_collision = False
            self.diag = False
            coll = False
            index = list(map.CaseNoire.keys())
            i = 0
            ##print("test11")
            dx = random.randint(-1, 1)
            dy = random.choice([-1, 1]) if dx == 0 else 0  # Empêche les mouvements en diagonal
            new_x1 = self.monster_x1 + dx * self.moveDistance
            new_y1 = self.monster_y1 + dy * self.moveDistance
            new_x2 = self.monster_x2 + dx * self.moveDistance
            new_y2 = self.monster_y2 + dy * self.moveDistance
            stop = False
            for monster in playerSelf.monsterDico.values():
                            if areaPlay.coords(monster) != areaPlay.coords(self.monster):
                                if (new_x2 > monster[0] 
                                and new_y2 > monster[1]
                                and new_x1 < monster[2]
                                and new_y1 < monster[3]):
                                    stop = True
            # Vérification de collision avec les murs (cases noires) et les carrés bleus
            while (any(new_x2 > case[0] and new_y2 > case[1] and new_x1 < case[2] and new_y1 < case[3] for case in map.CaseNoire.values()) or
                any(new_x2 > monster[0] and new_y2 > monster[1] and new_x1 < monster[2] and new_y1 < monster[3] for monster in playerSelf.monsterDico.values()) or stop == True):
                ##print("Whiletest11")
                stop = False
                for monster in playerSelf.monsterDico.values():
                            if areaPlay.coords(monster) != areaPlay.coords(self.monster):
                                if (new_x2 > monster[0] 
                                and new_y2 > monster[1]
                                and new_x1 < monster[2]
                                and new_y1 < monster[3]):
                                    stop = True
                if self.antiInfinite > 150:
                    return
                self.antiInfinite += 1
                ##print((new_x1, new_y1, new_x2, new_y2))
                dx = random.randint(-1, 1)
                dy = random.choice([-1, 1]) if dx == 0 else 0  # Empêche les mouvements en diagonal
                new_x1 = self.monster_x1 + dx * self.moveDistance
                new_y1 = self.monster_y1 + dy * self.moveDistance
                new_x2 = self.monster_x2 + dx * self.moveDistance
                new_y2 = self.monster_y2 + dy * self.moveDistance
            playerSelf.eventMWVar = True
            areaPlay.move(self.monster, dx * self.moveDistance, dy * self.moveDistance)
            areaPlay.move(self.health_bar, dx * self.moveDistance, dy * self.moveDistance)
    
    # Vérifier si deux segments de ligne s'intersectent
    def intersect(self, x1, y1, x2, y2, x3, y3, x4, y4):
        # Implémentez ici votre algorithme de détection d'intersection
        # Renvoyez True si les segments s'intersectent, False sinon

        # Exemple d'implémentation simplifiée avec une intersection de segments basée sur les coordonnées des points
        if max(x1, x2) < min(x3, x4) or max(x3, x4) < min(x1, x2) or max(y1, y2) < min(y3, y4) or max(y3, y4) < min(y1, y2):
            return False
        return True
    
         
