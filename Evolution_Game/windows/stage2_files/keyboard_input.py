import getpass
import math
# from arcade import *
# from arcade import gui
import os
import pathlib
import json
import random
import datetime

import numpy


import arcade
from arcade.gui import UIView, UIAnchorLayout
from pycparser.c_ast import Return
from pyglet.math import clamp
from pyglet.window.key import modifiers_string

# from Evolution_Game.windows.stage2_files.live_food_stats import live_food_functions, live_food_stats_list
import Evolution_Game.windows.stage2_files.live_food_stats as live
from Evolution_Game.windows.stage2_files.environmentSetupMkII import tree_list

# from arcade.gui import UIManager, UIView
import time
SPRITE_SCALING = 0.15

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 600

NORMAL_SPEED = 1

import arcade


class Animal(arcade.Sprite):
    def __init__(self, image, x, y, scale=1.0, game_view=None):
        super().__init__()
        self.image = image
        self.center_x = x
        self.center_y = y
        self.scale = scale
        self.texture = arcade.load_texture(image)
        self.angle = 0
        self.fleeing = False
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

    def simple_prey_Ai(self, predpos, preypos, prey_spr, pred_spr, prey_sight, range):
        angle_deg = self.detect_threats(predpos, preypos)
        distance = arcade.get_distance_between_sprites(prey_spr,pred_spr)


        if distance < ((range*1.5)*prey_sight)/5:
            self.fleeing = True
            game = GameView1()
            changex,changey = self.get_adj_and_opp(angle_deg,10)
            game.prey_flee(prey_spr, angle_deg, changex, changey)
            return True
        else:
            # self.wander(prey_spr)
            return False


    def get_adj_and_opp(self,angle_degrees, h):
        angle_radians = math.radians(angle_degrees)
        opposite = h * math.sin(angle_radians)
        adjacent = h * math.cos(angle_radians)
        return [opposite,adjacent]

    # def wander(self,prey_spr):
    #     x = numpy.random.normal(scale=1)
    #     print(x)
    #     y = random.choice(["x","y"])
    #     if y == "x":
    #         prey_spr.change_x += x/10
    #     if y == "y":
    #         prey_spr.change_y += x/10


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
        self.username = "None"
        self.logic_timer = 0.0  # Accumulated time
        self.prey_logic_timer = 0  # Accumulated time
        self.alivetimer = 0.0
        self.kills = 0
        self.prey_is_alive = True
        from Evolution_Game.windows.stage2_files.environmentSetupMkII import EnvironmentSetup
        self.environment = EnvironmentSetup()
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.physic_engine = None
        # Track the current state of what key is press
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
        self.fleeing = False
        # Set the background color
        self.background_color = arcade.color.AMAZON
        self.NO_SETUP = True
        self.spawning_prey = False

    def center_function(self):
        """ central function """
        import Evolution_Game.windows.stage2_files.environmentSetupMkII as enviro_setup
        select_randxy = random.choice(enviro_setup.EnvironmentSetup.tree_locations)
        self.animalsprite = Animal(self.filefood_path, select_randxy["center_x"], select_randxy["center_y"], scale=0.15,
                                   game_view=self)
        self.player_list.append(self.animalsprite)

    def load_image(self):
        self.prey_choices = []
        project_root = pathlib.Path(__file__).resolve().parents[2]  # adjust if needed

        # Cache JSON file path
        self.cache_file_path = project_root / "windows" / "stage2_files" / "saved_cache" / "fifo.json"
        self.save_path = project_root / "windows" / "stage2_files" / "secrets" / "logins.json"



        if os.path.getsize(self.cache_file_path) > 0:
            with open(self.cache_file_path, "r") as f:
                data = json.load(f)
                print(data)
        else:
            print("JSON file is empty!")
            data = {}


        # Load JSON cache safely
        if self.cache_file_path.exists():
            with open(self.cache_file_path, "r") as f:
                data = json.load(f)

            # Access the "prey" list
            prey_list = data.get("prey", [])  # Use .get() for safety
            print(prey_list)
            # try:
                #     cache = json.load(cf)
                #     self.fifo = cache.get("prey", [])
                #     print(self.fifo)
                # except json.JSONDecodeError:
                #     self.fifo = []
                #     print("failed3")
        # else:
        #     self.fifo = []
        #     print("failed4")

        # Collect prey from all entries in fifo cache
        # for entry in self.fifo:
        # prey_list = self.fifo.get("prey")
        print(prey_list)
        # Add each prey to prey_choices list
        self.prey_choices.extend(prey_list)

        # Remove duplicates if you want (optional)
        self.prey_choices = list(set(self.prey_choices))
        #
        # if not self.prey_choices:
        #     # Fallback if no prey found, choose default or empty
        #     self.prey_choices = ["debug"]

        # Choose random prey from list
        random_prey = random.choice(self.prey_choices)
        self.chosen_prey = random_prey

        # Build path to the prey image
        self.filefood_path = os.path.join(project_root, "assets", "images", "animal_textures_fixed",
                                          "pig.png")

    import json

    def setup(self):
        self.setupdone = True
        self.player_list = arcade.SpriteList()

        project_root = pathlib.Path(__file__).resolve().parents[2]  # go up 2 levels
        cache_file_path = project_root / "windows" / "stage2_files" / "saved_cache" / "fifo.json"

        # Load the JSON cache properly
        if cache_file_path.exists():
            with open(cache_file_path, "r") as f:
                cache_data = json.load(f)
            fifo_cache = cache_data.get("fifo_cache", [])

            if fifo_cache:
                # Get the last entry or first, depending on your FIFO usage
                last_entry = fifo_cache # or fifo_cache[0]
                try:
                    self.chosen_animal1 = fifo_cache.get("creature_name", "")
                    print(self.chosen_animal1)
                    self.creature_type = fifo_cache.get("creature_type", "")
                    print(self.creature_type)
                except:
                    print("nope1")
                finally:
                    print("yep1")
            else:
                self.chosen_animal1 = "debug"
                self.creature_type = "debug"
                print("nope2")
        else:
            self.chosen_animal1 = "debug"
            self.creature_type = "debug"
            print("nope3")

        # Rest of your code (finding creature data, setting up sprites etc.)
        # ...

        # Find the correct creature index in the predator_roles list based on chosen_animal1 name
        from Evolution_Game.windows.stage2_files.creature_stats import predator_roles
        creature_list = predator_roles.get(self.creature_type, [])

        for i, creature in enumerate(creature_list):
            if creature["name"] == self.chosen_animal1:
                self.cr_index = i
                break

        # Use the creature data for stats
        if creature_list:
            creature_data = creature_list[self.cr_index]

            self.stamina = creature_data["stamina"]
            self.max_stamina = creature_data["stamina"]
            self.range = creature_data["normal_detectable_range"]
            self.sneak_range = creature_data["sneak_detectable_range"]
            self.current_range = self.range
            self.stat_speed = creature_data["sprint_speed"]
            self.sprint_speed = self.stat_speed / 2.5
            self.metabolism = creature_data["metabolism"]
            # self.nutritional_value = self.prey_data[self.chosen_prey]["nutritional_value"]
            self.nutritional_value = creature_data["nutritional_value"]
        else:
            # Fallback defaults if something’s missing
            self.stamina = 50
            self.max_stamina = 50
            self.range = 30
            self.sneak_range = 15
            self.current_range = self.range
            self.stat_speed = 5
            self.sprint_speed = self.stat_speed / 2.5
            self.metabolism = 7
            self.nutritional_value = 50

        # Set file path for player texture
        self.file_path = os.path.join(project_root, "assets", "images", "animal_textures_fixed",
                                      f"{self.chosen_animal1}.png")

        # Setup environment
        tree_texture_path = self.environment.asset_paths("tree1.png")
        self.environment.create_random_trees(tree_texture_path)

        # Create player sprite
        self.player_sprite = Player()
        self.player_sprite.texture = arcade.load_texture(self.file_path)
        self.player_sprite.scale = 0.15
        self.player_sprite._angle = 0  # Start facing up
        self.player_list.append(self.player_sprite)

        # Create animal sprite at random location
        import Evolution_Game.windows.stage2_files.environmentSetupMkII as enviro_setup
        select_randxy = random.choice(enviro_setup.EnvironmentSetup.tree_locations)
        self.load_image()

        self.animalsprite = Animal(self.filefood_path, select_randxy["center_x"], select_randxy["center_y"], scale=0.15,
                                   game_view=self)
        self.player_list.append(self.animalsprite)

        # Load other data related to prey
        self.prey_data = live.live_food_stats_list

        self.animal = Animal(self.filefood_path, 0, 0)
        # Setup hunger and stamina info display
        self.hunger = 100
        self.max_hunger = 100
        self.max_hunger_ratio = (self.hunger / 100)
        self.hunger_ratio = self.max_hunger_ratio

        info_list = [
            "Stamina:",
            "Hunger:",
            f"Metabolism = {self.metabolism}\nSpeed = {round(self.stat_speed, 1)}\nDetectable Range = {self.range}"
        ]
        self.top_right_info_add(3, info_list, 300, 40, bold=False)

        self.setupdone = True

    def getfoodfile(self):
        return self.filefood_path

    def prey_flee(self, prey_spr, angle, changex, changey):
        """ The 'Flee' mechanic for prey """
        angle -= 180
        prey_spr.angle = angle
        
        # Get current position
        current_x = prey_spr.center_x
        current_y = prey_spr.center_y
        
        # Calculate potential new position
        new_x = current_x + changex/5
        new_y = current_y + changey/5
        
        # Check boundaries and adjust movement
        if new_x < 50:  # Left boundary
            prey_spr.change_x = abs(changex/5)  # Move right
        elif new_x > WINDOW_WIDTH - 50:  # Right boundary
            prey_spr.change_x = -abs(changex/5)  # Move left
        else:
            prey_spr.change_x = changex/5
        
        if new_y < 50:  # Bottom boundary
            prey_spr.change_y = abs(changey/5)  # Move up
        elif new_y > WINDOW_HEIGHT - 50:  # Top boundary
            prey_spr.change_y = -abs(changey/5)  # Move down
        else:
            prey_spr.change_y = changey/5

    def check_bounds(self, pos) -> bool:
        if ((pos[0] > 80) and (pos[1] > 80)) and (pos[0] < WINDOW_WIDTH-10) and (pos[1] < WINDOW_HEIGHT-10):
            return True
        else:
            return False

    def stopflee(self,prey_spr):
        prey_spr.change_y = 0
        prey_spr.change_x = 0
        self.fleeing = False

    import math

    def update_player_speed(self):
        # Add stamina regeneration rate as a class attribute
        self.stamina_regen_rate = self.sprint_speed / 15
        self.hunger_decay_rate = self.sprint_speed / 30
        
        # Add stamina penalty when hungry
        if self.hunger < 30:
            self.stamina_regen_rate *= 0.5  # Slower stamina regen when hungry

        # Speed and Movement processing
        move_x = 0
        move_y = 0
        final_speed = 0

        # Movement condition
        condition = (self.up_pressed or self.down_pressed or self.left_pressed or self.right_pressed)
        a_andnot_b = (self.shift_pressed and not self.ctrl_pressed)

        # Movement input and stamina/hunger effects
        if a_andnot_b and self.stamina > 20 and self.hunger > 9 and condition:
            final_speed = self.sprint_speed
            self.stamina -= 0.15
        elif a_andnot_b and self.stamina > 10 and self.hunger > 9 and condition:
            final_speed = self.sprint_speed
            self.stamina -= 0.15
        elif self.ctrl_pressed and self.stamina > 20 and self.hunger > 9 and condition:
            final_speed = NORMAL_SPEED / 1.5
            self.stamina -= 0.05
        elif self.ctrl_pressed and self.stamina > 10 and self.hunger > 9 and condition:
            final_speed = NORMAL_SPEED / 1.5
            self.stamina -= 0.1
        elif a_andnot_b and self.stamina <= 10 and self.hunger > 9 and condition:
            final_speed = NORMAL_SPEED * 1.2
        elif not (self.shift_pressed or self.ctrl_pressed) and self.stamina > 9 and self.hunger > 9 and condition:
            final_speed = NORMAL_SPEED * 1.5
        elif self.ctrl_pressed and self.stamina <= 10 and self.hunger > 9 and condition:
            final_speed = NORMAL_SPEED / 2.5
            self.hunger -= 0.1
            self.hunger = clamp(self.hunger, 10, 100)

        # Regenerate stamina/hunger if not sprinting
        if not (self.shift_pressed or self.ctrl_pressed) or not condition:
            if self.hunger > 10 and self.stamina < self.max_stamina:
                self.stamina += self.sprint_speed / 15
                self.stamina = clamp(self.stamina, 10, self.max_stamina)
                self.hunger -= (self.metabolism ** 1.75) / 10
                self.hunger = clamp(self.hunger, 10, 100)

        # Raw movement input (no clamping yet)
        if self.up_pressed and self.player_sprite.center_y < (WINDOW_HEIGHT - 50):
            move_y += 1
        if self.down_pressed and self.player_sprite.center_y > 50:
            move_y -= 1
        if self.left_pressed and self.player_sprite.center_x > 50:
            move_x -= 1
        if self.right_pressed and self.player_sprite.center_x < (WINDOW_WIDTH - 50):
            move_x += 1

        # Normalize direction vector
        magnitude = math.hypot(move_x, move_y)
        if magnitude > 0:
            move_x /= magnitude
            move_y /= magnitude

        # Apply final movement
        self.player_sprite.change_x = move_x * final_speed
        self.player_sprite.change_y = move_y * final_speed

        # Set angle manually
        if move_x == 0 and move_y > 0:
            self.player_sprite.angle = 180  # Up
        elif move_x == 0 and move_y < 0:
            self.player_sprite.angle = 0  # Down
        elif move_x < 0 and move_y == 0:
            self.player_sprite.angle = 90  # Left
        elif move_x > 0 and move_y == 0:
            self.player_sprite.angle = 270  # Right
        elif move_x > 0 and move_y > 0:
            self.player_sprite.angle = 225  # Up-Right
        elif move_x < 0 and move_y > 0:
            self.player_sprite.angle = 135  # Up-Left
        elif move_x < 0 and move_y < 0:
            self.player_sprite.angle = 45  # Down-Left
        elif move_x > 0 and move_y < 0:
            self.player_sprite.angle = 315  # Down-Right

    def on_draw(self):
        """ Render the screen. """
        self.clear()
        tree_list.draw()
        self.player_list.draw()  # Draw player first
        self.manager.draw()  # Draw UI (if you have any)
        max_stam = self.max_stamina
        max_hung = self.max_hunger
        self.draw_hunger_bar(width=max_hung * 2)
        self.draw_stamina_bar(width=max_stam * 4)


    def update_constant_logic(self):
        pred = self.player_sprite
        prey = self.animalsprite
        chsn_prey = self.chosen_prey
        if Animal.simple_prey_Ai(self.animal,
          pred.position,
          prey.position,
          prey,
          pred,
          self.prey_data[chsn_prey]["vision_range"],
          # self.prey_data[chsn_prey]["awareness"],
          self.current_range):
            self.fleeing = True
        if self.hunger < 30:
            self.player_died()

    def load_cache_username(self):
        project_root = pathlib.Path(__file__).resolve().parents[4]  # go up 2 levels
        self.cache_file_path = project_root  / "windows" / "stage2_files" / "saved_cache" / "fifo.json"
        print(self.cache_file_path)
        if self.cache_file_path.exists():
            with open(self.cache_file_path, 'r') as f:
                return json.load(f)
        else:
            return "none"
    #
    # # Load cache
    # def load_cache(self):
    #     if self.cache_file.exists():
    #         with self.cache_file.open("r") as f:
    #             return json.load(f)
    #     return {"fifo_cache": []}
    #
    # # Save cache
    # def save_cache(self,cache):
    #     self.cache_file_path.parent.mkdir(parents=True, exist_ok=True)
    #     with self.cache_file_path.open("w") as f:
    #         json.dump(cache, f, indent=4)
    #
    # # Add play session to FIFO cache
    # def add_play_session(self,creature_name, creature_type, prey_list):
    #     cache = self.load_cache()
    #     fifo = cache.get("fifo_cache", [])
    #
    #     entry = {
    #         "creature_name": creature_name,
    #         "creature_type": creature_type,
    #         "prey": prey_list,
    #         "username": self.username
    #     }
    #
    #     fifo.append(entry)
    #
    #     # Enforce FIFO size limit
    #     if len(fifo) > 2:
    #         fifo.pop(0)
    #
    #     cache["fifo_cache"] = fifo
    #     self.save_cache(cache)
    #
    #     print(f"Added creature: {creature_name} | Current FIFO ({len(fifo)}):")
    #     for e in fifo:
    #         print("-", e["creature_name"], "by", e["username"])
    #
    # def player_died(self):
    #     project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    #     logins_path = os.path.join(project_root, "windows", "stage2_files", "secrets", "logins.json")
    #     self.username = self.load_cache_username()
    #     item = self.username.text
    #     cache = self.load_cache()
    #     fifo = cache.get("fifo_cache", [])
    #
    #     fifo.append(item)  # Add to end (newest)
    #     if len(fifo) > 2:
    #         fifo.pop(0)  # Remove oldest (first)
    #
    #     cache["fifo_cache"] = fifo
    #     self.save_cache(cache)
    #
    #     print(f"Added: {item}")
    #     print("Current FIFO:", fifo)
    #     with open(logins_path,"a+") as logins:
    #         logins.write(f'Date: {time.strftime("%Y-%m-%d %H:%M:%S")}'
    #                      f' | Username: {self.username} | Creature: {self.chosen_animal1}'
    #                      f' | Score: {round(self.alivetimer, 1)} | Kills: {self.kills}\n')
    #     arcade.exit()

    def load_cache(self):
        if self.cache_file_path.exists():
            with self.cache_file_path.open("r") as f:
                return json.load(f)
        return {"fifo_cache": []}

    # Save cache
    def save_cache(self,cache):
        self.cache_file_path.parent.mkdir(parents=True, exist_ok=True)
        with self.cache_file_path.open("w") as f:
            json.dump(cache, f, indent=4)

    def player_died(self):
        # Make sure the save folder exists
        self.save_path.parent.mkdir(parents=True, exist_ok=True)

        # Load existing cache or initialize
        if self.save_path.exists():
            with open(self.save_path, "r") as f:
                try:
                    cache = json.load(f)
                except json.JSONDecodeError:
                    cache = {"logins": []}
        else:
            cache = {"logins": []}

        fifo = cache.get("logins", [])

        # Build log entry

        new_entry = {
            "creature_name": self.chosen_animal1,
            "creature_type": self.creature_type,
            "prey": [self.chosen_prey] if self.chosen_prey else [],
            "username": self.load_cache_username() if self.username != "None" else getpass.getuser(),
            "time_of_death": time.strftime("%Y-%m-%d %H:%M:%S"),
            "time_alive": round(self.alivetimer, 1),
            "kills": self.kills
        }

        fifo.append(new_entry)

        # Optional: enforce a limit
        MAX_SIZE = 10
        if len(fifo) > MAX_SIZE:
            fifo.pop(0)

        cache["logins"] = fifo

        # Save to disk
        print("Writing to file:", self.save_path)  # Debug print
        with open(self.save_path, "w") as f:
            json.dump(cache, f, indent=4)
            print("File saved.")

        arcade.exit()

    def on_update(self, delta_time):
        debugvarnum = 0
        # try:
        debugvarnum += 1
        print(debugvarnum)
        if self.setupdone is True:
            """ Movement and game logic """
            self.logic_timer += delta_time
            self.alivetimer += delta_time
            debugvarnum += 1
            print(debugvarnum)
            if self.logic_timer >= 0.1 and not self.fleeing:
                self.update_constant_logic()
                self.logic_timer = 0.0
                debugvarnum += 1
                print(debugvarnum)
            if self.fleeing:
                self.prey_logic_timer += 1
                debugvarnum += 1
                print(debugvarnum)
                if self.prey_logic_timer >= 80:
                    self.stopflee(self.animalsprite)
                    self.fleeing = False
                    self.prey_logic_timer = 0
                    debugvarnum += 1
                    print(debugvarnum)
            # if self.spawning_prey:
            #     self.spawnprey_Timer += 1
            #     if self.spawnprey_Timer >= 20:
            #         self.center_function()
            #         self.spawning_prey = False
            #         self.spawnprey_Timer = 0

            self.update_player_speed()  # Update speed and rotation here
            self.player_list.update(delta_time)  # Make sure this is updating the sprite
            self.check_prey_collision()
            print("worked1")
        # except:
        #     print("failed1")
        #     print("AttributeError: 'GameView1' object has no attribute 'setupdone'")


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
        # if key == arcade.key.A:
            # self.renamethis1()
            # live.live_food_functions.load_image(live.live_food_functions)
            # live.live_food()
        if key == arcade.key.LCTRL:
            self.ctrl_pressed = True
            self.current_range = self.sneak_range

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key."""
        if key == arcade.key.UP:
            self.up_pressed = False
            self.update_player_speed()
        if key == arcade.key.DOWN:
            self.down_pressed = False
            self.update_player_speed()
        if key == arcade.key.LEFT:
            self.left_pressed = False
            self.update_player_speed()
        if key == arcade.key.RIGHT:
            self.right_pressed = False
            self.update_player_speed()
        if key == arcade.key.LSHIFT:
            self.shift_pressed = False
            self.update_player_speed()
        if key == arcade.key.A:
            self.A_pressed = False
        if key == arcade.key.LCTRL:
            self.ctrl_pressed = False

    def on_show_view(self):
        self.setup()

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

    def remove_prey(self):
        # Remove the prey and update hunger
        self.hunger = min(self.max_hunger, self.hunger + self.nutritional_value)

        # Remove prey from sprite lists
        self.player_list.remove(self.animalsprite)
        self.center_function()
        # self.spawning_prey = True

    def check_prey_collision(self):
        hit_list = arcade.check_for_collision_with_list(
            self.animalsprite,
            self.player_list
        )
        hit_list = arcade.check_for_collision(
            self.animalsprite,
            self.player_sprite)

        # Handle each collision
        if hit_list:
            self.kills += 1
            self.remove_prey()