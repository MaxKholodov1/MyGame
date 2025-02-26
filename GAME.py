import pygame
import random

# Константы
WIDTH = 750
HEIGHT = 750
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
speed_x=5
accel_y=0.09
speed_y=1
max_speed_y=1
# Спрайт
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 50))  # Размеры
        self.image.fill(GREEN)  # Цвет
        self.rect = self.image.get_rect()  # Прямоугольник его окружающий
        self.rect.center = (WIDTH / 2, HEIGHT / 2)  # Размещение в центре
    def update(self):
        global speed_x
        global accel_y
        global speed_y

        # Движение по Y
        self.rect.y += speed_y
        speed_y += accel_y

        # Проверка столкновения с блоком
        if self.rect.colliderect(block.rect):
            print(self.rect.bottom, block.rect.top)
            if 0 <= self.rect.bottom - block.rect.top <= 5 and speed_y > 0:
                self.rect.bottom = block.rect.top  
                speed_y = -max_speed_y  
        # Управление
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:  
            self.rect.x -= speed_x
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:  
            self.rect.x += speed_x
class Block(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((300,20))
        self.image.fill(RED)
        self.rect = self.image.get_rect()  # Прямоугольник его окружающий
        self.rect.center = (WIDTH / 2, HEIGHT / 2+100)  # Размещение в центре

# Группа спрайтов
all_sprites = pygame.sprite.Group()
player = Player()
block=Block()
all_sprites.add(player)
all_sprites.add(block)


# Цикл игры
running = True
while running:
    clock.tick(FPS)  # Ограничение FPS
    screen.fill(BLACK)  # Очищаем экран

    # Ввод (обработка событий)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    all_sprites.update()  # Обновляем все спрайты
    all_sprites.draw(screen)  # **Рисуем спрайты**
    
    pygame.display.flip()  # Обновление экрана

pygame.quit()
