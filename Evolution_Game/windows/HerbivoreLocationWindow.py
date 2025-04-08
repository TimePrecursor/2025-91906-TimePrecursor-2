# not yet

import arcade
from arcade.gui import *
from arcade import gui
import main
import os


WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = f"Evolution Game - Herbivore Selection"

class PageView(arcade.View):
    def __init__(self):
        super().__init__()
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
        size = 50
        title = arcade.gui.UILabel(
            text="H E R B I V O R E S",
            text_color=arcade.color.WHITE,
            font_name="SwanseaBold-D0ox.ttf",
            x=((WINDOW_WIDTH/2)-(size*6)),
            y=(WINDOW_HEIGHT-(size*4)),
            font_size=size)
        # title = arcade.draw_text("test", 100, 500, (250, 250, 250), 100, font_name='comic')
        # self.grid.add(title)
        self.manager.add(title)