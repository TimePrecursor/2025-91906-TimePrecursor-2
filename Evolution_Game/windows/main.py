import arcade
from arcade.gui import *
from arcade import gui
import os

#-----------------------
codeVersion= "V 0.5.13.10"
'''
Software versioning is now: (Finished Version, Major Rewrite, Bug fixing, Small changes)
Keys:
 - Finished Version  = How many times it has reached being a fully operational Game / Stages complete 
 - Major Rewrite     = New file(s), changed a large portion of code to either fix/change/optimise
 - Bug fixing        = Fixed or added small things | Fixed possibly game breaking bugs | Added needed files/assets
 - Small changes     = Minor tweaks to either the appearance or small optimizations
'''
#-----------------------

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 600
center_xz = 0
center_yz = 0
WINDOW_TITLE = f"Evolution Game V {codeVersion}"


class FirstButtons(arcade.gui.UITextureButton):

    def __init__(self, text, width, height, button_id):
        super().__init__(text=text, width=width, height=height)
        self.button_id = button_id

    def on_click(self, event):
        import CarnivoreProfessionWindow as cw
        import HerbivoreLocationWindow as hw
        import DecomposerTypeWindow as dw

        next_file_list = {
            0 : cw.PageView(),
            1 : hw.PageView(),
            2 : dw.PageView()
        }

        print(f"To the {self.button_id} window!")
        x = next_file_list[self.button_id]
        Orginismselectionveiw.showveiwfunc(x,x)



class Orginismselectionveiw(UIView):
    """
    Main application class.

    """
    def __init__(self):
        super().__init__()
        self.ui = UIManager()
        self.fontsize = 50

        self.background_color = arcade.color.CINEREOUS
        # self.window.width = WINDOW_WIDTH
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        self.anchor = UIAnchorLayout()
        self.ui.add(UIAnchorLayout(children=[self.anchor]))

        self.grid = UIGridLayout(
            column_count=6,
            row_count=6,
            vertical_spacing=0,
            horizontal_spacing=50,
        )
        self.ui.add(UIGridLayout(children=[self.grid]))


        # If I have sprites or buttons, I will create them here:
        self.sprite_list = {
            0: ["CarnivoreFinal2.png", "CarnivoreFinal2Hover.png", "CarnivoreFinal2Pressed.png", "Carnivore"],
            1: ["HerbivoreFinal2.png", "HerbivoreFinal2Hover.png", "HerbivoreFinal2Pressed.png", "Herbivore"],
            2: ["DecomposerFinal2.png" , "DecomposerFinal2Hover.png", "DecomposerFinal2Pressed.png", "Decomposer"],
        }
        self.sprites = arcade.SpriteList()

        self.setup_buttons()
        self.label_making1()



    def setup_buttons(self):
        for count, i in enumerate(self.sprite_list):
            texture_button = FirstButtons(text="", width=300, height=300, button_id=count)
            file_path_list = []
            for x in range(0,3):
                # Define the filename to search for:
                project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

                # Path to assets/images
                image_folder = os.path.join(project_root, "assets", "images")

                # Final file path
                file_name = self.sprite_list[count][x]  # e.g. "CarnivoreFinal2.png"
                file_path = os.path.join(image_folder, file_name)

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

            # type = self.sprite_list[count][3]
            # self.on_FirstButton_Click(type)

            self.grid.add(texture_button, row=1, column=int(count))
            self.manager.add(texture_button)
    def label_making1(self):
        self.title = arcade.gui.UILabel(
            bold=True,
            text="Choose your Creature!",
            text_color=arcade.color.WHITE,
            font_name=(
                "Times New Roman",  # Comes with Windows
                "Times",  # MacOS may sometimes have this variant
                "Liberation Serif"  # Common on Linux systems
            ),
            x= 100 ,#((WINDOW_WIDTH / 2) - (self.fontsize * 5.5)),
            y= 100 ,#((WINDOW_HEIGHT) - (self.fontsize * 2)),
            font_size=self.fontsize)

        # self.title.draw()
        # self.grid.add(self.title,row=0, column=1)
        self.manager.add(self.title)
        self.anchor.add(self.title,anchor_x="center",anchor_y="top")

        for i in range(0, 3):
            self.labelvar = arcade.gui.UILabel(
                text=self.sprite_list[i][3] ,
                text_color=arcade.color.WHITE,
                font_name=(
                "Times New Roman",  # Comes with Windows
                "Times",  # MacOS may sometimes have this variant
                "Liberation Serif"  # Common on Linux systems
                ),
                # x=((WINDOW_WIDTH / 2) - (self.fontsize * 5.5)),
                # y=((WINDOW_HEIGHT) - (self.fontsize * 2)),
                font_size=(self.fontsize/2))
            self.grid.add(self.labelvar,row=0,column=i)
            self.manager.add(self.labelvar)

    def on_update(self, delta_time):
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
    def on_hide_view(self):
        self.grid.clear()
        self.anchor.clear()
        self.ui.disable()
        self.ui.clear()
        self.manager.disable()

    def showveiwfunc(self, viewselected):
        self.window.show_view(viewselected)


    # def on_hide_view(self):
    #     self.manager.disable()

def main():
    """ Main function """
    # Create a window class.
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE, resizable=False, center_window=True)


    # Show GameView on screen
    window.show_view(Orginismselectionveiw())

    # Start the arcade game loop
    arcade.run()


if __name__ == "__main__":
    main()