import numpy as np
import math
import random
import time

ROW_COUNT = 6
COLUMN_COUNT = 7
PLAYER = 0
AI = 1
PLAYER_PIECE = 1
AI_PIECE = 2
WINDOW_LENGTH = 4
EMPTY = 0
MAX_DEPTH = 6
# Bảng băm để lưu trữ trạng thái
transposition_table = {}

def drop_piece(board, row, col, piece):
    board[row][col] = piece
    
def winning_move(board, piece):
    # Kiểm tra ngang
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if all(board[r][c+i] == piece for i in range(4)):
                return True

    # Kiểm tra dọc
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if all(board[r+i][c] == piece for i in range(4)):
                return True

    # Kiểm tra chéo /
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if all(board[r+i][c+i] == piece for i in range(4)):
                return True

    # Kiểm tra chéo \
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if all(board[r-i][c+i] == piece for i in range(4)):
                return True

    return False

def evaluate_window(window, piece):
    opponent_piece = 2 if piece == 1 else 1
    score = 0
    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(0) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(0) == 2:
        score += 2
    if window.count(opponent_piece) == 3 and window.count(0) == 1:
        score -= 4 
    return score

def score_position(board, piece):
    score = 0
    center_array = [int(i) for i in list(board[:, COLUMN_COUNT // 2])]
    center_count = center_array.count(piece)
    score += center_count * 3

    # Kiểm tra hàng ngang
    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(COLUMN_COUNT - 3):
            window = row_array[c:c+WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    # Kiểm tra dọc
    for c in range(COLUMN_COUNT):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(ROW_COUNT - 3):
            window = col_array[r:r+WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    # Kiểm tra chéo /
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    # Kiểm tra chéo \
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    return score

def is_terminal_node(board, winning_move):
    return winning_move(board, 1) or winning_move(board, 2) or len(get_valid_locations(board)) == 0

def get_valid_locations(board):
    return [col for col in range(board.shape[1]) if board[0][col] == 0]

def get_next_open_row(board, col):
    for r in range(board.shape[0]-1, -1, -1):
        if board[r][col] == 0:
            return r

# Heuristic đơn giản để ưu tiên cột giữa
def simple_move_order(valid_locations, board_width):
    center = board_width // 2
    return sorted(valid_locations, key=lambda x: abs(x - center))

def minimax(board, depth, alpha, beta, maximizingPlayer):
    valid_locations = get_valid_locations(board)
    terminal = is_terminal_node(board)

    if depth == 0 or terminal:
        if terminal:
            if winning_move(board, AI_PIECE):
                return (None, 1000000000000)
            elif winning_move(board, PLAYER_PIECE):
                return (None, -1000000000000)
            else:
                return (None, 0)
        else:
            return (None, score_position(board, AI_PIECE))

    if maximizingPlayer:
        value = -math.inf
        best_col = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            temp_board = board.copy()
            drop_piece(temp_board, row, col, AI_PIECE)
            new_score = minimax(temp_board, depth-1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                best_col = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return best_col, value

    else:  # Minimizing player
        value = math.inf
        best_col = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            temp_board = board.copy()
            drop_piece(temp_board, row, col, PLAYER_PIECE)
            new_score = minimax(temp_board, depth-1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                best_col = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return best_col, value
# Iterative Deepening với giới hạn thời gian
def get_move(board, piece, winning_move):
    col, _ = minimax(board, 9 , -math.inf, math.inf, True, piece, winning_move)
    return col 