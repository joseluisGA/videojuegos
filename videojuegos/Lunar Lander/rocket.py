import pygame
from settings import *
from pygame import Vector2
from moon import Moon
import random

class Rocket(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((ROCKET_WIDTH, ROCKET_HEIGHT))
        self.image.fill(BLUISHGREY)
        self.rect = self.image.get_rect()
        self.rect.center = Vector2(x, y)
        self.velocity = Vector2(0,0)
        self.engine = ROCKET_ENGINE
        self.fuel = 1
        self.alive = True
        self.landed = False

#nos permite ir moviendo cosas por el espacio


    def update(self, moon):
        if not self.alive:
            return

        if self.landed:
            return

        if self.fuel > 0:
            self.keyboard_input()
        
        self.velocity.y += GRAVITY
        self.rect.center += self.velocity

        if self.rect.centerx < 0:
            self.rect.centerx = WIDTH-1 # pasa de un lado a otro de la pantalla
            # self.rect.centerx = 0
            # self.velocity.x *=-1
        if self.rect.centerx > WIDTH-1:
            self.rect.centerx = 0
            # self.rect.centerx = WIDTH-1
            # self.velocity.x *= -1

        is_grounded = self.check_landing(moon)
        if is_grounded:
            landing_velocity_ok = self.velocity.magnitude() < 3
            landing_left = moon.landing_spot_x - moon.landing_spot_width
            landing_right = moon.landing_spot_x + moon.landing_spot_width
            landing_on_platform_ok = landing_left < self.rect.centerx < landing_right
            print(self.velocity.magnitude())

            if landing_on_platform_ok and landing_velocity_ok:
                self.landed = True
            else:
                self.alive = False
    
    def check_landing(self, moon):
        x, y = self.rect.midbottom
        terrain_height = HEIGHT - moon.heights[x]
        is_grounded = y > terrain_height
        return is_grounded

    

    def keyboard_input(self):
        keystate = pygame.key.get_pressed()
        delta = Vector2(0, 0)
        if keystate[pygame.K_UP]:
            delta.y -= self.engine
        if keystate[pygame.K_LEFT]:
            delta.x -= self.engine
        if keystate[pygame.K_RIGHT]:
            delta.x += self.engine

        if not delta.magnitude() == 0:
            self.fuel -= ROCKET_CONSUMPTION
            self.fuel = max(0, min(1, self.fuel))
        
        self.velocity += delta
        

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        if not self.alive:
            pygame.draw.circle(surface, RED, self.rect.center,
            random.randrange(5,25))
