import arcade
# from arcade import *
# from arcade import gui
import os
import math

from arcade.gui import UIView, UIAnchorLayout, UIGridLayout

from Evolution_Game.depricated_files.files_to_be_added.simpleCreatureSetup1 import creature_setup

# from arcade.gui import UIManager, UIView

SPRITE_SCALING = 0.2

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 600

NORMAL_SPEED = 3


class Player(arcade.Sprite):
    def update(self, delta_time: float = 1 / 60):
        """ Move the player """
        self.center_x += self.change_x
        self.center_y += self.change_y


class GameView(UIView):
    def __init__(self):
        super().__init__()
        from Evolution_Game.windows.stage2_files.environmentSetupMkII import EnvironmentSetup

        self.environment = EnvironmentSetup()

        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        # Variables that will hold sprite lists
        self.player_list = None
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
        self.setup()


    def setup(self):
        """ Set up the game and initialize the variables. """
        self.player_list = arcade.SpriteList()

        # Find the texture
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        cache_file_path = os.path.join(project_root, "windows", "stage2_files", "saved_cache", "cache1.txt")
        with open(cache_file_path, "r") as f:
            file_val = f.readline()
        self.chosen_animal = file_val
        self.top_right_info()
        # file_path1 = os.path.join(cache_file_path, str(file_val))
        # Set up the player

        file_path = os.path.join(project_root, "assets", "images", "animal_textures_fixed", f"{file_val}.png")
        tree_texture_path = self.environment.asset_paths("tree1.png")
        self.environment.create_random_trees(tree_texture_path)

        self.player_sprite = Player(file_path, scale=SPRITE_SCALING)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 50
        self.player_sprite.angle = 0  # Start by facing up (90 degrees)
        self.player_list.append(self.player_sprite)
        # self.otherimports()

    def on_draw(self):
        """ Render the screen. """
        self.clear()
        self.player_list.draw()  # Draw player first
        self.environment.draw_trees()  # Draw trees afterward
        self.manager.draw()  # Draw UI (if you have any)

    def update_player_speed(self):
        self.player_sprite.change_x = 0
        self.player_sprite.change_y = 0

        sprint_speed = 0
        import creature_stats
        creature = str(self.chosen_animal)
        if self.shift_pressed:
            sprint_speed = creature_stats.predator_roles["Speed"][0]["sprint_speed"]

        # Movement input
        final_speed = NORMAL_SPEED + sprint_speed
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
        if magnitude > NORMAL_SPEED:
            scale = NORMAL_SPEED / magnitude
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
            print("Shift pressed")
            self.update_player_speed()

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
            print("Shift released")
            self.update_player_speed()

    # def load_choice(self, file_path):
    #     from Evolution_Game.windows.stage2_files.saved_cache import functions_misc as f
    #     settings = f.functions.load_settings(self,file_path=file_path)
    #     return settings["random_carnivore_choice"]

    def top_right_info(self):
        self.chosen_label = arcade.gui.UILabel(
            # x=10,
            # y=WINDOW_HEIGHT-20,
            font_size=20,
            text=self.chosen_animal,
            height=20,
            width=len(self.chosen_animal)+10,
            bold=True
        )
        self.grid.add(self.chosen_label,align_y=(WINDOW_HEIGHT/2)-25,align_x=0)
        self.manager.add(self.chosen_label)

def main():
    """ Main function """
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT)
    game = GameView()
    game.setup()
    window.show_view(game)
    arcade.run()


if __name__ == "__main__":
    main()