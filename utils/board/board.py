import re

from graphics import BoardGraphics


class Tile(object):
    def __init__(self, tileStr=""):
        self.player = 0
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
            self.floors = int(floors.group(1))
        player = re.search(self._playerPattern, tileStr)
        if player:
            self.player = int(player.group(1))


class Board(object):

    def __init__(self, boardStr=""):
        self.graphics = BoardGraphics(self)
        self.tiles = [Tile() for i in range(0, 25)]
        self._tilePattern = re.compile("t(\d{1,2})")
        self.loadBoardStr(boardStr)
        self._playerMovePattern = re.compile(r'm(\d+)-(\d+)')
        self._buildPattern = re.compile(r'b(\d+)')
        self.nextMoveSequence = []
        # self.tiles[10]._player = 1
        # self.tiles[6]._player = 2
        # self.tiles[13]._player = 3

    def indexToRowCol(self, index):
        return index / 5, index % 5

    def getPiece(self, row, col):
        assert 0 <= row <= 4
        assert 0 <= col <= 4
        return self.tiles[row * 5 + col]

    def getTileFromPixel(self, x, y):
        return self.graphics.getTileFromPixel(x, y)

    def getBoardStr(self):
        def getTileStr(tile):
            ret = ""
            if tile.floors:
                ret += "f%s" % tile.floors
            if tile.player:
                ret += "p%s" % tile.player

        return ','.join(
            ["t%s%s" % (index, getTileStr(tile)) for index, tile in enumerate(self.tiles) if getTileStr(tile)])

    def loadBoardStr(self, boardStr):
        for tileStr in boardStr.split(","):
            tileNumber = re.search(self._tilePattern, tileStr)
            if tileNumber:
                self.tiles[int(tileNumber.group(1))] = Tile(tileStr)

    def _parseMoveStr(self, moveStr):
        sequence = []
        for subMove in moveStr.split(","):
            pMoveMatch = self._playerMovePattern.search(subMove)
            if pMoveMatch:
                sequence.append(('m', int(pMoveMatch.group(1)), int(pMoveMatch.group(2))))
                continue
            bMoveMatch = self._buildPattern.search(moveStr)
            if bMoveMatch:
                sequence.append(('b', int(bMoveMatch.group(1))))
        return sequence

    def isAdjacent(self, origin, target):
        orgRow, orgCol = self.indexToRowCol(origin)
        targRow, targCol = self.indexToRowCol(target)
        return abs(orgRow - targRow) <= 1 and abs(orgCol - targCol) <= 1

    def _standardMoveValidator(self, move):
        def isLegalPlayerMove(move):
            if len(move) != 3:
                return False
            if move[0] != 'm':
                return False
            if move[1] == move[2]:
                return False
            if not 0 <= move[1] <= 24:
                return False
            if not 0 <= move[2] <= 24:
                return False
            if not self.isAdjacent(move[1], move[2]):
                return False
            if self.tiles[move[1]].player < 0:
                return False
            if self.tiles[move[2]].player != 0:
                return False
            if self.tiles[move[2]].floors >= 4:
                return False
            if not self.tiles[move[2]].floors - self.tiles[move[1]].floors <= 1:
                return False
            return True

        def isLegalBuild(pos, buildMove):
            if buildMove[0] != 'b':
                return False
            if not 0 <= buildMove[1] <= 24:
                return False
            if not self.isAdjacent(pos, buildMove[1]):
                return False
            if self.tiles[buildMove[1]].floors >= 4:
                return False
            if self.tiles[buildMove[1]].player > 0:
                return False
            return True

        return len(move) == 2 and isLegalPlayerMove(move[0]) and isLegalBuild(move[0][2], move[1])

    def isValidMove(self, moveSequence):
        # This will change based on ability cards.
        # TODO: devise good way to handle this
        return self._standardMoveValidator(moveSequence)

    def performMove(self, moveSequence):
        for move in moveSequence:
            if move[0] == 'p':
                self.tiles[move[2]].player = self.tiles[move[1]].player
                self.tiles[move[1]].player = 0
            elif move[0] == 'b':
                self.tiles[move[1]] += 1
