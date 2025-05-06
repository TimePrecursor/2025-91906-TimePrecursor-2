import math
# from arcade import *
# from arcade import gui
import os

import arcade
from arcade.gui import UIView, UIAnchorLayout
from pyglet.math import clamp

from Evolution_Game.windows.stage2_files import prey_AI


# from arcade.gui import UIManager, UIView

SPRITE_SCALING = 0.15

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 600

NORMAL_SPEED = 1

class Player(arcade.Sprite):
    def __init__(self, image, scale):
        """ Initialize the player sprite """
        self.center_x = WINDOW_WIDTH // 2  # Start in the middle of the screen
        self.center_y = WINDOW_HEIGHT // 2
        self.change_y = 0
        self.change_x = 0



class GameView1(UIView):
    def __init__(self):
        super().__init__()
        self.selected_prey = None
        from Evolution_Game.windows.stage2_files.environmentSetupMkII import EnvironmentSetup

        self.environment = EnvironmentSetup()
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        # Variables that will hold sprite lists
        self.player_list = arcade.SpriteList()
        # Set up the player info
        self.player_sprite = None

        # Track the current state of what key is pressed
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.shift_pressed = False

        self.grid = UIAnchorLayout()
        self.manager.add(self.grid)

        # Set the background color
        self.background_color = arcade.color.AMAZON
        # self.setup()


    def setup(self):
        """ Set up the game and initialize the variables. """
        self.player_list = arcade.SpriteList()

        # Find the texture
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        cache_file_path = os.path.join(project_root, "windows", "stage2_files", "saved_cache", "cache1.txt")
        with open(cache_file_path, "r") as f:
            line1 = f.readline().rstrip("\n")
            line2 = f.readline().rstrip("\n")
        self.chosen_animal = line1
        self.creature_type = line2
        self.cr_index = 0
        # file_path1 = os.path.join(cache_file_path, str(file_val))
        # Set up the player

        self.file_path = os.path.join(project_root, "assets", "images", "animal_textures_fixed", f"{self.chosen_animal}.png")
        tree_texture_path = self.environment.asset_paths("tree1.png")
        self.environment.create_random_trees(tree_texture_path)

        self.player_sprite = arcade.Sprite(self.file_path, scale=SPRITE_SCALING)
        # self.player_sprite.center_x = WINDOW_WIDTH/2
        # self.player_sprite.center_y = WINDOW_HEIGHT/2
        self.player_sprite._angle = 0  # Start by facing up (90 degrees)
        self.player_list.append(self.player_sprite)
        print(self.player_list)

        from Evolution_Game.windows.stage2_files.creature_stats import predator_roles
        creature_type = predator_roles[self.creature_type]
        if creature_type == self.chosen_animal:
            pass
        elif creature_type != self.chosen_animal:
            self.cr_index = 1
        self.stamina = (predator_roles[self.creature_type][self.cr_index]["stamina"])
        self.max_stamina = (predator_roles[self.creature_type][self.cr_index]["stamina"])
        self.range = (predator_roles[self.creature_type][self.cr_index]["normal_detectable_range"])
        self.stat_speed = (predator_roles[self.creature_type][self.cr_index]["sprint_speed"])
        self.sprint_speed = self.stat_speed / 2.5
        # implement metabolism and hunger
        self.metabolism = (predator_roles[self.creature_type][self.cr_index]["metabolism"])
        self.hunger = 100
        self.max_hunger = 100
        self.max_hunger_ratio = (self.hunger/100)
        self.hunger_ratio = self.max_hunger_ratio
        list = ["Stamina:", "Hunger:", f"Metabolism = {self.metabolism}\nSpeed = {round(self.stat_speed,ndigits=1)}\nDetectable Range = {self.range}"]
        self.top_right_info_add(3,list,300,40,bold=False)

    def on_draw(self):
        """ Render the screen. """
        self.clear()
        self.player_list.draw()  # Draw player first
        # self.environment.draw_trees()  # Draw trees afterward
        self.manager.draw()  # Draw UI (if you have any)
        max_stam = self.max_stamina
        max_hung = self.max_hunger
        self.draw_hunger_bar(width=max_hung * 2)
        self.draw_stamina_bar(width=max_stam * 4)


    def update_player_speed(self,x=False):
        self.player_sprite.change_x = 0
        self.player_sprite.change_y = 0

        # Movement input and stamina/hunger effects
        if self.shift_pressed and self.stamina > 10 and self.hunger > 10:
            final_speed = self.sprint_speed
            self.stamina -= 0.5
        elif self.shift_pressed and self.stamina > 10 and self.hunger < 20:
            final_speed = self.sprint_speed-1
            self.stamina -= 0.5
        else:
            final_speed = NORMAL_SPEED

        if self.shift_pressed is False and self.stamina < self.max_stamina and self.hunger > 20:
            self.stamina += (self.sprint_speed/2.5)
            self.stamina = clamp(self.stamina,0,self.max_stamina)
            self.hunger -= (self.sprint_speed/3)
            self.hunger = clamp(self.hunger,0,100)


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

    def on_update(self, delta_time):
        """ Movement and game logic """
        predator = self.player_sprite
        prey_AI.PreySprite.update_ai(self=prey_AI.PreySprite, dt=delta_time, predators=self.player_sprite)
        self.update_player_speed()  # Update speed and rotation here
        self.player_list.update(delta_time)  # Make sure this is updating the sprite


    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""
        if key == arcade.key.UP:
            self.up_pressed = True
            self.update_player_speed()
        elif key == arcade.key.DOWN:
            self.down_pressed = True
            self.update_player_speed()
        elif key == arcade.key.LEFT:
            self.left_pressed = True
            self.update_player_speed()
        elif key == arcade.key.RIGHT:
            self.right_pressed = True
            self.update_player_speed()
        elif key == arcade.key.LSHIFT:
            self.shift_pressed = True
            self.update_player_speed(x=True)
        elif key == arcade.key.A:
            self.create_references()
        #     import Evolution_Game.windows.stage2_files.live_food_stats as live
        #     food = live.live_food_functions.load_image(self)
        #     self.player_list.append(food)
        #     # Create references foranaimal sprite
        #
        #     # Create an animal sprite to hunt (will move later):
        #     deer_data = {
        #         "name": live.live_food_stats[],
        #         "speed": 7,
        #         "awareness": 6,
        #         "nutritional_value": 8,
        #         "health": 60,
        #         "vision_range": 25,
        #         "stamina": 70
        #     }
        #     deer = PreySprite(deer_data, "deer_image.png")

    def create_references(self):
        import Evolution_Game.windows.stage2_files.live_food_stats as live
        food = live.live_food_functions.load_image(self)
        self.player_list.append(food[0])

        # Create references for an animal sprite and
        # create an animal sprite to hunt (will move later):
        for x in live.live_food_stats:
            if x["name"] == food[1]:
                # name = x["name"]
                # speed = x["speed"]
                # awareness = x["awareness"]
                # nutritional_value = x["nutritional_value"]
                # health = x["health"]
                # vision_range = x["vision_range"]

                # deer_data = {
                #     "name": x["name"],
                #     "speed": x["speed"],
                #     "awareness": x["awareness"],
                #     "nutritional_value": x["nutritional_value"],
                #     "health": x["health"],
                #     "vision_range": x["vision_range"],
                #     "stamina": 70
                # }
                self.selected_prey = prey_AI.PreySprite(image_file=f"{self.file_path}",predator=self.player_list[0])



    def on_key_release(self, key, modifiers):
        """Called when the user releases a key."""
        if key == arcade.key.UP:
            self.up_pressed = False
            self.update_player_speed()
        elif key == arcade.key.DOWN:
            self.down_pressed = False
            self.update_player_speed()
        elif key == arcade.key.LEFT:
            self.left_pressed = False
            self.update_player_speed()
        elif key == arcade.key.RIGHT:
            self.right_pressed = False
            self.update_player_speed()
        elif key == arcade.key.LSHIFT:
            self.shift_pressed = False
            self.update_player_speed()


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
                text=self.chosen_animal,
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
        # Stamina bar (colored based on health ratio)
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

    def get_hunger_color(self):
        if self.hunger >= 80:
            return arcade.color.LIGHT_SKY_BLUE
        elif 80 > self.hunger >= 20:
            return arcade.color.YELLOW
        elif self.hunger < 20:
            return arcade.color.RED

    def check_key(self,key):
        if key == True:
            return True
        else:
            return False










def main():
    """ Main function """
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT)
    game = GameView1()
    game.setup()
    window.show_view(game)
    arcade.run()


if __name__ == "__main__":
    main()