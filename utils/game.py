import pygame

from utils.board.board import Board


class Game(object):
    def __init__(self, win):
        self.window = win
        videoInfo = pygame.display.Info()
        self.width, self.height = videoInfo.current_w, videoInfo.current_h
        self.board = Board()
        self.board.graphics.resize(windowWidth=self.width, windowHeight=self.height)
        self.clock = pygame.time.Clock()
        self.running = True

    def processEvents(self):
        for event in pygame.event.get():
            print(event)
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.VIDEORESIZE:
                self.resize(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                row, col = self.board.getTileFromPixel(x, y)
                if row is not None and col is not None and self.board.pieces[row * 5 + col].floors < 4:
                    self.board.pieces[row * 5 + col].floors = self.board.pieces[row * 5 + col].floors + 1

    def update(self):
        pass

    def draw(self, win):
        win.fill((0, 0, 0))
        self.board.graphics.draw(win)
        pygame.display.update()

    def resize(self, resizeEvent):
        width = max(resizeEvent.w, 430)
        height = max(resizeEvent.h, 430)
        self.board.graphics.resize(width, height)

    def run(self):
        while self.running:
            self.processEvents()
            self.update()
            self.draw(self.window)
            self.clock.tick(60)  # limit to 60 FPS
        pygame.quit()
