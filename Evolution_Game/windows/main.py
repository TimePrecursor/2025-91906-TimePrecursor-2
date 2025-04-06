codeVersion= "1.73"

import arcade
from arcade.gui import *
from arcade import gui
import os


WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = f"Evolution Game V{codeVersion}"




class FirstButtons(arcade.gui.UITextureButton):

    def __init__(self, text, width, height, button_id):
        super().__init__(text=text, width=width, height=height)
        self.button_id = button_id
    def on_click(self, event):
        print(f"To the {self.button_id} window!")


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

        self.grid = UIGridLayout(
            column_count=3,
            row_count=5,
            size_hint=(0, 0),
            vertical_spacing=0,
            horizontal_spacing=10,
        )
        self.ui.add(UIAnchorLayout(children=[self.grid]))


        # If I have sprites or buttons, I will create them here:
        self.sprite_list = {
            0: ["CarnivoreFinal2.png", "CarnivoreFinal2Hover.png", "CarnivoreFinal2Pressed.png", "Carnivore"],
            1: ["HerbivoreFinal2.png", "HerbivoreFinal2Hover.png", "HerbivoreFinal2Pressed.png", "Herbivore"],
            2: ["DecomposerFinal2.png" , "DecomposerFinal2Hover.png", "DecomposerFinal2Pressed.png", "Decomposer"],
        }
        self.sprites = arcade.SpriteList()
        self.setup_buttons()

    def reset(self):
        """Reset the game to the initial state."""
        # Do changes needed to restart the game here if you want to support that
        pass

    def setup_buttons(self):
        for count, i in enumerate(self.sprite_list):
            texture_button = FirstButtons(text="", width=300, height=300, button_id=count)
            file_path_list = []
            for x in range(0,3):
                # Define the filename to search for:
                file_path = os.path.join('..', 'assets', self.sprite_list[count][x])
                file_path_list.append(file_path)

            # Loading textures to a specific file path:
            sprite_Norm_TEX = arcade.load_texture(file_path_list[0])
            sprite_Hover_TEX = arcade.load_texture(file_path_list[1])
            sprite_Pressed_TEX = arcade.load_texture(file_path_list[2])

            # Set the loaded texture to each button
            texture_button.texture = sprite_Norm_TEX
            texture_button.texture_pressed = sprite_Pressed_TEX
            texture_button.texture_hovered = sprite_Hover_TEX

            # Create a UIManager instance
            # self.ui_manager = arcade.gui.UIManager(self)
            # self.ui_manager.add(texture_button)

            type = self.sprite_list[count][3]
            # self.on_FirstButton_Click(type)
            self.ui_manager = arcade.gui.UIManager()
            self.ui_manager.add(texture_button)
            self.grid.add(texture_button, row=1, column=int(0 + count))
            # x = texture_button.get_current_state()
            # print(x)



    def on_FirstButton_Click(self, type):
        print(f"{type} button clicked!")

    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
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