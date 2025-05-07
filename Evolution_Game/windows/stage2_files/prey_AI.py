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


