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
        score += 10 
    elif window.count(piece) == 2 and window.count(0) == 2:
        score += 5
    if window.count(opponent_piece) == 3 and window.count(0) == 1:
        score -= 20 
    elif window.count(opponent_piece) == 4:
        score -= 100000 
    return score

def score_position(board, piece):
    score = 0
    center_array = [int(i) for i in list(board[:, board.shape[1]//2])]
    center_count = center_array.count(piece)
    score += center_count * 5 
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
# def advanced_move_order(valid_locations, board, piece, winning_move):
#     opponent_piece = 2 if piece == 1 else 1
#     move_scores = []
#     for col in valid_locations:
#         row = get_next_open_row(board, col)
#         b_copy = board.copy()
#         b_copy[row][col] = piece
#         if winning_move(b_copy, piece):  # Thắng ngay
#             return [col]
#         b_copy[row][col] = opponent_piece
#         if winning_move(b_copy, opponent_piece):  # Chặn đối thủ thắng
#             return [col]
#         score = score_position(b_copy, piece)  # Đánh giá heuristic
#         move_scores.append((col, score))
#     move_scores.sort(key=lambda x: x[1], reverse=True)  # Sắp xếp theo điểm
#     return [col for col, _ in move_scores]

def advanced_move_order(valid_locations, board, piece, winning_move):
    opponent_piece = 2 if piece == 1 else 1
    move_scores = []
    center_column = 3  # Cột giữa (giả sử bàn cờ 7 cột, chỉ số từ 0 đến 6)
    center_bias = 5   # Hệ số ưu tiên cho cột giữa, có thể điều chỉnh

    for col in valid_locations:
        row = get_next_open_row(board, col)
        b_copy = board.copy()
        
        # Kiểm tra nước đi thắng ngay
        b_copy[row][col] = piece
        if winning_move(b_copy, piece):
            return [col]
        
        # Kiểm tra chặn đối thủ thắng
        b_copy[row][col] = opponent_piece
        if winning_move(b_copy, opponent_piece):
            return [col]
        
        # Đánh giá heuristic
        b_copy[row][col] = piece  # Đặt lại để đánh giá cho piece của mình
        score = score_position(b_copy, piece)
        
        # Thêm hệ số ưu tiên cho cột giữa
        if col == center_column:
            score += center_bias
        # Có thể thêm ưu tiên giảm dần cho các cột gần giữa
        elif col in [center_column - 1, center_column + 1]:
            score += center_bias // 2  # Ưu tiên thấp hơn cho cột sát giữa

        move_scores.append((col, score))
    
    # Sắp xếp theo điểm số, ưu tiên cột có score cao hơn
    move_scores.sort(key=lambda x: x[1], reverse=True)
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
    pieces_on_board = np.count_nonzero(board)
    base_depth = 7 
    depth_increase = pieces_on_board // 10 
    depth = base_depth + depth_increase*2 
    col, _ = minimax(board, depth, -math.inf, math.inf, True, piece, winning_move)
    return col