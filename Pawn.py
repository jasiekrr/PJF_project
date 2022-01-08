import pygame as p
import numpy as np
import chess
from Element import Element


class Pawn(Element):
    def __init__(self, chessboard, screen: p.surface, position: str, player: bool):
        self.screen = screen
        self.position = position
        self.player = player
        chessboard[position] = self
        self.enPassantAbility = False

        if player is True:
            self.pic = p.image.load("images/wp.png")
        else:
            self.pic = p.image.load("images/bp.png")
        self.draw_element()

    def gets_promoted(self):
        del self

