import os.path
from idlelib.configdialog import font_sample_text
import arcade
from arcade.gui import *
from arcade import gui
import sys

# cool thing!
# from pymunk.examples.spiderweb import update

WINDOW_TITLE = f"Evolution Game - Carnivore Selection"

class PageView(arcade.View):
    def __init__(self):
        super().__init__()
        self.fontsize = 50
        self.WINDOW_WIDTH = 1000
        self.WINDOW_HEIGHT = 600
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.grid = UIGridLayout(
            column_count=5,
            row_count=5,
            vertical_spacing=0,
            horizontal_spacing=10,
        )
        self.grid.add(UIAnchorLayout(children=[self.grid]))

        self.background_color = arcade.color.ATOMIC_TANGERINE

        self.back_button = arcade.gui.UIFlatButton(
            text="Back to Menu",
            width=self.WINDOW_WIDTH,height=50
        )
        self.back_button.on_click = self.go_back
        self.manager.add(self.back_button)
        self.ui = UIManager()

        self.fontdefaults = (
            "Times New Roman",  # Comes with Windows
            "Times",  # MacOS may sometimes have this variant
            "Liberation Serif"  # Common on Linux systems
        )

        self.carni_professions_list = [
            "Speed",
            "Ambush",
            "Persistence",
            "Strategy",
            "Scavenger",
            "Pack"]

        # Index : [Type, Pros, Cons]
        self.carni_profession_desc = {
            0: ["Speed",
                "These are lighting fast sprinters, able to run faster than 100km/h, but only for short periods of time.",
                "Pros: Fast ",
                "Cons: High Metabolism (Has to eat more). Overheats quickly."],
            1: ["Ambush",
                "With camouflage based on their environmental surroundings, these hunters can easily sneak up on prey and wait for the perfect moment to strike. They are usually strong enough to kill prey with a single blow.",
                "Pros: Stealthy. Intelligent. Strong.",
                "Cons: "],
            2: ["Persistence",
                "Equipt with one goal and persistence, these creatures can hunt a single animal for days.",
                "Pros: Very patient. Strong. Slow Metabolism (Can go without eating for a longer than usual period)",
                "Cons: Slow. Lonely."],
            3: ["Strategy",
                "",
                "Pros: ",
                "Cons: "],
            4: ["Scavenger",
                "",
                "Pros:"
                "",
                "Cons: "],
            5: ["Pack",
                "Hunting in with pack can be both beneficial and a hindrance. More teeth means both easier and larger kills. While more mouths means les food per hunter.",
                "Pros: Great",
                "Cons: "]
        }


        self.carni_title()
        self.choose_carni_profession()






    def on_draw(self):
        self.clear(color=arcade.color.CORDOVAN) #CHINESE_RED #CHESTNUT
        self.manager.draw()



    def go_back(self, event):
        from main import Orginismselectionveiw as orgwindow
        self.window.show_view(orgwindow())

    def on_hide_view(self):
        self.grid.clear()
        self.ui.disable()
        self.ui.clear()
        self.manager.disable()

    def carni_title(self):
        text="C A R N I V O R E S",

        self.title = arcade.gui.UILabel(
            text=str(*text),
            bold=True,
            text_color=arcade.color.WHITE,
            font_name=self.fontdefaults,
            x=((self.WINDOW_WIDTH/3.9)-(len(text)*self.fontsize)),
            y=((self.WINDOW_HEIGHT)-(self.fontsize*1.8)),
            font_size=self.fontsize)
        self.grid.add(self.title)
        self.manager.add(self.title)


    def choose_carni_profession(self):
        text="Choose your hunting style!"
        self.carni_profession_text = arcade.gui.UILabel(
            text=str(text),
            font_name=self.fontdefaults,
            x=((self.WINDOW_WIDTH/3.25)-(len(text))),
            y=(self.WINDOW_HEIGHT/2.5)+(self.WINDOW_HEIGHT/2.8),
            font_size=30,
        )
        # self.grid.add(self.carni_profession_text)
        self.manager.add(self.carni_profession_text)

        self.dropdownmain = arcade.gui.UIDropdown(
            x= (self.WINDOW_WIDTH/4),
            y= (self.WINDOW_HEIGHT/1.5),
            width= (self.WINDOW_WIDTH/2),
            height=50,
            options=self.carni_professions_list)

        # self.grid.add(self.dropdownmain)
        self.manager.add(self.dropdownmain)

        pass
















        # if I want to resize -----

        # self.title.move(dy=float((self.height/2)-(self.fontsize)))
    #
    # def on_resize(self, width: int, height: int):
    #     super().on_resize(width, height)
    #     self.WINDOW_WIDTH = width
    #     self.WINDOW_HEIGHT = height
    #     # self.title.x = float((self.width/2)-(self.fontsize*6))
    #     # self.title.y = float((self.height/2)-(self.fontsize*4))
    #     self.title.center_on_screen()
    #     self.title.move(dy=float((self.height/2)-(self.fontsize)))
    #     print(self.WINDOW_WIDTH)

        # if I want to resize -----