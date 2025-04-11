import numpy as np
import math
import random
import time

# Bảng băm để lưu trữ trạng thái
transposition_table = {}

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
        score -= 10 
    elif window.count(opponent_piece) == 4:
        score -= 10000000000 
    return score

def score_position(board, piece):
    score = 0
    center_array = [int(i) for i in list(board[:, board.shape[1]//2])]
    center_count = center_array.count(piece)
    score += center_count * 3 
    for r in range(board.shape[0]):
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(board.shape[1] - 3):
            window = row_array[c:c + 4]
            score += evaluate_window(window, piece)
    for c in range(board.shape[1]):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(board.shape[0]-3):
            window = col_array[r:r+4]
            score += evaluate_window(window, piece)
    for r in range(3, board.shape[0]):
        for c in range(board.shape[1] - 3):
            window = [board[r-i][c+i] for i in range(4)]
            score += evaluate_window(window, piece)
    for r in range(3, board.shape[0]):
        for c in range(3, board.shape[1]):
            window = [board[r-i][c-i] for i in range(4)]
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
def advanced_move_order(valid_locations, board, piece, winning_move):
    opponent_piece = 2 if piece == 1 else 1
    move_scores = []
    for col in valid_locations:
        row = get_next_open_row(board, col)
        b_copy = board.copy()
        b_copy[row][col] = piece
        if winning_move(b_copy, piece):  # Thắng ngay
            return [col]
        b_copy[row][col] = opponent_piece
        if winning_move(b_copy, opponent_piece):  # Chặn đối thủ thắng
            return [col]
        score = score_position(b_copy, piece)  # Đánh giá heuristic
        move_scores.append((col, score))
    move_scores.sort(key=lambda x: x[1], reverse=True)  # Sắp xếp theo điểm
    return [col for col, _ in move_scores]

def simple_move_order(valid_locations, board_width):
    center = board_width // 2
    return sorted(valid_locations, key=lambda x: abs(x - center))

def minimax(board, depth, alpha, beta, maximizing_player, piece, winning_move):
    board_hash = hash(str(board.tobytes()))
    if board_hash in transposition_table and transposition_table[board_hash][0] >= depth:
        return transposition_table[board_hash][1]

    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board, winning_move)
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, piece):
                return (None, 10000000)
            elif winning_move(board, 2 if piece == 1 else 1):
                return (None, -10000000)
            else:
                return (None, 0)
        else:
            return (None, score_position(board, piece))

    ordered_moves = advanced_move_order(valid_locations, board, piece, winning_move)

    if maximizing_player:
        value = -math.inf
        column = ordered_moves[0]
        for col in ordered_moves:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            b_copy[row][col] = piece
            new_score = minimax(b_copy, depth-1, alpha, beta, False, piece, winning_move)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(value, alpha)
            if alpha >= beta:
                break
        result = (column, value)
        transposition_table[board_hash] = (depth, result)
        return result
    else:
        value = math.inf
        column = ordered_moves[0]
        opponent_piece = 2 if piece == 1 else 1
        for col in ordered_moves:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            b_copy[row][col] = opponent_piece
            new_score = minimax(b_copy, depth-1, alpha, beta, True, piece, winning_move)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(value, beta)
            if alpha >= beta:
                break
        result = (column, value)
        transposition_table[board_hash] = (depth, result)
        return result

def get_move(board, piece, winning_move):
    # Count the number of pieces on the board
    pieces_on_board = np.count_nonzero(board)
    
    # Define depth based on game progress
    base_depth = 6
    max_depth = 12   # Cap the maximum depth to avoid excessive computation
    depth_increase = pieces_on_board // 7   # Increase depth by 1 for every 10 pieces
    depth = min(base_depth + depth_increase, max_depth)
    
    # Run minimax with the calculated depth
    col, _ = minimax(board, depth, -math.inf, math.inf, True, piece, winning_move)
    return col