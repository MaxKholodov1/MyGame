import pygame

WIDTH = 450
HEIGHT = 700
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

def draw_button(text, x, y, width, height, color, text_color, screen):
    font = pygame.font.Font(None, 50)
    pygame.draw.rect(screen, color, (x, y, width, height))  # Рисуем кнопку
    text_surf = font.render(text, True, text_color)
    text_rect = text_surf.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(text_surf, text_rect)
    return pygame.Rect(x, y, width, height)

def show_restart_screen(screen, score, blocks, doubled_blocks, restart_function):
    screen.fill(BLACK)
    font = pygame.font.Font(None, 50)
    
    text1 = font.render("GAME OVER!", True, WHITE)
    text2 = font.render(f"YOUR SCORE: {score}", True, WHITE)
    
    text1_rect = text1.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 80)) 
    text2_rect = text2.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 30)) 
    screen.blit(text1, text1_rect)
    screen.blit(text2, text2_rect)

    button_rect = draw_button("Restart", WIDTH // 2 - 100, HEIGHT // 2 + 40, 200, 60, RED, WHITE, screen)

    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:  # Проверяем клик мыши
                if button_rect.collidepoint(event.pos):
                    waiting = False
                    restart_function(blocks, doubled_blocks)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Нажатие пробела
                    waiting = False
                    restart_function(blocks, doubled_blocks)
