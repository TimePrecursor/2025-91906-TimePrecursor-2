import arcade
from arcade.gui import *
from arcade.gui import UIView

'''
-----------------------------------------------------------------------------------
🥩 Carnivores (Predators)
Fox – A cunning, agile predator with sharp senses. Hunts small prey with stealth.

Cheetah – The fastest land animal. Relies on bursts of speed to chase down prey.

Lion – A powerful apex predator. Hunts in groups and dominates open plains.

Tiger – A solitary, stealthy hunter. Strong, territorial, and loves dense forests.

Meerkat – Tiny but fierce. Hunts insects and small creatures in coordinated groups.
-----------------------------------------------------------------------------------
🌿 Herbivores (Prey)
Mouse – Small and quick. A staple prey for many predators. Excellent at hiding.

Rabbit – Rapid breeder. Uses speed and tunnels to escape danger.

Deer – Graceful and alert. Lives in herds and uses speed to flee from threats.

Gazelle – Extremely fast and agile. A common prey in the savannah food chain.

Reindeer – Hardy and strong. Adapted to cold climates with a keen sense of smell.
-----------------------------------------------------------------------------------
'''

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800

class animal_info(UIView):
    def __init__(self):
        super().__init__()
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        self.grid = UIGridLayout(
            column_count=5,
            row_count=5,
            vertical_spacing=0,
            horizontal_spacing=10,
        )
        self.grid.add(UIGridLayout(children=[self.grid]))

        self.background_color = arcade.color.JET













def main():
    """ Main function """
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, "EVOLUTION DEMO", resizable=False, center_window=True)
    window.show_view(animal_info())
    arcade.run()

if __name__ == "__main__":
    main()
