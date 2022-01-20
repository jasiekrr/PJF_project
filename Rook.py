import pygame as p
from Element import Element


class Rook(Element):
    def __init__(self, chessboard, screen: p.surface, position: str, player: bool):
        self.screen = screen
        self.position = position
        self.player = player
        chessboard[position] = self
        self.everMoved = False

        if player is True:
            self.pic = p.image.load("images/wr.png")
        else:
            self.pic = p.image.load("images/br.png")
        self.draw_element()
