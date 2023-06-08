import random
import tkinter as tk

class Monster:

    def __init__(self, MapLevel) -> None:
        self.damage = 10
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
        elif(self.level <= 4 and self.level > 2):
            self.damage = 10
        elif(self.level <= 7 and self.level > 4):
            self.damage = 15
        elif(self.level <= 10 and self.level > 7):
            self.damage = 25
        elif(self.level > 10):
            self.damage = 30
    
    def generateMonster(self, areaPlay):
        self.monster = areaPlay.create_rectangle(250, 250, 280, 280, fill="black")



        
