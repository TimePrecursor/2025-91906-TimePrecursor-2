import math
import random
import arcade

from Evolution_Game.windows.stage2_files.keyboard_input import GameView1
import Evolution_Game.windows.stage2_files.live_food_stats as live

class PreySprite3(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.change_y = 0
        self.change_x = 0

        from Evolution_Game.windows.stage2_files import keyboard_input
        # gameveiw = keyboard_input.GameView1
        prey_name = keyboard_input.GameView1.getfoodname(keyboard_input.GameView1())
        print(prey_name, "== prey name")
        for x in enumerate(live.live_food_stats):
            if "name" == str(prey_name):
                print("YAY", x)
                y = live.live_food_stats.index()
        prey_data = (x for x in live.live_food_stats if x["name"] == prey_name)
        prey_data = live.live_food_stats[0]
        # if prey_data is None:
        #     raise ValueError(f"Prey data not found for name: {prey_name}")
        # Core stats
        self.name = prey_data["name"]
        self.speed = prey_data["speed"]
        self.awareness = prey_data["awareness"]
        self.nutritional_value = prey_data["nutritional_value"]
        self.health = prey_data["health"]
        self.vision_range = prey_data["vision_range"]
        self.stamina = prey_data["stamina"]
        self.max_stamina = prey_data["stamina"]

        # variables
        self.is_grazing = True

    def update_ai(self, dt):
        """Update AI logic"""
        if self.detect_threats():
            print("LOL")

    def detect_threats(self):
        live_food = live.live_food()
        lol1 = live_food.center_y
        lol2 = live_food.center_x
        print(lol1, "= 'live_food.center_y'")
        from Evolution_Game.windows.stage2_files import keyboard_input
        lol0 = keyboard_input.Player()
        predator_x, predator_y = keyboard_input.Player.get_pos(lol0)
        lol3 = predator_y
        lol4 = predator_x
        distances_xy = [
            lol1 - lol3,
            lol2 - lol4
        ]
        angle_rad = math.atan2(distances_xy[0], distances_xy[1])
        self.angle = angle_rad
        print(angle_rad, "ANGLE")
        # pred_distance = math.sqrt(distances_xy[0] + distances_xy[1])
        # pred_is_vis = (pred_vis_dis > pred_distance)
        # if pred_is_vis:  # and not self.is_fleeing:
        #     self.flee(angle_rad)


    def flee(self):
        pass

    def graze(self):
        pass

