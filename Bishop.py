import pygame as p
import numpy as np
import chess
from Piece import Piece
class Bishop(Piece):
    def __init__(self,chessboard, screen: p.surface, position: str, player: bool):
        self.screen = screen
        self.position = position
        self.player = player
        chessboard[position] = self


        if player is True:
            self.pic = p.image.load("images/wb.png")
        else:
            self.pic = p.image.load("images/bb.png")
        self.draw_element()