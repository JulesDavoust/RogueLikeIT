import random


class PNJ:
    def __init__(self):
        self.shop = {}
        self.NumberItems = 3

        self.sword = {}
        self.PH = {}
        self.PM = {}
        self.armor = {}
        self.bow = {}
        self.WS = {}

    def generatePNJ(self, areaPlay, x, y):
        self.pnj = areaPlay.create_rectangle(x, y, x + 10, y + 10, fill="brown", outline = "")

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
                    self.shop["Potion of mana"] = {"heal" : mana, "cost" : 3}
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

