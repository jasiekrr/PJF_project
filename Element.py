import pygame as p
import numpy as np
import chess


class Element():
    def __init__(self, chessboard, screen: p.surface, position: str, player: bool, pic: str):
        self.screen = screen
        self.position = position
        self.player = player
        self.pic = pic

    def change_position(self, new_pos: str):
        self.position = new_pos

    def draw_element(self, pos: str = None):
        if pos is None:
            line, row = self.pgn_to_position()
            row = 9 - row
            self.screen.blit(self.pic, p.Rect(((line - 1) * 64, (row - 1) * 64, 64, 64)))
        else:
            line,row = self.pgn_to_position(pos)
            row = 9 - row
            self.screen.blit(self.pic, p.Rect(((line - 1) * 64, (row - 1) * 64, 64, 64)))

    def pgn_to_position(self, pos: str = None):
        line_dict = {"a": 1, "b": 2, "c": 3, "d": 4, "e": 5, "f": 6, "g": 7, "h": 8}
        if pos is None:
            return line_dict[self.position[0]], int(self.position[1])
        else:
            return line_dict[pos[0]], int(pos[1])
