# THIS FILE IS FOR TEXTING
# FOR NOW

import arcade
from arcade.examples.maze_recursive import create_outside_walls
from arcade.gui import *
import random

class creature_setup(UIView):
    def __init__(self):
        super().__init__()
        self.starting_food = 100
        self.starting_count = 10
        self.creature_details = {}
        self.all_details = None
        self.index1 = 0
        self.creature_types = ["carnivore", "herbivore", "decomposer"]
        self.all_details = ["max_speed", "sight_range", "max_stamina",
                            "stamina_recovery", "max_health", "metabolism",
                            "reproduction_rate", "lifespan", "mutation_rate",
                            "aggression", "intelligence", "camouflage",
                            "efficiency", "thermal_tolerance",
                            "social_behavior"]
        self.sim_state = False

        self.elapsed_time = 0.0  # Timer accumulator self.background_color = arcade.color.AIR_FORCE_BLUE
        self.update_interval = 0.1  # Update logic every 0.1 second(s)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            if self.sim_state is False:
                self.sim_state = True
                self.creature_setup(food_type="carnivore")
                print("SETUP FINISHED, PRESS AGAIN TO SIMULATE")
            elif self.sim_state is True:
                self.sim_state = False
                self.creature_simulate()
                print("Finished")

            # Left
        elif key == arcade.key.LEFT or key == arcade.key.A:
            print("left")

            # Right
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            print("right")

        # def random_with_bias(self):
        #     # rnum = random.randint(0,10)
        #     rnum = random.gauss(0.1,0.1)
        #     print(rnum)

    def on_update(self, delta_time):
        if self.sim_state == True:
            self.elapsed_time += delta_time
            if self.elapsed_time >= self.update_interval:
                self.elapsed_time = 0.0
                # Run slower logic here



    def creature_setup(self, food_type):
        # START THE CREATURE SETUP:
        #  Carnivores: higher sense distance, higher speed, lower efficiency.
        #  Herbivores: medium sense distance, slower speed, high efficiency.
        #  Decomposers: low sense distance, low speed, high efficiency.
        if food_type == "carnivore":
            print()
            # two traits: SENSE AND SPEED
            # math = ((Speed^2)+Sense)
            for i in range(1,21):
                speed = random.randint(1,10)
                sense = random.randint(1, 10)
                stamina = 10
                self.creature_details.setdefault(i,[speed,sense,stamina])
                print(i,[speed,sense])

    def creature_simulate(self):
        move_cost = lambda a, b : ((a^2)+b)
        deaths = []
        for x in self.creature_details:
            creature = self.creature_details[x]
            speed = self.creature_details[x][0]
            sense = self.creature_details[x][1]
            stamina = self.creature_details[x][2]
            food_found = random.randint(0,(sense+speed))
            new_stamina = stamina-move_cost(speed,sense)
            if new_stamina <= 0:
                print(f"{x} died!")
                deaths.append(x)

            self.starting_food -= 1
            self.food_remain = self.starting_food
            if self.food_remain < 1:
                arcade.exit()

        for x in deaths:
            self.creature_details.pop(x)

        print(self.food_remain)





        # loop though all details
        # for x in self.creature_startcount
        #
        #     self.main_details.setdefault(x, random.randint(1,10))




        # random_number = random.gauss(0, 0.05)


        # self.index1 += 1
        # with open(r"saved_cache\cache1.txt", "w") as f:
        #     f.write(f"{self.index1}")
        print("One evolution step done!")















def main():
    """ Main function """
    # Create a window class.
    window = arcade.Window(title="TESTING", resizable=False,center_window=True)

    # Show GameView on screen
    window.show_view(creature_setup())

    # Start the arcade game loop
    arcade.run()

if __name__ == "__main__":
    main()
