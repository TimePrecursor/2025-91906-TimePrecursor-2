codeVersion= "1.049"

import arcade
from arcade.gui import *
from arcade import gui
import os


WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = f"Evolution Game V{codeVersion}"




# The texture will only be loaded during the first sprite creation

class GameView(arcade.View):
    """
    Main application class.

    1.0 NOTE: I have already programmed most necessary functions
    that will allow the user to play.
    """

    def __init__(self):
        super().__init__()

        # setting up window variables:
        self.background_color = arcade.color.AMAZON
        # self.grid = UIGridLayout(
        #     column_count=3,
        #     row_count=4,
        #     size_hint=(0, 0),
        #     vertical_spacing=10,
        #     horizontal_spacing=10,
        # )
        # self.box = arcade.gui.UIGridLayout()
        self.box = arcade.gui.UIBoxLayout()

        sprite_list = {
            "CarnivoreFinal2.png" : [0,"carnivore_sprite"],
            "HerbivoreFinal2.png" : [1,"herbivore_sprite"],
            "DecomposerFinal2.png" : [2,"decomposer_sprite"]
        }
        # If I have sprites, I will create them here
        # This may help:
        # ac.sprite_creation(self,name.png",1,1)
        # The offset percent default is 1 AKA (100%)
        self.sprites = arcade.SpriteList()
        index1 = 0

        for i in sprite_list:
            # Define the filename to search for
            file_to_find = i
            file_path = os.path.join('..', 'assets', i)  # Go up one level from 'windows' folder
            # ---------------
            # def on_mouse_press(x, y, button, modifiers):
            #     # Check if the mouse click is within the sprite's bounds
            #     if sprite.left <= x <= sprite.right and sprite.bottom <= y <= sprite.top:
            #         # Perform actions when the sprite is clicked
            #         print("Sprite clicked!")
            #         # ... (other actions)
            # ---------------
            index1 += 0.5
            sprite_texture = arcade.load_texture(file_path)
            xsprite = arcade.Sprite(sprite_texture)
            xsprite.draw_hit_box()
            xsprite.sync_hit_box_to_texture()
            xsprite.center_x = ((WINDOW_WIDTH / 2) * index1)
            xsprite.center_y = ((WINDOW_HEIGHT / 2) + 0)
            self.sprites.append(xsprite)

        # self.carnivore_sprite = ac.sprite_creation(self, "assets/Carnivores1.png", 100,1)
        # self.herbivore_sprite = ac.sprite_creation(self, "assets/Herbivores1.png",1,1)
        # self.decomposer_sprite = ac.sprite_creation(self, "assets/Decomposers1.png",1,1)

    # def sprite_creation(self, sprite_file, offset_X, offset_Y):
    #     self.sprite_texture = arcade.load_texture(sprite_file)
    #     self.first_sprite = arcade.Sprite(self.sprite_texture)
    #     self.first_sprite.center_x = ((WINDOW_WIDTH / 2) + offset_X)
    #     self.first_sprite.center_y = ((WINDOW_HEIGHT / 2) + offset_Y)
    #     return self.first_sprite

    def reset(self):
        """Reset the game to the initial state."""
        # Do changes needed to restart the game here if you want to support that
        pass

    def on_draw(self):
        """
        Render the screen.
        """
        # texture_button = UITextureButton(
        #     text="UITextureButton",
        #     width=200,
        #     texture=TEX_RED_BUTTON_NORMAL,
        #     texture_hovered=TEX_RED_BUTTON_HOVER,
        #     texture_pressed=TEX_RED_BUTTON_PRESS,
        # )
        #     grid.add(texture_button, row=0, column=2)


        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        self.clear()
        #stuff here:
        self.sprites.draw()
        # arcade.draw_sprite(self.carnivore_sprite)
        # arcade.draw_sprite(self.herbivore_sprite)
        # arcade.draw_sprite(self.decomposer_sprite)



    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        pass

    def on_key_press(self, key, key_modifiers):
        """
        Called whenever a key on the keyboard is pressed.
        """
        pass

    def on_key_release(self, key, key_modifiers):
        """
        Called whenever the user lets off a previously pressed key.
        """
        pass

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        """
        Called whenever the mouse moves.
        """
        pass

    def on_mouse_press(self, x, y, button, key_modifiers):
        """
        Called when the user presses a mouse button.
        """
        pass

    def on_mouse_release(self, x, y, button, key_modifiers):
        """
        Called when a user releases a mouse button.
        """
        pass


def main():
    """ Main function """
    # Create a window class.
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)

    # Create and setup the GameView
    game = GameView()

    # Show GameView on screen
    window.show_view(game)

    # Start the arcade game loop
    arcade.run()



if __name__ == "__main__":
    main()