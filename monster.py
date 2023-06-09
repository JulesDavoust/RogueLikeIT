import random
import tkinter as tk

class Monster:
    
    def __init__(self, MapLevel) -> None:
        self.monster_collision = False
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
        self.monster = areaPlay.create_rectangle(x, y, x + 30, y + 30, fill="black")

    def moveMonster(self, areaPlay, x1P, y1P, x2P, y2P, target_x, target_y, x2, x1, y2, y1, playerSelf):
        self.monster_coords = areaPlay.coords(self.monster)
        self.monster_x1 = self.monster_coords[0]
        self.monster_y1 = self.monster_coords[1]  
        self.monster_x2 = self.monster_coords[2]
        self.monster_y2 = self.monster_coords[3]
        print("Monster : x1 : ",self.monster_x1)
        

        self.current_x = (self.monster_coords[0] + self.monster_coords[2])/2
        self.current_y = (self.monster_coords[1] + self.monster_coords[3])/2

        
        """if x1_rect1 < x2_rect2 and x2_rect1 > x1_rect2 and y1_rect1 < y2_rect2 and y2_rect1 > y1_rect2:"""
        if(self.monster_x1 < x2 and self.monster_x2 > x1 and self.monster_y1 < y2 and self.monster_y2 > y1 and playerSelf.player_collision == False):
            playerSelf.player_collision = True
            playerSelf.startFight()
        elif(self.monster_x1 < x2P and self.monster_x2 > x1P and self.monster_y1 < y2P and self.monster_y2 > y1P and playerSelf.player_collision == False):
            print("Monster : x1 : ",self.monster_x1," y1 : ",self.monster_y1," x2 : ",self.monster_x2," y2 : ",self.monster_y2)
            dx = target_x - self.current_x  # Déplacement en x nécessaire
            dy = target_y - self.current_y  # Déplacement en y nécessaire

            self.step_x = dx/self.speed
            self.step_y = dy/self.speed

            for _ in range(50):
                areaPlay.move(self.monster, self.step_x, self.step_y)
                areaPlay.update()  # Mise à jour de la fenêtre du canvas
        elif(playerSelf.player_collision == False):
            dx = random.randint(-20, 20)
            dy = random.randint(-20, 20)

            new_x1 = self.monster_x1 + dx
            new_y1 = self.monster_y1 + dy
            new_x2 = self.monster_x2 + dx
            new_y2 = self.monster_y2 + dy

            
            if new_x1 < 0:  # Bord gauche
                new_x1 = 0
                new_x2 = new_x1 + (self.monster_x2 - self.monster_x1)
            elif new_x2 > 1000:  # Bord droit
                new_x2 = 1000
                new_x1 = new_x2 - (self.monster_x2 - self.monster_x1)
            if new_y1 < 0:  # Bord supérieur
                new_y1 = 0
                new_y2 = new_y1 + (self.monster_y2 - self.monster_y1)
            elif new_y2 > 700:  # Bord inférieur
                new_y2 = 700
                new_y1 = new_y2 - (self.monster_y2 - self.monster_y1)

            areaPlay.move(self.monster, new_x1 - self.monster_x1, new_y1 - self.monster_y1)

        
        
        
        