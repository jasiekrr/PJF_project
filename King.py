import pygame as p
import numpy as np
import chess
from Piece import Piece
class King(Piece):
    def __init__(self, screen: p.surface, position: str, player: bool):
        self.screen = screen
        self.position = position
        self.player = player
        self.everMoved = False

        if player is True:
            self.pic = p.image.load("images/wk.png")
        else:
            self.pic = p.image.load("images/bk.png")
        self.drawElement()


