import sys
from CurrentPosition import CurrentPosition
import pandas
import pygame as p

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

            event_log.append(sq_pgn)  # adding move to log
            moved_piece = pieces[event_log[-2]]
            moved_piece.change_position(sq_pgn)
            pieces.update({event_log[-2]: moved_piece, sq_pgn: moved_piece})  # adding new position to dict
            del pieces[event_log[-2]]  # deleting obsolete position

            if sq_pgn in opponent_pieces:  # capturing enemy's pieces
                del opponent_pieces[sq_pgn]

            display_board(screen)  # redrawing chessboard
            cp.draw_position()  # drawing updated pieces

            PLAYER_TO_MOVE = not PLAYER_TO_MOVE

            p.display.flip()
            clicks.clear()


def num_to_pgn(square_x: int, square_y: int) -> str:
    line_dict = {1: "a", 2: "b", 3: "c", 4: "d", 5: "e", 6: "f", 7: "g", 8: "h"}
    return line_dict[square_x] + str(square_y)


if __name__ == '__main__':
    app_Run()
