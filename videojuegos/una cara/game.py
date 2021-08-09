import pygame
from settings import *
from pygame import Vector2
import math


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode([800, 600])
        pygame.display.set_caption("una cara")


    def run(self):
        self.playing = True
        while (self.playing):
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False

    def update(self):
        pass

    def draw(self):
        self.screen.fill(WHITE)
        pygame.draw.circle(self.screen, BLACK, Vector2(300, 200), 60)
        pygame.draw.circle(self.screen, BLACK, Vector2(450, 220), 60)
        pygame.draw.circle(self.screen, WHITE, Vector2(300, 200), 40)
        pygame.draw.circle(self.screen, WHITE, Vector2(450, 220), 40)
        pygame.draw.circle(self.screen, BLACK, Vector2(350, 320), 100)
        pygame.draw.circle(self.screen, WHITE, Vector2(350, 350), 30)
        pygame.draw.circle(self.screen, WHITE, Vector2(300, 280), 10)
        pygame.draw.circle(self.screen, WHITE, Vector2(350, 280), 10)
        pygame.draw.arc(self.screen, DARKGREY, pygame.Rect(280, 300, 60, 35), math.radians(180), 0, 15)
        pygame.draw.circle(self.screen, LIGHTGREY, Vector2(290, 320), 10)
        pygame.display.flip()




game = Game()
game.run()