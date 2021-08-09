from pygame.math import Vector2
import pygame

from settings import *
import random

class Snake(pygame.sprite.Sprite):
    def __init__(self, tile_x, tile_y, groups):
        pygame.sprite.Sprite.__init__(self, groups)
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.tail_image = pygame.Surface((TILESIZE, TILESIZE))
        self.tail_image.fill(DARKGREEN)
        self.head = Vector2(tile_x, tile_y)
        self.delta = Vector2(0, 0)
        self.move_heat = 0
        self.move_delta_heat = 0.1
        self.tail = []
        self.tail_lenght = 1
        self.is_alive = True

    def update(self):
        self.keyboard_input()

        self.move_heat += self.move_delta_heat
        if self.move_heat > 1:
            self.unpdate_tail()
            self.move_heat = 0
            self.head += self.delta
            self.check_collition_with_tail()

        self.wrap_around_world()
        self.rect.topleft = self.head * TILESIZE

    def draw(self, surface):
        surface.blit(self.image, self.rect)


    def keyboard_input(self):
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.delta.x = -1
            self.delta.y = 0
        if keystate[pygame.K_RIGHT]:
            self.delta.x = 1
            self.delta.y = 0
        
        if keystate[pygame.K_UP]:
            self.delta.x = 0
            self.delta.y = -1
        if keystate[pygame.K_DOWN]:
            self.delta.x = 0
            self.delta.y = 1

    def unpdate_tail(self):
        if len(self.tail) >= self.tail_lenght:
            self.tail.pop()
        self.tail.insert(0, Vector2(self.head.x, self.head.y))

    def wrap_around_world(self):
        if self.head.x < 0:
            self.head.x = GRID_WIDTH-1
        if self.head.x > GRID_WIDTH -1:
            self.head.x = 0
        
        if self.head.y < 0:
            self.head.y = GRID_HEIGHT -1
        if self.head.y > GRID_HEIGHT -1:
            self.head.y = 0

    def draw_tail(self, surface):
        for i in range(0, len(self.tail)):
            tail_tile = self.tail[i]
            surface.blit(self.tail_image, tail_tile * TILESIZE)    
    

    def grow(self, size_delta):
        self.tail_lenght += size_delta
        self.move_delta_heat += min(0.8, self.move_delta_heat + 0.025)

    
    def check_collition_with_tail(self):
        if self.delta.magnitude()== 0:
            return
        if self.head in self.tail:
            self.is_alive = False
            print("ouch")