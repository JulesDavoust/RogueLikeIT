import Tile
from windowParameters import WindowParameter

class GameMap:
    def __init__(self,width,height):
        self.width = width
        self.height = height
        self.tiles = self.initialized_tiles(self)

    def initialized_tiles(self):
        tiles = [[Tile(False) for y in range(self.height)] for  x in range(self.width)]

        tiles[30][22].blocked = True
        tiles[30][22].blocked.sight = True
        tiles[31][22].blocked = True
        tiles[31][22].blocked.sight = True
        tiles[32][22].blocked = True
        tiles[32][22].blocked.sight = True

