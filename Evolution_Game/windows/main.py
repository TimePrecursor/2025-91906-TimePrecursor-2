codeVersion= "1.06"

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
            column_count=10,
            row_count=5,
            size_hint=(0, 0),
            vertical_spacing=0,
            horizontal_spacing=0,
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
        0 = Normal Texture
        1 = Pressed Texture
        2 = Hover Texture
        '''
        sprite_list = {
            "CarnivoreIcons": ["CarnivoreFinal2.png", "CarnivoreFinal2Pressed.png", "CarnivoreFinal2Hover.png"],
            "HerbivoreIcons": ["HerbivoreFinal2.png", "HerbivoreFinal2Hover.png", "HerbivoreFinal2Pressed.png"],
            "DecomposerIcons": ["DecomposerFinal2.png" , "DecomposerFinal2Hover.png", "DecomposerFinal2Pressed.png"],

        }

        # sprite_list2 = {
        #     "CarnivoreFinal2.png" : [0,"carnivore_sprite_Normal"],
        #     "HerbivoreFinal2.png" : [0,"herbivore_sprite_Normal"],
        #     "DecomposerFinal2.png" : [0,"decomposer_sprite_Normal"],
        #     "CarnivoreFinal2Hover.png": [1, "carnivore_sprite_Hover"],
        #     "HerbivoreFinal2Hover.png": [1, "herbivore_sprite_Hover"],
        #     "DecomposerFinal2Hover.png": [1, "decomposer_sprite_Hover"],
        #     "CarnivoreFinal2Pressed.png": [2, "carnivore_sprite_Pressed"],
        #     "HerbivoreFinal2Pressed.png": [2, "herbivore_sprite_Pressed"],
        #     "DecomposerFinal2Pressed.png": [2, "decomposer_sprite_Pressed"]
        # }


        # If I have sprites, I will create them here
        # This may help:
        # ac.sprite_creation(self,name.png",1,1)
        # The offset percent default is 1 AKA (100%)
        self.sprites = arcade.SpriteList()
        index1 = 0

        for count, i in enumerate(sprite_list.keys()):
            print(count)
            index1 += 1
            value = sprite_list[count] if i[0] == index1 else None
            # for x in range(0,3):

            # Define the filename to search for:
            file_path = os.path.join('..', 'assets', value)  # This goes up one level from 'windows' folder

            # Loading textures to a specific file path:
            sprite_Norm_TEX = arcade.load_texture(file_path)
            sprite_Pressed_TEX = arcade.load_texture(file_path)
            sprite_Hover_TEX = arcade.load_texture(file_path)

            # Create the Texture Button:
            texture_button = UITextureButton(
                text="",
                width=300,
                height=300,
                texture=sprite_Norm_TEX,
                texture_hovered=sprite_Hover_TEX,
                texture_pressed=sprite_Pressed_TEX,
            )
            if sprite_list[i][0] == 0:
                grid.add(texture_button, row=0, column=int(0+index1))

            # index1 += 0.5
            # sprite_texture = arcade.load_texture(file_path)
            # xsprite = arcade.Sprite(sprite_texture)
            # xsprite.draw_hit_box()
            # xsprite.sync_hit_box_to_texture()
            # xsprite.center_x = ((WINDOW_WIDTH / 2) * index1)
            # xsprite.center_y = ((WINDOW_HEIGHT / 2) + 0)
            # self.sprites.append(xsprite)

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
    window = arcade.Window(800, 600, WINDOW_TITLE, resizable=True)


    # Show GameView on screen
    window.show_view(MyView())

    # Start the arcade game loop
    arcade.run()



if __name__ == "__main__":
    main()