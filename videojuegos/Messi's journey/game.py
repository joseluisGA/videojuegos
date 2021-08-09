
import pygame
from settings import *
from map import Map
from player import *
from items import *
from mobs import *
from os import path

class Game():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Plataformas")
        self.clock = pygame.time.Clock()
        self.cont_cd_mob_shot = 0
        self.cont_cd_jagger = 0
        self.large_font = pygame.font.SysFont('arial', 100)
        self.small_font = pygame.font.SysFont('arial', 32)
        self.load_data()



    def load_data(self):
        root_folder = path.dirname(__file__)
        sound_folder = path.join(root_folder, "assets/sound")
        img_folder = path.join(root_folder, "assets/sprites")
        self.load_images(img_folder)
        self.load_sounds(sound_folder)


        self.border_image = pygame.Surface((TILESIZE, TILESIZE))
        self.border_image.fill(BLACK)


        
    def load_images(self, img_folder):
        self.player_image = pygame.image.load(path.join(img_folder, "messi2.png")).convert_alpha()
        self.robe_image = pygame.image.load(path.join(img_folder, "robe.png")).convert_alpha()
        self.cigarrete_image = pygame.image.load(path.join(img_folder, "cigarrete.png")).convert_alpha()
        self.fart_image = pygame.image.load(path.join(img_folder, "fart.png")).convert_alpha()
        self.mega_fart_image = pygame.image.load(path.join(img_folder, "megafart.png")).convert_alpha()
        self.jagger_image = pygame.image.load(path.join(img_folder, "jagger.png")).convert_alpha()
        self.wall_image = pygame.image.load(path.join(img_folder, "element_yellow_square.png")).convert_alpha()

    def load_sounds(self, sound_folder):
        self.bounce_fx = pygame.mixer.Sound(path.join(sound_folder, "bounce.wav"))
        self.fart_fx = pygame.mixer.Sound(path.join(sound_folder, "fart.wav"))
        self.bounce_fx.set_volume(0.1)
        self.main_theme = pygame.mixer.Sound(path.join(sound_folder, "main_theme.wav"))

    def start(self):
        self.walls_group = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.items_group = pygame.sprite.Group()
        self.mobs_group = pygame.sprite.Group()



        self.current_map =  Map()
        self.current_map.load_map_from_file("sample.txt")
        self.current_map.create_sprites_from_data(self)

        x_player, y_player = self.current_map.entry_point_Player
        self.player = Player(x_player, y_player, (self.all_sprites), self.player_image,
                            self.on_player_dies)

        x_mob, y_mob = self.current_map.entry_point_Mob
        self.robe = Robe(x_mob, y_mob, self.mobs_group, self.robe_image)
        self.main_theme.play()
        self.run()

    def run(self):
        self.isPlaying = True
        while (self.isPlaying):
            self.dt = self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
        self.main_theme.stop()
        if self.player.lifes ==0:
            self.game_over_menu()
        elif self.robe.healt_points ==0:
            self.win_menu()

        
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player_shoot()

            

    def update(self):
        self.player.update(self.dt, self.walls_group)
        self.items_group.update(self.player, self.robe, self.walls_group)
        self.mobs_group.update(self.dt, self.walls_group)
        self.cont_cd_mob_shot += self.dt
        self.cont_cd_jagger += self.dt
        if self.cont_cd_mob_shot>= CD_MOB_SHOOT:
            self.mob_shoot()
            self.cont_cd_mob_shot = 0
        if self.cont_cd_jagger>= CD_JAGGER_DROP:
            self.jagger_drop()
            self.cont_cd_jagger = 0
        if self.player.lifes ==0 or self.robe.healt_points ==0:
            self.isPlaying=False

    def draw(self):
        self.screen.fill(LIGHTGREY)
        self.walls_group.draw(self.screen)
        self.all_sprites.draw(self.screen)
        self.items_group.draw(self.screen)
        self.mobs_group.draw(self.screen)
        self.draw_life_bar_mob()
        self.draw_energy_bar()

        lifes = self.small_font.render(f"Lifes: {self.player.lifes}", True, WHITE)
        self.screen.blit(lifes, (100,680))

        pygame.display.flip()


    #MENU
    def main_menu(self):
        title_text = self.large_font.render("Messi's Journey", True, WHITE)
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
        self.screen.fill(BLACK)
        self.screen.blit(title_text, (WIDTH//2 - title_text.get_rect().width//2, 25))
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


    def win_menu(self):
    
        title_text = self.large_font.render("YOU WIN", True, GREEN)
        instructions_Text = self.small_font.render("press any key to restart", True, LIGHTGREY)
        self.screen.fill(BLACK)
        self.screen.blit(title_text, (WIDTH//2 - title_text.get_rect().width//2, 25))
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


    #Events
    def player_shoot(self):
        player_reference = self.player
        if self.player.energy == PLAYER['MAX_ENERGY']:
            shoot =  Fart(player_reference.rect.midright, player_reference.rect.centery, self.items_group, self.mega_fart_image, True )
            self.player.energy = 0
        else:
            shoot =  Fart(player_reference.rect.midright, player_reference.rect.centery, self.items_group, self.fart_image, False)
        shoot.velocity = Vector2(shoot.velocity.x + 1, shoot.velocity.y)
        self.fart_fx.play()

    def mob_shoot(self):
        mob_reference = self.robe
        shoot = Cigarrete(mob_reference.rect.midleft, mob_reference.rect.centery, self.items_group, self.cigarrete_image)
        shoot.velocity = Vector2(shoot.velocity.x - 1, shoot.velocity.y)
        self.bounce_fx.play()

    def jagger_drop(self):
        jagger = Jagger(random.randrange(TILESIZE +1, WIDTH/2), TILESIZE+50, self.items_group, self.jagger_image)


    #game specifies
    def on_player_dies(self):
        self.player.teleport_to_save_point

    def draw_life_bar_mob(self):
        pygame.draw.rect(self.screen, WHITE, pygame.Rect(800, 650, 400, 21))
        pygame.draw.rect(self.screen, RED, pygame.Rect(
            800, 650, 4* self.robe.healt_points, 21))
    
    def draw_energy_bar(self):
        pygame.draw.rect(self.screen, WHITE, pygame.Rect(100, 650, 400, 21))
        pygame.draw.rect(self.screen, BLUE, pygame.Rect(
            100, 650, 4* self.player.energy, 21))


game = Game()
game.main_menu()