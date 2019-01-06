from graphics import BoardGraphics


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

    def __init__(self):
        self.graphics = BoardGraphics(self)
        self.pieces = [Tile() for i in range(0, 25)]
        self.pieces[10]._player = 1
        self.pieces[6]._player = 2
        self.pieces[13]._player = 3

    def getPiece(self, row, col):
        assert row >= 0
        assert row <= 4
        assert col >= 0
        assert col <= 4
        return self.pieces[row * 5 + col]

    def getTileFromPixel(self, x, y):
        return self.graphics.getTileFromPixel(x, y)
