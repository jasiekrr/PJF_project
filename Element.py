import pygame as p
import numpy as np
import chess
class Element():
    def __init__(self,screen : p.surface, position : str, player : bool, pic : str):
        self.screen = screen
        self.position = position
        self.player = player
        self.pic = pic
    def drawElement(self):
        line, row = self.positionToPNG()
        row = 9 - row
        self.screen.blit(self.pic, p.Rect((line - 1) * 64,(row - 1) * 64, 64,64))
    def positionToPNG(self):
        lineDict = {"a" : 1, "b" : 2,"c" : 3,"d" : 4,"e" : 5,"f" : 6,"g" : 7,"h" : 8}
        return lineDict[self.position[0]],int(self.position[1])



