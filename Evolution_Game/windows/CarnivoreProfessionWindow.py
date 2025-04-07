# file made in previous versions. next commit will start coding

import arcade
from arcade.gui import *
from arcade import gui
import main
import os


WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = f"Evolution Game - Carnivore Selection"

class PageView(arcade.View):
    def __init__(self):
        super().__init__()
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.v_box = arcade.gui.UIBoxLayout()
        # set color:
        self.background_color = arcade.color.LION

        back_button = arcade.gui.UIFlatButton(text="Back to Menu", width=200)
        back_button.on_click = self.go_back
        self.v_box.add(back_button)

        self.manager.add(
            arcade.gui.UIAnchorLayout(anchor_x="center_x", anchor_y="center_y", child=self.v_box)
        )

    def on_draw(self):
        self.clear(color=arcade.color.LION)
        self.manager.draw()

    def go_back(self, event):
        from main import Orginismselectionveiw as orgwindow
        self.window.show_view(orgwindow())

    def on_hide_view(self):
        self.manager.disable()


