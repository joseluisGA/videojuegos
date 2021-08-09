import pygame
from pygame import Vector2
from settings import  * 
class Item (pygame.sprite.Sprite):
    def __init__(self, x, y, groups, item_image):
        pygame.sprite.Sprite.__init__(self, groups)
        self.image = item_image
        self.rect = self.image.get_rect()
        self.rect.topleft = Vector2(x, y)


    def update(self, player, mob):
        self.check_hits(player)


    def check_hits(self, player):
        if pygame.sprite.collide_rect(self, player):
            self.kill()


class Fart(Item):
    def __init__(self, x, y, groups, fart_image, megafart):
        super().__init__(x, y, groups, fart_image)
        self.rect.center = Vector2(x, y)
        self.velocity = Vector2(0, 0)
        self.megafart = megafart
    
    def update(self,player, mob, walls_group):

        position = self.rect.center + self.velocity.normalize() * SHOOT_SPEED
        self.rect.centerx = position.x
        self.rect.centery = position.y
        self.impact(mob, player)

    def impact(self, mob, player):
        if pygame.sprite.collide_rect(self, mob):
            self.kill()
            if self.megafart:
                mob.healt_points -= 20
                
            else:
                mob.healt_points -=2


class Cigarrete(Item):
    def __init__(self, x, y, groups, cigarrete_image):
        super().__init__(x, y, groups, cigarrete_image)
        self.rect.center = Vector2(x, y)
        self.velocity = Vector2(0, 0)

    def update(self,player, mob, walls_group):

        position = self.rect.center + self.velocity.normalize() * SHOOT_SPEED
        self.rect.centerx = position.x
        self.rect.centery = position.y
        self.impact(player)

    def impact(self, player):
        if pygame.sprite.collide_rect(self, player):
            self.kill()
            player.lifes -=1

class Jagger(Item):
    def __init__(self, x, y, groups, jagger_image):
        super().__init__(x, y, groups, jagger_image)
        self.rect.center = Vector2(x, y)
        self.velocity = Vector2(0, 0)

    def update(self, player, mob, walls_group):
        self.velocity.y += WORLD['GRAVITY']
        self.rect.center += self.velocity

        self.landing(walls_group)

        if pygame.sprite.collide_rect(self, player):
            if player.energy < PLAYER['MAX_ENERGY']:
                self.kill()
                player.energy += 25
                

    def landing(self, walls_group):
        hits = pygame.sprite.spritecollide(self, walls_group, False)
        if len(hits)== 0:
            return
        hit_rect = hits[0].rect
        if self.velocity.y >0:
            self.rect.bottom = hit_rect.top
        self.velocity.y = 0



        
