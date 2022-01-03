import sys
from CurrentPosition import CurrentPosition
import pandas
import pygame as p

def app_Run() :
    p.init()
    screen = p.display.set_mode((512,512))
    clk = p.time.Clock()
    display_Board(screen)
    cp = CurrentPosition(screen)
    cp.resetPosition(screen)
    while True:
        #events handling:
        for event in p.event.get():
            if event.type == p.QUIT:
                sys.exit()
        clk.tick(15)
        p.display.flip()


def display_Board(screen):
    for i in range(8):
        for j in range(8):
            if (i+j)%2 == 0:
                p.draw.rect(screen, p.Color("white"), p.Rect(i * 512 / 8, j * 512 / 8, 512 / 8, 512 / 8))
            else:
                p.draw.rect(screen, p.Color("dark grey"), p.Rect(i * 512 / 8, j * 512 / 8, 512 / 8, 512 / 8))




if __name__ == '__main__':
    app_Run()


