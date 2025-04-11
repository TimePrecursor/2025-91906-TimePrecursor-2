# not yet

import arcade
from arcade.gui import *
from arcade import gui
import main
import os


WINDOW_TITLE = f"Evolution Game - Herbivore Selection"

class PageView(arcade.View):
    def __init__(self):
        super().__init__()
        self.fontsize = 50
        self.fontdefaults = (
            "Times New Roman",  # Comes with Windows
            "Times",  # MacOS may sometimes have this variant
            "Liberation Serif"  # Common on Linux systems
        )
        self.WINDOW_WIDTH = 1000
        self.WINDOW_HEIGHT = 600
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.grid = UIGridLayout(
            column_count=3,
            row_count=5,
            vertical_spacing=0,
            horizontal_spacing=10,
        )
        self.grid.add(UIAnchorLayout(children=[self.grid]))

        self.back_button = arcade.gui.UIFlatButton(
            text="Back to Menu",
            width=self.WINDOW_WIDTH, height=50
        )
        self.back_button.on_click = self.go_back
        self.manager.add(self.back_button)


        self.carni_professions_list = [
            "Speed",
            "Ambush",
            "Persistence",
            "Strategy",
            "Scavenger",
            "Pack"]
        # Index : [Type, Pros, Cons]
        # self.carni_profession_desc = {
        #     0: ["Speed",
        #         "These are lighting fast sprinters, able to run faster than 100km/h, but only for short periods of time.",
        #         "Pros: Fast ",
        #         "Cons: High Metabolism (Has to eat more). Overheats quickly."],
        #     1: ["Ambush",
        #         "With camouflage based on their environmental surroundings, these hunters can easily sneak up on prey and wait for the perfect moment to strike. They are usually strong enough to kill prey with a single blow.",
        #         "Pros: Stealthy. Intelligent. Strong.",
        #         "Cons: "],
        #     2: ["Persistence",
        #         "Equipt with one goal and persistence, these creatures can hunt a single animal for days.",
        #         "Pros: Very patient. Strong. Slow Metabolism (Can go without eating for a longer than usual period)",
        #         "Cons: Slow. Lonely."],
        #     3: ["Strategy",
        #         "",
        #         "Pros: ",
        #         "Cons: "],
        #     4: ["Scavenger",
        #         "",
        #         "Pros:"
        #         "",
        #         "Cons: "],
        #     5: ["Pack",
        #         "Hunting in with pack can be both beneficial and a hindrance. More teeth means both easier and larger kills. While more mouths means les food per hunter.",
        #         "Pros: Great",
        #         "Cons: "]
        # }
        self.herbi_title()
        self.choose_carni_profession()

        self.ui = UIManager()
    def on_draw(self):
        self.clear(color=arcade.color.AMAZON)
        self.manager.draw()

    def go_back(self, event):
        from main import Orginismselectionveiw as orgwindow
        self.window.show_view(orgwindow())

    def on_hide_view(self):
        self.grid.clear()
        self.manager.disable()
        self.manager.clear()
        self.manager.disable()

    def herbi_title(self):
        self.title = arcade.gui.UILabel(
            text="H E R B I V O R E S",
            text_color=arcade.color.WHITE,
            font_name=self.fontdefaults,
            x=((self.WINDOW_WIDTH / 2) - (self.fontsize * 5.5)),
            y=((self.WINDOW_HEIGHT) - (self.fontsize * 2)),
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