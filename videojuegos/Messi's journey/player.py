import pygame
from settings import *
from pygame import Vector2

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, groups, player_image, on_death_callback):
        pygame.sprite.Sprite.__init__(self, groups)
        self.image = player_image
        self.rect = self.image.get_rect()
        self.rect.topleft = Vector2(x, y)

        self.velocity = Vector2(0,0)
        self.desired_velocity = Vector2(0,0)
        
        #salto
        self.trigger_jump = False
        self.grounded = False
        self.jump_time = 0
        self.double_jump_state = DOUBLE_JUMP_AVAILABLE


        self.on_death_callback = on_death_callback
        self.last_save_point = Vector2(x, y)
        self.current_tile = None

        self.key_down = False

        self.energy = 0

        self.lifes = 5

    def update(self, deltaTime,walls_group):
        self.handle_input()

        self.velocity -= self.velocity * WORLD['DRAG']
        self.velocity += self.desired_velocity
        self.velocity.y += WORLD['GRAVITY']
        if self.velocity.y > WORLD['TERMINAL_VELOCITY']:
            self.velocity.y = WORLD['TERMINAL VELOCITY']

        if self.trigger_jump:
            self.trigger_jump = False
            self.velocity.y = PLAYER['JUMP_SPEED']
            self.jump_time += deltaTime
        
        if abs(self.velocity.x) < 1:
            self.velocity.x = 0

        position = self.rect.center + self.velocity * PLAYER['MAX_SPEED']
        self.rect.centerx = position.x
        self.collision_with_walls('x', walls_group)
        self.rect.centery = position.y
        self.collision_with_walls('y', walls_group)

        if self.grounded:
            self.steps_on(self.current_tile)

        self.check_death_conditions()
        


    def handle_input(self):

        delta = Vector2(0,0)
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] or key[pygame.K_a]:
            delta.x = -1
        if key[pygame.K_RIGHT] or key[pygame.K_d]:
            delta.x = 1
        if key[pygame.K_UP] or key[pygame.K_w]:
            if (self.grounded or self.double_jump_state== DOUBLE_JUMP_READY) or self.jump_time < PLAYER['JUMP_MAX_TIME']:
                self.trigger_jump = True
                if self.double_jump_state == DOUBLE_JUMP_READY:
                    self.double_jump_state = DOUBLE_JUMP_USED
                    self.jump_time = 0
        if key[pygame.K_DOWN] or key[pygame.K_s]:
            self.key_down=True

                
        

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
                if not self.key_down or not hits[0].canGoThrough:
                    self.rect.bottom = hit_rect.top
                    self.grounded = True
                    self.jump_time = 0
                    self.double_jump_state = DOUBLE_JUMP_AVAILABLE
                    self.current_tile = hits[0]
                else:
                    self.key_down = False
                    self.rect.top = hit_rect.bottom
            if self.velocity.y <0:
                  if not hits[0].canGoThrough:
                        self.rect.top = hit_rect.bottom
            self.velocity.y = 0

    
    def check_death_conditions(self):
        if self.rect.top > HEIGHT:
            self.die()

    def die(self):
        self.on_death_callback()

    def steps_on(self, tile):
        tile.stepped_on(self)

    def update_save_point(self, x, y):
        self.last_save_point = Vector2(x, y)

    def teleport_to_save_point(self):
        self.rect.topleft = self.last_save_point
        self.velocity = Vector2(0,0)

    def push(self, push_speed):
        self.velocity += push_speed