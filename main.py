import sys
from CurrentPosition import CurrentPosition
import pygame as p
import chess
from Background import Background
from Pawn import Pawn
from Queen import Queen
from Button import Button

PLAYER_TO_MOVE = None
WHITE_MOVES = []
BLACK_MOVES = []
en_passant_pawn = None


def app_Run():
    p.init()
    screen = p.display.set_mode((700, 700))
    p.display.set_caption("Chess Application")
    clk = p.time.Clock()
    display_board(screen)
    cp = CurrentPosition(screen)
    cp.reset_position(screen)
    tlo = Background(screen)
    # manage_buttons(1,screen,font)
    btn_restart = Button(screen, (520, 80), "restart", (100, 50), (19, 143, 118), (91, 181, 131), (255, 255, 255))

    global PLAYER_TO_MOVE
    PLAYER_TO_MOVE = True
    clicks = []

    while True:
        # events handling:

        for event in p.event.get():
            if event.type == p.QUIT:
                sys.exit()
            elif event.type == p.MOUSEBUTTONDOWN:
                manage_move(screen, cp, clicks)
            elif event.type == p.K_ESCAPE:
                main_menu = True
            elif btn_restart.clicked is True:
                event_restart(cp, screen, clicks, cp.white_pieces)

        btn_restart.draw()
        clk.tick(60)
        p.display.flip()


def display_board(screen: p.surface):
    for i in range(8):
        for j in range(8):
            if (i + j) % 2 == 0:
                p.draw.rect(screen, p.Color("white"), p.Rect(i * 64, j * 64, 64, 64))
            else:
                p.draw.rect(screen, p.Color("dark grey"), p.Rect(i * 64, j * 64, 64, 64))


def manage_click():
    point_x, point_y = p.mouse.get_pos()
    if point_x <= 512 and point_y <= 512:
        sq_selected = point_x // 64 + 1, 9 - (point_y // 64 + 1)
        print(num_to_pgn(sq_selected[0], sq_selected[1]))
        return num_to_pgn(sq_selected[0], sq_selected[1])
    else:
        return None


def manage_move(screen: p.surface, cp: CurrentPosition, clicks: list):
    global PLAYER_TO_MOVE
    global en_passant_pawn

    sq_pgn = manage_click()

    if sq_pgn is not None:
        if PLAYER_TO_MOVE is True:  # white to move
            event_log = WHITE_MOVES
            pieces = cp.white_pieces
            opponent_pieces = cp.black_pieces
        else:
            event_log = BLACK_MOVES
            pieces = cp.black_pieces
            opponent_pieces = cp.white_pieces

        if sq_pgn in pieces:  # checking whether player's piece is clicked
            event_log.append(sq_pgn)
            clicks.clear()
            clicks.append(sq_pgn)
        else:
            if len(clicks) == 1:
                move_squares = event_log[-1] + sq_pgn  # saving a move in format : "sq1sq2"
                if chess.Move.from_uci(move_squares + "q") in cp.board.legal_moves:
                    move_squares += 'q'

                if chess.Move.from_uci(
                        move_squares) in cp.board.legal_moves:  # checking whether requested move is legal
                    # if it is, executing a move:
                    check_en_passant(move_squares, sq_pgn, cp, pieces, opponent_pieces)
                    en_passant_pawn = set_en_passant(cp, move_squares, event_log, sq_pgn, pieces, opponent_pieces)

                    if PLAYER_TO_MOVE is True and sq_pgn == "g1" and cp.white_short_castles_rights is True:  # managing
                        # white's kingside castles
                        pieces["h1"].change_position("f1")  # rotate the castled rook
                        cp.white_short_castles_rights = False
                    elif PLAYER_TO_MOVE is True and sq_pgn == "c1" and cp.white_long_castles_rights is True:  # managing
                        # white's queenside castles
                        pieces["a1"].change_position("e1")  # rotate the castled rook
                        cp.white_long_castles_rights = False
                    if PLAYER_TO_MOVE is False and sq_pgn == "g8" and cp.black_short_castles_rights is True:  # managing
                        # black's kingside castles
                        pieces["h8"].change_position("f8")  # rotate the castled rook
                        cp.black_short_castles_rights = False
                    elif PLAYER_TO_MOVE is False and sq_pgn == "c8" and cp.black_long_castles_rights is True:
                        # managing black's queenside castles
                        pieces["a8"].change_position("e8")  # rotate the castled rook
                        cp.black_long_castles_rights = False

                    # checking white's rights to castle kingside, changing to FALSE if king or rook are moved
                    if event_log[-1] == "e1" or event_log[-1] == "h1":
                        cp.white_short_castles_rights = False
                    # checking white's rights to castle queenside, changing to FALSE if king or rook are moved
                    elif event_log[-1] == "e1" or event_log[-1] == "a1":
                        cp.white_long_castles_rights = False
                    # checking black's rights to castle kingside, changing to FALSE if king or rook are moved
                    if event_log[-1] == "e8" or event_log[-1] == "h8":
                        cp.black_short_castles_rights = False
                    # checking black's rights to castle queenside, changing to FALSE if king or rook are moved
                    elif event_log[-1] == "e8" or event_log[-1] == "a8":
                        cp.black_long_castles_rights = False

                    board_refresh(cp, move_squares, event_log, sq_pgn, pieces, opponent_pieces, screen, clicks)
                else:  # if move is illegal, resetting list of clicks to 1
                    clicks.pop()


