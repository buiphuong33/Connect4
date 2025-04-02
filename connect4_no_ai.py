import pygame
import math
from connect4_utils import *


def play_no_ai_game(screen, event, board, turn, not_over, my_font):
    if event.type == pygame.MOUSEMOTION and not_over:
        pygame.draw.rect(screen, BLACK, (0, 0, COLS * SQUARESIZE, SQUARESIZE))
        xpos = pygame.mouse.get_pos()[0]
        color = RED if turn == 0 else YELLOW
        pygame.draw.circle(screen, color, (xpos, int(SQUARESIZE / 2)), circle_radius)
    if event.type == pygame.MOUSEBUTTONDOWN and not_over:
        pygame.draw.rect(screen, BLACK, (0, 0, COLS * SQUARESIZE, SQUARESIZE))
        xpos = event.pos[0]
        col = int(math.floor(xpos / SQUARESIZE))
        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            piece = 1 if turn == 0 else 2
            drop_piece(board, row, col, piece)
            if winning_move(board, piece):
                label = my_font.render(f"PLAYER {piece} WINS!", 1, RED if piece == 1 else YELLOW)
                screen.blit(label, (40, 10))
                not_over = False
                Timer(3.0, end_game).start()
            draw_board(screen, board)
            turn = (turn + 1) % 2
    return turn, not_over
