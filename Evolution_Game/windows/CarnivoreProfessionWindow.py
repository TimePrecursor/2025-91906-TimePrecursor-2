import arcade
from arcade.gui import *
from arcade import gui
import importlib.util
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
        self.grid.add(UIGridLayout(children=[self.grid]))

        self.background_color = arcade.color.ATOMIC_TANGERINE

        self.back_button = arcade.gui.UIFlatButton(
            text="Back to Menu",
            width=self.WINDOW_WIDTH,
            height=50
        )
        self.back_button.on_click = self.go_back
        self.manager.add(self.back_button)
        # self.ui = UIManager()

        self.fontdefaults = (
            "Times New Roman",  # Comes with Windows
            "Times",  # MacOS may sometimes have this variant
            "Liberation Serif"  # Common on Linux systems
        )

        self.carni_professions_list = [
            "Speed",
            "Ambush",
            "Persistence",
            "Scavenger",
            "Pack"]

        # Index : [Type, Pros, Cons]
        self.carni_profession_desc = {
            0: ["Speed",
                "These are lighting fast sprinters, able to run faster than 100km/h, but only for short periods of time.",
                "\nPros: Fast ",
                "\nCons: High Metabolism (Has to eat more). Overheats quickly."],
            1: ["Ambush",
                "With camouflage based on their environmental surroundings, these hunters can easily sneak up on prey and wait for the perfect moment to strike. They are usually strong enough to kill prey with a single blow.",
                "\nPros: Stealthy. Intelligent. Strong.",
                "\nCons: Slow runner. Might have to wait a while between feeds. Prey might notice them and run away."],
            2: ["Persistence",
                "Equipt with one goal and persistence, these creatures can hunt a single animal for days.",
                "\nPros: Very patient. Strong. Slow Metabolism (Can go without eating for a longer than usual period)",
                "\nCons: Slow. Solo hunter."],
            3: ["Scavenger",
                "Carnivores with this hunting style usually find their food source in either dead or already killed prey.",
                "\nPros: Easy food",
                "\nCons: Can be a long time between feeds, especially in winter."],
            4: ["Pack",
                "Hunting in with pack can be both beneficial and a hindrance. More teeth means both easier and larger kills. While more mouths means less food per hunter.",
                "\nPros: Great social benefits. Usually intelligent.",
                "\nCons: Not an effective killer alone."]
        }

        self.carni_title()
        self.choose_carni_profession()
        self.choosebutton()
        self.choose_button.visible = False


    def on_draw(self):
        self.clear(color=arcade.color.CORDOVAN) #CHINESE_RED #CHESTNUT
        self.manager.draw()



    def go_back(self, event):
        from main import Orginismselectionveiw as orgwindow
        self.window.show_view(orgwindow())

    def on_hide_view(self):
        self.grid.clear()
        self.manager.disable()
        self.manager.clear()


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
        # self.grid.add(self.title)
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

        self.profession_desc_area = arcade.gui.UILabel(
            width=self.WINDOW_WIDTH/1.25,
            height=self.WINDOW_WIDTH/4,
            multiline=True,
            x=(self.WINDOW_WIDTH/4)-self.WINDOW_WIDTH/8,
            y=(self.WINDOW_HEIGHT/4)-20,
            text='',
            font_name=self.fontdefaults,
            font_size=18
        )

        self.manager.add(self.profession_desc_area)

        dropdown = self.dropdownmain
        @dropdown.event()
        def on_change(event: UIOnChangeEvent):
            x = self.carni_professions_list.index(event.new_value)
            y = '\n'.join(self.carni_profession_desc[x][1:4])
            self.profession_desc_area.text = y
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