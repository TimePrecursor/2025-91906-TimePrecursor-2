from xmlrpc.client import Boolean

import arcade
import matplotlib as matp
from arcade.gui import *
from arcade import gui
import os
import random




simulate_Gen_count = 10

from matplotlib.pyplot import title


# I will need the basics such as;
#   food,
#   simple AI (Differs between creatures),
#   and stats for all creatures!

class creature_actions():
    def __init__(self,name,age,hunger,health):
        self.name = name
        self.age = age
        self.hunger = hunger
        self.health = health

    # MAIN ACTIONS:
    def creature_reproduce(self):
        pass

    def creature_eat(self):
        pass

    def creature_drink(self):
        pass

    def creature_sleep(self):
        pass

    def creature_hunt(self):
        pass

    # SECONDARY ACTIONS:
    def creature_fight(self):
        pass

    def creature_flee(self):
        pass

    def creature_defend(self):
        pass

    def creature_gather(self):
        pass

    def creature_communicate(self):
        pass

    def creature_roam(self):
        pass

    def creature_rest(self):
        pass

    def creature_scavenge(self):
        pass


class creature_evolve_stats(arcade.Sprite):
    def __init__(self, max_speed, sight_range, max_stamina, stamina_recovery, max_health, metabolism, reproduction_rate,
                 lifespan, mutation_rate, aggression, intelligence, camouflage, efficiency,
                 thermal_tolerance, social_behavior, evolution_stage):
        # Evolution traits (set based on input or randomly generated)
        super().__init__()
        self.max_speed = max_speed
        self.sight_range = sight_range
        self.max_stamina = max_stamina
        self.stamina_recovery = stamina_recovery
        self.max_health = max_health
        self.metabolism = metabolism
        self.reproduction_rate = reproduction_rate
        self.lifespan = lifespan
        self.mutation_rate = mutation_rate
        self.aggression = aggression
        self.intelligence = intelligence
        self.camouflage = camouflage
        self.efficiency = efficiency
        self.thermal_tolerance = thermal_tolerance
        self.social_behavior = social_behavior
        self.evolution_stage = evolution_stage

        # Additional stats that change during the simulation
        self.age = 0
        self.hunger = 100  # Max hunger (this can decrease over time)
        self.stamina = self.max_stamina
        self.health = self.max_health

class environment_stats():
    def __init__(self,biome_type,weather_variability,water_availability,plant_density,terrain_difficulty,light_level,humidity,temperature,food_available):
        self.biome_type = biome_type
        self.weather_variability = weather_variability
        self.water_availability = water_availability
        self.plant_density = plant_density
        self.terrain_difficulty = terrain_difficulty
        self.light_level = light_level
        self.humidity = humidity
        self.temperature = temperature
        self.food_available = food_available



class environment_simlation(UIView):
    def __init__(self):
        super().__init__()
        self.index1 = 0
        self.sim_state = False
        self.background_color = arcade.color.AIR_FORCE_BLUE
        self.elapsed_time = 0.0  # Timer accumulator
        self.update_interval = 0.5  # Update logic every 0.5 second(s)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            if self.sim_state is False:
                self.sim_state = True
                print("Started")
            elif self.sim_state is True:
                self.sim_state = False
                print("Stopped")

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
                self.simulate_step()  # Run your slower logic here

    def simulate_step(self):
        rnum = random.gauss(0,0.05)
        # Age the creatures, mutate, update world state, etc.

        #Carnivores: higher aggression, higher speed, lower efficiency.
        #Herbivores: lower aggression, better stamina, high efficiency.
        #Decomposers: low speed, high efficiency.

        self.index1 += 1
        with open(r"saved_cache/cache1.txt", "w") as f:
            f.write(f"{self.index1}")

        print(f"One evolution step done!")













def main():
    """ Main function """
    # Create a window class.
    window = arcade.Window(title="TESTING",resizable=False,center_window=True)

    # Show GameView on screen
    window.show_view(environment_simlation())

    # Start the arcade game loop
    arcade.run()

if __name__ == "__main__":
    main()
