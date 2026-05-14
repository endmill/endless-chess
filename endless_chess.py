import chess
import chess.engine
import time
import keyboard
import numpy
import random
import pygame
import sys
import tkinter
import pathlib
import shutil

#engine path------------------------------------------------------------------------------------------------------------
HERE = pathlib.Path(__file__).resolve().parent
candidates = [
    HERE / "file" / "stockfish_15.1_x64_bmi2.exe",
    HERE / "file" / "stockfish.exe",
    pathlib.Path(r"file\stockfish_15.1_x64_bmi2.exe"),
]
which = shutil.which("stockfish") or shutil.which("stockfish.exe")
if which:
    candidates.insert(0, pathlib.Path(which))

engine_stockfish = None
for p in candidates:
    try:
        if p and p.exists():
            engine_stockfish = chess.engine.SimpleEngine.popen_uci(str(p))
            break
    except:
        pass

if engine_stockfish is None:
    sys.exit(1)

time.sleep(0.3)
#global variable--------------------------------------------------------------------------------------------------------

root = tkinter.Tk()
dx = root.winfo_screenwidth()
dy = root.winfo_screenheight()
root.destroy()

square_lenth = dx//15
pygame.init()
#screen = pygame.display.set_mode((dx, dy), pygame.FULLSCREEN)
screen = pygame.display.set_mode((dx, dy))
state = 'lobby'
tick = pygame.time.Clock()
frame = 0
now_frame = frame
x = 0
y = 0
counter = 10
board_x_zero = dx//2 - dx//15 * 4
board_y_zero = dy//2 - dx//15 * 4
# use script folder (HERE) so relative paths work regardless of current working directory
with open(HERE / "file" / "mate1.txt", 'r', encoding='utf-8') as mate1, \
     open(HERE / "file" / "mate2.txt", 'r', encoding='utf-8') as mate2, \
     open(HERE / "file" / "mate3.txt", 'r', encoding='utf-8') as mate3, \
     open(HERE / "file" / "mate4.txt", 'r', encoding='utf-8') as mate4:
    list_mate_1 = mate1.readlines()
    list_mate_2 = mate2.readlines()
    list_mate_3 = mate3.readlines()
    list_mate_4 = mate4.readlines()

#True면 문제를 풀고있지 않은 상황, False면 문제를 풀고있는 상황
solving_puzzle = True
matrix = None
list_pieces = []
solved = False
list_select_square = [[8,8],[8,8]]
finish_text_timer_onoff = True
failed = False
move_counter = 0
turn = 'white'
board = chess.Board()
fen = board.fen()
select_square = [8,8]
promotion_onoff = False
promotion_notation = 'none'
list_promotion_square = list_select_square
puzzles_number = 10
list_move_capture = []
list_move_stack = []
correct = False
display_text_puzzles_number = ''
#image path-------------------------------------------------------------------------------------------------------------
image_black_pawn = pygame.image.load(str(HERE / "file" / "bp.png"))
image_knight_black = pygame.image.load(str(HERE / "file" / "bn.png"))
image_black_bishop = pygame.image.load(str(HERE / "file" / "bb.png"))
image_black_rook = pygame.image.load(str(HERE / "file" / "br.png"))
image_black_queen = pygame.image.load(str(HERE / "file" / "bq.png"))
image_black_king = pygame.image.load(str(HERE / "file" / "bk.png"))

image_white_pawn = pygame.image.load(str(HERE / "file" / "wp.png"))
image_knight_white = pygame.image.load(str(HERE / "file" / "wn.png"))
image_white_bishop = pygame.image.load(str(HERE / "file" / "wb.png"))
image_white_rook = pygame.image.load(str(HERE / "file" / "wr.png"))
image_white_queen = pygame.image.load(str(HERE / "file" / "wq.png"))
image_white_king = pygame.image.load(str(HERE / "file" / "wk.png"))

image_star = pygame.image.load(str(HERE / "file" / "star.png"))
image_bomb = pygame.image.load(str(HERE / "file" / "bomb.png"))

