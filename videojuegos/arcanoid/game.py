import pygame
from settings import *
from pygame import Vector2
import math

from ball import Ball
from pad import Pad
from brick import Brick
import random
from os import path

# El jugador controla una PALA que mueve en horizontal, con incercia
# Debe evitar que la/s BOLAS caigan por la parte inferior de la pantalla
# Las BOLAS van rebotando por el espacio de juego contra los laterales,
# contra la pala del jugador y los LADRILLOS
# En cada FASE hay un conjunto de LADRILLOS que deben ser DESTRUIDOS,
# haciendo chocar la bola con ellos.
# La fase termina si todos los LADRILLOS son DESTRUIDOS
# Si una bola cae por la parte inferior de la pantalla se retira de la partida
# La partida termina si no hay ninguna bola en pantalla

# AÑADIDO: Muros de ladrillos con distintas formas


class Game:
    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 2, 1024)
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode([WIDTH, HEIGHT])
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.load_data()
        
    def load_data(self):
        root_folder = path.dirname(__file__)
        sound_folder = path.join(root_folder, "sound")
        img_folder = path.join(root_folder, "img")
        self.load_images(img_folder)
        self.load_sounds(sound_folder)

    def load_images(self, img_folder):
        self.ball_image = pygame.image.load(path.join(img_folder, "ballBlue.png")).convert_alpha()
        self.pad_image = pygame.image.load(path.join(img_folder, "paddleRed.png")).convert_alpha()
        brick_colors=["blue", "green", "grey", "purple", "yellow", "red"]
        self.brick_images = []
        for color in brick_colors:
            filename= f"element_{color}_rectangle.png"
            img = pygame.image.load(path.join(img_folder, filename))
            self.brick_images.append(img)


    def load_sounds(self, sound_folder):
        self.bounce_fx = pygame.mixer.Sound(path.join(sound_folder, "bounce.wav"))
        self.break_fx = pygame.mixer.Sound(path.join(sound_folder, "break.wav"))
        self.break_fx.set_volume(0.1)



    def start(self):
        self.all_sprites = pygame.sprite.Group()
        self.balls = pygame.sprite.Group()
        self.bricks = pygame.sprite.Group()
        self.lifes = 3
        self.pad = Pad(WIDTH//2, HEIGHT - PAD_HEIGHT*2, (self.all_sprites), self.pad_image, self.bounce_fx)
        #self.ball = Ball(self.pad.rect.centerx, self.pad.rect.top - PAD_HEIGHT*2, (self.balls), self.ball_image, self.bounce_fx)
        self.ball = self.create_ball_at(self.pad.rect.centerx, self.pad.rect.top - PAD_HEIGHT * 2)
        self.brick_wall()
        self.lifes = 5
        self.score = 0
        self.run()

    def brick_wall(self):
        for x in range(10):
            for y in range(7):
                brick_x = BRICK_WIDTH + x * BRICK_WIDTH + x * 5
                brick_y = BRICK_HEIGHT * 2 + y * BRICK_HEIGHT + y * 5
                Brick(brick_x, brick_y, (self.all_sprites, self.bricks), self.brick_images, self.break_fx)

    def create_ball_at(self, x, y):
        return Ball(x, y , (self.balls), self.ball_image, self.bounce_fx)

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
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.powerup_multiball()

    def update(self):
        self.pad.update()
        self.balls.update(self.bricks, self.pad, self.ball_lost)
        hits = pygame.sprite.spritecollide(self.pad, self.balls, False)
        for ball in hits:
            self.pad.hit(ball)

    def ball_lost(self):
        if len(self.balls.sprites())>0:
            return
            
        self.pad.velocity = 0
        self.lifes-=1
        if self.lifes >0:
            self.create_ball_at(self.pad.rect.centerx, self.pad.rect.top - PAD_HEIGHT *2)
        else:
            print("Game Over")


    def powerup_multiball(self):
        for _ in range(5):
            reference_ball = self.balls.sprites()[0]
            ball = self.create_ball_at(reference_ball.rect.centerx, reference_ball.rect.centery)
            ball.asleep = False
            ball.velocity = Vector2(ball.velocity.x + random.uniform(-0.5, 0.5), reference_ball.velocity.y)

    def draw(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        self.balls.draw(self.screen)
        pygame.display.flip()


game = Game()
game.start()
