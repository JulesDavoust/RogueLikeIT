class WindowParameter:
    #Unit interface size
    originTileSize = 16
    #A changer par player apres
    SCALE = 2

    tileSize= originTileSize*SCALE

    screenTileCol = 16*2
    screenTileRow = 9*2
    
    mapTileRow = 12*2
    mapTileCol = 9*2

    screenWidth = tileSize * screenTileCol
    screenHeight = tileSize * screenTileRow
    screenSize = f"{screenWidth}x{screenHeight}"

    mapWidth = tileSize * mapTileRow
    mapHeight = tileSize * mapTileCol