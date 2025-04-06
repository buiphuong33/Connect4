import numpy as np
import pygame
import sys
import random
from threading import Timer
from ai_1 import get_move as ai1_move
from ai_2 import get_move as ai2_move

# Global constants
ROWS = 6
COLS = 7
PLAYER_TURN = 0  # AI 1
AI_TURN = 1      # AI 2
PLAYER_PIECE = 1
AI_PIECE = 2
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Board creation and manipulation
def create_board():
    return np.zeros((ROWS, COLS))

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    return board[0][col] == 0

def get_next_open_row(board, col):
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == 0:
            return r

def winning_move(board, piece):
    for c in range(COLS-3):
        for r in range(ROWS):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True
    for c in range(COLS):
        for r in range(ROWS-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True
    for c in range(COLS-3):
        for r in range(3, ROWS):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True
    for c in range(3, COLS):
        for r in range(3, ROWS):
            if board[r][c] == piece and board[r-1][c-1] == piece and board[r-2][c-2] == piece and board[r-3][c-3] == piece:
                return True
    return False

def draw_board(board):
    for c in range(COLS):
        for r in range(ROWS):
            pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            if board[r][c] == 0:
                pygame.draw.circle(screen, BLACK, (int(c * SQUARESIZE + SQUARESIZE/2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE/2)), circle_radius)
            elif board[r][c] == 1:
                pygame.draw.circle(screen, RED, (int(c * SQUARESIZE + SQUARESIZE/2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE/2)), circle_radius)
            else:
                pygame.draw.circle(screen, YELLOW, (int(c * SQUARESIZE + SQUARESIZE/2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE/2)), circle_radius)
    pygame.display.update()

def end_game():
    global game_over
    game_over = True

# Game setup
board = create_board()
game_over = False
not_over = True
turn = 0    #ai 2  đi trước 

pygame.init()
SQUARESIZE = 100
width = COLS * SQUARESIZE
height = (ROWS + 1) * SQUARESIZE
circle_radius = int(SQUARESIZE/2 - 5)
size = (width, height)
screen = pygame.display.set_mode(size)
my_font = pygame.font.SysFont("monospace", 75)
draw_board(board)
pygame.display.update()

# Game loop
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    if not_over:
        if turn == PLAYER_TURN:  # AI 1's turn (Red)
            col = ai1_move(board, PLAYER_PIECE, winning_move)
            if col is None:  # Xử lý khi không có nước đi
                print("No valid moves left for AI 1! Game ends in a draw.")
                game_over = True
                break
            #col = int(col[0]) if isinstance(col, (list, np.ndarray)) else int(col)
            if is_valid_location(board, col):
                pygame.time.wait(500)
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, PLAYER_PIECE)
                if winning_move(board, PLAYER_PIECE):
                    print("AI 1 (Red) WINS!")
                    label = my_font.render("AI 1 WINS!", 1, RED)
                    screen.blit(label, (40, 10))
                    not_over = False
                    t = Timer(3.0, end_game)
                    t.start()
                draw_board(board)
                turn += 1
                turn = turn % 2

        elif turn == AI_TURN:  # AI 2's turn (Yellow)
            col = ai2_move(board, AI_PIECE, winning_move)
            if col is None:  
                print("No valid moves left for AI 1! Game ends in a draw.")
                game_over = True
                break
            #col = int(col[0]) if isinstance(col, (list, np.ndarray)) else int(col)
            if is_valid_location(board, col):
                pygame.time.wait(500)
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, AI_PIECE)
                if winning_move(board, AI_PIECE):
                    print("AI 2 (Yellow) WINS!")
                    label = my_font.render("AI 2 WINS!", 1, YELLOW)
                    screen.blit(label, (40, 10))
                    not_over = False
                    t = Timer(3.0, end_game)
                    t.start()
                draw_board(board)
                turn += 1
                turn = turn % 2

    pygame.display.update()

pygame.quit()