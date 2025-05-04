import arcade
import os
from arcade.gui import UIView

live_food_stats = [
    {
        "name": "Deer",
        "speed": 7,
        "awareness": 6,
        "nutritional_value": 8
    },
    {
        "name": "Gazelle",
        "speed": 9,
        "awareness": 8,
        "nutritional_value": 7
    },
    {
        "name": "Mouse",
        "speed": 3,
        "awareness": 5,
        "nutritional_value": 2
    },
    {
        "name": "Rabbit",
        "speed": 6,
        "awareness": 7,
        "nutritional_value": 4
    },
    {
        "name": "Pig",
        "speed": 4,
        "awareness": 4,
        "nutritional_value": 9
    }
]


class live_food(arcade.Sprite):
    def __init__(self,image, scale, window_width=1000,window_height=600):
        """ Initialize the live food sprite """
        super().__init__(image, scale)
        self.center_x = window_width // 2  # Start in the middle of the screen
        self.center_y = window_height // 2
        self.change_x = 0
        self.change_y = 0

class live_food_functions(UIView):
    def __init__(self):
        super().__init__()
    def load_image(self):
        self.sprite_list = arcade.SpriteList()
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        file_path = os.path.join(project_root, "assets", "images", "animal_textures_fixed", "pig.png")
        self.food_sprite = live_food(file_path, scale=0.15)
        self.food_sprite.center_x = 1000/2
        self.food_sprite.center_y = 600/2
        self.sprite_list.append(self.food_sprite)
        self.sprite_list.draw()  # Draw player first


    def on_draw(self):
        self.sprite_list.draw()  # Draw player first






