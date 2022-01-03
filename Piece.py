import pygame as p
import numpy as np
import chess
from Element import Element
class Piece(Element):
    def __init__(self, screen : p.surface, position : str, player : bool):
        self.screen = screen
        self.position = position
        self.player = player

