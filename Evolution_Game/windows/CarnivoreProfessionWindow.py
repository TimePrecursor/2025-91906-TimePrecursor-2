# GUI and system imports
import arcade
from arcade.gui import *
from arcade import gui
import random
import os

# Predator data
from Evolution_Game.windows.stage2_files.creature_stats import predator_roles

WINDOW_TITLE = f"Evolution Game - Carnivore Selection"

# Main view for profession selection
class PageView(arcade.View):
    def __init__(self):
        super().__init__()
        self.fontsize = 50
        self.WINDOW_WIDTH = 1000
        self.WINDOW_HEIGHT = 600
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        self.background_color = arcade.color.ATOMIC_TANGERINE

        # Back button setup
        self.back_button = arcade.gui.UIFlatButton(
            text="Back to Menu",
            width=self.WINDOW_WIDTH,
            height=50
        )
        self.back_button.on_click = self.go_back
        self.manager.add(self.back_button)

        self.fontdefaults = (
            "Times New Roman", "Times", "Liberation Serif"
        )

        # List of professions available
        self.carni_professions_list = [
            "Speed", "Ambush", "Persistence", "Scavenger"
        ]

        # Descriptions for each profession (index-matched)
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
                "\nCons: Can be a long time between feeds, especially in winter."]#,
            # 4: ["Pack",
            #     "Hunting in with pack can be both beneficial and a hindrance. More teeth means both easier and larger kills. While more mouths means less food per hunter.",
            #     "\nPros: Great social benefits. Usually intelligent.",
            #     "\nCons: Not an effective killer alone."]
        }

        self.carni_title()
        self.choose_carni_profession()
        self.choosebutton()
        self.choose_button.visible = False  # Only visible once an option is selected

    def on_draw(self):
        self.clear(color=arcade.color.CORDOVAN)
        self.manager.draw()

    def go_back(self, event):
        from main import Orginismselectionveiw as orgwindow
        self.window.show_view(orgwindow())

    def on_hide_view(self):
        self.manager.disable()
        self.manager.clear()

    def carni_title(self):
        text = "C A R N I V O R E S"
        self.title = arcade.gui.UILabel(
            text=text,
            bold=True,
            text_color=arcade.color.WHITE,
            font_name=self.fontdefaults,
            x=(self.WINDOW_WIDTH/3.9)-(len(text)*self.fontsize),
            y=(self.WINDOW_HEIGHT)-(self.fontsize*1.8),
            font_size=self.fontsize)
        self.manager.add(self.title)

    def choose_carni_profession(self):
        # Dropdown label
        text = "Choose your hunting style!"
        self.carni_profession_text = arcade.gui.UILabel(
            text=text,
            font_name=self.fontdefaults,
            x=(self.WINDOW_WIDTH/3.25)-len(text),
            y=(self.WINDOW_HEIGHT/2.5)+(self.WINDOW_HEIGHT/2.8),
            font_size=30,
        )
        self.manager.add(self.carni_profession_text)

        # Dropdown menu
        self.dropdownmain = arcade.gui.UIDropdown(
            x=self.WINDOW_WIDTH/4,
            y=self.WINDOW_HEIGHT/1.5,
            width=self.WINDOW_WIDTH/2,
            height=50,
            options=self.carni_professions_list)

        self.manager.add(self.dropdownmain)

        # Description area
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

        # Event handler for dropdown
        @self.dropdownmain.event()
        def on_change(event: UIOnChangeEvent):
            index = self.carni_professions_list.index(event.new_value)
            desc = '\n'.join(self.carni_profession_desc[index][1:4])
            self.profession_desc_area.text = desc
            self.choose_button.visible = True

    def choosebutton(self):
        # Confirm button
        self.choose_button = arcade.gui.UIFlatButton(
            x=(self.WINDOW_WIDTH/2)-(self.WINDOW_WIDTH/8),
            y=self.WINDOW_HEIGHT/8,
            width=self.WINDOW_WIDTH/4,
            height=50,
            text="Confirm!",
        )
        self.choose_button.on_click = self.click
        self.manager.add(self.choose_button)

    def click(self, event):
        # Get dropdown choice
        choice = self.dropdownmain.value

        # Get predator stats from cache
        choice_stats = predator_roles[choice]
        random_predator = random.choice(choice_stats)
        carnivore = random_predator["name"]

        # Determine index for prey info
        self.cr_index = 0 if choice == carnivore else 1
        prey = predator_roles[choice][self.cr_index]["prey"]

        # Save selection to cache file
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        cache_file = os.path.join(project_root, "windows", "stage2_files", "saved_cache", "cache1.txt")
        with open(cache_file, "w+") as f:
            username = f.read()
            f.write(f"{carnivore}\n{choice}\n|{prey[0]}|{prey[1]}|{prey[2]}\n{username}")

        # Move to next view
        import stage2_files.keyboard_input as play_view
        self.window.show_view(play_view.GameView1())