def board_refresh(cp: CurrentPosition, move_squares: str, event_log: list, sq_pgn: str, pieces: dict,
                  opponent_pieces: dict, screen: p.surface, clicks: list, promotion: bool = False):
    global PLAYER_TO_MOVE
    cp.board.push_uci(move_squares)
    event_log.append(sq_pgn)  # adding move to log
    moved_piece = pieces[event_log[-2]]
    moved_piece.change_position(sq_pgn)
    pieces.update({event_log[-2]: moved_piece, sq_pgn: moved_piece})  # adding new position to dict
    del pieces[event_log[-2]]  # deleting obsolete position
    if sq_pgn in opponent_pieces:  # capturing enemy's pieces
        del opponent_pieces[sq_pgn]

    if move_squares[-1] == 'q':  # checking whether it's a promotion
        del pieces[sq_pgn]
        pawn_promotion(PLAYER_TO_MOVE, sq_pgn[0], cp, screen)

    display_board(screen)  # redrawing chessboard
    cp.draw_position()  # drawing updated pieces
    PLAYER_TO_MOVE = not PLAYER_TO_MOVE
    p.display.flip()
    clicks.clear()


# function executing en_passant capture
def check_en_passant(move_squares: str, sq_pgn: str, cp: CurrentPosition, pieces: dict, opponent_pieces: dict):
    global PLAYER_TO_MOVE
    global en_passant_pawn
    if cp.en_passant is True and en_passant_pawn is not None:
        if PLAYER_TO_MOVE is True:
            if type(pieces[(move_squares[0] + move_squares[1])]) is Pawn and (sq_pgn == (en_passant_pawn[0] + '6')):
                deleted_piece = sq_pgn[0] + str(int(sq_pgn[1]) - 1)
                del opponent_pieces[deleted_piece]
                cp.en_passant = False
            else:
                cp.en_passant = False
        elif PLAYER_TO_MOVE is False:
            if type(pieces[(move_squares[0] + move_squares[1])]) is Pawn and (sq_pgn == (en_passant_pawn[0] + '3')):
                deleted_piece = sq_pgn[0] + str(int(sq_pgn[1]) + 1)
                del opponent_pieces[deleted_piece]
                cp.en_passant = False
            else:
                cp.en_passant = False


# function checking, whether actual move is en-passant possible, and setting en_passant flag
def set_en_passant(cp: CurrentPosition, move_squares: str, event_log: list, sq_pgn: str, pieces: dict,
                   opponent_pieces: dict):
    global PLAYER_TO_MOVE
    en_passant_pawn: str
    if PLAYER_TO_MOVE is True:
        if move_squares[1] == '2' and move_squares[3] == '4' and type(pieces[event_log[-1]]) is Pawn:
            if neighboring_pawn(sq_pgn, opponent_pieces) is not None:
                cp.en_passant = True
                return sq_pgn  # returns square of pawn which is possible to capture en_passant next move
    if PLAYER_TO_MOVE is False:
        if move_squares[1] == '7' and move_squares[3] == '5' and type(pieces[event_log[-1]]) is Pawn:
            if neighboring_pawn(sq_pgn, opponent_pieces) is not None:
                cp.en_passant = True
                return sq_pgn  # returns square of pawn which is possible to capture en_passant next move


