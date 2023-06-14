import math
import random
import tkinter as tk
from windowParameters import WindowParameter

class Monster:
    
    def __init__(self, MapLevel) -> None:
        self.direction = [0, 1, 2, 3]
        self.monster_collision = False
        self.monster_positions = []  # Liste pour stocker les positions des monstres
        self.life_points_monster = 50
        self.moveDistance = WindowParameter.tileSize
        #self.zombie = tk.PhotoImage(file="C:/Users/jules/Desktop/big_zombie_idle_anim_f0.png")

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
        elif(self.level <= 4 and self.level > 2):
            self.damage = 10
        elif(self.level <= 7 and self.level > 4):
            self.damage = 15
        elif(self.level <= 10 and self.level > 7):
            self.damage = 25
        elif(self.level > 10):
            self.damage = 30

    

    def generateMonster(self, areaPlay, x, y):
        self.monster = areaPlay.create_rectangle(x, y, x + WindowParameter.tileSize-1, y + WindowParameter.tileSize-1, fill="black", outline = "")
        #self.monster_pic = areaPlay.create_image((x+x+30)/2, (y+y+30)/2, image=self.zombie)
        self.monster_positions.append((x, y))  # Ajouter la position du monstre à la liste

    

    def moveMonster(self, areaPlay, x1P, y1P, x2P, y2P, target_x, target_y, x2, x1, y2, y1, playerSelf, map):
        self.monster_coords = areaPlay.coords(self.monster)
        self.monster_x1 = self.monster_coords[0]
        self.monster_y1 = self.monster_coords[1]  
        self.monster_x2 = self.monster_coords[2]
        self.monster_y2 = self.monster_coords[3]
        #print("Monster : x1 : ",self.monster_x1)
        

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
        print(slope)

        dx = self.moveDistance
        dy = -self.moveDistance
        """if x1_rect1 < x2_rect2 and x2_rect1 > x1_rect2 and y1_rect1 < y2_rect2 and y2_rect1 > y1_rect2:"""
        
        if(self.monster_x1-3 < x2 and self.monster_x2+3 > x1 and self.monster_y1-3 < y2 and self.monster_y2+3 > y1 and playerSelf.player_collision == False):
            #playerSelf.player_collision = True
            self.monster_collision = True
            #playerSelf.startFight()
            print("collision with player")
            
        elif(self.monster_x1 < x2P and self.monster_x2 > x1P and self.monster_y1 < y2P and self.monster_y2 > y1P and playerSelf.player_collision == False and playerSelf.collPNJ == False):
            
            # Tracer une ligne entre les centres des carrés 
            line_equation = lambda x: (red_center_y - black_center_y) * (x - black_center_x) / (red_center_x - black_center_x) + black_center_y
            is_black_tile_in_between = False
            for x in range(int(min(black_center_x, red_center_x)), int(max(black_center_x, red_center_x))):
                y = line_equation(x)
                print(y)
                if self.isBlackTile(x, y, map):
                    is_black_tile_in_between = True
                    break
            
            
            #print(is_black_tile_in_between)
            if is_black_tile_in_between == False:
                dx = (target_x - self.current_x)  # Déplacement en x nécessaire
                dy = (target_y - self.current_y)  # Déplacement en y nécessaire

                print(dx)
                print(dy)
                if dx == 0 and dy < 0:

                    areaPlay.move(self.monster, 0, -1 * self.moveDistance)
                elif dx == 0 and dy > 0:
                    areaPlay.move(self.monster, 0, 1 * self.moveDistance)
                elif dx < 0 and dy == 0:
                    areaPlay.move(self.monster, -1 * self.moveDistance , 0)
                elif dx > 0 and dy == 0:
                    areaPlay.move(self.monster, +1 * self.moveDistance , 0)
            else:
                dx = random.randint(-1, 1)
                dy = random.choice([-1, 1]) if dx == 0 else 0  # Empêche les mouvements en diagonal
                new_x1 = self.monster_x1 + dx * self.moveDistance
                new_y1 = self.monster_y1 + dy * self.moveDistance
                new_x2 = self.monster_x2 + dx * self.moveDistance
                new_y2 = self.monster_y2 + dy * self.moveDistance
                #print(new_x1, new_y1, new_x2, new_y2)
                while any(new_x2 > case[0] and new_y2 > case[1] and new_x1 < case[2] and new_y1 < case[3] for case in map.CaseNoire.values()):
                    dx = random.randint(-1, 1)
                    dy = random.choice([-1, 1]) if dx == 0 else 0  # Empêche les mouvements en diagonal
                    new_x1 = self.monster_x1 + dx * self.moveDistance
                    new_y1 = self.monster_y1 + dy * self.moveDistance
                    new_x2 = self.monster_x2 + dx * self.moveDistance
                    new_y2 = self.monster_y2 + dy * self.moveDistance

                areaPlay.move(self.monster, dx * self.moveDistance, dy * self.moveDistance)
                #areaPlay.move(self.monster_pic, dx, dy)

        elif self.monster_x2 + 10 > map.map_width:
                    #print("x2")
                    areaPlay.move(self.monster, -1*self.moveDistance, 0)
                    #areaPlay.move(self.monster_pic, -20, 0)
        elif self.monster_x1 - 10 < 0:
                    #print("x1")
                    areaPlay.move(self.monster, +1*self.moveDistance, 0)
                    #areaPlay.move(self.monster_pic, -20, 0)
        elif self.monster_y2 + 10 > map.map_height:
                    #print("y2")
                    areaPlay.move(self.monster, 0, -1*self.moveDistance)
                    #areaPlay.move(self.monster_pic, -20, 0)
        elif self.monster_y1 - 10 < 0:
                    #print("y1")
                    areaPlay.move(self.monster, 0, +1*self.moveDistance)
                    #areaPlay.move(self.monster_pic, -20, 0)
        elif(playerSelf.player_collision == False):
            coll = False
            index = list(map.CaseNoire.keys())
            i = 0
            dx = random.randint(-1, 1)
            dy = random.choice([-1, 1]) if dx == 0 else 0  # Empêche les mouvements en diagonal
            new_x1 = self.monster_x1 + dx * self.moveDistance
            new_y1 = self.monster_y1 + dy * self.moveDistance
            new_x2 = self.monster_x2 + dx * self.moveDistance
            new_y2 = self.monster_y2 + dy * self.moveDistance
            #print(new_x1, new_y1, new_x2, new_y2)
            while any(new_x2 > case[0] and new_y2 > case[1] and new_x1 < case[2] and new_y1 < case[3] for case in map.CaseNoire.values()):
                dx = random.randint(-1, 1)
                dy = random.choice([-1, 1]) if dx == 0 else 0  # Empêche les mouvements en diagonal
                new_x1 = self.monster_x1 + dx * self.moveDistance
                new_y1 = self.monster_y1 + dy * self.moveDistance
                new_x2 = self.monster_x2 + dx * self.moveDistance
                new_y2 = self.monster_y2 + dy * self.moveDistance

            areaPlay.move(self.monster, dx * self.moveDistance, dy * self.moveDistance)

    def isBlackTile(self, x, y, map):
        for cle, valeur in map.CaseNoire.items():
            if valeur[0] < x < valeur[2] and valeur[1] < y < valeur[3]:
                return True
        return False

         
