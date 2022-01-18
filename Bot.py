import random

import pygame as p
import chess
import chess.engine


class Bot:
    def __init__(self, board: chess.Board):
        self.board = board
        self.engine = chess.engine.SimpleEngine.popen_uci(
            r"C:\Users\jroma\Desktop\stockfish\stockfish_14.1_win_x64_avx2\stockfish_14.1_win_x64_avx2.exe")

    def get_random_move(self):
        moves_list = []
        for move in self.board.legal_moves:
            moves_list.append(move.uci())
        iterator = random.randint(0, len(moves_list) - 1)
        return moves_list[iterator]

    def get_best_move(self):
        result = self.engine.play(self.board, chess.engine.Limit(time=0.1))
        self.board.push(result.move)
        return str(result.move)

    def analise_pos(self):
        info = self.engine.analyse(self.board, chess.engine.Limit(time=0.1))
        print("Score:", info["score"])

    def refresh(self):
        self.board = chess.Board()
        return self.board
