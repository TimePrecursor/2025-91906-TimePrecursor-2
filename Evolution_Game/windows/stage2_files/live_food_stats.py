import random

import arcade
import os
from arcade.gui import UIView

live_food_stats = [
    {
        "name": "Deer",
        "speed": 7,
        "awareness": 6,
        "nutritional_value": 8,
        "health": 60,
        "vision_range": 25,
        "stamina": 70
    },
    {
        "name": "Gazelle",
        "speed": 9,
        "awareness": 8,
        "nutritional_value": 7,
        "health": 50,
        "vision_range": 30,
        "stamina": 80
    },
    {
        "name": "Mouse",
        "speed": 3,
        "awareness": 5,
        "nutritional_value": 2,
        "health": 10,
        "vision_range": 15,
        "stamina": 25
    },
    {
        "name": "Rabbit",
        "speed": 6,
        "awareness": 7,
        "nutritional_value": 4,
        "health": 30,
        "vision_range": 20,
        "stamina": 50
    },
    {
        "name": "Pig",
        "speed": 4,
        "awareness": 4,
        "nutritional_value": 9,
        "health": 80,
        "vision_range": 18,
        "stamina": 40
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

class live_food_functions():
    def __init__(self):
        super().__init__()

    def load_image(self):
        self.prey_choices = []
        self.sprite_list = arcade.SpriteList()
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        cache_file = os.path.join(project_root, "windows", "stage2_files", "saved_cache", "cache1.txt")
        with open(cache_file, "r") as cf:
            for line in cf.readlines():
                if line.startswith("|"):
                    line.rstrip("\n")
                    line.lstrip("|")
                    self.prey_choices = line.split("|")
                else:
                    print()

        self.prey_choices.pop(0)
        random_prey = random.choice(self.prey_choices)
        file_path = os.path.join(project_root, "assets", "images", "animal_textures_fixed", f"{random_prey}.png")
        self.food_sprite = live_food(file_path, scale=0.15)
        import Evolution_Game.windows.stage2_files.environmentSetupMkII as enviro_setup
        select_randx = random.choice(enviro_setup.EnvironmentSetup.tree_locations)
        self.food_sprite.center_x = (select_randx["center_x"])
        self.food_sprite.center_y = (select_randx["center_y"])
        # self.sprite_list.append(self.food_sprite)
        # print(self.prey_choices)
        return [self.food_sprite, random_prey]






