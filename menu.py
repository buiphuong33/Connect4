import pygame
import subprocess

# Khởi tạo pygame
pygame.init()

# Kích thước màn hình
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Connect 4 - Menu")

# Màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
YELLOW = (200, 200, 0)
BG_COLOR = (218, 244, 255)
BUTTON_COLOR = (81, 167, 191)
HOVER_COLOR = (30, 130, 230)


# Font chữ
font = pygame.font.Font(None, 40)

# Hàm vẽ nút
def draw_button(text, x, y, w, h, color, hover_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x < mouse[0] < x + w and y < mouse[1] < y + h:
        pygame.draw.rect(screen, hover_color, (x, y, w, h), border_radius=20)
        if click[0] and action:
            pygame.time.delay(200)  # Tránh nhấn 2 lần do sự kiện lặp lại
            action()
    else:
        pygame.draw.rect(screen, color, (x, y, w, h), border_radius=20)

    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=(x + w // 2, y + h // 2))
    screen.blit(text_surface, text_rect)

# Hàm chạy game với người chơi
def run_connect4_no_ai():
    subprocess.run(["python", "connect4_no_ai.py"])

# Hàm chạy game với AI
def run_connect4_ai():
    subprocess.run(["python", "connect4_ai.py"])

# Vòng lặp chính
running = True
while running:
    screen.fill(BG_COLOR)

    title_text = font.render("Choose Game Mode", True, BLACK)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 80))

    draw_button("Play vs Player", 285, 200, 250, 60, BUTTON_COLOR, HOVER_COLOR, run_connect4_no_ai)
    draw_button("Play vs AI", 285, 300, 250, 60, BUTTON_COLOR, HOVER_COLOR, run_connect4_ai)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()

pygame.quit()
