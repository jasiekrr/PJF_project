import sys
from CurrentPosition import CurrentPosition
import pygame as p
import chess

from Pawn import Pawn
from Queen import Queen

PLAYER_TO_MOVE = None
WHITE_MOVES = []
BLACK_MOVES = []


def app_Run():
    p.init()
    screen = p.display.set_mode((512, 512))
    clk = p.time.Clock()
    display_board(screen)
    cp = CurrentPosition(screen)
    cp.reset_position(screen)
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
        clk.tick(15)
        p.display.flip()


def display_board(screen: p.surface):
    for i in range(8):
        for j in range(8):
            if (i + j) % 2 == 0:
                p.draw.rect(screen, p.Color("white"), p.Rect(i * 512 / 8, j * 512 / 8, 512 / 8, 512 / 8))
            else:
                p.draw.rect(screen, p.Color("dark grey"), p.Rect(i * 512 / 8, j * 512 / 8, 512 / 8, 512 / 8))


def manage_click():
    point_x, point_y = p.mouse.get_pos()
    sq_selected = point_x // 64 + 1, 9 - (point_y // 64 + 1)
    print(num_to_pgn(sq_selected[0], sq_selected[1]))
    return num_to_pgn(sq_selected[0], sq_selected[1])


def manage_move(screen: p.surface, cp: CurrentPosition, clicks: list):
    global PLAYER_TO_MOVE
    sq_pgn = manage_click()
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

            if chess.Move.from_uci(move_squares) in cp.board.legal_moves:  # checking whether requested move is legal
                # if it is, executing a move:
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


def num_to_pgn(square_x: int, square_y: int) -> str:
    line_dict = {1: "a", 2: "b", 3: "c", 4: "d", 5: "e", 6: "f", 7: "g", 8: "h"}
    return line_dict[square_x] + str(square_y)


def pawn_promotion(player: bool, line: str, cp: CurrentPosition, screen: p.surface):
    if player is True:  # white's promotion
        square = line + '8'
        wqn = Queen(cp.white_pieces, screen, square, True)
    else:
        square = line + '1'
        wqn = Queen(cp.black_pieces, screen, square, False)


if __name__ == '__main__':
    app_Run()
