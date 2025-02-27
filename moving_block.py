import pygame
import random
WIDTH=450
HEIGHT=700
import config
class Moving_Block(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        x = random.randint(40, WIDTH-40)
        global max_height
        if len(config.blocks) == 0:
            x = WIDTH / 2
            y = HEIGHT / 2+200
        else:
            prevblock=config.blocks[-1]
            prevy=prevblock.rect.centery
            y = random.randint(prevy-max_height, prevy-max_height//5)
        self.image = pygame.Surface((80, 10))
        self.image.fill(RED)
        self.rect = self.image.get_rect()  
        self.rect.center = (x, y)  
