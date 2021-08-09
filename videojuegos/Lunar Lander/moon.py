import pygame
from settings import *
import random
import math

class Moon():
    def __init__(self, max_heights, min_heights):
        self.max_heights = math.floor(max_heights)
        self.min_heights = math.floor(min_heights)

        self.heights = []
        self.landing_spot_x = 0
        self.landing_spot_width = 0

    def generate_terrain(self):
        last_height = random.randrange(self.min_heights, self.max_heights)
        mid_height = (self.min_heights + self.max_heights)//2
        for _ in range(0, WIDTH):
            rnd = random.randrange(self.min_heights, self.max_heights)
            go_up = rnd > mid_height
            if go_up:
                last_height += random.randrange(1,5)
            else:
                last_height -= random.randrange(1,5)
            last_height = max(self.min_heights, 
                min(self.max_heights, last_height))
            self.heights.append(last_height)

        landing_spot_x = random.randrange(WIDTH * 0.15, WIDTH * 0.85)
        landing_spot_width = random.randrange(20,30)
        landing_spot_height = self.heights[landing_spot_x]
        for x in range(landing_spot_x-landing_spot_width,
            landing_spot_x+landing_spot_width):
            self.heights[x] = landing_spot_height
        
        self.landing_spot_x = landing_spot_x
        self.landing_spot_width = landing_spot_width

    def draw(self, surface):
        for x in range(0, WIDTH):

            pygame.draw.line(surface, RED, (x, HEIGHT), 
                (x, HEIGHT-self.heights[x]))
        
        landing_spot_height = HEIGHT - self.heights[self.landing_spot_x]
        start_pos = (self.landing_spot_x -
                     self.landing_spot_width, landing_spot_height)

        end_pos = (self.landing_spot_x +

                   self.landing_spot_width, landing_spot_height)
        pygame.draw.line(surface, LIGHTGREY,start_pos,end_pos, 3)
