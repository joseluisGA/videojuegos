import pygame
from settings import *
from pygame import Vector2


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_x, tile_y, groups, tile_image):
        pygame.sprite.Sprite.__init__(self, groups)
        self.image = tile_image
        self.rect = self.image.get_rect()
        self.rect.topleft = Vector2(tile_x, tile_y) * TILESIZE

    def stepped_on(self, mob):
        pass

class Wall(Tile):
    def __init__(self, tile_x, tile_y, groups, wall_image, canGoThrough):
        super().__init__(tile_x, tile_y, groups, wall_image)

        self.canGoThrough = canGoThrough




