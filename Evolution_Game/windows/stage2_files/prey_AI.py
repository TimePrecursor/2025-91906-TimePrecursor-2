"""
live_food_stats = [
    {
        "name": "Deer",
        "speed": 7,
        "awareness": 6,
        "nutritional_value": 8,
        "health": 60,
        "vision_range": 25,
        "stamina": 70
    },
    {
        "name": "Gazelle",
        "speed": 9,
        "awareness": 8,
        "nutritional_value": 7,
        "health": 50,
        "vision_range": 30,
        "stamina": 80
    },
    {
        "name": "Mouse",
        "speed": 3,
        "awareness": 5,
        "nutritional_value": 2,
        "health": 10,
        "vision_range": 15,
        "stamina": 25
    },
    {
        "name": "Rabbit",
        "speed": 6,
        "awareness": 7,
        "nutritional_value": 4,
        "health": 30,
        "vision_range": 20,
        "stamina": 50
    },
    {
        "name": "Pig",
        "speed": 4,
        "awareness": 4,
        "nutritional_value": 9,
        "health": 80,
        "vision_range": 18,
        "stamina": 40
    }
]

"""
"""
import random
from typing import Optional, List, Tuple

class SimplePreyAI:
    def __init__(self, name: str, speed: int, awareness: int, nutrition: int, vision_range: float, stamina: int, health: int):
        self.name = name
        self.speed = speed  # 1–10 scale
        self.awareness = awareness  # 1–10 scale
        self.nutrition = nutrition  # How much food it gives when eaten
        self.vision_range = vision_range  # Detection radius
        self.field_of_view = 270  # Degrees
        self.stamina = stamina
        self.max_stamina = stamina

        self.health = health
        self.hunger = 0
        self.is_fleeing = False
        self.flee_direction = (0, 0)  # (x, y)
        self.alert_timer = 0
        self.graze_timer = random.randint(3, 8)
        self.position = (0, 0)  # Can be updated externally

    def detect_threats(self, predators: List[Tuple[str, Tuple[float, float]]]) -> Optional[str]:
        # Return name of predator if within range and field of view
        for predator_name, predator_pos in predators:
            if self._in_vision_range(predator_pos):
                self.is_fleeing = True
                self.alert_timer = 5
                self.flee_direction = self._calculate_flee_direction(predator_pos)
                return predator_name
        return None

    def update(self, dt: float):
        if self.is_fleeing:
            self._flee(dt)
        elif self.alert_timer > 0:
            self.alert_timer -= dt
        else:
            self._graze(dt)

    def _flee(self, dt: float):
        if self.stamina > 0:
            self.stamina -= dt * 10
            self._move(self.flee_direction, dt * (self.speed * 1.5))
        else:
            self.is_fleeing = False  # Exhausted

    def _graze(self, dt: float):
        self.graze_timer -= dt
        if self.graze_timer <= 0:
            self._wander()
            self.graze_timer = random.randint(3, 8)

    def _wander(self):
        dx = random.uniform(-1, 1)
        dy = random.uniform(-1, 1)
        self._move((dx, dy), self.speed * 0.3)

    def _move(self, direction: Tuple[float, float], distance: float):
        # Simple position update (replace with your game engine's method)
        x, y = self.position
        dx, dy = direction
        self.position = (x + dx * distance, y + dy * distance)

    def _calculate_flee_direction(self, predator_pos: Tuple[float, float]) -> Tuple[float, float]:
        px, py = predator_pos
        x, y = self.position
        dx = x - px
        dy = y - py
        length = (dx**2 + dy**2)**0.5 or 1
        return (dx / length, dy / length)

    def _in_vision_range(self, predator_pos: Tuple[float, float]) -> bool:
        x, y = self.position
        px, py = predator_pos
        dx = px - x
        dy = py - y
        dist = (dx**2 + dy**2)**0.5
        return dist <= self.vision_range
"""

import math
import random
import arcade


class PreySprite(arcade.Sprite):
    def __init__(self, prey_name: str, image_file: str, scale=0.5):
        super().__init__(image_file, scale)
        self.center_x = 1000 // 2  # Start in the middle of the screen
        self.center_y = 600 // 2
        self.change_y = 0
        self.change_x = 0

        import Evolution_Game.windows.stage2_files.live_food_stats as live
        prey_data = next((x for x in live.live_food_stats if x["name"] == prey_name), None)
        if prey_data is None:
            raise ValueError(f"Prey data not found for name: {prey_name}")

        # Core stats
        self.name = prey_data["name"]
        self.speed = prey_data["speed"]
        self.awareness = prey_data["awareness"]
        self.nutritional_value = prey_data["nutritional_value"]
        self.health = prey_data["health"]
        self.vision_range = prey_data["vision_range"]
        self.stamina = prey_data["stamina"]
        self.max_stamina = prey_data["stamina"]

        # AI behavior
        self.is_fleeing = False
        self.flee_direction = (0, 0)
        self.alert_timer = 0
        self.graze_timer = random.uniform(3.0, 6.0)

        # Add this property:

    def update_ai(self, dt, predators):
        """Update AI logic"""
        for predator in predators:
            if self.detect_threats(self,predator=predator):
                self._flee(dt)
                return  # Exit early after fleeing

        if self.alert_timer > 0:
            self.alert_timer -= dt
        else:
            self._graze(dt)

    def custom_get_distance(self,sprite1, sprite2):
        """Calculate distance between two sprites."""
        dx = sprite1.center_x - sprite2.center_x
        dy = sprite1.center_y - sprite2.center_y
        return math.hypot(dx, dy)

    def detect_threats(self, predator):
        """Check for threats within vision"""
        # Use center_x and center_y directly for both sprites
        distance = self.custom_get_distance(self,sprite1=PreySprite,sprite2=predator)
        if distance <= self.vision_range:
            self.is_fleeing = True
            self.alert_timer = 5.0
            dx = self.center_x - predator.center_x
            dy = self.center_y - predator.center_y
            magnitude = math.hypot(dx, dy) or 1
            self.flee_direction = (dx / magnitude, dy / magnitude)
            return True
        return False

        # return False

    def _flee(self, dt):
        if self.stamina > 0:
            self.stamina -= dt * 10
            speed = self.speed * 2.0
            dx, dy = self.flee_direction
            self.change_x = dx * speed
            self.change_y = dy * speed
        else:
            self.is_fleeing = False

    def _graze(self, dt):
        self.graze_timer -= dt
        if self.graze_timer <= 0:
            # Pick a random slow movement direction
            angle = random.uniform(0, 2 * math.pi)
            self.change_x = math.cos(angle) * self.speed * 0.3
            self.change_y = math.sin(angle) * self.speed * 0.3
            self.graze_timer = random.uniform(3.0, 6.0)

    def on_update(self, delta_time: float = 1/60):
        """Called every frame"""
        self.center_x += self.change_x
        self.center_y += self.change_y
        # Optional: Add stamina regen here
