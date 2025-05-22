import math
# from arcade import *
# from arcade import gui
import os
import random


import arcade
from arcade.gui import UIView, UIAnchorLayout
from pyglet.math import clamp
from pyglet.window.key import modifiers_string

# from Evolution_Game.windows.stage2_files.live_food_stats import live_food_functions, live_food_stats_list
import Evolution_Game.windows.stage2_files.live_food_stats as live
from Evolution_Game.windows.stage2_files.environmentSetupMkII import tree_list

# from arcade.gui import UIManager, UIView

SPRITE_SCALING = 0.15

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 600

NORMAL_SPEED = 1

import arcade


class Animal(arcade.Sprite):
    def __init__(self, image, x, y, scale=1.0):
        super().__init__()
        self.image = image
        self.center_x = x
        self.center_y = y
        self.scale = scale
        self.texture = arcade.load_texture(image)
        self.angle = 0
        self.main = GameView1()
    #
    # def update_angle(self, deg):
    #     self.angle = deg
    def get_angle_deg(self, x1, y1, x2, y2):
        dx = x2 - x1
        dy = y2 - y1
        return math.degrees(math.atan2(-dy, dx))

    def detect_threats(self, predpos, preypos):
        x2 = (predpos[0])# - WINDOW_WIDTH/2)
        y2 = (predpos[1])# - WINDOW_HEIGHT/2)
        x1 = preypos[0]
        y1 = preypos[1]

        # Retrieve/Return the angle
        angle = self.get_angle_deg(x1, y1, x2, y2)
        angle_deg = (angle - 90) % 360
        return angle_deg

    def simple_prey_Ai(self, predpos, preypos, prey_spr, pred_spr, prey_sight, awareness):
        angle_deg = self.detect_threats(predpos, preypos)
        distance = arcade.get_distance_between_sprites(prey_spr,pred_spr)
        if distance < (prey_sight*awareness):
            print("PREDATOR DETECTED!")
            game = GameView1()
            game.prey_flee()
            # self.flee(angle_deg)
        self.angle = angle_deg
        return angle_deg






class Player(arcade.Sprite):
    def __init__(self):
        """ Initialize the player sprite """
        super().__init__(scale=0.2)
        self.center_x = 0
        self.center_y = 0
        self.change_y = 0
        self.change_x = 0


