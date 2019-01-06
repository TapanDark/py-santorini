import pygame

BOARD_X = 50
BOARD_Y = 50
BOARD_SIDE = 700
BOARD_THICK = 3

RED_PIECE = 0b1000000
GREEN_PIECE = 0b0100000
BLUE_PIECE = 0b0010000

FIRST_FLOOR = 0b0000001
SECOND_FLOOR = 0b0000010
THIRD_FLOOR = 0b0000100
DOME = 0b0001000

BOARD_COLOR = (255, 255, 255)  # WHITE
BUILDING_COLOR = (192, 192, 192)  # SILVER
DOME_COLOR = (0, 0, 139)  # DARK BLUE


class Tile(object):
    def __init__(self):
        self._player = 0
        self._floors = 0

    @property
    def floors(self):
        return self._floors

    @floors.setter
    def floors(self, value):
        assert value >= 0
        assert value <= 4
        assert type(value) == int
        self._floors = value


class Board(object):

    def __init__(self, windowWidth, windowHeight):
        self.windowWidth = 0
        self.windowHeight = 0
        self.minDimension = 0
        self.resize(windowWidth, windowHeight)
        self.pieces = [Tile() for i in range(0, 25)]

    def resize(self, windowWidth, windowHeight):
        self.windowWidth = windowWidth
        self.windowHeight = windowHeight
        self.minDimension = min(windowHeight, windowWidth)

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
        for pos, tileData in enumerate(self.pieces):
            row = pos / 5
            col = pos % 5
            self.drawPieceOnTile(win, tileData, row, col)

    def getPiece(self, row, col):
        assert row >= 0
        assert row <= 4
        assert col >= 0
        assert col <= 4
        return self.pieces[row * 5 + col]

    def drawPieceOnTile(self, win, tileData, row, col):
        floorHeight = 0
        xOrg, yOrg = self._getTileCoordinates(row, col)
        if tileData.floors > 0:
            floorHeight += 0.2
            pygame.draw.rect(win, BUILDING_COLOR,
                             (xOrg + self.tileSide * 0.1, yOrg + self.tileSide * 0.75, self.tileSide * 0.82,
                              self.tileSide * 0.2), 1)
        if tileData.floors > 1:
            floorHeight += 0.18
            pygame.draw.rect(win, BUILDING_COLOR,
                             (xOrg + self.tileSide * 0.2, yOrg + self.tileSide * 0.59, self.tileSide * 0.62,
                              self.tileSide * 0.18), 1)
        if tileData.floors > 2:
            floorHeight += 0.15
            width = self.tileSide * 0.42
            pygame.draw.rect(win, BUILDING_COLOR,
                             (xOrg + self.tileSide * 0.3, yOrg + self.tileSide * 0.44, width,
                              self.tileSide * 0.15), 1)
            for i in range(1, 5):
                pygame.draw.line(win, BUILDING_COLOR,
                                 (xOrg + self.tileSide * 0.3 + width / 5 * i, yOrg + self.tileSide * 0.44),
                                 (xOrg + self.tileSide * 0.3 + width / 5 * i, yOrg + self.tileSide * 0.59), 1)

        if tileData.floors > 3:
            floorHeight += 1
            pygame.draw.arc(win, DOME_COLOR,
                            (xOrg + self.tileSide * 0.3, yOrg + self.tileSide * 0.30, self.tileSide * 0.42,
                             self.tileSide * 0.26),
                            0, 3.2, 10)
            pass

    def _drawSemiPolygon(self):
        pass

    def _getTileCoordinates(self, row, col):
        x = self.x + col * self.tileSide
        y = self.y + row * self.tileSide
        return x, y

    def getTileFromCoordinates(self, x, y):
        if x < self.x or x > self.x + self.width:
            return None, None
        if y < self.y or y > self.y + self.height:
            return None, None
        col = (x - self.x) / self.tileSide
        row = (y - self.y) / self.tileSide
        return row, col
