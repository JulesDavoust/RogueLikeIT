import random
import tkinter as tk
from windowParameters import WindowParameter


class PNJ:
    def __init__(self):
        self.finalShop = {}
        self.shop = {}
        self.NumberItems = 3

        self.sword = {}
        self.PH = {}
        self.PM = {}
        self.armor = {}
        self.bow = {}
        self.WS = {}
        self.buyIt1 = False
        self.buyIt2 = False
        self.buyIt3 = False
        self.pnj_position = []

        
        self.collPNJ = False

    def generatePNJ(self, areaPlay, x, y):
        ##print(f"In generatePNJ: \nX:{x} Y:{y}")
        x = x * WindowParameter.tileSize
        y = y * WindowParameter.tileSize
        self.pnj = areaPlay.create_rectangle(x +1, y +1 , x + WindowParameter.tileSize-1, y + WindowParameter.tileSize-1, fill="blue", outline = "")

    def openShop(self, window, selfPlayer, collPNJ):
        self.collPNJ = collPNJ
        self.selfP = selfPlayer
        #print(self.collPNJ)
        self.keysItem = list(self.shop.keys())
        """self.keySousItem0 = list()
        self.keySousItem1 = list(self.shop[self.keysItem[1]])
        self.keySousItem2 = list(self.shop[self.keysItem[2]])"""
        self.keySousDico0 = list(self.shop[self.keysItem[0]].keys())
        self.string0 = self.keysItem[0]+"\n"+self.keySousDico0[0]+" : "+str(self.shop[self.keysItem[0]][self.keySousDico0[0]])+" \n"+self.keySousDico0[1]+" : "+str(self.shop[self.keysItem[0]][self.keySousDico0[1]])
        self.keySousDico1 = list(self.shop[self.keysItem[1]].keys())
        self.string1 = self.keysItem[1]+"\n"+self.keySousDico1[0]+" : "+str(self.shop[self.keysItem[1]][self.keySousDico1[0]])+" \n"+self.keySousDico1[1]+" : "+str(self.shop[self.keysItem[1]][self.keySousDico1[1]])
        self.keySousDico2 = list(self.shop[self.keysItem[2]].keys())
        self.string2 = self.keysItem[2]+"\n"+self.keySousDico2[0]+" : "+str(self.shop[self.keysItem[2]][self.keySousDico2[0]])+" \n"+self.keySousDico2[1]+" : "+str(self.shop[self.keysItem[2]][self.keySousDico2[1]])
        self.windowShop = tk.Toplevel(window)
        self.windowShop.geometry("400x300")

        """self.keySousDico0[0]," : ",
        ,self.keySousDico0[1]," : " """

        #print("gold : ", self.selfP.gold, "inventory : ", self.selfP.inventory)
        #print(self.buyIt1,"\n",self.buyIt2,"\n",self.buyIt3)
        
        self.item0 = tk.Label(self.windowShop, text=self.string0)
        self.buyI0 = tk.Button(self.windowShop, text="Buy", command=self.buy1)
        self.item1 = tk.Label(self.windowShop, text=self.string1)
        self.buyI1 = tk.Button(self.windowShop, text="Buy", command=self.buy2)
        self.item2 = tk.Label(self.windowShop, text=self.string2)
        self.buyI2 = tk.Button(self.windowShop, text="Buy", command=self.buy3)
        
        self.item0.grid(row=0, column=0, pady=20, sticky="nsew")
        self.buyI0.grid(row=1, column=0, sticky="nsew")
        self.item1.grid(row=0, column=1, pady=20, sticky="nsew")
        self.buyI1.grid(row=1, column=1, sticky="nsew")
        self.item2.grid(row=0, column=2, pady=20, sticky="nsew")
        self.buyI2.grid(row=1, column=2, sticky="nsew")
        self.windowShop.grid_columnconfigure(0, weight=1)
        self.windowShop.grid_columnconfigure(1, weight=1)
        self.windowShop.grid_columnconfigure(2, weight=1)

    
        self.windowShop.bind("<KeyPress>", self.closeShop)
        """self.item0.place(anchor="center", x=60, y=120)
        self.buyI1.place(anchor="center", x = 60, y=150)"""

    def buy1(self):
        #print("buy")
        self.putInventoryItem1()

    def buy2(self):
        #print("buy")
        self.putInventoryItem2()

    def buy3(self):
        #print("buy")
        self.putInventoryItem3()


    def putInventoryItem1(self):
        #print(self.selfP.gold)
        if self.selfP.gold >= self.shop[self.keysItem[0]][self.keySousDico0[1]]:
            self.selfP.inventory[self.keysItem[0]] = self.shop[self.keysItem[0]]
            self.selfP.gold = self.selfP.gold - self.shop[self.keysItem[0]][self.keySousDico0[1]]
        #print(self.selfP.inventory)
        

    def putInventoryItem2(self):
        #print(self.selfP.gold)
        if self.selfP.gold >= self.shop[self.keysItem[1]][self.keySousDico1[1]]:
            self.selfP.inventory[self.keysItem[1]] = self.shop[self.keysItem[1]]
            self.selfP.gold = self.selfP.gold - self.shop[self.keysItem[1]][self.keySousDico1[1]]
        #print(self.selfP.inventory)

    def putInventoryItem3(self):
        #print(self.selfP.gold)
        if self.selfP.gold >= self.shop[self.keysItem[2]][self.keySousDico2[1]]:
            self.selfP.inventory[self.keysItem[2]] = self.shop[self.keysItem[2]]
            self.selfP.gold = self.selfP.gold - self.shop[self.keysItem[1]][self.keySousDico1[1]]
        #print(self.selfP.inventory)


    def closeShop(self, event):
        key = event.keysym
        self.selfP.collPNJ = False
        if key == "e":
            self.windowShop.destroy()
        
            

        

    #def closeShop(self, window)

    def generateShop(self,areaPlay, x1, y1):
        # #print(f"In generateShop: \nX:{x1} Y:{y1}")
        self.generatePNJ(areaPlay, x1, y1)
        AllItems = {0 : "Sword", 1 : "Potion of heal", 2 : "Potion of mana", 3: "Armor", 4:"Bow", 5:"Wizard's staff"}
        ItemsShop = []
        index =[]
        for i in range(0, self.NumberItems):
            indexRandom = random.randint(0, len(AllItems)-1)
            if i > 0:
                while indexRandom in index:
                    indexRandom = random.randint(0, len(AllItems)-1)
            index.append(indexRandom)
            ItemsShop.append(AllItems[indexRandom])
        ##print(index)
        ##print(ItemsShop)
        for i in range(0, len(ItemsShop)):
            if ItemsShop[i] == "Sword":
                damage = random.randint(5, 8)
                if(damage <= 8):
                    self.shop["sword"] = {"damage" : damage, "cost" : 5}
            elif ItemsShop[i] == "Potion of heal":
                heal = random.randint(3,5)
                if(heal <= 5):
                    self.shop["Potion of heal"] = {"heal" : heal, "cost" : 3}
            elif ItemsShop[i] == "Potion of mana":
                mana = random.randint(3,5)
                if(mana <= 5):
                    self.shop["Potion of mana"] = {"mana" : mana, "cost" : 3}
            elif ItemsShop[i] == "Armor":
                armor = random.randint(5,9)
                if(armor <= 9):
                    self.shop["Armor"] = {"armor" : armor, "cost" : 6}
            elif ItemsShop[i] == "Bow":
                damage = random.randint(3,7)
                if(damage <= 7):
                    self.shop["Bow"] = {"damage" : damage, "cost" : 4}
            elif ItemsShop[i] == "Wizard's staff":
                damage = random.randint(4,8)
                if(damage <= 8):
                    self.shop["Wizard's staff"] = {"damage" : damage, "cost" : 4}
        # #print(self.shop)



    

