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

        back_button = arcade.gui.UIFlatButton(text="Back to Menu", width=200, height=200)
        back_button.on_click = self.go_back
        self.manager.add(back_button)
        self.herbi_title()

    def on_draw(self):
        self.clear(color=arcade.color.AMAZON)
        self.manager.draw()

    def go_back(self, event):
        from main import Orginismselectionveiw as orgwindow
        self.window.show_view(orgwindow())

    def on_hide_view(self):
        self.manager.disable()

    def herbi_title(self):
        self.title = arcade.gui.UILabel(
            text="H E R B I V O R E S",
            text_color=arcade.color.WHITE,
            font_name=(
                "Times New Roman",  # Comes with Windows
                "Times",  # MacOS may sometimes have this variant
                "Liberation Serif"  # Common on Linux systems
            ),
            x=((self.WINDOW_WIDTH / 2) - (self.fontsize * 5.5)),
            y=((self.WINDOW_HEIGHT) - (self.fontsize * 2)),
            font_size=self.fontsize)
        self.grid.add(self.title)
        self.manager.add(self.title)