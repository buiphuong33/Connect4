import numpy as np
import pygame
import sys
import math
from threading import Timer

ROWS = 6
COLS = 7
PLAYER_TURN = 0
AI_TURN = 1
PLAYER_PIECE = 1
AI_PIECE = 2
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
SQUARESIZE = 100
circle_radius = int(SQUARESIZE / 2 - 5)

def create_board():
    return np.zeros((ROWS, COLS))

def drop_piece(board, row, col, piece):
    board[row][col] = piece

#kiểm tra xem cột đó đã đầy hay chưa
def is_valid_location(board, col):
    return board[0][col] == 0

# tìm hàng trống thấp nhất trong cột
def get_next_open_row(board, col):
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == 0:
            return r
        
# hàm kiểm tra xem piece có tạo thành 4 quân liên tiếp không
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
            pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            if board[r][c] == 0:
                pygame.draw.circle(screen, BLACK, (int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), circle_radius)
            elif board[r][c] == 1:
                pygame.draw.circle(screen, RED, (int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), circle_radius)
            else:
                pygame.draw.circle(screen, YELLOW, (int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), circle_radius)
    pygame.display.update()

def end_game():
    global game_over
    game_over = True