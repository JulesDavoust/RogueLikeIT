import random
import tkinter as tk


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

        self.pnj_position = []

    def generatePNJ(self, areaPlay, x, y):
        self.pnj = areaPlay.create_rectangle(x, y, x + 10, y + 10, fill="brown", outline = "")

    def openShop(self, window):
        self.keysItem = list(self.shop.keys())
        print(self.keysItem[0])
        self.windowShop = tk.Toplevel(window)
        self.windowShop.geometry("400x300")

    

        self.item0 = tk.Label(self.windowShop, text=self.keysItem[0])
        self.buyI0 = tk.Button(self.windowShop, text="Buy", command=self.buy())
        self.item1 = tk.Label(self.windowShop, text=self.keysItem[1])
        self.buyI1 = tk.Button(self.windowShop, text="Buy", command=self.buy())
        self.item2 = tk.Label(self.windowShop, text=self.keysItem[2])
        self.buyI2 = tk.Button(self.windowShop, text="Buy", command=self.buy())

        """self.item0.grid(row=0, column=0, sticky="nsew")
        self.buyI0.grid(row=2, column=0, sticky="nsew")
        self.item1.grid(row=0, column=1, sticky="nsew")
        self.buyI1.grid(row=5, column=1, sticky="nsew")
        self.item2.grid(row=0, column=2, sticky="nsew")
        self.buyI2.grid(row=4, column=2, sticky="nsew")

        self.windowShop.grid_columnconfigure(0, weight=1)
        self.windowShop.grid_columnconfigure(1, weight=1)
        self.windowShop.grid_columnconfigure(2, weight=1)"""
        self.item0.place(anchor="center", x=50, y=50)

    def buy(self):
        print("buy")

    def closeShop(self):
        self.windowShop.destroy()

    #def closeShop(self, window)

    def generateShop(self,areaPlay, x1, y1):
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
        print(index)
        print(ItemsShop)
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
        print(self.shop)



    

