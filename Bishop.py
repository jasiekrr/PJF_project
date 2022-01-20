import pygame as p

from Element import Element


class Bishop(Element):
    def __init__(self, chessboard, screen: p.surface, position: str, player: bool):
        self.screen = screen
        self.position = position
        self.player = player
        chessboard[position] = self

        if player is True:
            self.pic = p.image.load("images/wb.png")
        else:
            self.pic = p.image.load("images/bb.png")
        self.draw_element()
