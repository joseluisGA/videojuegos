import pygame
from pygame.math import Vector2
from settings import *
import random

class Fruit(pygame.sprite.Sprite):
    def __init__(self, groups):
        pygame.sprite.Sprite.__init__(self, groups)
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.colors = [RED, PINK, BLUE, YELLOW]

        self.rect = self.image.get_rect()
        self.teleport()


    def teleport(self):
        x = random.randrange(0, GRID_WIDTH)
        y = random.randrange(0, GRID_HEIGHT)

        self.rect.topleft = Vector2(x, y) * TILESIZE
        self.image.fill(random.choice(self.colors))
        
    