# function returning square occupied by opponents' pawn, which can capture en passant:
def neighboring_pawn(sq_pgn: str, opponent_pieces: dict):
    global PLAYER_TO_MOVE
    if PLAYER_TO_MOVE is True:
        if sq_pgn[0] == 'a':
            if "b4" in opponent_pieces and type(opponent_pieces["b4"]) is Pawn:
                return "b4"
        elif sq_pgn[0] == 'h':
            if "g4" in opponent_pieces and type(opponent_pieces["g4"]) is Pawn:
                return "g4"
        else:
            if num_to_pgn(pgn_to_num(sq_pgn)[0] - 1, pgn_to_num(sq_pgn)[1]) in opponent_pieces and type(
                    opponent_pieces[num_to_pgn(pgn_to_num(sq_pgn)[0] - 1, pgn_to_num(sq_pgn)[1])]) is Pawn:
                return num_to_pgn(pgn_to_num(sq_pgn)[0] - 1, pgn_to_num(sq_pgn)[1])
            elif num_to_pgn(pgn_to_num(sq_pgn)[0] + 1, pgn_to_num(sq_pgn)[1]) in opponent_pieces and type(
                    opponent_pieces[num_to_pgn(pgn_to_num(sq_pgn)[0] + 1, pgn_to_num(sq_pgn)[1])]) is Pawn:
                return num_to_pgn(pgn_to_num(sq_pgn)[0] + 1, pgn_to_num(sq_pgn)[1])
            else:
                return None
    else:
        if sq_pgn[0] == 'a':
            if "b6" in opponent_pieces and type(opponent_pieces["b6"]) is Pawn:
                return "b6"
        elif sq_pgn[0] == 'h':
            if "g6" in opponent_pieces and type(opponent_pieces["g6"]) is Pawn:
                return "g6"
        else:
            if num_to_pgn(pgn_to_num(sq_pgn)[0] - 1, pgn_to_num(sq_pgn)[1]) in opponent_pieces and type(
                    opponent_pieces[num_to_pgn(pgn_to_num(sq_pgn)[0] - 1, pgn_to_num(sq_pgn)[1])]) is Pawn:
                return num_to_pgn(pgn_to_num(sq_pgn)[0] - 1, pgn_to_num(sq_pgn)[1])
            elif num_to_pgn(pgn_to_num(sq_pgn)[0] + 1, pgn_to_num(sq_pgn)[1]) in opponent_pieces and type(
                    opponent_pieces[num_to_pgn(pgn_to_num(sq_pgn)[0] + 1, pgn_to_num(sq_pgn)[1])]) is Pawn:
                return num_to_pgn(pgn_to_num(sq_pgn)[0] + 1, pgn_to_num(sq_pgn)[1])
            else:
                return None


def num_to_pgn(square_x: int, square_y: int) -> str:
    line_dict = {1: "a", 2: "b", 3: "c", 4: "d", 5: "e", 6: "f", 7: "g", 8: "h"}
    return line_dict[square_x] + str(square_y)


def pgn_to_num(position: str) -> tuple:
    line_dict = {"a": 1, "b": 2, "c": 3, "d": 4, "e": 5, "f": 6, "g": 7, "h": 8}
    return line_dict[position[0]], int(position[1])


def pawn_promotion(player: bool, line: str, cp: CurrentPosition, screen: p.surface):
    if player is True:  # white's promotion
        square = line + '8'
        wqn = Queen(cp.white_pieces, screen, square, True)
    else:
        square = line + '1'
        wqn = Queen(cp.black_pieces, screen, square, False)


def manage_buttons(n: int, screen: p.surface, font: p.font):
    btn_restart = Button(screen, (600, 100), "restart", (100, 50), (1, 0, 0), (1, 1, 0), (1, 1, 1), font)


def event_restart(cp: CurrentPosition, screen: p.surface, clicks: list, pieces: dict):
    global PLAYER_TO_MOVE
    cp.reset_position(screen)
    display_board(screen)  # redrawing chessboard
    cp.draw_position()  # drawing updated pieces
    p.display.flip()
    clicks.clear()
    PLAYER_TO_MOVE = True

if __name__ == '__main__':
    app_Run()
