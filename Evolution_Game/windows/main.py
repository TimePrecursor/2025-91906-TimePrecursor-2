import arcade
from arcade.gui import *
from arcade import gui
import os
import random
#-----------------------
codeVersion= "V 1.40.3.0 - School"
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
WINDOW_TITLE = f"Evolution Game (DEMO) V {codeVersion}"


class FirstButtons(arcade.gui.UITextureButton):
    def __init__(self, text, width, height, button_id, ui_manager):
        super().__init__(text=text, width=width, height=height)
        self.button_id = button_id
        self.ui_manager = ui_manager
    def errormessage(self):
        message_box = UIMessageBox(
            width=500,
            height=100,
            message_text="This is a demo! \nYou can only select carnivores for now. Sorry!",
            buttons=["OK"]
        )
        self.ui_manager.add(message_box)

    def on_click(self, event):
        import CarnivoreProfessionWindow as cw
        import HerbivoreLocationWindow as hw
        import DecomposerTypeWindow as dw

        view_factory = {
            0: [lambda: cw.PageView(), "Carnivore Profession"],
            1: [lambda: hw.PageView(), "Herbivore Location"],
            2: [lambda: dw.PageView(), "Decomposer Type"]
        }
        next_view = view_factory[self.button_id][0]()
        if self.button_id > 0:
            self.errormessage()
        elif self.button_id == 0:
            Orginismselectionveiw.showveiwfunc(next_view, next_view)
            # print(f"DEBUGGING:  To the {view_factory[self.button_id][1]} window!")

class Orginismselectionveiw(UIView):
    def __init__(self):
        super().__init__()
        self.fontsize = 50

        self.background_color = arcade.color.CINEREOUS
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        self.anchor = UIAnchorLayout()
        self.manager.add(self.anchor)

        self.grid = UIGridLayout(
            column_count=6,
            row_count=6,
            vertical_spacing=0,
            horizontal_spacing=50,
        )
        self.manager.add(self.grid)

        self.sprite_list = {
            0: ["CarnivoreFinal2.png", "CarnivoreFinal2Hover.png", "CarnivoreFinal2Pressed.png", "Carnivore"],
            1: ["HerbivoreFinal2.png", "HerbivoreFinal2Hover.png", "HerbivoreFinal2Pressed.png", "Herbivore"],
            2: ["DecomposerFinal2.png", "DecomposerFinal2Hover.png", "DecomposerFinal2Pressed.png", "Decomposer"],
        }

        self.setup_buttons()
        self.label_making1()

    def username2(self):
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        cache_file = os.path.join(project_root, "Evolution_Game", "windows",
                                  "stage2_files", "saved_cache", "cache1.txt")
        tempcache = []
        with open(cache_file) as cf:
            try:
                if self.username.text != ("" or " "):
                    x = str(self.username.text)
                    cf.write(f"\nUsername: {x}")
                else:
                    cf.write(f"\nUsername: None")
            except:
                print("error in try expression!")
            finally:
                print("done")
                Lines = cf.readlines()

        print(Lines)
        self.writeovercache(Lines,cache_file)


    def writeovercache(self, Lines, cache):

        # joinedlist = ' \n'.join(Lines)
        # print(joinedlist)
        with open(cache, "w") as cf:
            cf.writelines(Lines)



    def setup_buttons(self):
        for count in self.sprite_list.keys():
            texture_button = FirstButtons(
                text="", width=300, height=300,
                button_id=count,
                ui_manager=self.manager
            )
            file_path_list = []
            for x in range(3):
                project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
                image_folder = os.path.join(project_root, "assets", "images")
                file_name = self.sprite_list[count][x]
                file_path = os.path.join(image_folder, file_name)
                file_path_list.append(file_path)

            sprite_Norm_TEX = arcade.load_texture(file_path_list[0])
            sprite_Hover_TEX = arcade.load_texture(file_path_list[1])
            sprite_Pressed_TEX = arcade.load_texture(file_path_list[2])

            texture_button.texture = sprite_Norm_TEX
            texture_button.texture_pressed = sprite_Pressed_TEX
            texture_button.texture_hovered = sprite_Hover_TEX

            self.grid.add(texture_button, row=1, column=int(count))
            self.manager.add(texture_button)

    def label_making1(self):
        self.title = arcade.gui.UILabel(
            bold=True,
            text="Choose your Creature!",
            text_color=arcade.color.WHITE,
            font_name=("Times New Roman", "Times", "Liberation Serif"),
            x=100,
            y=100,
            font_size=self.fontsize
        )
        self.title.add(self.anchor)
        self.manager.add(self.title)
        self.title.center_on_screen()
        self.title.move(dy=200)

        self.hintlabel = arcade.gui.UILabel(
            bold=True,
            text="Enter a Username! (optional)",
            text_color=arcade.color.WHITE,
            font_name=("Times New Roman", "Times", "Liberation Serif"),
            x=100,
            font_size=20
        )
        self.hintlabel.add(self.anchor)
        self.manager.add(self.hintlabel)
        self.hintlabel.center_on_screen()
        self.hintlabel.move(dy=130)

        self.username = arcade.gui.UIInputText(
            bold=True,
            width=325,
            border_color=arcade.color.BLACK,
            border_width=4,
            text_color=arcade.color.WHITE,
            font_name=("Times New Roman", "Times", "Liberation Serif"),
            x=100,
            font_size=12
        )
        self.username.add(self.anchor)
        self.manager.add(self.username)
        self.username.center_on_screen()
        self.username.move(dy=100)

        for i in range(3):
            label = arcade.gui.UILabel(
                text=self.sprite_list[i][3],
                text_color=arcade.color.WHITE,
                font_name=("Times New Roman", "Times", "Liberation Serif"),
                font_size=self.fontsize / 2
            )
            self.grid.add(label, row=0, column=i)
            self.manager.add(label)

    def on_draw(self):
        self.clear()
        self.manager.draw()  # ✅ Draw UI elements here

    def on_hide_view(self):
        self.username2()
        self.grid.clear()
        self.anchor.clear()
        self.manager.clear()
        self.manager.disable()

    def showveiwfunc(self, viewselected):
        self.window.show_view(viewselected)

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