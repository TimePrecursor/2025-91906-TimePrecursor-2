import math
import random
import arcade
from conda.instructions import PRINT

from Evolution_Game.windows.stage2_files.keyboard_input import GameView1


class animalSprite(arcade.Sprite):
    pass

class PreySprite2:
    def __init__(self):
        super().__init__()
        self.center_x = 1000 // 2  # Start in the middle of the screen
        self.center_y = 600 // 2
        self.prey_x = self.center_x
        self.prey_y = self.center_y
        self.change_y = 0
        self.change_x = 0
        import Evolution_Game.windows.stage2_files.live_food_stats as live
        from Evolution_Game.windows.stage2_files import keyboard_input
        gameveiw = GameView1()
        prey_name = keyboard_input.GameView1.getfoodname(gameveiw)
        print(prey_name, "== prey name")
        for x in enumerate(live.live_food_stats):
            if "name" == str(prey_name):
                print("YAY",x)
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



        # AI behavior
        self.is_fleeing = False
        self.is_grazing = False
        self.flee_direction = (0, 0)
        self.alert_timer = 0
        self.graze_timer = random.uniform(3.0, 6.0)
        from Evolution_Game.windows.stage2_files.keyboard_input import Player as currentPred
        self.predator = currentPred

    # @property
    # def center_x(self) -> float:
    #     """Get or set the center x position of the sprite."""
    #     return self._position[0]
    #
    # @center_x.setter
    # def center_x(self, new_value: float):
    #     if new_value == self._position[0]:
    #         return
    #
    #     self.position = (new_value, self._position[1])
    #
    # @property
    # def center_y(self) -> float:
    #     """Get or set the center y position of the sprite."""
    #     return self._position[1]
    #
    # @center_y.setter
    # def center_y(self, new_value: float):
    #     if new_value == self._position[1]:
    #         return
    #
    #     self.position = (self._position[0], new_value)

    def update_ai(self, dt, detec_range):
        """Update AI logic"""
        prey_ = PreySprite2()
        graze_ = prey_.is_grazing
        if self.detect_threats(pred_vis_dis=detec_range):
            self.flee(dt)
        elif graze_ is False and random.randint(0,10) == 1:
            self.graze()
            graze_ = True

    def flee(self, angle):
        self.angle = angle
        self.is_fleeing = True

    def detect_threats(self, pred_vis_dis=None):
        from Evolution_Game.windows.stage2_files.keyboard_input import Player as currentPred
        prey_y = animalSprite()
        lol1 = prey_y.center_y
        lol2 = prey_y.center_x
        from Evolution_Game.windows.stage2_files import keyboard_input
        lol0 = keyboard_input.Player()
        predator_x, predator_y = keyboard_input.Player.get_pos(lol0)
        lol3 = predator_y
        lol4 = predator_x
        distances_xy = [
            lol3 - lol1,
            lol4 - lol2]
        self.predator = currentPred
        angle_rad = math.atan2(distances_xy[0], distances_xy[1])
        self.angle = angle_rad
        # pred_distance = math.sqrt(distances_xy[0]+distances_xy[1])
        # pred_is_vis = (pred_vis_dis > pred_distance)
        # if pred_is_vis:# and not self.is_fleeing:
        #     self.flee(angle_rad)

    def graze(self):
        pass


    # def detect_threats(self, predator):
    #     """Check for threats within vision"""
    #     # Use center_x and center_y directly for both sprites
    #     distance = self.custom_get_distance(self,sprite1=PreySprite2,sprite2=predator)
    #     if distance <= self.vision_range:
    #         self.is_fleeing = True
    #         self.alert_timer = 5.0
    #         dx = self.center_x - predator.center_x
    #         dy = self.center_y - predator.center_y
    #         magnitude = math.hypot(dx, dy) or 1
    #         self.flee_direction = (dx / magnitude, dy / magnitude)
    #         return True
    #     return False
    #
    #
    # def _flee(self, dt):
    #     if self.stamina > 0:
    #         self.stamina -= dt * 10
    #         speed = self.speed * 2.0
    #         dx, dy = self.flee_direction
    #         self.change_x = dx * speed
    #         self.change_y = dy * speed
    #     else:
    #         self.is_fleeing = False
    #
    # def _graze(self, dt):
    #     self.graze_timer -= dt
    #     if self.graze_timer <= 0:
    #         # Pick a random slow movement direction
    #         angle = random.uniform(0, 2 * math.pi)
    #         self.change_x = math.cos(angle) * self.speed * 0.3
    #         self.change_y = math.sin(angle) * self.speed * 0.3
    #         self.graze_timer = random.uniform(3.0, 6.0)



