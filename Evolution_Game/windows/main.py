codeVersion= "1.048"

import arcade
from pathlib import *

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

        folder2 = Path('Evolution_Game/assets')
        sprite_list = {
            "assets/Carnivores1.png" : [0,"carnivore_sprite"],
            "assets/Herbivores1.png" : [1,"herbivore_sprite"],
            "assets/Decomposers1.png" : [2,"decomposer_sprite"]
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
            file_path = Path(i)
            print(file_path)
            # ---------------
            index1 += 0.5
            sprite_texture = arcade.load_texture(file_path)
            xsprite = arcade.Sprite(sprite_texture)
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