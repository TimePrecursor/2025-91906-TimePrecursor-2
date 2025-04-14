# not yet

import arcade
from arcade.gui import *
from arcade import gui
import main
import os


WINDOW_TITLE = f"Evolution Game - Decomposer Selection"

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

        self.decom_type_list = [
            "Fungi",
            "Bacteria",
            "Invertebrates"
        ]
        self.decom_type_desc= {
            0:["Fungi","A group of spore-producing organisms feeding on organic matter, including moulds, yeast, and mushrooms."],
            1:["Bacteria","Unicellular microorganisms which have cell walls but lack organelles and an organized nucleus, including some that can cause disease"],
            2:["Invertebrates","An animal that doesn't have a backbone or spine. Examples of invertebrates include insects, worms, and snails."]
        }

        self.decom_title()
        self.choose_herbi_habitat()
        self.choosebutton()

    def on_draw(self):
        self.clear(color=arcade.color.CADET)
        self.manager.draw()

    def go_back(self, event):
        from main import Orginismselectionveiw as orgwindow
        self.window.show_view(orgwindow())

    def on_hide_view(self):
        self.grid.clear()
        self.manager.disable()
        self.manager.clear()
        self.manager.disable()

    def decom_title(self):
        self.title = arcade.gui.UILabel(
            text="D E C O M P O S E R S",
            text_color=arcade.color.WHITE,
            font_name=self.fontdefaults,
            x=((self.WINDOW_WIDTH / 2) - (self.fontsize * 6)),
            y=((self.WINDOW_HEIGHT) - (self.fontsize * 2)),
            font_size=self.fontsize)
        self.grid.add(self.title)
        self.manager.add(self.title)


    def choose_herbi_habitat(self):
        text="Choose your location!"
        self.decom_type_text = arcade.gui.UILabel(
            width=len(text),
            text=str(text),
            font_name=self.fontdefaults,
            x=((self.WINDOW_WIDTH/4)+(len(text))*3.2),
            y=(self.WINDOW_HEIGHT/2.5)+(self.WINDOW_HEIGHT/2.8),
            font_size=30,
        )
        # self.grid.add(self.carni_profession_text)
        self.manager.add(self.decom_type_text)

        self.dropdownmain = arcade.gui.UIDropdown(
            x= (self.WINDOW_WIDTH/4),
            y= (self.WINDOW_HEIGHT/1.5),
            width= (self.WINDOW_WIDTH/2),
            height=50,
            options=self.decom_type_list)

        self.manager.add(self.dropdownmain)

        self.decom_desc_area = arcade.gui.UILabel(
            align="center",
            width=self.WINDOW_WIDTH / 2,
            height=self.WINDOW_WIDTH / 4,
            multiline=True,
            x=(self.WINDOW_WIDTH / 2) - self.WINDOW_WIDTH / 4,
            y=(self.WINDOW_HEIGHT / 4) - 20,
            text='',
            font_name=self.fontdefaults,
            font_size=18
        )
        self.manager.add(self.decom_desc_area)

        dropdown = self.dropdownmain
        @dropdown.event()
        def on_change(event: UIOnChangeEvent):
            x = self.decom_type_list.index(event.new_value)
            y = self.decom_type_desc[x][1]
            self.decom_desc_area.text = y
            self.choose_button.visible = True


    def choosebutton(self):
        self.choose_button = arcade.gui.UIFlatButton(
            x=(self.WINDOW_WIDTH/2)-(self.WINDOW_WIDTH/8),
            y=self.WINDOW_HEIGHT/8,
            width=self.WINDOW_WIDTH/4,
            height=50,
            text="Confirm!",
        )
        self.manager.add(self.choose_button)