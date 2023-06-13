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
        self.buyIt = False
        self.pnj_position = []

    def generatePNJ(self, areaPlay, x, y):
        self.pnj = areaPlay.create_rectangle(x, y, x + 10, y + 10, fill="brown", outline = "")

    def openShop(self, window):
        self.keysItem = list(self.shop.keys())
        """self.keySousItem0 = list()
        self.keySousItem1 = list(self.shop[self.keysItem[1]])
        self.keySousItem2 = list(self.shop[self.keysItem[2]])"""
        self.keySousDico0 = list(self.shop[self.keysItem[0]].keys())
        self.string0 = self.keysItem[0]+"\n"+self.keySousDico0[0]+" : "+str(self.shop[self.keysItem[0]][self.keySousDico0[0]])+" \n"+self.keySousDico0[1]+" : "+str(self.shop[self.keysItem[0]][self.keySousDico0[1]])
        self.keySousDico1 = list(self.shop[self.keysItem[1]].keys())
        self.string1 = self.keysItem[1]+"\n"+self.keySousDico1[0]+" : "+str(self.shop[self.keysItem[1]][self.keySousDico1[0]])+" \n"+self.keySousDico1[1]+" : "+str(self.shop[self.keysItem[1]][self.keySousDico1[1]])
        print(self.string1)
        self.keySousDico2 = list(self.shop[self.keysItem[2]].keys())
        self.string2 = self.keysItem[2]+"\n"+self.keySousDico2[0]+" : "+str(self.shop[self.keysItem[2]][self.keySousDico2[0]])+" \n"+self.keySousDico2[1]+" : "+str(self.shop[self.keysItem[2]][self.keySousDico2[1]])
        print(self.string2)
        self.windowShop = tk.Toplevel(window)
        self.windowShop.geometry("400x300")

        """self.keySousDico0[0]," : ",
        ,self.keySousDico0[1]," : " """

    
        if self.buyIt == True:
            self.putInventory()
        else:
            self.item0 = tk.Label(self.windowShop, text=self.string0)
            self.buyI0 = tk.Button(self.windowShop, text="Buy", command=self.buy())
            self.item1 = tk.Label(self.windowShop, text=self.string1)
            self.buyI1 = tk.Button(self.windowShop, text="Buy", command=self.buy())
            self.item2 = tk.Label(self.windowShop, text=self.string2)
            self.buyI2 = tk.Button(self.windowShop, text="Buy", command=self.buy())

            self.item0.grid(row=0, column=0, pady=20, sticky="nsew")
            self.buyI0.grid(row=1, column=0, sticky="nsew")
            self.item1.grid(row=0, column=1, pady=20, sticky="nsew")
            self.buyI1.grid(row=1, column=1, sticky="nsew")
            self.item2.grid(row=0, column=2, pady=20, sticky="nsew")
            self.buyI2.grid(row=1, column=2, sticky="nsew")

            self.windowShop.grid_columnconfigure(0, weight=1)
            self.windowShop.grid_columnconfigure(1, weight=1)
            self.windowShop.grid_columnconfigure(2, weight=1)
        """self.item0.place(anchor="center", x=60, y=120)
        self.buyI1.place(anchor="center", x = 60, y=150)"""

    def buy(self):
        print("buy")
        self.buyIt = True

    def putInventory(self):
        print("In inventory")

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



    

