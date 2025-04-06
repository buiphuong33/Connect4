import numpy as np
import pygame
import sys
import math
from threading import Timer

# Hằng số cơ bản
ROWS = 6
COLS = 7
PLAYER_TURN = 0
AI_TURN = 1
PLAYER_PIECE = 1
AI_PIECE = 2
BLUE = (75, 158, 235)       # Nền bảng
WHITE = (255, 255, 255)    # Ô trống
RED = (220, 0, 0)          # Người chơi 1
YELLOW = (255, 204, 0)     # Người chơi 2
BLACK = (0, 0, 0)
SQUARESIZE = 85             # Tăng từ 80 lên 85 để khít hơn
circle_radius = int(SQUARESIZE / 2 - 5)  # Bán kính vòng tròn
BOARD_X_OFFSET = 0         
BOARD_Y_OFFSET = SQUARESIZE  # Dịch bảng xuống dưới màn đen

def create_board():
    return np.zeros((ROWS, COLS))

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    return board[0][col] == 0

def get_valid_locations(board):
    return [col for col in range(COLS) if is_valid_location(board, col)]

def get_next_open_row(board, col):
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == 0:
            return r

def winning_move(board, piece):        
    for r in range(ROWS):
        for c in range(COLS - 3):
            if all(board[r][c+i] == piece for i in range(4)):
                return True
    for c in range(COLS):
        for r in range(ROWS - 3):
            if all(board[r + i][c] == piece for i in range(4)):
                return True
    for c in range(COLS - 3):
        for r in range(3, ROWS):
            if all(board[r - i][c + i] == piece for i in range(4)):
                return True
    for c in range(3, COLS):
        for r in range(3, ROWS):
            if all(board[r - i][c - i] == piece for i in range(4)):
                return True
    return False

def draw_board(screen, board):
    for c in range(COLS):
        for r in range(ROWS):
            pygame.draw.rect(screen, (74, 171, 241), (c * SQUARESIZE + BOARD_X_OFFSET, r * SQUARESIZE + BOARD_Y_OFFSET, SQUARESIZE, SQUARESIZE))
            if board[r][c] == 0:
                pygame.draw.circle(screen, WHITE, (int(c * SQUARESIZE + SQUARESIZE / 2 + BOARD_X_OFFSET), int(r * SQUARESIZE + SQUARESIZE / 2 + BOARD_Y_OFFSET)), circle_radius)
            elif board[r][c] == 1:
                pygame.draw.circle(screen, RED, (int(c * SQUARESIZE + SQUARESIZE / 2 + BOARD_X_OFFSET), int(r * SQUARESIZE + SQUARESIZE / 2 + BOARD_Y_OFFSET)), circle_radius)
            else:
                pygame.draw.circle(screen, YELLOW, (int(c * SQUARESIZE + SQUARESIZE / 2 + BOARD_X_OFFSET), int(r * SQUARESIZE + SQUARESIZE / 2 + BOARD_Y_OFFSET)), circle_radius)

def end_game():
    global game_over
    game_over = True

if __name__ == "__main__":
    print("connect4_utils.py loaded successfully")