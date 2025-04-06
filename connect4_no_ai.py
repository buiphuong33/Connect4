import pygame
import math
from connect4_utils import *

def play_no_ai_game(screen, event, board, turn, not_over, my_font):
    winner = None
    if event.type == pygame.MOUSEBUTTONDOWN and not_over:
        xpos = event.pos[0]
        col = int(math.floor((xpos - BOARD_X_OFFSET) / SQUARESIZE))
        if 0 <= col < COLS and is_valid_location(board, col):
            row = get_next_open_row(board, col)
            piece = 1 if turn == 0 else 2
            drop_piece(board, row, col, piece)
            if winning_move(board, piece):
                winner = "Player 1 WIN!" if turn == 0 else "Player 2 WIN!"
                not_over = False
            elif len(get_valid_locations(board)) == 0:
                winner = "Draw!"
                not_over = False
            turn = (turn + 1) % 2
    return turn, not_over, winner