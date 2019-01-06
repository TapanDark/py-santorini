import pygame

from utils.board import Board


class Game(object):
    def __init__(self, win):
        self.window = win
        videoInfo = pygame.display.Info()
        self.width, self.height = videoInfo.current_w, videoInfo.current_h
        self.board = Board(windowWidth=self.width, windowHeight=self.height)
        self.clock = pygame.time.Clock()
        self.running = True

    def processEvents(self):
        for event in pygame.event.get():
            print(event)
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.VIDEORESIZE:
                self.resize(event)

    def update(self):
        pass

    def draw(self, win):
        win.fill((0, 0, 0))
        self.board.draw(win)
        pygame.display.update()

    def resize(self, resizeEvent):
        width = max(resizeEvent.w, 430)
        height = max(resizeEvent.h, 430)
        self.board.resize(width, height)

    def run(self):
        while self.running:
            self.processEvents()
            self.update()
            self.draw(self.window)
            self.clock.tick(60)  # limit to 60 FPS
        pygame.quit()
