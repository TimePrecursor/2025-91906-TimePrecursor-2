import math
import random
import arcade


import Evolution_Game.windows.stage2_files.live_food_stats as live


def detect_threats(x,y):
    # print(lol1, "= 'live_food.center_y'")
    from Evolution_Game.windows.stage2_files import keyboard_input
    lol0 = keyboard_input.Player()
    predator_x, predator_y = keyboard_input.Player.get_pos(lol0)
    lol3 = predator_y
    lol4 = predator_x
    # print(predator_y,predator_x)
    distances_xy = [
        x - lol3,
        y - lol4
    ]
    angle_rad = math.atan2(distances_xy[0], distances_xy[1])
    # print(angle_rad, "ANGLE")
    # pred_distance = math.sqrt(distances_xy[0] + distances_xy[1])
    # pred_is_vis = (pred_vis_dis > pred_distance)
    # if pred_is_vis:  # and not self.is_fleeing:
    #     self.flee(angle_rad)


class PreySprite3:
    def __init__(self):
        super().__init__()

        from Evolution_Game.windows.stage2_files import keyboard_input
        lol2 = keyboard_input.GameView1.getfoodname(keyboard_input.GameView1())
        print(lol2)
        print(prey_name, "== prey name")
        for x in enumerate(live.live_food_stats_list):
            if "name" == str(prey_name):
                print("YAY", x)
                y = live.live_food_stats_list.index()
        prey_data = (x for x in live.live_food_stats_list if x["name"] == prey_name)
        prey_data = live.live_food_stats_list[0]
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

    def update_ai(self, dt, x=0, y=0):
        """Update AI logic"""
        if detect_threats(x,y):
            print("LOL")

    def flee(self):
        pass

    def graze(self):
        pass

