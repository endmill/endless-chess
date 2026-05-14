import time
import chess
import chess.engine
import random
import re
import numpy

mate1 = open('mate1.txt', 'a')
mate2 = open('mate2.txt', 'a')
mate3 = open('mate3.txt', 'a')
mate4 = open('mate4.txt', 'a')

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

engine_stockfish = chess.engine.SimpleEngine.popen_uci(r"file\stockfish_15.1_x64_bmi2.exe")


def mate_creator():
    board = chess.Board()
    number_mate4 = 0
    number_mate3 = 0
    number_mate2 = 0
    number_mate1 = 0

    while True:
        if board.is_game_over():
            board = chess.Board()
            continue

        depth = random.choice(range(5, 11))
        info = engine_stockfish.analyse(board, chess.engine.Limit(depth=depth))
        score = str(info['score'])

        pieces_score = pieces_counter(board.fen())
        if pieces_score >= 3:
            board = chess.Board()
            continue

        if 'Mate' in score and '+' in score:
            score = int(re.sub(r"\D", "", score))
            if score == 4:
                mate4.write(board.fen())
                mate4.write('\n')
                mate4.flush()
                print("4수메이트 생성, ", board.fen())
                number_mate4 += 1
                print('현재 생성한 4수 메이트 문제 개수 : {}'.format(number_mate4))

            if score == 3:
                mate3.write(board.fen())
                mate3.write('\n')
                mate3.flush()
                print("3수메이트 생성, ", board.fen())
                number_mate3 += 1
                print('현재 생성한 3수 메이트 문제 개수 : {}'.format(number_mate3))

            if score == 2:
                mate2.write(board.fen())
                mate2.write('\n')
                mate2.flush()
                print("2수메이트 생성, ", board.fen())
                number_mate2 += 1
                print('현재 생성한 2수 메이트 문제 개수 : {}'.format(number_mate2))

            if score == 1:
                mate1.write(board.fen())
                mate1.write('\n')
                mate1.flush()
                print("1수메이트 생성, ", board.fen())
                number_mate1 += 1
                print('현재 생성한 1수 메이트 문제 개수 : {}'.format(number_mate1))

        # 가장 점수 높은 수를 출력하고 반영
        best_move = info["pv"][0]  # pv는 엔진이 추천한 최선 수의 수순 리스트
        board.push(best_move)

        if board.is_game_over():
            board = chess.Board()
            continue

        info = engine_stockfish.analyse(board, chess.engine.Limit(depth=1))

        worst_move = info['pv'][0]
        board.push(worst_move)

mate_creator()
engine_stockfish.quit()