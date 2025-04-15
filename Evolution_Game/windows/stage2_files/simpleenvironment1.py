import arcade
from arcade.gui import *
from arcade import gui
import os
import random

# I will need the basics such as;
#   food,
#   simple AI (Differs between creatures),
#   and stats for all creatures!

class creature_live_stats():
    def __init__(self,name,age,hunger,health):
        self.name = name
        self.age = age
        self.hunger = hunger
        self.health = health

class creature_evolve_stats:
    def __init__(self, max_speed, sight_range, max_stamina, stamina_recovery, max_health,
                 metabolism, reproduction_rate, lifespan, mutation_rate, aggression,
                 intelligence, camouflage, efficiency, biome_affinity, thermal_tolerance,
                 social_behavior, evolution_stage):
        # Evolution traits (set based on input or randomly generated)
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
        self.biome_affinity = biome_affinity
        self.thermal_tolerance = thermal_tolerance
        self.social_behavior = social_behavior
        self.evolution_stage = evolution_stage

        # Additional stats that change during the simulation
        self.age = 0
        self.hunger = 100  # Max hunger (this can decrease over time)
        self.stamina = self.max_stamina
        self.health = self.max_health

class environment_simlation(arcade.Sprite):
    def __init__(self):
        pass
    def update(self):
        pass




