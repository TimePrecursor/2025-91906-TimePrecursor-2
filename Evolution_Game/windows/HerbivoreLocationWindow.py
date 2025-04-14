import arcade
from arcade.gui import *
from arcade import gui



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



        self.herbi_habitat_list = [
            "Savana",
            "Jungle",
            "Swamp",
            "Arctic",
            "Desert"
        ]
        self.herbi_habitat_desc = {
            0:["Savana","A mixed woodland-grassland biome characterised by trees being widely spaced"],
            1:["Jungle","An area of land overgrown with dense forest and tangled vegetation. Usually very damp and humid"],
            2:["Swamp","An area permanently saturated, or filled, with water. Rich in moss and alge"],
            3:["Arctic","A land characterized by low temperatures and abundant snowfall, resulting in a landscape dominated by snow and ice"],
            4:["Desert","A large, extremely dry area of land with sparse vegetation. Can contain oases"]
        }

        self.herbi_title()
        self.choose_herbi_habitat()
        self.choosebutton()
        self.choose_button.visible = False


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

    def choose_herbi_habitat(self):
        text="Choose your location!"
        self.herbi_habitat_text = arcade.gui.UILabel(
            width=len(text),
            text=str(text),
            font_name=self.fontdefaults,
            x=((self.WINDOW_WIDTH/4)+(len(text))*3.2),
            y=(self.WINDOW_HEIGHT/2.5)+(self.WINDOW_HEIGHT/2.8),
            font_size=30,
        )
        self.manager.add(self.herbi_habitat_text)

        self.dropdownmain = arcade.gui.UIDropdown(
            x= (self.WINDOW_WIDTH/4),
            y= (self.WINDOW_HEIGHT/1.5),
            width= (self.WINDOW_WIDTH/2),
            height=50,
            options=self.herbi_habitat_list)

        self.manager.add(self.dropdownmain)

        self.habitat_desc_area = arcade.gui.UILabel(
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
        self.manager.add(self.habitat_desc_area)

        dropdown = self.dropdownmain
        @dropdown.event()
        def on_change(event: UIOnChangeEvent):
            x = self.herbi_habitat_list.index(event.new_value)
            y = self.herbi_habitat_desc[x][1]
            self.habitat_desc_area.text = y
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