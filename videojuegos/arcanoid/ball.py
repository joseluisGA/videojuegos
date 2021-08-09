import pygame
from settings import *
from pygame import Vector2
import random

from brick import Brick


class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y, groups, ball_image, bounce_fx):
        pygame.sprite.Sprite.__init__(self, groups)
        #self.image = pygame.Surface((BALL_WIDTH, BALL_HEIGHT))
        #self.image.fill(BLUISHGREY)
        self.image = ball_image
        self.rect = self.image.get_rect()
        self.rect.center = Vector2(x, y)
        self.velocity = Vector2(0, 0)
        self.bounce_fx = bounce_fx
        self.asleep = True


    def update(self, bricks, pad, ball_lost_callback):
        if self.asleep:
            if pad.velocity != 0:
                self.velocity =  Vector2(pad.velocity, -5).normalize()
                self.asleep = False
            return

        position = self.rect.center + self.velocity.normalize() * BALL_SPEED
        self.rect.centerx = position.x
        self.collide_with('x', bricks)
        self.rect.centery = position.y
        self.collide_with('y', bricks)

        if self.rect.centerx < 0:
            self.rect.centerx = 0
            self.velocity.x *= -1
            self.bounce_fx.play()
        if self.rect.centerx > WIDTH-1:
            self.rect.centerx = WIDTH-1
            self.velocity.x *= -1
            self.bounce_fx.play()
        if self.rect.centery < 0:
            self.rect.centery = 0
            self.velocity.y *= -1
            self.bounce_fx.play()

        if self.rect.centery > HEIGHT-1:
            self.kill()
            ball_lost_callback()

    def collide_with(self, dir, groups):
        hits = pygame.sprite.spritecollide(self, groups, False)
        if len(hits) == 0:
            return

        if dir == 'x':
            if self.velocity.x > 0:
                self.rect.right = hits[0].rect.left
            if self.velocity.x < 0:
                self.rect.left = hits[0].rect.right
            self.velocity.x *= -1

        if dir == 'y':
            if self.velocity.y > 0:
                self.rect.bottom = hits[0].rect.top
            if self.velocity.y < 0:
                self.rect.top = hits[0].rect.bottom
            self.velocity.y *= -1

        if type(hits[0]) == Brick:
            hits[0].breakIt()
