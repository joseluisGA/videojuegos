import pygame
from pygame import surface
from settings import *
from pygame import Vector2
import math
from snake import Snake
from fruit import Fruit

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode([WIDTH, HEIGHT])
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()

        self.large_font = pygame.font.SysFont('arial', 100)
        self.small_font = pygame.font.SysFont('arial', 32)


    def start(self):
        self.all_sprites = pygame.sprite.Group()
        self.fruits = pygame.sprite.Group()
        self.snake = Snake(10, 10, self.all_sprites)
        self.fruit = Fruit((self.all_sprites, self.fruits))
        self.score = 0
        self.run()

    def run(self):
        self.playing = True
        while (self.playing):
            self.dt = self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
        self.game_over_menu()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

    def update(self):
        self.all_sprites.update()
        hits = pygame.sprite.spritecollide(self.snake, self.fruits, False)
        for hit in hits:
            self.snake.grow(1)
            hit.teleport()
            self.score +=100
        self.playing = self.snake.is_alive

    def draw(self):
        self.screen.fill(BLACK)
        for x in range(0, WIDTH, TILESIZE):
            pygame.draw.line(self.screen, MIDGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pygame.draw.line(self.screen, MIDGREY, (0, y), (WIDTH, y))
        self.snake.draw_tail(self.screen)
        self.all_sprites.draw(self.screen)

        score_Text = self.small_font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_Text, (5,5))

        pygame.display.flip()

    def main_menu(self):
        title_text = self.large_font.render("SNAKE", True, WHITE)
        instructions_Text = self.small_font.render("press any key to begin", True, LIGHTGREY)

        self.screen.fill(BLACK)
        self.screen.blit(title_text, (WIDTH//2 - title_text.get_rect().width//2, 25))
       
        self.screen.blit(instructions_Text,  (WIDTH//2 - instructions_Text.get_rect().width//2, HEIGHT-50))

        pygame.display.flip()
        in_main_menu = True

        while (in_main_menu):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    in_main_menu = False

        self.start()

    def game_over_menu(self):
       
        title_text = self.large_font.render("GAME OVER", True, RED)
        instructions_Text = self.small_font.render("press any key to restart", True, LIGHTGREY)
        score_Text = self.small_font.render(f"Score: {self.score}", True, WHITE)
        self.screen.fill(BLACK)
        self.screen.blit(title_text, (WIDTH//2 - title_text.get_rect().width//2, 25))
        self.screen.blit(score_Text, (WIDTH//2 - score_Text.get_rect().width//2, HEIGHT//2 ))
        self.screen.blit(instructions_Text,  (WIDTH//2 - instructions_Text.get_rect().width//2, HEIGHT-50))

        pygame.display.flip()
        in_game_over_menu = True

        while (in_game_over_menu):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    in_game_over_menu = False

        self.main_menu()


game = Game()
game.main_menu()