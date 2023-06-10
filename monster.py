import math
import random
import tkinter as tk

class Monster:
    
    def __init__(self, MapLevel) -> None:
        self.direction = [0, 1, 2, 3]
        self.monster_collision = False
        self.monster_positions = []  # Liste pour stocker les positions des monstres

        #self.zombie = tk.PhotoImage(file="C:/Users/jules/Desktop/big_zombie_idle_anim_f0.png")

        if(MapLevel == 1):
            self.level = random.randint(1, 2)
        elif(MapLevel == 2 and MapLevel <=4):
            self.level = random.randint(2,4)
        elif(MapLevel == 5 and MapLevel <= 7):
            self.level = random.randint(5, 7)
        elif(MapLevel == 8 and MapLevel <= 10):
            self.level = random.randint(8, 10)
        elif(MapLevel > 10):
            self.level = random.randint(10, 15)
        
        if(self.level <= 2):
            self.damage = 5
            self.speed = 300
        elif(self.level <= 4 and self.level > 2):
            self.damage = 10
            self.speed = 300
        elif(self.level <= 7 and self.level > 4):
            self.damage = 15
            self.speed = 250
        elif(self.level <= 10 and self.level > 7):
            self.damage = 25
            self.speed = 200
        elif(self.level > 10):
            self.damage = 30
            self.speed = 200

    

    def generateMonster(self, areaPlay, x, y):
        self.monster = areaPlay.create_rectangle(x, y, x + 10, y + 10, fill="black", outline = "")
        #self.monster_pic = areaPlay.create_image((x+x+30)/2, (y+y+30)/2, image=self.zombie)
        self.monster_positions.append((x, y))  # Ajouter la position du monstre à la liste

    def moveMonster(self, areaPlay, x1P, y1P, x2P, y2P, target_x, target_y, x2, x1, y2, y1, playerSelf, map):
        self.monster_coords = areaPlay.coords(self.monster)
        self.monster_x1 = self.monster_coords[0]
        self.monster_y1 = self.monster_coords[1]  
        self.monster_x2 = self.monster_coords[2]
        self.monster_y2 = self.monster_coords[3]
        print("Monster : x1 : ",self.monster_x1)
        

        self.current_x = (self.monster_coords[0] + self.monster_coords[2])/2
        self.current_y = (self.monster_coords[1] + self.monster_coords[3])/2

        dx = +10
        dy = -10
        """if x1_rect1 < x2_rect2 and x2_rect1 > x1_rect2 and y1_rect1 < y2_rect2 and y2_rect1 > y1_rect2:"""
        if(self.monster_x1 < x2 and self.monster_x2 > x1 and self.monster_y1 < y2 and self.monster_y2 > y1 and playerSelf.player_collision == False):
            playerSelf.player_collision = True
            playerSelf.startFight()
        elif(self.monster_x1 < x2P and self.monster_x2 > x1P and self.monster_y1 < y2P and self.monster_y2 > y1P and playerSelf.player_collision == False):
            print("Monster : x1 : ",self.monster_x1," y1 : ",self.monster_y1," x2 : ",self.monster_x2," y2 : ",self.monster_y2)
            """self.caseNoireEntre = False
            for cle, valeur in map.CaseNoire.items():
                if ((self.current_x < valeur[0] and target_x > valeur[0]) 
                    or (self.current_x > valeur[0] and target_x < valeur[0])):
                    self.caseNoireEntre = True
                elif((self.current_y < valeur[1] and target_y > valeur[1]) 
                    or (self.current_y > valeur[1] and target_y < valeur[1])):
                     self.caseNoireEntre = True"""
            black_center_x = (self.monster_x1 + self.monster_x2) // 2
            black_center_y = (self.monster_y1 + self.monster_y2) // 2
            red_center_x = (x1P + x2P) // 2
            red_center_y = (y1P + y2P) // 2

            # Tracer une ligne entre les centres des carrés
            line_equation = lambda x: (red_center_y - black_center_y) * (x - black_center_x) / (red_center_x - black_center_x) + black_center_y
            is_black_tile_in_between = False
            for x in range(int(min(black_center_x, red_center_x)), int(max(black_center_x, red_center_x))):
                y = line_equation(x)
                if self.isBlackTile(x, y, map):
                    is_black_tile_in_between = True
                    break
            
            print(is_black_tile_in_between)
            if is_black_tile_in_between == False:
                dx = target_x - self.current_x  # Déplacement en x nécessaire
                dy = target_y - self.current_y  # Déplacement en y nécessaire

                self.step_x = dx/self.speed
                self.step_y = dy/self.speed

                for _ in range(50):
                    #areaPlay.move(self.monster_pic, self.step_x, self.step_y)
                    areaPlay.move(self.monster, self.step_x, self.step_y)
                    areaPlay.update()  # Mise à jour de la fenêtre du canvas
            else:
                dx = random.randint(-10, 10)
                dy = random.randint(-10, 10)
                new_x1 = self.monster_x1 + dx
                new_y1 = self.monster_y1 + dy
                new_x2 = self.monster_x2 + dx
                new_y2 = self.monster_y2 + dy

                for cle, valeur in map.CaseNoire.items():
                    if (
                        new_x2 > valeur[0]
                        and new_y2 > valeur[1]
                        and new_x1 < valeur[2]
                        and new_y1 < valeur[3]
                    ):
                        return
                areaPlay.move(self.monster, dx, dy)
                #areaPlay.move(self.monster_pic, dx, dy)

        elif self.monster_x2 + 10 > map.map_width:
                    print("x2")
                    areaPlay.move(self.monster, -10, 0)
                    #areaPlay.move(self.monster_pic, -20, 0)
        elif self.monster_x1 - 10 < 0:
                    print("x1")
                    areaPlay.move(self.monster, +10, 0)
                    #areaPlay.move(self.monster_pic, -20, 0)
        elif self.monster_y2 + 10 > map.map_height:
                    print("y2")
                    areaPlay.move(self.monster, 0, -10)
                    #areaPlay.move(self.monster_pic, -20, 0)
        elif self.monster_y1 - 10 < 0:
                    print("y1")
                    areaPlay.move(self.monster, 0, +10)
                    #areaPlay.move(self.monster_pic, -20, 0)
        elif(playerSelf.player_collision == False):
            dx = random.randint(-10, 10)
            dy = random.randint(-10, 10)
            new_x1 = self.monster_x1 + dx
            new_y1 = self.monster_y1 + dy
            new_x2 = self.monster_x2 + dx
            new_y2 = self.monster_y2 + dy

            for cle, valeur in map.CaseNoire.items():
                if (
                    new_x2 > valeur[0]
                    and new_y2 > valeur[1]
                    and new_x1 < valeur[2]
                    and new_y1 < valeur[3]
                ):
                    return
            #areaPlay.move(self.monster_pic, dx, dy)
            areaPlay.move(self.monster, dx, dy)

    def isBlackTile(self, x, y, map):
        for cle, valeur in map.CaseNoire.items():
            if valeur[0] < x < valeur[2] and valeur[1] < y < valeur[3]:
                return True
        return False
