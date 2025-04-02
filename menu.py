import pygame
import random
from connect4_utils import *
from connect4_ai import play_ai_game
from connect4_no_ai import play_no_ai_game

pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 700, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Connect 4")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BG_COLOR = (218, 244, 255)
BUTTON_COLOR = (81, 167, 191)
HOVER_COLOR = (30, 130, 230)

# Fonts
font = pygame.font.Font(None, 40)
my_font = pygame.font.SysFont("monospace", 75)

# Button drawing function
def draw_button(text, x, y, w, h, color, hover_color):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    hovered = x < mouse[0] < x + w and y < mouse[1] < y + h
    pygame.draw.rect(screen, hover_color if hovered else color, (x, y, w, h), border_radius=20)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=(x + w // 2, y + h // 2))
    screen.blit(text_surface, text_rect)
    return hovered and click[0]

# Main game loop
def main():
    global game_over
    state = "menu"
    board = None
    turn = 0
    game_over = False
    not_over = True
    ai_mode = False

    while True:
        
        # Xử lý sự kiện
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if state == "menu":
                if draw_button("Play vs AI", 225, 300, 250, 60, BUTTON_COLOR, HOVER_COLOR):
                    state = "game"
                    ai_mode = True
                    board = create_board()
                    game_over = False
                    not_over = True
                    turn = random.randint(PLAYER_TURN, AI_TURN)
                    screen.fill(BLACK)  
                    draw_board(screen, board)
                elif draw_button("Play vs Player", 225, 200, 250, 60, BUTTON_COLOR, HOVER_COLOR):
                    state = "game"
                    ai_mode = False
                    board = create_board()
                    game_over = False
                    not_over = True
                    turn = 0
                    screen.fill(BLACK)  
                    draw_board(screen, board) 
            elif state == "game" and not game_over:
                if ai_mode:
                    turn, not_over = play_ai_game(screen, event, board, turn, not_over, my_font)
                else:
                    turn, not_over = play_no_ai_game(screen, event, board, turn, not_over, my_font)
                if game_over:
                    state = "menu"

        # Vẽ giao diện dựa trên trạng thái
        if state == "menu":
            screen.fill(BG_COLOR)
            title_text = font.render("Choose Game Mode", True, BLACK)
            screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 80))
            draw_button("Play vs Player", 225, 200, 250, 60, BUTTON_COLOR, HOVER_COLOR)
            draw_button("Play vs AI", 225, 300, 250, 60, BUTTON_COLOR, HOVER_COLOR)

        pygame.display.update()

if __name__ == "__main__":
    main()
    pygame.quit()