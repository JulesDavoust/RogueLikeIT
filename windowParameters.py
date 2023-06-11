class WindowParameter:
    #Unit interface size
    originTileSize = 16
    
    #A changer par player apres
    SCALE = 2
    FIX = 2 * SCALE

    tileSize= originTileSize*SCALE
    # objectSize = tileSize - FIX

    screenTileCol = 36
    screenTileRow = 21
    
    mapTileRow = 21
    mapTileCol = 21

    screenWidth = tileSize * screenTileCol #21 * 16 = 672
    screenHeight = tileSize * screenTileRow
    screenSize = f"{screenWidth}x{screenHeight}"

    mapWidth = tileSize * mapTileRow
    mapHeight = tileSize * mapTileCol