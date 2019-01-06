import pygame
from utils.game import Game

VERSION = 0.1

if __name__ == "__main__":

    pygame.init()
    win = pygame.display.set_mode((730, 730), pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE)
    pygame.display.set_caption("Tdark Santorini Version %s" % VERSION)
    game = Game(win)
    game.run()
