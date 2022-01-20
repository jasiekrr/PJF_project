import sys

from Bot import Bot
from CurrentPosition import CurrentPosition
import pygame as p
from Background import Background
from Pawn import Pawn
from Queen import Queen
from Button import Button
import chess
import chess.engine

PLAYER_TO_MOVE = None
MOVED = False
AGAINST_BOT = False
CHOSEN_COLOR = True
CHALLENGE = False

en_passant_pawn = None
event_log = []

def app_Run():
    p.init()
    screen = p.display.set_mode((700, 700))
    p.display.set_caption("Chess Application")
    clk = p.time.Clock()
    display_board(screen)
    cp = CurrentPosition(screen)
    cp.reset_position(screen)
    tlo = Background(screen)

    btn_restart = Button(screen, (550, 80), "restart", (100, 50), (19, 143, 118), (91, 181, 131), (255, 255, 255))
    btn_challenge = Button(screen, (550, 180), "train", (100, 50), (19, 143, 118), (91, 181, 131), (255, 255, 255))
    btn_against_bot = Button(screen, (550, 280), "pvp", (100, 50), (19, 143, 118), (91, 181, 131), (255, 255, 255))
    btn_exit = Button(screen, (550, 380), "exit", (100, 50), (19, 143, 118), (91, 181, 131), (255, 255, 255))
    btn_change_color = Button(screen, (80, 550), "change color", (200, 50), (10, 20, 10), (105, 105, 105),
                              (255, 255, 255))
    global PLAYER_TO_MOVE
    global MOVED
    global AGAINST_BOT
    global CHOSEN_COLOR
    global CHALLENGE
    PLAYER_TO_MOVE = True
    clicks = []

    while True:
        for event in p.event.get():
            if event.type == p.QUIT:
                sys.exit()
            elif event.type == p.MOUSEBUTTONDOWN:
                manage_move(screen, cp, clicks)
            elif event.type == p.K_ESCAPE:
                sys.exit()
            elif btn_restart.clicked is True:
                AGAINST_BOT = False
                event_restart(cp, screen, clicks)
            elif btn_challenge.clicked is True:
                AGAINST_BOT = False
                CHALLENGE = True
                event_challenge(cp, screen, clicks)
            elif btn_against_bot.clicked is True:
                AGAINST_BOT = True
            elif btn_change_color.clicked is True:
                btn_change_color = event_change_color(cp, screen, clicks, btn_change_color)
            elif btn_exit.clicked is True:
                sys.exit()
            else:
                pass

        btn_restart.draw()
        btn_challenge.draw()
        btn_against_bot.draw()
        btn_exit.draw()
        btn_change_color.draw()
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
        if CHOSEN_COLOR is True:
            sq_selected = point_x // 64 + 1, 9 - (point_y // 64 + 1)
            print(num_to_pgn(sq_selected[0], sq_selected[1]))
            return num_to_pgn(sq_selected[0], sq_selected[1])
        else:
            sq_selected = 8 - (point_x // 64), (point_y // 64 + 1)
            print(num_to_pgn(sq_selected[0], sq_selected[1]))
            return num_to_pgn(sq_selected[0], sq_selected[1])
    else:
        return None


def manage_move(screen: p.surface, cp: CurrentPosition, clicks: list, move: str = None):
    global PLAYER_TO_MOVE
    global en_passant_pawn
    global MOVED
    global event_log
    sq_pgn = manage_click()
    if move is not None:
        event_log = [move[0] + move[1]]
        sq_pgn = move[2] + move[3]
        clicks.append(event_log[0])
        print(
            f"ruch silnika, clicks: {clicks} , event log: {event_log}  , sq_pgn : {sq_pgn} , player : {PLAYER_TO_MOVE}")

    if sq_pgn is not None:
        if PLAYER_TO_MOVE is True:  # white to move
            pieces = cp.white_pieces
            opponent_pieces = cp.black_pieces
        else:
            pieces = cp.black_pieces
            opponent_pieces = cp.white_pieces

        if sq_pgn in pieces:  # checking whether player's piece is clicked
            print(clicks)
            event_log.append(sq_pgn)
            clicks.clear()
            clicks.append(sq_pgn)
        else:
            if len(clicks) == 1:
                print(pieces[event_log[-1]])
                move_squares = event_log[-1] + sq_pgn  # saving a move in format : "sq1sq2"

                if chess.Move.from_uci(move_squares + "q") in cp.bot.board.legal_moves:
                    move_squares += 'q'
                if chess.Move.from_uci(
                        move_squares) in cp.bot.board.legal_moves:  # checking whether requested move is legal
                    # if it is, executing a move:
                    check_en_passant(move_squares, sq_pgn, cp, pieces, opponent_pieces)
                    en_passant_pawn = set_en_passant(cp, move_squares, event_log, sq_pgn, pieces, opponent_pieces)

                    if PLAYER_TO_MOVE is True and sq_pgn == "g1" and cp.white_short_castles_rights is True and \
                            (move_squares[0] + move_squares[1]) == "e1":  # managing
                        # white's kingside castles
                        pieces["h1"].change_position("f1")  # rotate the castled rook
                        cp.white_short_castles_rights = False
                        pieces.update({"f1": pieces["h1"], sq_pgn: pieces["h1"]})  # adding new position to dict
                        del pieces["h1"]  # deleting obsolete position

                    elif PLAYER_TO_MOVE is True and sq_pgn == "c1" and cp.white_long_castles_rights is True and \
                            (move_squares[0] + move_squares[1]) == "e1":  # managing
                        # white's queenside castles
                        pieces["a1"].change_position("d1")  # rotate the castled rook
                        cp.white_long_castles_rights = False
                        pieces.update({"d1": pieces["a1"], sq_pgn: pieces["a1"]})  # adding new position to dict
                        del pieces["a1"]  # deleting obsolete position

                    if PLAYER_TO_MOVE is False and sq_pgn == "g8" and cp.black_short_castles_rights is True and \
                            (move_squares[0] + move_squares[1]) == "e8":  # managing
                        # black's kingside castles
                        pieces["h8"].change_position("f8")  # rotate the castled rook
                        cp.black_short_castles_rights = False
                        pieces.update({"f8": pieces["h8"], sq_pgn: pieces["h8"]})  # adding new position to dict
                        del pieces["h8"]  # deleting obsolete position

                    elif PLAYER_TO_MOVE is False and sq_pgn == "c8" and cp.black_long_castles_rights is True and \
                            (move_squares[0] + move_squares[1]) == "e8":
                        # managing black's queenside castles
                        pieces["a8"].change_position("d8")  # rotate the castled rook
                        cp.black_long_castles_rights = False
                        pieces.update({"d8": pieces["a8"], sq_pgn: pieces["a8"]})  # adding new position to dict
                        del pieces["a8"]  # deleting obsolete position

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
                    if move is None:
                        MOVED = True

                    board_refresh(cp, move_squares, screen, clicks)
                    clicks.clear()
                else:  # if move is illegal, resetting list of clicks to 1
                    clicks.pop()


def board_refresh(cp: CurrentPosition, move_squares: str, screen: p.surface, clicks: list):
    global PLAYER_TO_MOVE
    global AGAINST_BOT
    global MOVED
    global CHALLENGE

    if PLAYER_TO_MOVE is True:
        pieces = cp.white_pieces
        opponent_pieces = cp.black_pieces
    else:
        pieces = cp.black_pieces
        opponent_pieces = cp.white_pieces

    eventlog = [move_squares[0] + move_squares[1], move_squares[2] + move_squares[3]]
    sq_pgn = eventlog[1]

    print(cp.bot.analyse_pos())

    moved_piece = pieces[eventlog[-2]]
    moved_piece.change_position(sq_pgn)
    pieces.update({eventlog[-2]: moved_piece, sq_pgn: moved_piece})  # adding new position to dict
    del pieces[eventlog[-2]]  # deleting obsolete position
    if sq_pgn in opponent_pieces:  # capturing enemy's pieces
        del opponent_pieces[sq_pgn]

    if move_squares[-1] == 'q':  # checking whether it's a promotion
        del pieces[sq_pgn]
        pawn_promotion(PLAYER_TO_MOVE, sq_pgn[0], cp, screen)

    display_board(screen)  # redrawing chessboard
    print(f"draw results: {move_squares}")
    draw_result(move_squares, screen, cp)
    cp.bot.board.push(chess.Move.from_uci(move_squares))

    cp.draw_position(CHOSEN_COLOR)  # drawing updated pieces

    if CHOSEN_COLOR == PLAYER_TO_MOVE:
        MOVED = True
    else:
        MOVED = False

    PLAYER_TO_MOVE = not PLAYER_TO_MOVE

    if AGAINST_BOT and CHALLENGE and cp.bot.board.is_game_over():
        CHALLENGE = False

    if AGAINST_BOT is True and MOVED is True:  # if managed move was made by a player its engine's turn to make move
        clicks.clear()
        MOVED = False
        if cp.bot.board.is_game_over() is False:
            engine_move = cp.bot.get_best_move()
            manage_move(screen, cp, clicks, str(engine_move))
        else:
            print("koniec gry 1 ")
    else:
        if cp.bot.board.is_game_over() is True:
            print("koniec gry 2 ")
            event_restart(cp, screen, clicks)
    p.display.flip()


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
    # en_passant_pawn: str
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


def event_restart(cp: CurrentPosition, screen: p.surface, clicks: list, color_change: bool = True):
    global PLAYER_TO_MOVE
    global MOVED
    global AGAINST_BOT

    cp.reset_position(screen)
    display_board(screen)  # redrawing chessboard
    cp.draw_position(color_change)  # drawing updated pieces
    p.display.flip()
    clicks.clear()
    PLAYER_TO_MOVE = True

    if color_change is True:
        MOVED = False
    else:
        MOVED = True

    AGAINST_BOT = False


def event_challenge(cp: CurrentPosition, screen: p.surface, clicks: list, n=20, doctrine=False):
    global PLAYER_TO_MOVE
    global CHOSEN_COLOR
    event_restart(cp, screen, clicks, CHOSEN_COLOR)

    if doctrine is True:
        while not ("Mate" in cp.bot.analyse_pos()):
            if cp.bot.board.is_game_over() is False:
                result = cp.bot.engine.play(cp.bot.board, chess.engine.Limit(time=0.1))
                manage_move(screen, cp, clicks, str(result.move))
            else:
                print("koniec gry")
        event_against_bot(cp, screen, clicks, PLAYER_TO_MOVE)
        to_mate = cp.bot.analyse_pos()
        to_mate = int(to_mate[15])
        print(f"mate in {to_mate} moves")

    else:
        while not ("Mate" in cp.bot.analyse_pos()):
            if cp.bot.board.is_game_over() is False:
                result_move = cp.bot.get_best_move()
                manage_move(screen, cp, clicks, str(result_move))
                move = cp.bot.get_random_move()
                manage_move(screen, cp, clicks, str(move))

            else:
                print("koniec gry w evnt")

        print(PLAYER_TO_MOVE)
        event_against_bot(cp, screen, clicks, PLAYER_TO_MOVE)
        to_mate = cp.bot.analyse_pos()
        to_mate = int(to_mate[15])
        print(f"mate in {to_mate} moves")

    display_board(screen)  # redrawing chessboard
    cp.draw_position()  # drawing updated pieces
    p.display.flip()
    clicks.clear()


def event_against_bot(cp: CurrentPosition, screen: p.surface, clicks: list, color: bool = True):
    global PLAYER_TO_MOVE
    global MOVED
    global AGAINST_BOT
    MOVED = not color
    AGAINST_BOT = True


def event_change_color(cp: CurrentPosition, screen: p.surface, clicks: list, btn: Button):
    global PLAYER_TO_MOVE
    global CHOSEN_COLOR
    global MOVED

    CHOSEN_COLOR = not CHOSEN_COLOR
    PLAYER_TO_MOVE = True

    event_restart(cp, screen, clicks, CHOSEN_COLOR)


    if CHOSEN_COLOR is True:
        del btn
        btn = Button(screen, (80, 550), "change color", (200, 50), (10, 20, 10), (105, 105, 105),
                     (255, 255, 255))
    else:
        del btn
        btn = Button(screen, (80, 550), "change color", (200, 50), (250, 240, 240), (105, 105, 105),
                     (10, 20, 10))

    return btn


def draw_result(move: str, screen: p.surface, cp: CurrentPosition):
    global CHALLENGE
    global CHOSEN_COLOR
    best_move = cp.bot.get_best_move()
    sq1_best = best_move[0] + best_move[1]
    sq2_best = best_move[2] + best_move[3]

    if CHOSEN_COLOR:
        if CHALLENGE is True:
            if move is not (sq1_best, sq2_best):
                red1 = p.draw.rect(screen, p.Color("Red"),
                                   p.Rect((pgn_to_num(move[0] + move[1])[0] - 1) * 64,
                                          (7 - (pgn_to_num(move[0] + move[1])[1] - 1)) * 64, 64, 64))
                red2 = p.draw.rect(screen, p.Color("Red"),
                                   p.Rect((pgn_to_num(move[2] + move[3])[0] - 1) * 64,
                                          (7 - (pgn_to_num(move[2] + move[3])[1] - 1)) * 64, 64, 64))

                green1 = p.draw.rect(screen, p.Color("Green"),
                                     p.Rect((pgn_to_num(sq1_best)[0] - 1) * 64, (7 - (pgn_to_num(sq1_best)[1] - 1)) * 64,
                                            64,
                                            64))
                green2 = p.draw.rect(screen, p.Color("Green"),
                                     p.Rect((pgn_to_num(sq2_best)[0] - 1) * 64, (7 - (pgn_to_num(sq2_best)[1] - 1)) * 64,
                                            64,
                                            64))
            else:
                green1 = p.draw.rect(screen, p.Color("Green"),
                                   p.Rect((pgn_to_num(move[0] + move[1])[0] - 1) * 64,
                                          (7 - (pgn_to_num(move[0] + move[1])[1] - 1)) * 64, 64, 64))
                green2 = p.draw.rect(screen, p.Color("Green"),
                                   p.Rect((pgn_to_num(move[2] + move[3])[0] - 1) * 64,
                                          (7 - (pgn_to_num(move[2] + move[3])[1] - 1)) * 64, 64, 64))
        else:
            yellow1 = p.draw.rect(screen, p.Color("Yellow"),
                                  p.Rect((pgn_to_num(move[0] + move[1])[0] - 1) * 64,
                                         (7 - (pgn_to_num(move[0] + move[1])[1] - 1)) * 64, 64, 64))
            yellow2 = p.draw.rect(screen, p.Color("Yellow"),
                                  p.Rect((pgn_to_num(move[2] + move[3])[0] - 1) * 64,
                                         (7 - (pgn_to_num(move[2] + move[3])[1] - 1)) * 64, 64, 64))
            green1 = p.draw.rect(screen, p.Color("Green"),
                                 p.Rect((pgn_to_num(sq1_best)[0] - 1) * 64, (7 - (pgn_to_num(sq1_best)[1] - 1)) * 64, 64,
                                        64))
            green2 = p.draw.rect(screen, p.Color("Green"),
                                 p.Rect((pgn_to_num(sq2_best)[0] - 1) * 64, (7 - (pgn_to_num(sq2_best)[1] - 1)) * 64, 64,
                                        64))
    else:
        if CHALLENGE is True:
            if move is not (sq1_best, sq2_best):
                red1 = p.draw.rect(screen, p.Color("Red"),
                                   p.Rect((7 - (pgn_to_num(move[0] + move[1])[0] - 1)) * 64,
                                          (pgn_to_num(move[0] + move[1])[1] - 1) * 64, 64, 64))
                red2 = p.draw.rect(screen, p.Color("Red"),
                                   p.Rect((7-(pgn_to_num(move[2] + move[3])[0] - 1)) * 64,
                                          (pgn_to_num(move[2] + move[3])[1] - 1) * 64, 64, 64))

                green1 = p.draw.rect(screen, p.Color("Green"),
                                     p.Rect((7 - (pgn_to_num(move[0] + move[1])[0] - 1)) * 64,
                                            (pgn_to_num(move[0] + move[1])[1] - 1) * 64, 64, 64))
                green2 = p.draw.rect(screen, p.Color("Green"),
                                     p.Rect((7-(pgn_to_num(move[2] + move[3])[0] - 1)) * 64,
                                            (pgn_to_num(move[2] + move[3])[1] - 1) * 64, 64, 64))
            else:
                green1 = p.draw.rect(screen, p.Color("Green"),
                                     p.Rect((7 - (pgn_to_num(move[0] + move[1])[0] - 1)) * 64,
                                            (pgn_to_num(move[0] + move[1])[1] - 1) * 64, 64, 64))
                green2 = p.draw.rect(screen, p.Color("Green"),
                                     p.Rect((7-(pgn_to_num(move[2] + move[3])[0] - 1)) * 64,
                                            (pgn_to_num(move[2] + move[3])[1] - 1) * 64, 64, 64))
        else:
            yellow1 = p.draw.rect(screen, p.Color("Yellow"),
                                  p.Rect((7 - (pgn_to_num(move[0] + move[1])[0] - 1)) * 64,
                                         (pgn_to_num(move[0] + move[1])[1] - 1) * 64, 64, 64))
            yellow2 = p.draw.rect(screen, p.Color("Yellow"),
                                  p.Rect((7 - (pgn_to_num(move[2] + move[3])[0] - 1)) * 64,
                                         (pgn_to_num(move[2] + move[3])[1] - 1) * 64, 64, 64))
            green1 = p.draw.rect(screen, p.Color("Green"),
                                 p.Rect((7 - (pgn_to_num(sq1_best)[0] - 1)) * 64,
                                        (pgn_to_num(sq1_best)[1] - 1) * 64, 64, 64))
            green2 = p.draw.rect(screen, p.Color("Green"),
                                 p.Rect((7 - (pgn_to_num(sq2_best)[0] - 1)) * 64,
                                        (pgn_to_num(sq2_best)[1] - 1) * 64, 64, 64))



if __name__ == '__main__':
    app_Run()
