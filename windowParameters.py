class WindowParameter:
    #Unit interface size
    originTileSize = 16
    #A changer par player apres
    SCALE = 4

    tileSize= originTileSize*SCALE

    screenTileCol = 16
    screenTileRow = 9
    mapTileCol = 12
    mapTileRow = 9

    screenWidth = tileSize * screenTileCol
    screenHeight = tileSize * screenTileRow
    screenSize = f"{screenWidth}x{screenHeight}"

    mapWidth = tileSize * mapTileCol
    mapHeight = tileSize * mapTileRow