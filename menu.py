import pygame
import random
from connect4_utils import *
from connect4_utils import BOARD_X_OFFSET, BOARD_Y_OFFSET, COLS, SQUARESIZE, circle_radius, PLAYER_TURN, AI_TURN
from connect4_ai import play_ai_game
from connect4_no_ai import play_no_ai_game

pygame.init()

WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Connect 4")

try:
    background = pygame.image.load("images/connect4_theme.png")
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
except pygame.error as e:
    print(f"Could not download background: {e}")
    background = pygame.Surface((WIDTH, HEIGHT))
    background.fill((0, 0, 0))

BLUE = (75, 158, 235)       # Nền bảng
WHITE = (255, 255, 255)    # Ô trống
RED = (220, 0, 0)          # Người chơi 1
YELLOW = (255, 204, 0)     # Người chơi 2 / AI
HOVER_COLOR = (238, 201, 0)

font = pygame.font.Font(None, 35)
my_font = pygame.font.SysFont("monospace", 40)  # Giảm kích thước font để tránh bị cắt
info_font = pygame.font.Font(None, 50)

def draw_button(text, x, y, w, h, color, hover_color):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    hovered = x < mouse[0] < x + w and y < mouse[1] < y + h
    pygame.draw.rect(screen, hover_color if hovered else color, (x, y, w, h), border_radius=20)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=(x + w // 2, y + h // 2))
    screen.blit(text_surface, text_rect)
    return hovered and click[0]

def draw_game_info(turn, ai_mode, winner=None):
    info_x = 595
    info_y = 0 
    info_width = 405
    info_height = HEIGHT

    corner_radius = 15
    border_thickness = 3
    BORDER_COLOR = (34, 44, 54)

    pygame.draw.rect(screen, BORDER_COLOR,
                     (info_x, info_y, info_width, info_height),
                     border_radius=corner_radius)

    pygame.draw.rect(screen, WHITE,
                     (info_x + border_thickness, info_y + border_thickness,
                      info_width - 2 * border_thickness, info_height - 2 * border_thickness),
                     border_radius=corner_radius)

    if not winner:
        if ai_mode:
            turn_text = "Player's turn" if turn == PLAYER_TURN else "FFF_AI's turn"
            turn_color = RED if turn == PLAYER_TURN else YELLOW
        else:
            turn_text = f"Player {1 if turn == 0 else 2}'s turn"
            turn_color = RED if turn == 0 else YELLOW
        turn_surface = info_font.render(turn_text, True, turn_color)
        screen.blit(turn_surface, (info_x + 80, info_y + 150))
    else:
        # Xác định màu dựa trên người thắng
        if "Player 1" in winner:
            winner_color = RED
        elif "Player 2" in winner or "FFF_AI" in winner:
            winner_color = YELLOW
        else:  # Draw
            winner_color = BLACK
        winner_surface = my_font.render(winner, True, winner_color)
        # Căn giữa văn bản trong khu vực info
        winner_rect = winner_surface.get_rect(center=(info_x + info_width / 2, info_y + 150))
        screen.blit(winner_surface, winner_rect)

def draw_preview_circle(turn, not_over, ai_mode):
    pygame.draw.rect(screen, BLACK, (BOARD_X_OFFSET, 0, COLS * SQUARESIZE, SQUARESIZE))
    if not_over and (not ai_mode or (ai_mode and turn == PLAYER_TURN)):
        xpos = pygame.mouse.get_pos()[0]
        xpos = max(BOARD_X_OFFSET + circle_radius, min(xpos, BOARD_X_OFFSET + COLS * SQUARESIZE - circle_radius))
        color = RED if turn == 0 else YELLOW
        pygame.draw.circle(screen, color, (xpos, int(SQUARESIZE / 2)), circle_radius)

def main():
    global game_over, winner
    game_over = False
    state = "menu"
    board = None
    turn = 0
    not_over = True
    ai_mode = False
    winner = None
    end_time = None

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if state == "menu":
                if draw_button("Play vs AI", 535, 410, 250, 50, YELLOW, HOVER_COLOR):
                    state = "game"
                    ai_mode = True
                    board = create_board()
                    game_over = False
                    not_over = True
                    winner = None
                    turn = 0
                elif draw_button("Play vs Player", 535, 340, 250, 50, YELLOW, HOVER_COLOR):
                    state = "game"
                    ai_mode = False
                    board = create_board()
                    game_over = False
                    not_over = True
                    winner = None
                    turn = 0
                elif draw_button("Compete", 535, 480, 250, 50, YELLOW, HOVER_COLOR):
                    pass

            elif state == "game" and board is not None:
                if draw_button("New Game", 720, 400, 150, 50, (68, 184, 154), HOVER_COLOR):
                    board = create_board()
                    game_over = False
                    not_over = True
                    winner = None
                    end_time = None
                    turn = random.randint(PLAYER_TURN, AI_TURN) if ai_mode else 0
                if draw_button("Exit", 720, 470, 150, 50, (15, 171, 103), HOVER_COLOR):
                    state = "menu"
                    board = None
                    game_over = False
                    not_over = True
                    winner = None
                    end_time = None

                if not game_over and not_over:
                    if ai_mode:
                        turn, not_over, winner = play_ai_game(screen, event, board, turn, not_over, my_font)
                    else:
                        turn, not_over, winner = play_no_ai_game(screen, event, board, turn, not_over, my_font)
                    if not not_over and end_time is None:
                        end_time = pygame.time.get_ticks()

        if state == "game" and not not_over and end_time is not None:
            current_time = pygame.time.get_ticks()
            if current_time - end_time >= 2000:
                state = "menu"
                board = None
                game_over = False
                not_over = True
                winner = None
                end_time = None

        screen.blit(background, (0, 0))
        if state == "menu":
            draw_button("Play vs Player", 535, 340, 250, 50, YELLOW, HOVER_COLOR)
            draw_button("Play vs AI", 535, 410, 250, 50, YELLOW, HOVER_COLOR)
            draw_button("Compete", 535, 480, 250, 50, YELLOW, HOVER_COLOR)
        elif state == "game" and board is not None:
            draw_board(screen, board)
            draw_preview_circle(turn, not_over, ai_mode)
            draw_game_info(turn, ai_mode, winner)
            draw_button("New Game", 720, 400, 150, 50, (68, 184, 154), HOVER_COLOR)
            draw_button("Exit", 720, 470, 150, 50, (15, 171, 103), HOVER_COLOR)

        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    main()
    pygame.quit()