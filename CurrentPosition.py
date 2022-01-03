import pygame as p
import numpy as np
import chess
from Pawn import Pawn
from King import  King
from Knight import Knight
from Bishop import Bishop
from Rook import Rook
from Queen import Queen

class CurrentPosition():
    def __init__(self, screen : p.surface):
        #BOOLS:
        self.alreadyCastled = False



        self.lines = ["1","2","3","4","5","6","7","8"]
        self.rows = ["a","b","c","d","e","f","g","h"]
        self.chessBoard = [self.rows[j] + self.lines[i] for j in range(len(self.lines)) for i in range(len(self.lines))]
        self.whitePieces = []
        self.blackPieces = []


    def resetPosition(self, screen):
        for piece in self.whitePieces:
            piece is None
        for piece in self.blackPieces:
            piece is None
        #for i in range(len(self.lines)):
        wp1 = Pawn(screen, "a2", True)
        wp2 = Pawn(screen, "b2", True)
        wp3 = Pawn(screen, "c2", True)
        wp4 = Pawn(screen, "d2", True)
        wp5 = Pawn(screen, "e2", True)
        wp6 = Pawn(screen, "f2", True)
        wp7 = Pawn(screen, "g2", True)
        wp8 = Pawn(screen, "h2", True)

        bp1 = Pawn(screen, "a7", False)
        bp2 = Pawn(screen, "b7", False)
        bp3 = Pawn(screen, "c7", False)
        bp4 = Pawn(screen, "d7", False)
        bp5 = Pawn(screen, "e7", False)
        bp6 = Pawn(screen, "f7", False)
        bp7 = Pawn(screen, "g7", False)
        bp8 = Pawn(screen, "h7", False)

        wk = King(screen, "e1", True)
        bk = King(screen, "e8", False)

        wq = Queen(screen, "d1", True)
        bq = Queen(screen, "d8", False)

        wb1 = Bishop(screen, "c1", True)
        wb2 = Bishop(screen, "f1", True)

        bb1 = Bishop(screen, "c8", False)
        bb2 = Bishop(screen, "f8", False)

        wn1 = Knight(screen, "b1", True)
        wn2 = Knight(screen, "g1", True)

        bn1 = Knight(screen, "b8", False)
        bn2 = Knight(screen, "g8", False)

        wr1 = Rook(screen, "a1", True)
        wr2 = Rook(screen, "h1", True)

        br1 = Rook(screen, "a8", False)
        br2 = Rook(screen, "h8", False)


