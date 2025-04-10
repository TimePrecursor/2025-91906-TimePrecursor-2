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

        self.carni_title()
        self.ui = UIManager()

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
        self.title = arcade.gui.UILabel(
            text="C A R N I V O R E S",
            text_color=arcade.color.WHITE,
            font_name=(
                "Times New Roman",  # Comes with Windows
                "Times",  # MacOS may sometimes have this variant
                "Liberation Serif"  # Common on Linux systems
            ),
            x=((self.WINDOW_WIDTH/2)-(self.fontsize*5.5)),
            y=((self.WINDOW_HEIGHT)-(self.fontsize*2)),
            font_size=self.fontsize)
        self.grid.add(self.title)
        self.manager.add(self.title)




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