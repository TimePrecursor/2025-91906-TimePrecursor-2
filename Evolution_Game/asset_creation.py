# this file will define the assets for easy programming later (I think)
import arcade
from main import WINDOW_WIDTH, WINDOW_HEIGHT

class sprites:
    def __init__(self, sprite_File, sprite_W, sprite_H, sprite_X, sprite_Y):
        self.sprite_File = sprite_File
        self.sprite_W = sprite_W
        self.sprite_H = sprite_H
        self.sprite_X = sprite_X
        self.sprite_Y = sprite_Y

    def sprite_creation(self,sprite_File, sprite_W, sprite_H, sprite_X, sprite_Y):
        self.sprite_texture = arcade.load_texture(self.sprite_File)
        self.first_sprite = arcade.Sprite(self.sprite_texture)
        self.first_sprite.center_x = WINDOW_WIDTH / 4
        self.first_sprite.center_y = WINDOW_HEIGHT / 4

# def sprite_pngs(self, WINDOW_WIDTH, WINDOW_HEIGHT):
#     carnivore_png = arcade.Sprite(self.player_texture)
#     carnivore_png.center_x = WINDOW_WIDTH / 4
#     carnivore_png.center_y = WINDOW_HEIGHT / 4