class GameView1(UIView):
    def __init__(self):
        super().__init__()
        self.logic_timer = 0.0  # Accumulated time
        self.prey_is_alive = True
        from Evolution_Game.windows.stage2_files.environmentSetupMkII import EnvironmentSetup
        self.environment = EnvironmentSetup()
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        # Variables that will hold sprite lists
        # Set up the player info
        """
        GET RID OF SPRITE LISTS!?
             self.player_sprite = None
        """


        # Track the current state of what key is press
        # self.movementkey_pressed = False
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.shift_pressed = False
        self.ctrl_pressed = False
        self.A_pressed = False
        self.grid = UIAnchorLayout()
        self.manager.add(self.grid)
        self.chosen_animal = None
        self.chosen_prey = None
        # Set the background color
        self.background_color = arcade.color.AMAZON
        self.NO_SETUP = True
        if self.NO_SETUP == False:
            self.setup()
            self.chosen_animal = self.chosen_animal1

    def center_function(self):
        """ central function """
        self.load_image()
        import Evolution_Game.windows.stage2_files.environmentSetupMkII as enviro_setup
        select_randxy = random.choice(enviro_setup.EnvironmentSetup.tree_locations)
        self.animalsprite = Animal(self.filefood_path, select_randxy["center_x"], select_randxy["center_y"], scale=0.15)
        self.player_list.append(self.animalsprite)




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
        self.chosen_prey = random_prey
        self.filefood_path = os.path.join(project_root, "assets", "images", "animal_textures_fixed", f"{random_prey}.png")
        live.live_food(arcade.load_image(self.filefood_path), scale=1)
        # live.live_food.center_x = (select_randxy["center_x"])
        # live.live_food.center_y = (select_randxy["center_y"])

        # keyboard_input.GameView1.renamethis1(keyboard_input.GameView1(),self.filefood_path,100,100)


    def setup(self):
        self.NO_SETUP = True
        """ Set up the game and initialize the variables. """
        self.player_list = arcade.SpriteList()
        # Find the texture
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        cache_file_path = os.path.join(project_root, "windows", "stage2_files", "saved_cache", "cache1.txt")
        with open(cache_file_path, "r") as f:
            line1 = f.readline().rstrip("\n")
            line2 = f.readline().rstrip("\n")
        self.chosen_animal1 = line1
        self.creature_type = line2
        self.cr_index = 0
        # file_path1 = os.path.join(cache_file_path, str(file_val))
        # Set up the player

        self.file_path = os.path.join(project_root, "assets", "images", "animal_textures_fixed", f"{self.chosen_animal1}.png")
        tree_texture_path = self.environment.asset_paths("tree1.png")
        self.environment.create_random_trees(tree_texture_path)

        self.player_sprite = Player()
        self.player_sprite.texture = arcade.load_texture(self.file_path)
        self.player_sprite.scale = 0.15
        # self.player_sprite.center_x = WINDOW_WIDTH/2
        # self.player_sprite.center_y = WINDOW_HEIGHT/2
        self.player_sprite._angle = 0  # Start by facing up (90 degrees)
        self.player_list.append(self.player_sprite)
        # print(self.player_list)

        from Evolution_Game.windows.stage2_files.creature_stats import predator_roles
        creature_type = predator_roles[self.creature_type]
        if creature_type == self.chosen_animal1:
            pass
        elif creature_type != self.chosen_animal1:
            self.cr_index = 1
        self.stamina = (predator_roles[self.creature_type][self.cr_index]["stamina"])
        self.max_stamina = (predator_roles[self.creature_type][self.cr_index]["stamina"])
        self.range = (predator_roles[self.creature_type][self.cr_index]["normal_detectable_range"])
        self.sneak_range = (predator_roles[self.creature_type][self.cr_index]["sneak_detectable_range"])
        self.current_range = self.range
        self.stat_speed = (predator_roles[self.creature_type][self.cr_index]["sprint_speed"])
        self.sprint_speed = self.stat_speed / 2.5
        self.prey_data = live.live_food_stats_list
        # implement metabolism and hunger
        self.metabolism = (predator_roles[self.creature_type][self.cr_index]["metabolism"])
        self.hunger = 100
        self.max_hunger = 100
        self.max_hunger_ratio = (self.hunger/100)
        self.hunger_ratio = self.max_hunger_ratio
        list = ["Stamina:", "Hunger:", f"Metabolism = {self.metabolism}\nSpeed = {round(self.stat_speed,ndigits=1)}\nDetectable Range = {self.range}"]
        self.top_right_info_add(3,list,300,40,bold=False)
        self.center_function()
        self.animal = Animal(self.filefood_path,0,0)
        self.setup_done = True

    def getfoodfile(self):
        return self.filefood_path

    def prey_flee(self):
        self.animalsprite.change_x = 10
        print("LOL")

    def update_player_speed(self): # Speed and Movement processing
        Player.change_x = 0
        Player.change_y = 0
        final_speed = 0

        # Conditions
        condition = (self.up_pressed or self.down_pressed or self.left_pressed or self.right_pressed)
        modifiers_condition = (self.shift_pressed or self.ctrl_pressed)


        # Movement input and stamina/hunger effects
        #MOVEMENT

        a_andnot_b = (self.shift_pressed and not self.ctrl_pressed)

        if a_andnot_b and self.stamina > 20 and self.hunger > 9 and condition:
            final_speed = self.sprint_speed/1.25
            self.stamina -= 0.15
        if a_andnot_b and self.stamina > 10 and self.hunger > 9 and condition:
            final_speed = self.sprint_speed/1.5
            self.stamina -= 0.15
        if self.ctrl_pressed and self.stamina > 20 and self.hunger > 9 and condition:
            final_speed = NORMAL_SPEED/1.5
            self.stamina -= 0.05
        if self.ctrl_pressed and self.stamina > 10 and self.hunger > 9 and condition:
            final_speed = NORMAL_SPEED/2.2
            self.stamina -= 0.1
        if a_andnot_b and self.stamina <= 10 and self.hunger > 9 and condition:
            final_speed = NORMAL_SPEED
        if (not(self.shift_pressed or self.ctrl_pressed)) and self.stamina > 9 and self.hunger > 9 and condition:
            final_speed = NORMAL_SPEED
        if self.ctrl_pressed and self.stamina <= 10 and self.hunger > 9 and condition:
            final_speed = NORMAL_SPEED/2.2
            self.hunger -= 0.1
            self.hunger = clamp(self.hunger, 10, 100)


        # SNEAKING
        # elif self.ctrl_pressed and self.stamina > 20 and self.hunger > 9 and condition:
        #     final_speed = NORMAL_SPEED/2
        #     self.stamina -= 0.2
        # elif self.ctrl_pressed and self.stamina > 10 and self.hunger > 9 and condition:
        #     final_speed = NORMAL_SPEED/2.2
        #     self.stamina -= 0.2

        # elif (not (self.shift_pressed and self.ctrl_pressed)) and self.stamina > 20 and self.hunger > 20 and condition:
        #     final_speed = NORMAL_SPEED

        # NORMAL SPEED
        if ((not (self.shift_pressed or self.ctrl_pressed))or not condition) and self.hunger > 10 and self.stamina < self.max_stamina:
            self.stamina += self.sprint_speed/15
            self.stamina = clamp(self.stamina,10,self.max_stamina)
        # if ((not (self.shift_pressed or self.ctrl_pressed))or not condition) and self.hunger > 10 and self.stamina < self.max_stamina:
            self.hunger -= self.sprint_speed/30
            self.hunger = clamp(self.hunger,10,100)



        if self.up_pressed and (self.player_sprite.center_y < (WINDOW_HEIGHT-50)):
            self.player_sprite.change_y += final_speed
        if self.down_pressed and (self.player_sprite.center_y > 50):
            self.player_sprite.change_y -= final_speed
        if self.left_pressed and (self.player_sprite.center_x > 50):
            self.player_sprite.change_x -= final_speed
        if self.right_pressed and (self.player_sprite.center_x < (WINDOW_WIDTH-50)):
            self.player_sprite.change_x += final_speed



        # Normalize diagonal movement to fix faster diagonal speed
        magnitude = math.hypot(self.player_sprite.change_x, self.player_sprite.change_y)
        if magnitude > final_speed:
            scale = final_speed / magnitude
            self.player_sprite.change_x *= scale
            self.player_sprite.change_y *= scale



        # Set angle manually based on keys
        if self.up_pressed and not self.down_pressed and not self.left_pressed and not self.right_pressed:
            self.player_sprite.angle = 180  # Up
        elif self.down_pressed and not self.up_pressed and not self.left_pressed and not self.right_pressed:
            self.player_sprite.angle = 0  # Down
        elif self.left_pressed and not self.right_pressed and not self.up_pressed and not self.down_pressed:
            self.player_sprite.angle = 90  # Left
        elif self.right_pressed and not self.left_pressed and not self.up_pressed and not self.down_pressed:
            self.player_sprite.angle = 270  # Right
        elif self.up_pressed and self.right_pressed:
            self.player_sprite.angle = 225  # Up-Right
        elif self.up_pressed and self.left_pressed:
            self.player_sprite.angle = 135  # Up-Left
        elif self.down_pressed and self.left_pressed:
            self.player_sprite.angle = 45  # Down-Left
        elif self.down_pressed and self.right_pressed:
            self.player_sprite.angle = 315  # Down-Right


    def on_draw(self):
        """ Render the screen. """
        self.clear()
        tree_list.draw()
        self.player_list.draw()  # Draw player first
        # self.environment.draw_trees()  # Draw trees afterward
        self.manager.draw()  # Draw UI (if you have any)
        max_stam = self.max_stamina
        max_hung = self.max_hunger
        self.draw_hunger_bar(width=max_hung * 2)
        self.draw_stamina_bar(width=max_stam * 4)



    def update_constant_logic(self):
        pred = self.player_sprite
        prey = self.animalsprite
        chsn_prey = self.chosen_prey
        Animal.simple_prey_Ai(self.animal,
                              pred.position,
                              prey.position,
                              prey,
                              pred,
                              self.prey_data[chsn_prey]["vision_range"],
                              self.prey_data[chsn_prey]["awareness"])

    def on_update(self, delta_time):
        """ Movement and game logic """
        self.logic_timer += delta_time
        if self.logic_timer >= 1:
            self.logic_timer = 0.0  # Reset timer
            self.update_constant_logic()
        self.update_player_speed()  # Update speed and rotation here
        self.player_list.update(delta_time)  # Make sure this is updating the sprite



    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""
        if key == arcade.key.UP:
            self.up_pressed = True
            # self.movementkey_pressed = True
            self.update_player_speed()
        if key == arcade.key.DOWN:
            self.down_pressed = True
            # self.movementkey_pressed = True
            self.update_player_speed()
        if key == arcade.key.LEFT:
            self.left_pressed = True
            # self.movementkey_pressed = True
            self.update_player_speed()
        if key == arcade.key.RIGHT:
            self.right_pressed = True
            # self.movementkey_pressed = True
            self.update_player_speed()
        if key == arcade.key.LSHIFT:
            self.shift_pressed = True
            self.update_player_speed()
        if key == arcade.key.A:
            # self.renamethis1()
            # live.live_food_functions.load_image(live.live_food_functions)
            live.live_food()
        if key == arcade.key.LCTRL:
            self.ctrl_pressed = True
            self.current_range = self.sneak_range

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key."""
        if key == arcade.key.UP:
            self.up_pressed = False
            # self.movementkey_pressed = False
            self.update_player_speed()
        if key == arcade.key.DOWN:
            self.down_pressed = False
            # self.movementkey_pressed = False
            self.update_player_speed()
        if key == arcade.key.LEFT:
            self.left_pressed = False
            # self.movementkey_pressed = False
            self.update_player_speed()
        if key == arcade.key.RIGHT:
            self.right_pressed = False
            # self.movementkey_pressed = False
            self.update_player_speed()
        if key == arcade.key.LSHIFT:
            self.shift_pressed = False
            self.update_player_speed()
        if key == arcade.key.A:
            self.A_pressed = False
        if key == arcade.key.LCTRL:
            self.ctrl_pressed = False
            self.current_range = self.range


        #     import Evolution_Game.windows.stage2_files.live_food_stats_list as live
        #     food = live.live_food_functions.load_image(self)
        #     self.player_list.append(food)
        #     # Create references foranaimal sprite
        #
        #     # Create an animal sprite to hunt (will move later):
        #     deer_data = {
        #         "name": live.live_food_stats_list[],
        #         "speed": 7,
        #         "awareness": 6,
        #         "nutritional_value": 8,
        #         "health": 60,
        #         "vision_range": 25,
        #         "stamina": 70
        #     }
        #     deer = PreySprite(deer_data, "deer_image.png")


    def top_right_info_add(self, amount=4, text=None, width=200, height=30, font_size=20, bold=True, y_val=(WINDOW_HEIGHT / 2) - 25):
        self.y2 = 60
        for y in range(amount):
            x = y
            if x > 1:
                x *= 1.5
                font_size /= 1.5
            y = arcade.gui.UILabel(
                font_size=font_size,
                text=text[y],
                height=height,
                width=width,
                bold=bold,
                multiline=True
            )
            self.grid.add(y, align_y=y_val - self.y2*x, align_x=(-WINDOW_WIDTH // 2) + 90)
            self.manager.add(y)
            self.chosen_label = arcade.gui.UILabel(
                font_size=20,
                text=self.chosen_animal1,
                height=20,
                width=200,
                bold=True
            )
            self.grid.add(self.chosen_label, align_y=(WINDOW_HEIGHT / 2) - 25, align_x=0)
            self.manager.add(self.chosen_label)
        """
        #
        # self.health_lab = arcade.gui.UILabel(
        #     font_size=15,
        #     text="Stamina:",
        #     height=40,
        #     width=200,
        #     bold=True
        # )
        # self.grid.add(self.health_lab, align_y=(WINDOW_HEIGHT//2)-25, align_x=(-WINDOW_WIDTH//2)+60)
        # self.manager.add(self.health_lab)
        #
        # self.hunger_lab = arcade.gui.UILabel(
        #     font_size=15,
        #     text="Hunger:",
        #     height=40,
        #     width=200,
        #     bold=True
        # )
        # self.grid.add(self.hunger_lab, align_y=(WINDOW_HEIGHT//2)-85, align_x=(-WINDOW_WIDTH//2)+60)
        # self.manager.add(self.hunger_lab)
        #
        # self.stats_lab = arcade.gui.UILabel(
        #     font_size=12,
        #     text=f"Metabolism = {self.metabolism}\nSpeed = {round(self.stat_speed,ndigits=1)}\nDetectable Range = {self.range}",
        #     height=40,
        #     width=400,
        #     bold=False,
        #     italic=True,
        #     multiline=True
        # )
        # self.grid.add(self.stats_lab, align_x=(-WINDOW_WIDTH // 2) + 100, align_y=(WINDOW_HEIGHT // 2) - 150)
        # self.manager.add(self.stats_lab)
        """
    # def draw_health_bar(self, x=(WINDOW_WIDTH/-2)-100, y=(WINDOW_HEIGHT/2)+200, width=200, height=100):
    def draw_stamina_bar(self, x=(WINDOW_WIDTH // 40), y=WINDOW_HEIGHT - 50, width=None, height=25):
        # Left and right coordinates
        left = x
        right = x + width
        # Correct the Y coordinates
        top = y + height / 2
        bottom = y - height / 2
        # Stamina bar (colored based on health ratio)
        Stamina_ratio = self.stamina / self.max_stamina
        Stamina_right = x + (width * Stamina_ratio)
        color = self.get_Stamina_color()
        arcade.draw_lrbt_rectangle_filled(left, Stamina_right, bottom, top, color)
        # Outline (optional border)
        arcade.draw_lrbt_rectangle_outline(left, right, bottom, top, arcade.color.BLACK, 3)

    def draw_hunger_bar(self, x=(WINDOW_WIDTH // 40), y=WINDOW_HEIGHT - 110, width=None, height=25):
        # Left and right coordinates
        left = x
        right = x + width
        # Correct the Y coordinates
        top = y + height / 2
        bottom = y - height / 2
        # Stamina bar (colored based on a health ratio)
        hunger_ratio = self.hunger / 100
        hunger_right = x + (width * hunger_ratio)
        color = self.get_hunger_color()
        arcade.draw_lrbt_rectangle_filled(left, hunger_right, bottom, top, color)
        # Outline (optional border)
        arcade.draw_lrbt_rectangle_outline(left, right, bottom, top, arcade.color.BLACK, 3)

    def get_Stamina_color(self):
        if self.stamina >= 80:
            return arcade.color.LIGHT_SKY_BLUE
        elif 80 > self.stamina >= 20:
            return arcade.color.YELLOW
        elif self.stamina < 20:
            return arcade.color.RED
        return None

    def get_hunger_color(self):
        if self.hunger >= 80:
            return arcade.color.LIGHT_SKY_BLUE
        elif 80 > self.hunger >= 20:
            return arcade.color.YELLOW
        elif self.hunger < 20:
            return arcade.color.RED
        return None

    # def check_key(self,key):
    #     if key == True:
    #         return True
    #     else:
    #         return False










def main():
    """ Main function """
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT)
    game = GameView1()
    window.show_view(game)
    game.setup()
    arcade.run()



if __name__ == "__main__":
    main()