# not yet

import arcade
from arcade.gui import *
from arcade import gui
import main
import os


WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = f"Evolution Game - Decomposer Selection"

class PageView(arcade.View):
    def __init__(self):
        super().__init__()
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.v_box = arcade.gui.UIBoxLayout()
        # set color:
        self.background_color = arcade.color.PEAR

    def on_draw(self):
        self.clear(color=arcade.color.CADET)
        self.manager.draw()

    def go_back(self, event):
        from main import Orginismselectionveiw as orgwindow
        self.window.show_view(orgwindow())

    def on_hide_view(self):
        self.manager.disable()