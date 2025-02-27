import pygame
import random
import os

# Константы
WIDTH =400
HEIGHT = 700
FPS = 120

# Инициализация Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Окно
pygame.display.set_caption("My Game")  # Название окна
clock = pygame.time.Clock()  # Контроль времени

# Цвета (R, G, B)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

speed_x = 4
accel_y = 0.15
speed_y = 9
max_speed_y = 9
max_height= int((max_speed_y**2)/(2*accel_y))
game_over=False
# Путь к файлу с изображением
PLAYER_IMAGE_PATH = "images.png"


#перезапуск
def restart_game():
    global blocks, all_sprites, player, speed_y
    speed_y = 10
    
    all_sprites.empty()
    blocks.clear()

    player = Player()
    all_sprites.add(player)

    for _ in range(6):
        block = Block()
        blocks.append(block)
        all_sprites.add(block)
# Спрайт игрока
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        if os.path.exists(PLAYER_IMAGE_PATH):
            self.image = pygame.image.load(PLAYER_IMAGE_PATH).convert_alpha()
            self.image = pygame.transform.scale(self.image, (40, 40))  # Масштабируем
        else:
            self.image = pygame.Surface((40, 40))
            self.image.fill(GREEN)

        self.rect = self.image.get_rect()  
        self.rect.center = (WIDTH / 2, HEIGHT / 2+100)  

    def update(self):
        global speed_x, accel_y, speed_y

        if self.rect.top > HEIGHT:
            global game_over  
            game_over = True
        #гравитация
        self.rect.y += speed_y
        speed_y += accel_y

        # Проверка столкновения с блоком
        for block in blocks:
            if self.rect.colliderect(block.rect):
                if 0 <= self.rect.bottom - block.rect.top <= 5 * speed_y and speed_y > 0 and not (self.rect.left + 2 * speed_x > block.rect.right) and not (self.rect.right - 2 * speed_x < block.rect.left):
                    self.rect.bottom = block.rect.top  
                    speed_y = -max_speed_y  

        # Управление
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:  
            self.rect.centerx = (self.rect.centerx - speed_x + WIDTH) % WIDTH
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:  
            self.rect.centerx = (self.rect.centerx + speed_x + WIDTH) % WIDTH
        cnt=0
        #добавление и удаление блока и имитация бесконечного поднятия
        if self.rect.bottom<HEIGHT//2:
            remove=[]
            for i in range(len(blocks)):
                block=blocks[i]
                block.rect.bottom+=(HEIGHT/2-self.rect.bottom)
                if(block.rect.bottom>HEIGHT):
                    remove.append(i)
                    cnt+=1
            self.rect.bottom=HEIGHT//2
            for i in range (cnt-1, -1, -1):
                all_sprites.remove(blocks[remove[i]])
                del blocks[i]
            for i in range(cnt):
                block=Block()
                blocks.append(block)
                all_sprites.add(block)


# Блоки
blocks = []

class Block(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        x = random.randint(40, WIDTH-40)
        global max_height
        if len(blocks) == 0:
            x = WIDTH / 2
            y = HEIGHT / 2+200
        else:
            prevblock=blocks[-1]
            prevy=prevblock.rect.centery
            y = random.randint(prevy-max_height, prevy-max_height//5)
        self.image = pygame.Surface((80, 10))
        self.image.fill(RED)
        self.rect = self.image.get_rect()  
        self.rect.center = (x, y)  

# Группа спрайтов
# 

all_sprites = pygame.sprite.Group()
player = Player()
block = Block()
blocks = [block]
for i in range(6):
    block_new=Block()
    all_sprites.add(block_new)
    blocks.append(block_new)


all_sprites.add(player)
all_sprites.add(block)


def draw_button(text, x, y, width, height, color, text_color):
    font = pygame.font.Font(None, 50)
    pygame.draw.rect(screen, color, (x, y, width, height))  # Рисуем кнопку
    text_surf = font.render(text, True, text_color)
    text_rect = text_surf.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(text_surf, text_rect)
    return pygame.Rect(x, y, width, height) 

#кнопка перезапуска
def show_restart_screen():
    screen.fill(BLACK)
    font = pygame.font.Font(None, 50)
    text = font.render("Game Over!", True, WHITE)
    screen.blit(text, (WIDTH // 2 - 100, HEIGHT // 2 - 100))

    button_rect = draw_button("Restart", WIDTH // 2 - 100, HEIGHT // 2, 200, 60, RED, WHITE)
    pygame.display.flip()
    waiting =True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:  # Проверяем нажатие мыши
                if button_rect.collidepoint(event.pos):  # Проверяем, попала ли мышь в кнопку
                    waiting = False
                    global game_over
                    game_over=False
                    restart_game()

# Цикл игры
running = True
while running:
    clock.tick(FPS)  
    screen.fill(BLACK)  

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    all_sprites.update()  
    if game_over == True:
        show_restart_screen()
    all_sprites.draw(screen)  
    
    pygame.display.flip()  

pygame.quit()
