codeVersion= "1.7"

import arcade
from arcade.gui import *
from arcade import gui
import os


WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = f"Evolution Game V{codeVersion}"







# The texture will only be loaded during the first sprite creation

class MyView(UIView):
    """
    Main application class.

    1.0 NOTE: I have already programmed most necessary functions
    that will allow the user to play.
    """

    def __init__(self):
        super().__init__()
        self.background_color = arcade.color.AMAZON

        grid = UIGridLayout(
            column_count=3,
            row_count=5,
            size_hint=(0, 0),
            vertical_spacing=0,
            horizontal_spacing=10,
        )

        self.ui.add(UIAnchorLayout(children=[grid]))

        # setting up window variables:

        # self.grid = UIGridLayout(
        #     column_count=3,
        #     row_count=4,
        #     size_hint=(0, 0),
        #     vertical_spacing=10,
        #     horizontal_spacing=10,
        # )
        # self.box = arcade.gui.UIGridLayout()

        '''
        CarnivoreIcons = 0
        HerbivoreIcons = 1
        DecomposerIcons = 2
        '''

        sprite_list = {
            0: ["CarnivoreFinal2.png", "CarnivoreFinal2Hover.png", "CarnivoreFinal2Pressed.png"],
            1: ["HerbivoreFinal2.png", "HerbivoreFinal2Hover.png", "HerbivoreFinal2Pressed.png"],
            2: ["DecomposerFinal2.png" , "DecomposerFinal2Hover.png", "DecomposerFinal2Pressed.png"],
        }

        # If I have sprites or buttons, I will create them here:

        self.sprites = arcade.SpriteList()

        for count, i in enumerate(sprite_list):
            texture_button = UITextureButton(
                text="",
                width=300,
                height=300
            )
            file_path_list = []
            for x in range(0,3):
                # Define the filename to search for:
                file_path = os.path.join('..', 'assets', sprite_list[count][x])
                file_path_list.append(file_path)

            # Loading textures to a specific file path:
            sprite_Norm_TEX = arcade.load_texture(file_path_list[0])
            sprite_Hover_TEX = arcade.load_texture(file_path_list[1])
            sprite_Pressed_TEX = arcade.load_texture(file_path_list[2])

            # Set the loaded texture to each button
            texture_button.texture = sprite_Norm_TEX
            texture_button.texture_pressed = sprite_Pressed_TEX
            texture_button.texture_hovered = sprite_Hover_TEX

            grid.add(texture_button, row=1, column=int(0 + count))

    def reset(self):
        """Reset the game to the initial state."""
        # Do changes needed to restart the game here if you want to support that
        pass


    # def on_draw(self):
    #     """
    #     Render the screen.
    #     """
    #
    #     # This command should happen before we start drawing. It will clear
    #     # the screen to the background color, and erase what we drew last frame.
    #     self.clear()
    #     #stuff here:
    #     self.sprites.draw()
    #     # arcade.draw_sprite(self.carnivore_sprite)
    #     # arcade.draw_sprite(self.herbivore_sprite)
    #     # arcade.draw_sprite(self.decomposer_sprite)



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
    window = arcade.Window(1000, 600, WINDOW_TITLE, resizable=True)


    # Show GameView on screen
    window.show_view(MyView())

    # Start the arcade game loop
    arcade.run()



if __name__ == "__main__":
    main()