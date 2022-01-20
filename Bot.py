import random
import chess
import chess.engine


class Bot:
    def __init__(self):
        self.board = chess.Board()
        #self.engine = await chess.engine.popen_uci(r"C:\Users\jroma\Desktop\stockfish\stockfish_14.1_win_x64_avx2\stockfish_14.1_win_x64_avx2.exe")
        self.engine = chess.engine.SimpleEngine.popen_uci(
           r"C:\Users\jroma\Desktop\stockfish\stockfish_14.1_win_x64_avx2\stockfish_14.1_win_x64_avx2.exe")

    def get_random_move(self):
        moves_list = []
        for move in self.board.legal_moves:
            moves_list.append(move.uci())
        iterator = random.randint(0, len(moves_list) - 1)
        return moves_list[iterator]

    def get_best_move(self, depth: int = 10):
        result = self.engine.play(self.board, chess.engine.Limit(time=1, depth= depth))
        return str(result.move)

    def analyse_pos(self):
        info = self.engine.analyse(self.board, chess.engine.Limit(depth=10))
        return str(info["score"])
