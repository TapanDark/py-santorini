import re

from graphics import BoardGraphics


class Tile(object):
    def __init__(self, tileStr=""):
        self._player = 0
        self._floors = 0
        self._floorPattern = re.compile("f([0-4])")
        self._playerPattern = re.compile("p([0-3])")
        self.loadTileStr(tileStr)

    @property
    def floors(self):
        return self._floors

    @floors.setter
    def floors(self, value):
        assert value >= 0
        assert value <= 4
        assert type(value) == int
        self._floors = value

    def loadTileStr(self, tileStr=""):
        floors = re.search(self._floorPattern, tileStr)
        if floors:
            self._floors = int(floors.group(1))
        player = re.search(self._playerPattern, tileStr)
        if player:
            self._player = int(player.group(1))


class Board(object):

    def __init__(self, boardStr=""):
        self.graphics = BoardGraphics(self)
        self.tiles = [Tile() for i in range(0, 25)]
        self._tilePattern = re.compile("t(\d{1,2})")
        self.loadBoardStr(boardStr)
        # self.tiles[10]._player = 1
        # self.tiles[6]._player = 2
        # self.tiles[13]._player = 3

    def getPiece(self, row, col):
        assert row >= 0
        assert row <= 4
        assert col >= 0
        assert col <= 4
        return self.tiles[row * 5 + col]

    def getTileFromPixel(self, x, y):
        return self.graphics.getTileFromPixel(x, y)

    def getBoardStr(self):
        def getTileStr(tile):
            ret = ""
            if tile.floors:
                ret += "f%s" % tile.floors
            if tile._player:
                ret += "p%s" % tile._player

        return ','.join(
            ["t%s%s" % (index, getTileStr(tile)) for index, tile in enumerate(self.tiles) if getTileStr(tile)])

    def loadBoardStr(self, boardStr):
        for tileStr in boardStr.split(","):
            tileNumber = re.search(self._tilePattern, tileStr)
            if tileNumber:
                self.tiles[int(tileNumber.group(1))] = Tile(tileStr)
