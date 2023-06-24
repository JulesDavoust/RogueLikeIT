import random
import tkinter as tk
from PIL import Image, ImageTk
from windowParameters import WindowParameter
from equipements import Equipements, Items


class PNJ:
    def __init__(self):
        self.finalShop = {}
        self.shop = {}
        self.NumberItems = 3

        self.WS = {}
        self.buyIt1 = False
        self.buyIt2 = False
        self.buyIt3 = False
        self.pnj_position = []
    
        self.shop_weapon = ""
        self.shop_armor = ""
        self.shop_item =""

        
        self.collPNJ = False

    def generatePNJ(self, areaPlay, x, y):
        #####print(f"In generatePNJ: \nX:{x} Y:{y}")
        x = x * WindowParameter.tileSize
        y = y * WindowParameter.tileSize

        self.pnj = areaPlay.create_rectangle(x +1, y +1 , x + WindowParameter.tileSize-1, y + WindowParameter.tileSize-1, outline = "")
        image_item = Image.open("./sprites/PNJ.png").convert("P")
        image_item = image_item.resize((WindowParameter.tileSize, WindowParameter.tileSize))
        self.image_pnj = ImageTk.PhotoImage(image_item)
        areaPlay.create_image(
           x, y, image=self.image_pnj , anchor = "nw"
        )
        

    def openShop(self, window, selfPlayer, collPNJ):
        self.collPNJ = collPNJ
        self.selfP = selfPlayer
        ####print(self.collPNJ)
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
        self.windowShop.geometry("400x200")
       
        #Remove window decorations (Top-right)
        self.windowShop.overrideredirect(True)

        # Get the width and height of the Toplevel window
        window_width = self.windowShop.winfo_reqwidth()
        window_height = self.windowShop.winfo_reqheight()

        # Calculate the position of the window based on the dimensions of the parent window
        position_top = int(window.winfo_y() + (window.winfo_height() / 2) - (window_height / 2))
        position_right = int(window.winfo_x() + (window.winfo_width() / 2) - (window_width / 2))

        # Set the geometry of the window with the calculated position
        self.windowShop.geometry("+{}+{}".format(position_right - 200, position_top))

        self.windowShop.lift()
        self.windowShop.grab_set()
        self.windowShop.focus_set()

        ####print("gold : ", self.selfP.gold, "inventory : ", self.selfP.inventory)
        ####print(self.buyIt1,"\n",self.buyIt2,"\n",self.buyIt3)
        
        self.item0 = tk.Label(self.windowShop, text=self.string0)
        self.buyI0 = tk.Button(self.windowShop, text="Buy", command=self.buy1)
        self.item1 = tk.Label(self.windowShop, text=self.string1)
        self.buyI1 = tk.Button(self.windowShop, text="Buy", command=self.buy2)
        self.item2 = tk.Label(self.windowShop, text=self.string2)
        self.buyI2 = tk.Button(self.windowShop, text="Buy", command=self.buy3)

        indication = tk.Button(self.windowShop, text="Quit", command=self.closeShop)
        indication.place(x=200, y=160, anchor="center")
        
        self.item0.grid(row=0, column=0, pady=20, sticky="nsew")
        self.buyI0.grid(row=1, column=0, sticky="nsew")
        self.item1.grid(row=0, column=1, pady=20, sticky="nsew")
        self.buyI1.grid(row=1, column=1, sticky="nsew")
        self.item2.grid(row=0, column=2, pady=20, sticky="nsew")
        self.buyI2.grid(row=1, column=2, sticky="nsew")
        self.windowShop.grid_columnconfigure(0, weight=1)
        self.windowShop.grid_columnconfigure(1, weight=1)
        self.windowShop.grid_columnconfigure(2, weight=1)

    def buy1(self):
        # ##print("buy1")
        self.putInventoryItem1()

    def buy2(self):
        # ##print("buy2")
        self.putInventoryItem2()

    def buy3(self):
        # ##print("buy3")
        self.putInventoryItem3()

    # Weapon
    def putInventoryItem1(self):
        if self.selfP.gold >= self.shop[self.keysItem[0]][self.keySousDico0[1]]:
            self.selfP.weapon = self.shop_weapon
            self.selfP.gold = self.selfP.gold - self.shop[self.keysItem[0]][self.keySousDico0[1]]
            self.closeShop()
        
        
        
    # Armor
    def putInventoryItem2(self):
        if self.selfP.gold >= self.shop[self.keysItem[1]][self.keySousDico1[1]]:
            # self.selfP.inventory[self.keysItem[1]] = self.shop[self.keysItem[1]]
            self.selfP.armor = self.shop_armor
            self.selfP.gold = self.selfP.gold - self.shop[self.keysItem[1]][self.keySousDico1[1]]
            self.closeShop()
            
        ####print(self.selfP.inventory)

    # Item
    def putInventoryItem3(self):
        if self.selfP.gold >= self.shop[self.keysItem[2]][self.keySousDico2[1]]:
            # self.selfP.inventory[self.keysItem[2]] = self.shop[self.keysItem[2]]
            self.selfP.inventory[self.shop_item] += 1
            self.selfP.gold = self.selfP.gold - self.shop[self.keysItem[1]][self.keySousDico1[1]]
            self.closeShop()
        ####print(self.selfP.inventory)


    def closeShop(self):
        self.selfP.collPNJ = False
        self.windowShop.destroy()
        

    def generateShop(self,areaPlay, x1, y1):
        self.generatePNJ(areaPlay, x1, y1)
        
        random_weapon = random.choice(["blade"])
        random_index = random.randint(1,2)
        self.shop_weapon = f"{random_weapon}_{random_index}"
        random_armor = random.choice(["ring"])
        random_index = random.randint(1,3)
        self.shop_armor = f"{random_armor}_{random_index}"
        self.shop_item = random.choice(["potion_PV", "potion_MP"])

        #First for weapon
        self.shop[Equipements.equipement_name[self.shop_weapon]] = {
            "DMG: " : Equipements.equipement_stats[self.shop_weapon],
            "COST: ": Equipements.equipement_price[self.shop_weapon]
            }
        #Second for armor
        self.shop[Equipements.equipement_name[self.shop_armor]] = {
            "DEF: " : Equipements.equipement_stats[self.shop_armor],
            "COST: ": Equipements.equipement_price[self.shop_armor]
            }
        #Thrid for item
        if(self.shop_item == "potion_PV"):
            self.shop["Potion PV"] = {
                "HEAL" : Items.healthAmount,
                "COST: ": Items.potionPrice
                }
            
        if(self.shop_item == "potion_MP"):
            self.shop["Potion MP"] = {
                "RESTORE" : Items.magicAmount,
                "COST: ": Items.potionPrice
                }
            
        # Archive merchandise method
        # AllItems = {0 : "Sword", 1 : "Potion of heal", 2 : "Potion of mana", 3: "Armor", 4:"Slingshot", 5:"Wizard's staff"}
        # ItemsShop = []
        # index =[]
        # for i in range(0, self.NumberItems):
        #     indexRandom = random.randint(0, len(AllItems)-1)
        #     if i > 0:
        #         while indexRandom in index:
        #             indexRandom = random.randint(0, len(AllItems)-1)
        #     index.append(indexRandom)
        #     ItemsShop.append(AllItems[indexRandom])
        #####print(index)
        #####print(ItemsShop)
        # for i in range(0, len(ItemsShop)):
        #     if ItemsShop[i] == "Sword":
        #         damage = random.randint(5, 8)
        #         if(damage <= 8):
        #             self.shop["sword"] = {"damage" : damage, "cost" : 5}
        #     elif ItemsShop[i] == "Potion of heal":
        #         heal = random.randint(3,5)
        #         if(heal <= 5):
        #             self.shop["Potion of heal"] = {"heal" : heal, "cost" : 3}
        #     elif ItemsShop[i] == "Potion of mana":
        #         mana = random.randint(3,5)
        #         if(mana <= 5):
        #             self.shop["Potion of mana"] = {"mana" : mana, "cost" : 3}
        #     elif ItemsShop[i] == "Armor":
        #         armor = random.randint(5,9)
        #         if(armor <= 9):
        #             self.shop["Armor"] = {"armor" : armor, "cost" : 6}
        #     elif ItemsShop[i] == "Slingshot":
        #         damage = random.randint(3,7)
        #         if(damage <= 7):
        #             self.shop["Slingshot"] = {"damage" : damage, "cost" : 4}
        #     elif ItemsShop[i] == "Wizard's staff":
        #         damage = random.randint(4,8)
        #         if(damage <= 8):
        #             self.shop["Wizard's staff"] = {"damage" : damage, "cost" : 4}
        # ####print(self.shop)




    

