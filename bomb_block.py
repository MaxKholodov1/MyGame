import pygame
import random
block_speed_x=2
flag=False
WIDTH=450
HEIGHT=700
RED = (255, 0, 0)
class Bomb_Block(pygame.sprite.Sprite):
    def __init__(self, sz, max_height, prev_block_height):
        pygame.sprite.Sprite.__init__(self)
        x = random.randint(40, WIDTH-40)
        if(sz!=0):
            y = random.randint(prev_block_height-max_height, prev_block_height-max_height//5)
            self.image = pygame.Surface((80, 10))
            self.image.fill(RED)
            self.rect = self.image.get_rect()  
            self.rect.center = (x, y)  
        else:
            flag=True
            y = random.randint(0, HEIGHT)
            self.image = pygame.Surface((80, 10))
            self.image.fill(RED)
            self.rect = self.image.get_rect()  
            self.rect.center = (x, y) 

    # def update(self):
    #     global block_speed_x
    #     speed_x=0
    #     if(self.rect.left<0 or self.rect.right>WIDTH ):
    #         self.speed_x=-self.speed_x
    #     self.rect.x+=self.speed_x