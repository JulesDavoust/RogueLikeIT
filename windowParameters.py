class WindowParameter:
    #Unit interface size
    originTileSize = 16
    
    #A changer par player apres
    SCALE = 2
    FIX = 4 

    tileSize= originTileSize*SCALE  #16*2 = 32
    objectSize = (originTileSize - FIX*2)*SCALE
    characterSize = (originTileSize - FIX)*SCALE

    screenTileCol = 32
    screenTileRow = 21
    
    mapTileRow = 21
    mapTileCol = 21

    screenWidth = tileSize * screenTileCol #32 * 32 = 1024
    screenHeight = tileSize * screenTileRow #32 * 21 = 672
    screenSize = f"{screenWidth}x{screenHeight}"

    mapWidth = tileSize * mapTileRow
    mapHeight = tileSize * mapTileCol