import pygame

from settings import *

from os import path
from pygame import Vector2
from tiles import *
from items import *
from mobs import *


class Map:
    def __init__(self):
        self.map_data = []
        self.entry_point_Player = Vector2(0,0)
        self.entry_point_Mob = Vector2(0,0)

    def load_map_from_file(self, filename):
        root_folder = path.dirname(__file__)
        self.map_data = []

        with open(path.join(root_folder, "assets", "maps", filename), 'r') as file:
            for line in file:
                self.map_data.append(line)
                print(line)

    def create_sprites_from_data(self, game):
        for row, tiles in enumerate(self.map_data):
            for col, tile in enumerate(tiles):
                position = Vector2(col, row) * TILESIZE
                #tiles
                if tile == 'B':
                    Wall(col, row, game.walls_group, game.border_image, False)
                if tile == '1':
                    Wall(col, row, game.walls_group, game.wall_image, True)
                #items
                if tile== 'P':
                    self.entry_point_Player = position
                if tile == '*':
                    Item(position.x, position.y, game.items_group, "coin", game.coin_image)
                if tile=="L":
                    Item(position.x, position.y, game.items_group, "life", game.life_image)
                #mobs
                if tile == 'R':
                    self.entry_point_Mob = position
                