import math
import random
from connect4_utils import *

def evaluate_window(window, piece):
    opponent_piece = PLAYER_PIECE if piece == AI_PIECE else AI_PIECE
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
    center_array = [int(i) for i in list(board[:, COLS // 2])]
    score += center_array.count(piece) * 6
    for r in range(ROWS):
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(COLS - 3):
            window = row_array[c:c + 4]
            score += evaluate_window(window, piece)
    for c in range(COLS):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(ROWS - 3):
            window = col_array[r:r + 4]
            score += evaluate_window(window, piece)
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            window = [board[r - i][c + i] for i in range(4)]
            score += evaluate_window(window, piece)
    for r in range(3, ROWS):
        for c in range(3, COLS):
            window = [board[r - i][c - i] for i in range(4)]
            score += evaluate_window(window, piece)
    return score

def is_terminal_node(board):
    return winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE) or len(get_valid_locations(board)) == 0

def minimax(board, depth, alpha, beta, maximizing_player):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, AI_PIECE):
                return (None, 10000000)
            elif winning_move(board, PLAYER_PIECE):
                return (None, -10000000)
            else:
                return (None, 0)
        else:
            return (None, score_position(board, AI_PIECE))
    if maximizing_player:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, AI_PIECE)
            new_score = minimax(b_copy, depth - 1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(value, alpha)
            if alpha >= beta:
                break
        return column, value
    else:
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, PLAYER_PIECE)
            new_score = minimax(b_copy, depth - 1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(value, beta)
            if alpha >= beta:
                break
        return column, value
    
def get_valid_locations(board):
    return [col for col in range(COLS) if is_valid_location(board, col)]

def play_ai_game(screen, event, board, turn, not_over, my_font):
    winner = None
    if turn == PLAYER_TURN:
        if event.type == pygame.MOUSEBUTTONDOWN and not_over:
            xpos = event.pos[0]
            col = int(math.floor((xpos - BOARD_X_OFFSET) / SQUARESIZE))
            if 0 <= col < COLS and is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, PLAYER_PIECE)
                if winning_move(board, PLAYER_PIECE):
                    winner = "Player WIN!"
                    not_over = False
                elif len(get_valid_locations(board)) == 0:
                    winner = "It's a tie!"
                    not_over = False
                turn = (turn + 1) % 2
    elif turn == AI_TURN and not_over:
        col, _ = minimax(board, 5, -math.inf, math.inf, True)
        if 0 <= col < COLS and is_valid_location(board, col):
            pygame.time.wait(500)
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, AI_PIECE)
            if winning_move(board, AI_PIECE):
                winner = "FFF_AI WIN!"
                not_over = False
            elif len(get_valid_locations(board)) == 0:
                winner = "It's a tie!"
                not_over = False
            turn = (turn + 1) % 2
    return turn, not_over, winner