image_back = pygame.image.load(str(HERE / "file" / "back.png"))
#image transform--------------------------------------------------------------------------------------------------------
image_black_pawn = pygame.transform.smoothscale(image_black_pawn,(dx//18, dx//18))
image_knight_black = pygame.transform.smoothscale(image_knight_black,(dx//18, dx//18))
image_black_bishop = pygame.transform.smoothscale(image_black_bishop,(dx//18, dx//18))
image_black_rook = pygame.transform.smoothscale(image_black_rook,(dx//18, dx//18))
image_black_queen = pygame.transform.smoothscale(image_black_queen,(dx//18, dx//18))
image_black_king = pygame.transform.smoothscale(image_black_king,(dx//18, dx//18))

image_white_pawn = pygame.transform.smoothscale(image_white_pawn,(dx//18, dx//18))
image_knight_white = pygame.transform.smoothscale(image_knight_white,(dx//18, dx//18))
image_white_bishop = pygame.transform.smoothscale(image_white_bishop,(dx//18, dx//18))
image_white_rook = pygame.transform.smoothscale(image_white_rook,(dx//18, dx//18))
image_white_queen = pygame.transform.smoothscale(image_white_queen,(dx//18, dx//18))
image_white_king = pygame.transform.smoothscale(image_white_king,(dx//18, dx//18))

image_star = pygame.transform.smoothscale(image_star, (dx//18, dx//18))
image_bomb = pygame.transform.smoothscale(image_bomb, (dx//18, dx//18))
dark_color = (115, 149, 82)
bright_color = (255, 255, 255)

#function---------------------------------------------------------------------------------------------------------------

def background():
    sq = dx // 8
    for a in range(0, 8, 2):
        for s in range(0, 10, 2):
            for d in range(0, sq):
                color_level = int(255 - 255 * (sq * s + d)/dy)
                if color_level < 0:
                    color_level = 0
                color = (color_level, color_level, color_level)
                pygame.draw.line(screen,color, (a * sq, s * sq + d), ((a + 1) * sq, s * sq + d))

    for a in range(1, 8, 2):
        for s in range(1, 10, 2):
            for d in range(0, sq):
                color_level = int(255 - 255 * (sq * s + d) / dy)
                if color_level < 0:
                    color_level = 0
                color = (color_level, color_level, color_level)
                pygame.draw.line(screen, color, (a * sq, s * sq + d), ((a + 1) * sq, s * sq + d))

def buttoner(text, size, color, start_x, start_y):
    font = pygame.font.Font(r"C:\Users\dygks\mython\pythonProject\ichess_training\file\HSSaemaul-Regular.ttf", size)
    text = font.render(text, True, color)
    pygame.draw.rect(screen, (255, 255, 255), (start_x - text.get_width()//2, start_y - text.get_height()//2, text.get_width(), text.get_height()))
    pygame.draw.rect(screen, (0, 0, 0), (start_x - text.get_width()//2 - dx//100, start_y - text.get_height()//2 - dx//100, text.get_width() + dx//50, text.get_height() +dx//50), dx//100)
    screen.blit(text, (start_x - text.get_width()//2, start_y - text.get_height()//2))

    if start_x - text.get_width()//2 <= x <= start_x + text.get_width()//2 and start_y - text.get_height()//2 <= y <= start_y + text.get_height()//2:
        return 1

def texter(text, size, color, x, y, center=True):
    """
    텍스트를 화면에 출력합니다.
    - center=True: (x,y)를 중앙으로 사용, False면 topleft 사용.
    - 반환: 렌더된 rect
    """
    font = _get_font(size)
    surf = font.render(str(text), True, color)
    rect = surf.get_rect()
    if center:
        rect.center = (int(x), int(y))
    else:
        rect.topleft = (int(x), int(y))
    screen.blit(surf, rect)
    return rect

# 안전한 폰트 로더 및 캐시
FONT_CACHE = {}
def _get_font(size: int):
    key = int(size)
    if key in FONT_CACHE:
        return FONT_CACHE[key]
    font_path = HERE / "file" / "HSSaemaul-Regular.ttf"
    try:
        f = pygame.font.Font(str(font_path), key)
    except Exception:
        f = pygame.font.SysFont(None, key)
    FONT_CACHE[key] = f
    return f

# 기존 코드가 textor 이름을 쓰는 경우 대비 alias
textor = texter

def back_button():
    screen.blit(image_back, (10, 10))
    if 10 <= x <= image_back.get_width() + 10 and 10 <= y <= image_back.get_height() + 10:
        return 1

def exiter():
    global state
    global x
    global y

    back_button()

    if state == 'lobby':
        if keyboard.is_pressed('backspace') or keyboard.is_pressed('esc') or back_button() == 1 or keyboard.is_pressed('right'):
            engine_stockfish.quit()
            sys.exit()
    else:
        if keyboard.is_pressed('backspace') or keyboard.is_pressed('esc') or back_button() == 1 or keyboard.is_pressed('right'):
            state = 'lobby'
            x, y = (0, 0)
            time.sleep(0.1)

def chessboard():
    global dark_color
    global bright_color
    for a in range(1, 8, 2):
        for s in range(0, 8, 2):
            pygame.draw.rect(screen,dark_color , (dx // 2 - dx // 15 * 4 + dx // 15 * s, dy //2 - dx // 15 * 4 + dx // 15 * a, dx // 15, dx // 15))
    for a in range(0, 8, 2):
        for s in range(1, 8, 2):
            pygame.draw.rect(screen, dark_color, (dx // 2 - dx // 15 * 4 + dx // 15 * s, dy //2 - dx // 15 * 4 + dx // 15 * a, dx // 15, dx // 15))
    for a in range(0, 8, 2):
        for s in range(0, 8, 2):
            pygame.draw.rect(screen, bright_color, (dx // 2 - dx // 15 * 4 + dx // 15 * s, dy //2 - dx // 15 * 4 + dx // 15 * a, dx // 15, dx // 15))
    for a in range(1, 8, 2):
        for s in range(1, 8, 2):
            pygame.draw.rect(screen, bright_color, (dx // 2 - dx // 15 * 4 + dx // 15 * s, dy //2 - dx // 15 * 4 + dx // 15 * a, dx // 15, dx // 15))

    pygame.draw.rect(screen, (0, 0, 0), (dx // 2 - dx // 15 * 4 - dx // 100, dy // 2 - dx // 15 * 4 - dx // 100, dx // 15 * 8 + dx //50, dx // 15 * 8 + dx // 50), dx // 100)

def draw_piece(image, row, column):
    x_pos = board_x_zero - image.get_width() // 2 + square_lenth // 2 + square_lenth * row
    y_pos = board_y_zero - image.get_height() // 2 + square_lenth // 2 + square_lenth * column
    screen.blit(image, (x_pos, y_pos))

def draw_pieces(piece_name, row, column):
    if piece_name == 'K':
        draw_piece(image_white_king, row, column)
    if piece_name == 'Q':
        draw_piece(image_white_queen, row, column)
    if piece_name == 'R':
        draw_piece(image_white_rook, row, column)
    if piece_name == 'B':
        draw_piece(image_white_bishop, row, column)
    if piece_name == 'N':
        draw_piece(image_knight_white, row, column)
    if piece_name == 'P':
        draw_piece(image_white_pawn, row, column)

    if piece_name == 'k':
        draw_piece(image_black_king, row, column)
    if piece_name == 'q':
        draw_piece(image_black_queen, row, column)
    if piece_name == 'r':
        draw_piece(image_black_rook, row, column)
    if piece_name == 'b':
        draw_piece(image_black_bishop, row, column)
    if piece_name == 'n':
        draw_piece(image_knight_black, row, column)
    if piece_name == 'p':
        draw_piece(image_black_pawn, row, column)

def board_to_matrix(fen):
    matrix = numpy.full((8,8), ' ')
    column = 0
    row = 0

    for a in fen:
        if row == 8:
            row = 0
            column += 1

        if a == 'k':
            matrix[column][row] = a
            row += 1
        if a == 'q':
            matrix[column][row] = a
            row += 1
        if a == 'r':
            matrix[column][row] = a
            row += 1
        if a == 'b':
            matrix[column][row] = a
            row += 1
        if a == 'n':
            matrix[column][row] = a
            row += 1
        if a == 'p':
            matrix[column][row] = a
            row += 1

        if a == 'K':
            matrix[column][row] = a
            row += 1
        if a == 'Q':
            matrix[column][row] = a
            row += 1
        if a == 'R':
            matrix[column][row] = a
            row += 1
        if a == 'B':
            matrix[column][row] = a
            row += 1
        if a == 'N':
            matrix[column][row] = a
            row += 1
        if a == 'P':
            matrix[column][row] = a
            row += 1
        try:
            space = int(a)
            row += space
        except:
            pass

        if a == ' ':
            break

    return matrix

def pieces_counter(fen):
    score = 0
    for a in fen:
        if a == 'Q':
            score += 9
        if a == 'R':
            score += 5
        if a == 'B':
            score += 3
        if a == 'N':
            score += 3
        if a == 'P':
            score += 1

        if a =='q':
            score -= 9
        if a == 'r':
            score -= 5
        if a == 'n':
            score -= 3
        if a == 'b':
            score -= 3
        if a == 'p':
            score -= 1

        if a == ' ':
            return score

def adress_finder(matrix, piece):
    column = len(matrix)
    row = len(matrix[0])

    adress_list = []

    for a in range(0, column):
        for s in range(0, row):
            if matrix[a][s] == piece:
                adress = [a, s]
                adress_list.append(adress)

    return adress_list

def black_king_safety(matrix):
    k_adress = adress_finder(matrix, 'k')
    k_column = k_adress[0][0]
    k_row = k_adress[0][1]
    shild_pawn = 0
    if k_column >= 3:
        return 'danger'

    if k_row == 0:
        if matrix[k_column + 1][k_row] == 'p':
            shild_pawn += 1

        if matrix[k_column + 1][k_row + 1] == 'p':
            shild_pawn += 1

    if 1<= k_row<= 6:
        if matrix[k_column + 1][k_row - 1] == 'p':
            shild_pawn += 1
        if matrix[k_column + 1][k_row] == 'p':
            shild_pawn += 1
        if matrix[k_column + 1][k_row + 1] == 'p':
            shild_pawn += 1

    if k_row == 7:
        if matrix[k_column + 1][k_row - 1] == 'p':
            shild_pawn += 1
        if matrix[k_column + 1][k_row] == 'p':
            shild_pawn += 1

    if shild_pawn <= 2:
        return 'danger'

def pos_to_notation(pos):
    pos_x, pos_y = pos
    file = chr(pos_x + 97)
    rank = str(8 - pos_y)
    half_notation = file + rank
    return half_notation

def notation_to_pos(notation):
    file = notation[0]  # 'a' ~ 'h'
    rank = notation[1]  # '1' ~ '8'

    pos_x = ord(file) - 97         # 'a' → 0, 'b' → 1, ..., 'h' → 7
    pos_y = 8 - int(rank)          # '8' → 0, '7' → 1, ..., '1' → 7
    return [pos_x, pos_y]

def creat_class(piece_name, row, column):
    global list_pieces
    if piece_name == 'K':
        white_king = piece(piece_name, image_white_king, row, column)
        list_pieces.insert(0, white_king)
    if piece_name == 'Q':
        white_queen = piece(piece_name, image_white_queen, row, column)
        list_pieces.insert(0, white_queen)
    if piece_name == 'R':
        white_rook = piece(piece_name, image_white_rook, row, column)
        list_pieces.insert(0, white_rook)
    if piece_name == 'B':
        white_bishop = piece(piece_name, image_white_bishop, row, column)
        list_pieces.insert(0, white_bishop)
    if piece_name == 'N':
        knight_white = piece(piece_name, image_knight_white, row, column)
        list_pieces.insert(0, knight_white)
    if piece_name == 'P':
        white_pawn = piece(piece_name, image_white_pawn, row, column)
        list_pieces.insert(0, white_pawn)

    if piece_name == 'k':
        black_king = piece(piece_name, image_black_king, row, column)
        list_pieces.insert(0, black_king)
    if piece_name == 'q':
        black_queen = piece(piece_name, image_black_queen, row, column)
        list_pieces.insert(0, black_queen)
    if piece_name == 'n':
        knight_black = piece(piece_name, image_knight_black, row, column)
        list_pieces.insert(0, knight_black)
    if piece_name == 'r':
        black_rook = piece(piece_name, image_black_rook, row, column)
        list_pieces.insert(0, black_rook)
    if piece_name == 'b':
        black_bishop = piece(piece_name, image_black_bishop, row, column)
        list_pieces.insert(0, black_bishop)
    if piece_name == 'p':
        black_pawn = piece(piece_name, image_black_pawn, row, column)
        list_pieces.insert(0, black_pawn)

def click_square():
    if board_x_zero < x < board_x_zero + square_lenth * 8 and board_y_zero < y < board_y_zero + square_lenth * 8:
        column = (y - board_y_zero) // square_lenth
        row = (x - board_x_zero) // square_lenth
        pygame.draw.rect(screen, (255, 0, 0), (
        board_x_zero + square_lenth * row, board_y_zero + square_lenth * column, square_lenth, square_lenth), 10)
        pos = [row, column]
        return pos

def creating_mate_fen(mate_number):
    global turn
    global solving_puzzle
    global list_select_square
    global list_pieces
    global board
    global matrix
    global select_square
    global fen

    if mate_number == 1:
        fen = random.choice(list_mate_1)
    elif mate_number == 2:
        fen = random.choice(list_mate_2)
    elif mate_number == 3:
        fen = random.choice(list_mate_3)
    elif mate_number == 4:
        fen = random.choice(list_mate_4)

    board = chess.Board(fen)
    matrix = board_to_matrix(board.fen())
    for column in range(8):
        for row in range(8):
            creat_class(matrix[column][row], row, column)

    list_select_square = [[8, 8], [8, 8]]
    turn = 'white'
    solving_puzzle = False

def white_move():
    global board
    global list_select_square
    global list_pieces
    global turn
    global select_square
    global matrix
    global promotion_onoff
    global promotion_notation
    global x
    global y

    select_square = click_square()
    if select_square == None:
        select_square = [8, 8]

    list_select_square.append(select_square)
    list_select_square.pop(0)

    if list_select_square[0] != list_select_square[1]:
        half_natation1 = pos_to_notation(list_select_square[0])
        half_natation2 = pos_to_notation(list_select_square[1])
        notation = half_natation1 + half_natation2

        for a in board.legal_moves:
            if len(str(a)) == 5:
                if str(a)[0:4] == notation:
                    promotion_onoff = True
                    promotion_notation = notation

        if promotion_onoff:
            if list_select_square[1] == [2, 2]:#프로모션 메뉴가 열였을때 퀸 그림을 누른다면
                notation = promotion_notation + 'q'
                promotion_onoff = False
                list_select_square[0] = notation_to_pos(notation[0:2])
                list_select_square[1] = notation_to_pos(notation[2:4])
                x = 0
                y = 0

            elif list_select_square[1] == [3, 2]:#프로모션 메뉴가 열였을때 퀸 그림을 누른다면
                notation = promotion_notation + 'r'
                promotion_onoff = False
                list_select_square[0] = notation_to_pos(notation[0:2])
                list_select_square[1] = notation_to_pos(notation[2:4])
                x = 0
                y = 0

            elif list_select_square[1] == [4, 2]:  # 프로모션 메뉴가 열였을때 퀸 그림을 누른다면
                notation = promotion_notation + 'n'
                promotion_onoff = False
                list_select_square[0] = notation_to_pos(notation[0:2])
                list_select_square[1] = notation_to_pos(notation[2:4])
                x = 0
                y = 0

            elif list_select_square[1] == [5, 2]:  # 프로모션 메뉴가 열였을때 퀸 그림을 누른다면
                notation = promotion_notation + 'b'
                promotion_onoff = False
                list_select_square[0] = notation_to_pos(notation[0:2])
                list_select_square[1] = notation_to_pos(notation[2:4])
                x = 0
                y = 0

        for a in board.legal_moves:
            if str(a) == notation:
                board.push(a)
                for s in list_pieces:
                    if s.row == list_select_square[0][0] and s.column == list_select_square[0][1]:
                        s.moving(list_select_square[1][0], list_select_square[1][1])
                        turn = 'black'
                        list_pieces = []
                        matrix = board_to_matrix(board.fen())
                        for column in range(8):
                            for row in range(8):
                                creat_class(matrix[column][row], row, column)

def reset_solving():
    global solving_puzzle
    global finish_text_timer_onoff
    global move_counter
    global puzzles_number
    global board
    global list_pieces

    solving_puzzle = True
    finish_text_timer_onoff = True
    move_counter = 0


    if board.result() == '1-0':
        if puzzles_number > 0:
            puzzles_number -= 1
    else:
        if puzzles_number > 0:
            puzzles_number += 1
        list_pieces = []

def game_over():
    global finish_text_timer_onoff
    global list_pieces
    global solving_puzzle
    global turn
    global now_frame
    global move_counter
    global puzzles_number
    global state
    global x
    global y

    if finish_text_timer_onoff:
        now_frame = frame
        finish_text_timer_onoff = False

    if board.result() == '1-0':
        for a in list_pieces:
            a.falling()

        if puzzles_number == 1:
            if now_frame + 10 > frame:
                pygame.draw.rect(screen, (255, 255, 255, 200), (0, 0, dx, dy))
            if now_frame + 120 > frame:
                texter("Sucess!!", dx // 6, (255, 100, 100), dx // 2, dy // 2)
        else:
            if now_frame + 10 > frame:
                pygame.draw.rect(screen, (255, 255, 255, 200), (0, 0, dx, dy))
            else:
                reset_solving()

    elif board.result() == '1/2-1/2':
        if board.is_stalemate():
            if now_frame + 60 > frame:
                texter("stale mate", dx//10, (100, 100, 100), dx // 2, dy // 2)
            else:
                reset_solving()


        elif board.is_repetition():
            if now_frame + 60 > frame:
                texter("repetition", dx//10, (100, 255, 100), dx // 2, dy // 2)
            else:
                reset_solving()


        elif board.is_insufficient_material():
            if now_frame + 60 > frame:
                texter("no mate", dx//10, (0, 0, 0), dx // 2, dy // 2)
            else:
                reset_solving()


    elif board.result() == '0-1':
        if now_frame + 60 > frame:
            texter("lose", dx//10, (100, 200, 200), dx // 2, dy // 2)

        else:
            reset_solving()

def black_move(depth):
    global list_pieces
    global turn
    global move_counter
    global matrix

    result = engine_stockfish.play(board, chess.engine.Limit(depth=depth))
    move_black = str(result.move)
    board.push(result.move)
    move_counter += 1
    turn = 'white'
    black_piece_pos1 = notation_to_pos(move_black[0:2])
    black_piece_pos2 = notation_to_pos(move_black[2:4])

    for s in list_pieces:
        if s.row == black_piece_pos1[0] and s.column == black_piece_pos1[1]:
            s.moving(black_piece_pos2[0], black_piece_pos2[1])
            list_pieces = []
            matrix = board_to_matrix(board.fen())
            for column in range(8):
                for row in range(8):
                    creat_class(matrix[column][row], row, column)

def puzzle_mate(move_number):
    global board
    global move_counter
    global failed
    global finish_text_timer_onoff
    global now_frame
    global solving_puzzle
    global list_pieces
    global promotion_onoff
    global puzzles_number
    global state
    global x
    global y

    chessboard()
    texter(state + text_puzzles_number, square_lenth // 2, (0, 0, 0), dx // 2, square_lenth // 4)
    chess_circle()
    for a in list_pieces:
        a.blit()
        if a.pos_y > dy:
            list_pieces.remove(a)

    if promotion_onoff:
        pos_x_menu_promotion = board_x_zero + square_lenth * 2 - square_lenth//2
        pos_y_menu_promotion = board_y_zero + square_lenth * 2 - square_lenth//2
        width_menu_promotion = square_lenth * 4 + square_lenth
        height_menu_promotion = square_lenth + square_lenth

        pygame.draw.rect(screen, (255, 255, 255), (pos_x_menu_promotion, pos_y_menu_promotion, width_menu_promotion, height_menu_promotion))
        pygame.draw.rect(screen, (0, 0, 0), (pos_x_menu_promotion, pos_y_menu_promotion, width_menu_promotion, height_menu_promotion), square_lenth//16)
        screen.blit(image_white_queen, (board_x_zero + square_lenth * 2, board_y_zero + square_lenth * 2))
        screen.blit(image_white_rook, (board_x_zero + square_lenth * 3, board_y_zero + square_lenth * 2))
        screen.blit(image_knight_white, (board_x_zero + square_lenth * 4, board_y_zero + square_lenth * 2))
        screen.blit(image_white_bishop, (board_x_zero + square_lenth * 5, board_y_zero + square_lenth * 2))

    if board.is_game_over():
        game_over()
        move_counter = 0

    else:
        if turn == 'white':
            white_move()
        elif turn == 'black':
            black_move(10)

    if move_counter == move_number:
        if finish_text_timer_onoff:
            now_frame = frame
            finish_text_timer_onoff = False

        if now_frame + 60 > frame:
            texter("failed", dx//10, (200, 0, 200), dx // 2, dy // 2)
            x = 0
            y = 0
        else:
            reset_solving()

def puzzle_ending():
    global board
    global move_counter
    global failed
    global finish_text_timer_onoff
    global now_frame
    global solving_puzzle
    global list_pieces
    global promotion_onoff
    global puzzles_number
    global state
    global x
    global y

    chessboard()
    texter(state + display_text_puzzles_number, square_lenth // 2, (0, 0, 0), dx // 2, square_lenth // 4)
    chess_circle()
    for a in list_pieces:
        a.blit()
        if a.pos_y > dy:
            list_pieces.remove(a)

    if promotion_onoff:
        pos_x_menu_promotion = board_x_zero + square_lenth * 2 - square_lenth//2
        pos_y_menu_promotion = board_y_zero + square_lenth * 2 - square_lenth//2
        width_menu_promotion = square_lenth * 4 + square_lenth
        height_menu_promotion = square_lenth + square_lenth

        pygame.draw.rect(screen, (255, 255, 255), (pos_x_menu_promotion, pos_y_menu_promotion, width_menu_promotion, height_menu_promotion))
        pygame.draw.rect(screen, (0, 0, 0), (pos_x_menu_promotion, pos_y_menu_promotion, width_menu_promotion, height_menu_promotion), square_lenth//16)
        screen.blit(image_white_queen, (board_x_zero + square_lenth * 2, board_y_zero + square_lenth * 2))
        screen.blit(image_white_rook, (board_x_zero + square_lenth * 3, board_y_zero + square_lenth * 2))
        screen.blit(image_knight_white, (board_x_zero + square_lenth * 4, board_y_zero + square_lenth * 2))
        screen.blit(image_white_bishop, (board_x_zero + square_lenth * 5, board_y_zero + square_lenth * 2))

    if board.is_game_over():
        game_over()
        move_counter = 0

    else:
        if turn == 'white':
            white_move()
        elif turn == 'black':
            black_move(10)

def is_white_piece_at_risk(board: chess.Board, list_move: list) -> bool:
    # 마지막 수를 되돌림 (블랙의 마지막 수)
    board.pop()

    # 화이트의 마지막 수 (예: 'e2e4')
    last_white_move = str(list_move[-1])
    to_square = chess.parse_square(last_white_move[2:4])  # 이동한 위치

    # 해당 위치에 화이트 기물이 있는지 확인
    piece = board.piece_at(to_square)
    if not piece or piece.color != chess.WHITE:
        return True  # 해당 위치에 화이트 기물이 없으면 위험 없음

    # 블랙의 legal_moves 중 해당 위치를 공격하는 수가 있는지 확인
    for move in board.legal_moves:
        if move.to_square == to_square:
            return False  # 잡힐 가능성 있음

    return True  # 잡힐 가능성 없음

def chess_circle():
    global puzzles_number

    pygame.draw.circle(screen, (255 ,255, 255), (dx//8 * 7, dy//8 * 7), dx//18)
    pygame.draw.circle(screen,(0, 0, 0), (dx//8 * 7, dy//8 * 7), dx//18, square_lenth//16)

    if puzzles_number <= 0:
        text_puzzles_number = '무한'
    else:
        text_puzzles_number = str(puzzles_number)

    texter(text_puzzles_number, dx//15, (0, 0, 0), dx//8 * 7, dy//8 * 7)

def score_to_cp(info_score):
    score = str(info_score)
    if 'Mate' in score:
        return -100000

    else:
        score = score.replace('PovScore(Cp(', '')
        if 'WHITE' in score:
            score = score.replace('), WHITE)', '')
        else:
            score = score.replace('), BLACK)', '')
        score = int(score)
        return score

#class------------------------------------------------------------------------------------------------------------------
#기물을 클래스로 하면 좋을텐데 딱히 그래야 하는 이유를 모르겠다
class piece:
    global list_pieces
    def __init__(self, name, image, row, column):
        self.name = name
        self.image = image
        self.row = row
        self.column = column
        self.half_notation = pos_to_notation((self.row, self.column))
        self.pos_x = board_x_zero - self.image.get_width() // 2 + square_lenth // 2 + square_lenth * self.row
        self.pos_y = board_y_zero - self.image.get_height() // 2 + square_lenth // 2 + square_lenth * self.column
        self.force_x = random.choice(range(-50, 50))/10
        self.force_y = random.choice(range(-100, -50))/10
        self.out = False
        self.speed = square_lenth//8
        self.fall = False

    def blit(self):
        if self.fall:
            self.force_y += 0.5
            self.pos_x += self.force_x
            self.pos_y += self.force_y

        if -self.image.get_height() < self.pos_y < dy + self.image.get_height():
            screen.blit(self.image, (self.pos_x, self.pos_y))

    def moving(self, to_row, to_column):
        move_pos_x = board_x_zero - self.image.get_width() // 2 + square_lenth // 2 + square_lenth * to_row
        move_pos_y = board_y_zero - self.image.get_height() // 2 + square_lenth // 2 + square_lenth * to_column

        while self.pos_x != move_pos_x or self.pos_y != move_pos_y:
            if self.pos_x < move_pos_x:
                self.pos_x += self.speed

            elif self.pos_x > move_pos_x:
                self.pos_x -= self.speed

            if self.pos_y < move_pos_y:
                self.pos_y += self.speed

            elif self.pos_y > move_pos_y:
                self.pos_y -= self.speed

            chessboard()
            chess_circle()
            for a in list_pieces:
                a.blit()
                if a.pos_y > dy:
                    list_pieces.remove(a)

            screen.blit(self.image, (self.pos_x, self.pos_y))
            pygame.display.update()

        self.row = to_row
        self.column = to_column


    def falling(self):
        self.fall = True
        self.row = 8
        self.column = 8

#loop code--------------------------------------------------------------------------------------------------------------
while True:
    frame += 1
    tick.tick(60)
    screen.fill((255, 255, 255))
    background()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # 마우스 버튼이 눌렸을 때의 처리
            if event.button == 1:  # 왼쪽 버튼
                (x, y) = pygame.mouse.get_pos()
    #lobby--------------------------------------------------------------------------------------------------------------
    if state == 'lobby':
        texter("무한 메이트", dx//10, (0, 0, 0), dx//2, dy//10 * 2)
        if buttoner("무한 메이트", dx // 15, (0, 0, 0), dx // 4 * 2, dy // 10 * 4) == 1:
            state = 'endless mate'
            x, y = (0, 0)
            puzzles_number = 10
        exiter()

    #endless mate--------------------------------------------------------------------------------------------------------
    if state == 'endless mate':
        texter("무한 메이트", dx // 10, (0, 0, 0), dx //2, dy // 10 * 2)
        if buttoner('1수 메이트', dx // 15, (0, 0, 0), dx // 4, dy// 10 * 4) == 1:
            state = 'mate in one'
            x, y = (0, 0)
            solving_puzzle = True
            list_pieces = []

        if buttoner('2수 메이트', dx // 15, (0, 0, 0), dx // 4, dy// 10 * 6) == 1:
            state = 'mate in two'
            x, y = (0, 0)
            solving_puzzle = True
            list_pieces = []

        if buttoner('3수 메이트', dx // 15, (0, 0, 0), dx // 4, dy// 10 * 8) == 1:
            state = 'mate in three'
            x, y = (0, 0)
            solving_puzzle = True
            list_pieces = []

        if buttoner('4수 메이트', dx // 15, (0, 0, 0), dx // 4 * 3, dy// 10 * 4) == 1:
            state = 'mate in four'
            x, y = (0, 0)
            solving_puzzle = True
            list_pieces = []

        if puzzles_number == -1:
            text_puzzles_number = '무한'
        else:
            text_puzzles_number = str(puzzles_number)

        pygame.draw.circle(screen, (255 ,255, 255), (dx//4 * 3, dy//10 * 6), dx // 15)
        pygame.draw.circle(screen, (0, 0, 0), (dx//4 * 3, dy//10 * 6), dx // 15, square_lenth // 16)

        texter(text_puzzles_number, dx//15, (0, 0, 0), dx//4 * 3, dy//10 * 6)

        if buttoner('무한', dx//30, (0, 0, 0), dx // 16 * 10, dy // 10 * 8) == 1:
            puzzles_number = -1
            display_text_puzzles_number = '무한'

        if buttoner('10', dx // 30, (0, 0, 0), dx // 16 * 11, dy // 10 * 8) == 1:
            puzzles_number = 10
            display_text_puzzles_number = '10'

        if buttoner('20', dx // 30, (0, 0, 0), dx // 16 * 12, dy // 10 * 8) == 1:
            puzzles_number = 20
            display_text_puzzles_number = '20'

        if buttoner('30', dx // 30, (0, 0, 0), dx // 16 * 13, dy // 10 * 8) == 1:
            puzzles_number = 30
            display_text_puzzles_number = '30'

        if buttoner('50', dx // 30, (0, 0, 0), dx // 16 * 14, dy // 10 * 8) == 1:
            puzzles_number = 50
            display_text_puzzles_number = '50'

        if buttoner('100', dx // 30, (0, 0, 0), dx // 16 * 15, dy // 10 * 8) == 1:
            puzzles_number = 100
            display_text_puzzles_number = '100'

        exiter()

    #mate---------------------------------------------------------------------------------------------------------------
    if state == 'mate in one':
        #퍼즐 불러오기
        if solving_puzzle:
            creating_mate_fen(1)
        else:
            puzzle_mate(1)
        exiter()
    if state == 'mate in two':
        # 퍼즐 불러오기
        if solving_puzzle:
            creating_mate_fen(2)
        else:
            puzzle_mate(2)
        exiter()
    if state == 'mate in three':
        # 퍼즐 불러오기
        if solving_puzzle:
            creating_mate_fen(3)
        else:
            puzzle_mate(3)
        exiter()
    if state == 'mate in four':
        # 퍼즐 불러오기
        if solving_puzzle:
            creating_mate_fen(4)
        else:
            puzzle_mate(4)
        exiter()

    #===================================================================================================================
    pygame.display.update()
    frame += 1
    #exit function------------------------------------------------------------------------------------------------------

