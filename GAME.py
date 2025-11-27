import pygame
import random
import os
import config
from bomb_block import Bomb_Block  # Импортируем класс из другого файла
# Константы
WIDTH =450
HEIGHT = 700
FPS = 120
score=0
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
VIOLET = (120, 60, 120)#180, 90, 180 238, 130, 238
speed_x = 4
accel_y = 0.15
speed_y = 8
max_speed_y = 8
max_height= int((max_speed_y**2)/(2*accel_y))
game_over=False
font = pygame.font.Font(None, 36)

BACKGROUND_IMAGE_PATH = "night.png"
background = pygame.image.load(BACKGROUND_IMAGE_PATH).convert()
background_height = background.get_height()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

def draw_background():
    # screen.blit(background, (0, 0), (0, background_height - HEIGHT, WIDTH, HEIGHT))
    screen.blit(background, (0, 0))

# Путь к файлу с изображением
PLAYER_IMAGE_PATH = "firesq.png"

#перезапуск

prev_block_height=750
# Спрайт игрока
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        if os.path.exists(PLAYER_IMAGE_PATH):
            self.image = pygame.image.load(PLAYER_IMAGE_PATH).convert_alpha()
            self.image = pygame.transform.scale(self.image, (40, 200))  # Масштабируем
        else:
            self.image = pygame.Surface((40, 200))
            self.image.fill(VIOLET)

        self.rect = self.image.get_rect()  
        self.rect.center = (WIDTH / 2, HEIGHT / 2+100)  

    def update(self):
        global speed_x, accel_y, speed_y, score

        if self.rect.top > HEIGHT:
            global game_over  
            game_over = True
        #гравитация
        self.rect.y += speed_y
        speed_y += accel_y

        # Проверка столкновения с блоком
        for i in range(len(blocks)-1, -1, -1):
            block=blocks[i]
            if self.rect.colliderect(block.rect):
                if 0 <= self.rect.bottom - block.rect.top <= 5 * speed_y and speed_y > 0 and not (self.rect.left +  1.5*speed_x > block.rect.right) and not (self.rect.right -  1.5*speed_x < block.rect.left):
                    self.rect.bottom = block.rect.top  
                    speed_y = -max_speed_y 
                    cnt=0
                    remove=[]
                    if isinstance(block, Bomb_Block):
                        remove.append(i)
                        score+=1
                        cnt+=1
                    for i in range (cnt-1, -1, -1):
                        all_sprites.remove(blocks[remove[i]])
                        del blocks[remove[i]]
                    level2=300
                    level3=500
                    v2=score/level2
                    v3=score/level3
                    v1=max(1-v2-v3, 0)
                    for i in range (cnt):
                        result = random.choices([1, 2, 3], weights=[v1, v2, v3], k=1)[0]
                        if result ==1:
                            block=Block()

                        elif result==2:
                            prev_block_height = doubled_blocks[-1].rect.y
                            block = Bomb_Block(sz=80, max_height=max_height, prev_block_height= prev_block_height)
                        else:
                            block=Moved_Block()
                        blocks.append(block)
                        doubled_blocks.append(block)
                        all_sprites.add(block)
                                

        # Управление
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:  
            self.rect.centerx = (self.rect.centerx - speed_x + WIDTH) % WIDTH
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:  
            self.rect.centerx = (self.rect.centerx + speed_x + WIDTH) % WIDTH


        #добавление и удаление блоков и имитация бесконечного поднятия
        cnt=0
        double_cnt=0
        level2=100
        level3=200
        v2=score/level2
        v3=score/level3
        v1=max(1-v2-v3, 0)
        if self.rect.bottom<HEIGHT/2:
            remove=[]
            double_remove=[]
            for i in range(len(blocks)):
                block=blocks[i]
                block.rect.bottom+=(HEIGHT/2-self.rect.bottom)
                if(block.rect.bottom>HEIGHT):
                    remove.append(i)
                    score+=1
                    cnt+=1
            for i in range (len(doubled_blocks)):
                doubled_block= doubled_blocks[i]
                if not (doubled_block in blocks): 
                    doubled_block.rect.bottom+=(HEIGHT/2-self.rect.bottom)
                    if(doubled_block.rect.bottom>HEIGHT):
                        double_remove.append(i)
                        double_cnt+=1

                
            for i in range (cnt-1, -1, -1):
                all_sprites.remove(blocks[remove[i]])
                del blocks[remove[i]]

            for i in range (double_cnt-1, -1, -1):
                del doubled_blocks[double_remove[i]]


            for i in range(cnt):
                result = random.choices([1, 2, 3], weights=[v1, v2, v3], k=1)[0]
                if result ==1:
                    block=Block()

                elif result==2:
                    prev_block_height = doubled_blocks[-1].rect.y
                    block = Bomb_Block(sz=80, max_height=max_height, prev_block_height= prev_block_height)
                else:
                    block=Moved_Block()
                blocks.append(block)
                doubled_blocks.append(block)
                all_sprites.add(block)
            self.rect.bottom=HEIGHT/2
        # чтобы игрок был поверх остальных
        all_sprites.remove(player)  
        all_sprites.add(player)


#движущиеся блоки
 
block_speed_x=2
flag=False
class Moved_Block(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        x = random.randint(40, WIDTH-40)
        self.speed_x=2
        global flag
        if(len(blocks)!=0):
            prev_block_height=doubled_blocks[-1].rect.y
            y = random.randint(prev_block_height-max_height, prev_block_height-max_height//5)
            self.image = pygame.Surface((80, 10))
            self.image.fill(BLUE)
            self.rect = self.image.get_rect()  
            self.rect.center = (x, y)  

        
    def update(self):
        global block_speed_x
        if(self.rect.left<0 or self.rect.right>WIDTH ):
            self.speed_x=-self.speed_x
        self.rect.x+=self.speed_x

# 

all_sprites = pygame.sprite.Group()
player = Player()
blocks=[]
doubled_blocks=[]
all_sprites.add(player)
# Блоки
class Block(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        x = random.randint(40, WIDTH-40)
        global max_height
        if len(blocks) ==0:
            x = WIDTH / 2
            y = HEIGHT / 2+200
        else:
            prev_block_height=doubled_blocks[-1].rect.y
            y = random.randint(prev_block_height-max_height, prev_block_height-max_height//4)
        self.image = pygame.Surface((80, 10))
        self.image.fill(VIOLET)
        self.rect = self.image.get_rect()  
        self.rect.center = (x, y)  

for i in range(5):
    block_new=Block()
    all_sprites.add(block_new)
    blocks.append(block_new)
    doubled_blocks.append(block_new)


from restart import show_restart_screen

def restart_game(blocks, doubled_blocks):
    global all_sprites, player, speed_y, score, game_over
    game_over=False
    speed_y = 10
    all_sprites.empty()
    blocks.clear()
    doubled_blocks.clear()

    player = Player()
    all_sprites.add(player)
    prev_block_height=750
    for _ in range(5):
        block = Block()
        blocks.append(block)
        doubled_blocks.append(block)
        all_sprites.add(block)

    score = 0
#кнопка перезапуска

# Цикл игры

running = True
while running:
    clock.tick(FPS)  
    # screen.fill(BLACK)  
    draw_background()  # Отображаем фон
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    all_sprites.update()  
    if game_over == True:
        if game_over:
            show_restart_screen(screen, score, blocks,doubled_blocks, restart_game)
    all_sprites.draw(screen)  
    
    pygame.display.flip()  

pygame.quit()
