import random

import arcade
import os
from arcade.gui import UIView

from Evolution_Game.windows.stage2_files import keyboard_input

live_food_stats_list = [
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
    def __init__(self,image=None, scale=1, window_width=1000,window_height=600):
        """ Initialize the live food sprite """
        super().__init__(image, scale)
        self.center_x = window_width // 2 # Start in the middle of the screen
        self.center_y = window_height // 2
        self.change_x = 0
        self.change_y = 0

class live_food_functions():
    def __init__(self):
        super().__init__()
    def load_image(self):
        self.prey_choices = []
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        cache_file = os.path.join(project_root, "windows", "stage2_files", "saved_cache", "cache1.txt")
        with open(cache_file, "r") as cf:
            for line in cf.readlines():
                if line.startswith("|"):
                    line.rstrip("\n")
                    line.lstrip("|")
                    self.prey_choices = line.split("|")
                else:
                    pass
                    # print() # line Break in terminal

        self.prey_choices.pop(0)
        random_prey = random.choice(self.prey_choices)
        file_path = os.path.join(project_root, "assets", "images", "animal_textures_fixed", f"{random_prey}.png")
        # print(file_path)
        live_food(arcade.load_image(file_path), scale=1)
        import Evolution_Game.windows.stage2_files.environmentSetupMkII as enviro_setup
        # print(enviro_setup.EnvironmentSetup.tree_locations)
        select_randxy = random.choice(enviro_setup.EnvironmentSetup.tree_locations)
        # print(select_randxy, "select_randxy")
        live_food.center_x = (select_randxy["center_x"])
        live_food.center_y = (select_randxy["center_y"])
        live_food.angle = 45

        # keyboard_input.GameView1.renamethis1(keyboard_input.GameView1(),file_path,100,100)





