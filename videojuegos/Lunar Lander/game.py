import pygame
from settings import *
from pygame import Vector2
import math

from rocket import Rocket
from moon import Moon

#REGLAS:
# Juego arcade
# El jugador controla un cohete que debe hacer aterrizar suavemente 
# Controla el cohete con los cursores
# El cohete tiene gasolina que se gasta al moverse
# El juego acaba si chocamos contra el suelo
# El juego gana si aterriza en la zona de aterrizaje

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode([WIDTH, HEIGHT])
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.start()


    def start(self):
        self.rocket = Rocket(WIDTH/2, 20)
        self.moon = Moon(HEIGHT/3, HEIGHT/10)
        self.moon.generate_terrain()


    def run(self):
        self.playing = True
        while (self.playing):
            self.dt = self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False

    def update(self):
        self.rocket.update(self.moon)
        if not self.rocket.alive:
            self.playing = False
            pass # game over
        
        if self.rocket.landed:
            self.start()

    def draw(self):
        self.screen.fill(BLACK)
        self.rocket.draw(self.screen)
        self.moon.draw(self.screen)
        self.draw_UI()
        pygame.display.flip()


    def draw_UI(self):
        pygame.draw.rect(self.screen, DARKGREY, pygame.Rect(5, 5, 200, 25))
        pygame.draw.rect(self.screen, LIGHTGREY, pygame.Rect(
            7, 7, 196 * self.rocket.fuel, 21))


game = Game()
game.run()