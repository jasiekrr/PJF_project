import pygame as p

from Bot import Bot
from Pawn import Pawn
from King import King
from Knight import Knight
from Bishop import Bishop
from Rook import Rook
from Queen import Queen


def pgn_to_num(position: str) -> tuple:
    line_dict = {"a": 1, "b": 2, "c": 3, "d": 4, "e": 5, "f": 6, "g": 7, "h": 8}
    return line_dict[position[0]], int(position[1])


class CurrentPosition:
    def __init__(self, screen: p.surface):
        # BOOLS:
        self.bot = None
        # self.board = None
        self.white_long_castles_rights = True
        self.white_short_castles_rights = True
        self.black_long_castles_rights = True
        self.black_short_castles_rights = True
        self.white_queens_spawned = 0  # numbers of queens can vary because of pawns' promotions
        self.black_queens_spawned = 0
        self.player_to_move = True
        self.en_passant = False
        self.lines = ["1", "2", "3", "4", "5", "6", "7", "8"]
        self.rows = ["a", "b", "c", "d", "e", "f", "g", "h"]
        self.chessboard = [self.rows[j] + self.lines[i] for j in range(len(self.lines)) for i in range(len(self.lines))]
        self.white_pieces = {}
        self.black_pieces = {}

    def draw_position(self, player: bool = True):
        if player is True:
            for piece in self.white_pieces:
                self.white_pieces[piece].draw_element()
            for piece in self.black_pieces:
                self.black_pieces[piece].draw_element()
        else:
            for piece in self.white_pieces:
                self.white_pieces[piece].draw_element(player=player)
            for piece in self.black_pieces:
                self.black_pieces[piece].draw_element(player=player)

    def reset_position(self, screen):
        self.bot = Bot()
        # self.board = chess.Board()
        self.white_pieces.clear()
        self.black_pieces.clear()
        self.white_queens_spawned = 0
        self.black_queens_spawned = 0
        self.white_long_castles_rights = True
        self.white_short_castles_rights = True
        self.black_long_castles_rights = True
        self.black_short_castles_rights = True
        self.player_to_move = True
        self.en_passant = False

        wp1 = Pawn(self.white_pieces, screen, "a2", True)
        wp2 = Pawn(self.white_pieces, screen, "b2", True)
        wp3 = Pawn(self.white_pieces, screen, "c2", True)
        wp4 = Pawn(self.white_pieces, screen, "d2", True)
        wp5 = Pawn(self.white_pieces, screen, "e2", True)
        wp6 = Pawn(self.white_pieces, screen, "f2", True)
        wp7 = Pawn(self.white_pieces, screen, "g2", True)
        wp8 = Pawn(self.white_pieces, screen, "h2", True)

        bp1 = Pawn(self.black_pieces, screen, "a7", False)
        bp2 = Pawn(self.black_pieces, screen, "b7", False)
        bp3 = Pawn(self.black_pieces, screen, "c7", False)
        bp4 = Pawn(self.black_pieces, screen, "d7", False)
        bp5 = Pawn(self.black_pieces, screen, "e7", False)
        bp6 = Pawn(self.black_pieces, screen, "f7", False)
        bp7 = Pawn(self.black_pieces, screen, "g7", False)
        bp8 = Pawn(self.black_pieces, screen, "h7", False)

        wk = King(self.white_pieces, screen, "e1", True)
        bk = King(self.black_pieces, screen, "e8", False)

        wq = Queen(self.white_pieces, screen, "d1", True)
        bq = Queen(self.black_pieces, screen, "d8", False)

        wb1 = Bishop(self.white_pieces, screen, "c1", True)
        wb2 = Bishop(self.white_pieces, screen, "f1", True)

        bb1 = Bishop(self.black_pieces, screen, "c8", False)
        bb2 = Bishop(self.black_pieces, screen, "f8", False)

        wn1 = Knight(self.white_pieces, screen, "b1", True)
        wn2 = Knight(self.white_pieces, screen, "g1", True)

        bn1 = Knight(self.black_pieces, screen, "b8", False)
        bn2 = Knight(self.black_pieces, screen, "g8", False)

        wr1 = Rook(self.white_pieces, screen, "a1", True)
        wr2 = Rook(self.white_pieces, screen, "h1", True)

        br1 = Rook(self.black_pieces, screen, "a8", False)
        br2 = Rook(self.black_pieces, screen, "h8", False)
