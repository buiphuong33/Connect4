import pygame
import numpy as np
import sys
import math
from ai_2  import get_move, get_valid_locations, get_next_open_row, is_terminal_node

ROW_COUNT = 6
COLUMN_COUNT = 7
SQUARESIZE = 100
RADIUS = int(SQUARESIZE/2 - 5)
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE
size = (width, height)

BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

pygame.init()
screen = pygame.display.set_mode(size)
myfont = pygame.font.SysFont("monospace", 60)

def create_board():
    return np.zeros((ROW_COUNT, COLUMN_COUNT), dtype=int)

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, (r+1)*SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int((r+1)*SQUARESIZE+SQUARESIZE/2)), RADIUS)

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), int((r+1)*SQUARESIZE+SQUARESIZE/2)), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), int((r+1)*SQUARESIZE+SQUARESIZE/2)), RADIUS)

    pygame.display.update()

def winning_move(board, piece):
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if all([board[r][c+i] == piece for i in range(4)]):
                return True
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if all([board[r+i][c] == piece for i in range(4)]):
                return True
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if all([board[r+i][c+i] == piece for i in range(4)]):
                return True
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if all([board[r-i][c+i] == piece for i in range(4)]):
                return True
    return False

board = create_board()
game_over = False
turn = 1   # 0: người, 1: AI

draw_board(board)

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if turn == 0:
            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                posx = event.pos[0]
                pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
                pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                posx = event.pos[0]
                col = int(math.floor(posx / SQUARESIZE))

                if col in get_valid_locations(board):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 1)

                    if winning_move(board, 1):
                        label = myfont.render("Bạn thắng!", 1, RED)
                        screen.blit(label, (40, 10))
                        game_over = True

                    turn = 1
                    draw_board(board)

        elif turn == 1 and not game_over:
            pygame.time.wait(500)
            col = get_move(board, 2, winning_move)
            if col is not None and col in get_valid_locations(board):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, 2)

                if winning_move(board, 2):
                    label = myfont.render("AI thắng!", 1, YELLOW)
                    screen.blit(label, (40, 10))
                    game_over = True

                draw_board(board)
                turn = 0

    if game_over:
        pygame.time.wait(3000)
