import pygame

BOARD_X = 50
BOARD_Y = 50
BOARD_SIDE = 700
BOARD_THICK = 3

BOARD_COLOR = (255, 255, 255)  # WHITE
BUILDING_COLOR = (192, 192, 192)  # SILVER
DOME_COLOR = (0, 0, 139)  # DARK BLUE


class BoardGraphics(object):

    def __init__(self, boardObj):
        self.boardObj = boardObj
        self.windowWidth = 0
        self.windowHeight = 0
        self.minDimension = 0

    def resize(self, windowWidth, windowHeight):
        self.windowWidth = windowWidth
        self.windowHeight = windowHeight
        self.minDimension = min(windowHeight, windowWidth)

    def draw(self, win):
        self._drawBoard(win)
        self.drawPieces(win)

    def _drawBoard(self, win):
        pygame.draw.rect(win, BOARD_COLOR, (self.x, self.y, self.width, self.height), BOARD_THICK)
        for i in range(1, 5):
            pygame.draw.line(win, BOARD_COLOR, (self.x, self.y + i * self.tileSide),
                             (self.x + self.side, self.y + i * self.tileSide), BOARD_THICK)
            pygame.draw.line(win, BOARD_COLOR, (self.x + i * self.tileSide, self.y),
                             (self.x + i * self.tileSide, self.y + self.side), BOARD_THICK)

    def drawPieces(self, win):
        for pos, tileData in enumerate(self.boardObj.tiles):
            row = pos / 5
            col = pos % 5
            self._drawPieceOnTile(win, tileData, row, col)

    @property
    def x(self):
        return self.minDimension / 22

    @property
    def y(self):
        return self.minDimension / 22

    @property
    def side(self):
        return self.minDimension / 11 * 10

    @property
    def tileSide(self):
        return self.side / 5

    @property
    def width(self):
        return self.side

    @property
    def height(self):
        return self.side

    def _drawPieceOnTile(self, win, tileData, row, col):
        groundHeightScale = self._drawBuildingsOnTile(win, tileData.floors, row, col)
        self._drawPlayerOnTile(win, tileData.player, groundHeightScale, row, col)

    def _drawBuildingsOnTile(self, win, floors, row, col):
        groundHeightScale = 0.05
        xOrg, yOrg = self._getTileCoordinates(row, col)

        # TODO: Remove hardcoded values and actually use these in code
        FIRST_FLOOR_HEIGHT_SCALE = 0.2
        FIRST_FLOOR_WIDTH_SCALE = 0.82
        SECOND_FLOOR_HEIGHT_SCALE = 0.18
        SECOND_FLOOR_WIDTH_SCALE = 0.62
        THIRD_FLOOR_HEIGHT_SCALE = 0.15
        THIRD_FLOOR_WIDTH_SCALE = 0.42
        DOME_HEIGHT_SCALE = 0.21
        DOME_WIDTH_SCALE = 0.42

        if floors > 0:
            groundHeightScale += 0.2
            pygame.draw.rect(win, BUILDING_COLOR,
                             (xOrg + self.tileSide * 0.1, yOrg + self.tileSide * 0.75, self.tileSide * 0.82,
                              self.tileSide * 0.2), 1)
        if floors > 1:
            groundHeightScale += 0.16
            pygame.draw.rect(win, BUILDING_COLOR,
                             (xOrg + self.tileSide * 0.2, yOrg + self.tileSide * 0.59, self.tileSide * 0.62,
                              self.tileSide * 0.18), 1)
        if floors > 2:
            groundHeightScale += 0.14
            width = self.tileSide * 0.42
            pygame.draw.rect(win, BUILDING_COLOR,
                             (xOrg + self.tileSide * 0.3, yOrg + self.tileSide * 0.44, width,
                              self.tileSide * 0.15), 1)
            for i in range(1, 5):
                pygame.draw.line(win, BUILDING_COLOR,
                                 (xOrg + self.tileSide * 0.3 + width / 5 * i, yOrg + self.tileSide * 0.44),
                                 (xOrg + self.tileSide * 0.3 + width / 5 * i, yOrg + self.tileSide * 0.59), 1)

        if floors > 3:
            pygame.draw.arc(win, DOME_COLOR,
                            (xOrg + self.tileSide * 0.3, yOrg + self.tileSide * 0.30, self.tileSide * 0.42,
                             self.tileSide * 0.26),
                            0, 3.2, 10)
        return groundHeightScale

    def _drawPlayerOnTile(self, win, playerId, groundHeightScale, row, col):
        if playerId == 0:
            return
        colorMap = {
            1: (255, 0, 0,),
            2: (0, 255, 0),
            3: (0, 0, 255)
        }
        PLAYER_TOTAL_HEIGHT_SCALE = 0.25
        PLAYER_TOTAL_WIDTH_SCALE = 0.15

        PLAYER_HEAD_TO_TOTAL_HEIGHT = 1 / 5

        xOrg, yOrg = self._getTileCoordinates(row, col)

        playerBottom = yOrg + (1 - groundHeightScale) * self.tileSide
        playerTop = playerBottom - (PLAYER_TOTAL_HEIGHT_SCALE * self.tileSide)

        # BOUNDING BOX
        # pygame.draw.rect(win, colorMap[playerId], (
        #     xOrg + (self.tileSide * (1 - PLAYER_TOTAL_WIDTH_SCALE) / 2), playerTop,
        #     self.tileSide * PLAYER_TOTAL_WIDTH_SCALE,
        #     self.tileSide * PLAYER_TOTAL_HEIGHT_SCALE),
        #                  1)

        #  HEAD
        pygame.draw.circle(win, colorMap[playerId], (int(xOrg + (self.tileSide / 2)),
                                                     int(playerTop + self.tileSide * PLAYER_TOTAL_HEIGHT_SCALE / 5)),
                           int(self.tileSide * PLAYER_TOTAL_HEIGHT_SCALE / 5), 1)

        # BODY
        pygame.draw.line(win, colorMap[playerId],
                         (xOrg + (self.tileSide / 2), playerTop + self.tileSide * PLAYER_TOTAL_HEIGHT_SCALE * 4 / 10),
                         (xOrg + (self.tileSide / 2), playerTop + self.tileSide * PLAYER_TOTAL_HEIGHT_SCALE * 8 / 10),
                         1)

        # LEFT ARM
        pygame.draw.line(win, colorMap[playerId],
                         (xOrg + (self.tileSide / 2), playerTop + self.tileSide * PLAYER_TOTAL_HEIGHT_SCALE * 6 / 10),
                         (xOrg + (self.tileSide * 0.55), playerTop + self.tileSide * PLAYER_TOTAL_HEIGHT_SCALE * 4 / 10),
                         1)

        # RIGHT ARM
        pygame.draw.line(win, colorMap[playerId],
                         (xOrg + (self.tileSide / 2), playerTop + self.tileSide * PLAYER_TOTAL_HEIGHT_SCALE * 6 / 10),
                         (xOrg + (self.tileSide * 0.45), playerTop + self.tileSide * PLAYER_TOTAL_HEIGHT_SCALE * 4 / 10),
                         1)

        # LEFT LEG
        pygame.draw.line(win, colorMap[playerId],
                         (xOrg + (self.tileSide / 2), playerTop + self.tileSide * PLAYER_TOTAL_HEIGHT_SCALE * 8 / 10),
                         (xOrg + (self.tileSide * 0.55), playerTop + self.tileSide * PLAYER_TOTAL_HEIGHT_SCALE),
                         1)

        # RIGHT LEG
        pygame.draw.line(win, colorMap[playerId],
                         (xOrg + (self.tileSide / 2), playerTop + self.tileSide * PLAYER_TOTAL_HEIGHT_SCALE * 8 / 10),
                         (xOrg + (self.tileSide * 0.45), playerTop + self.tileSide * PLAYER_TOTAL_HEIGHT_SCALE),
                         1)

    def _getTileCoordinates(self, row, col):
        x = self.x + col * self.tileSide
        y = self.y + row * self.tileSide
        return x, y

    def getTileFromPixel(self, x, y):
        if x < self.x or x > self.x + self.width:
            return None, None
        if y < self.y or y > self.y + self.height:
            return None, None
        col = (x - self.x) / self.tileSide
        row = (y - self.y) / self.tileSide
        return row, col
