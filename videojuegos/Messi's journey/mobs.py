import pygame
from pygame import Vector2
from settings import *
import random

class Robe(pygame.sprite.Sprite):
    def __init__(self, x, y, groups, mob_image):
        pygame.sprite.Sprite.__init__(self, groups)
        self.image = mob_image
        self.rect = self.image.get_rect()
        self.rect.topleft = Vector2(x, y)

        self.velocity = Vector2(0,0)
        self.desired_velocity = Vector2(0,0)
        
        #salto
        self.trigger_jump = False
        self.grounded = False
        self.jump_time = 0

        self.last_save_point = Vector2(x, y)
        self.current_tile = None

        self.move_down = False

        self.healt_points = ROBE['HEALT_POINTS']

        self.cd_move = 0

    def update(self, deltaTime,walls_group):
        self.cd_move += deltaTime
        if self.cd_move >= ROBE['MOVE_CD']:

            self.random_move()

            self.velocity -= self.velocity * WORLD['DRAG_MOB']
            self.velocity += self.desired_velocity
            self.velocity.y += WORLD['GRAVITY_MOB']


            if self.trigger_jump:
                self.trigger_jump = False
                self.velocity.y = ROBE['JUMP_SPEED']
                self.jump_time += deltaTime
            
            if abs(self.velocity.x) < 1:
                self.velocity.x = 0

            position = self.rect.center + self.velocity.normalize() * ROBE['MAX_SPEED']
            self.rect.centerx = position.x
            self.collision_with_walls('x', walls_group)
            self.rect.centery = position.y
            self.collision_with_walls('y', walls_group)

            self.cd_move = 0
        

    def random_move(self):
        delta = Vector2(0,0)
        move = random.randrange(0, 101)

        if move<=UP:
            if self.grounded or self.jump_time < ROBE['JUMP_MAX_TIME']:
                self.trigger_jump = True                               
            else:
                self.jump_time = ROBE['JUMP_MAX_TIME']
        if move>UP and move <=LEFT:
            if self.rect.x > WIDTH/2:
                delta.x = -1
            else:
                delta.x = 1
        if move>LEFT and move <=RIGHT:
            delta.x = 1
        if move> RIGHT:
            self.move_down = True


        self.desired_velocity = delta


    def collision_with_walls(self, dir, walls_group):
        hits = pygame.sprite.spritecollide(self, walls_group, False)
        if len(hits) == 0:
            self.grounded = False
            return
        hit_rect = hits[0].rect
        if dir == 'x':
            if self.velocity.x > 0:
                if not hits[0].canGoThrough:
                    self.rect.right = hit_rect.left
            if self.velocity.x < 0:
                if not hits[0].canGoThrough:
                    self.rect.left = hit_rect.right
            self.velocity.x =0

        if dir== 'y':
            if self.velocity.y >0:
                if not self.move_down or not hits[0].canGoThrough:
                    self.rect.bottom = hit_rect.top
                    self.grounded = True
                    self.jump_time = 0
                    self.current_tile = hits[0]
                else:
                    self.move_down = False
                    self.rect.top = hit_rect.bottom
            if self.velocity.y <0:
                  if not hits[0].canGoThrough:
                        self.rect.top = hit_rect.bottom
            self.velocity.y = 0
