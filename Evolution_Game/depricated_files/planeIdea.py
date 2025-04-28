import arcade
from arcade.gui import *
import random
import math
import os

from arcade.gui import UIView
WINDOW_TITLE = "Visuals Window"
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

class MovingSprite(arcade.Sprite):
    def __init__(self, texture_path, scale=0.5):
        super().__init__(texture_path, scale)
        self.target_x = self.center_x
        self.target_y = self.center_y
        self.speed = 2

    def set_new_target(self):
        # Set a random target within +/- 100 pixels
        self.target_x = self.center_x + random.randint(-100, 100)
        self.target_y = self.center_y + random.randint(-100, 100)

        # Clamp target within screen boundaries
        self.target_x = max(0, min(SCREEN_WIDTH, self.target_x))
        self.target_y = max(0, min(SCREEN_HEIGHT, self.target_y))

    def update(self, delta_time):  # Accept delta_time argument
        # Move sprite towards the target position
        dx = self.target_x - self.center_x
        dy = self.target_y - self.center_y
        distance = math.hypot(dx, dy)

        if distance < self.speed:
            # If reached target, set new target and move there
            self.center_x = self.target_x
            self.center_y = self.target_y
            self.set_new_target()
        else:
            # Continue moving towards the target
            self.center_x += dx / distance * self.speed
            self.center_y += dy / distance * self.speed

class PlaneOne(arcade.View):
    def __init__(self):
        super().__init__()
        self.thingstate = True
        self.elapsed_time = 0.0  # Timer accumulator
        self.update_interval = 0.5  # Update logic every 0.5 second(s)
        self.setup()

    def setup(self):
        self.sprite_list = arcade.SpriteList()

        # Path to assets/images
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..",".."))
        image_folder = os.path.join(project_root, "assets", "images")
        file_name = "Red_Ball.png"
        file_path = os.path.join(image_folder, file_name)
        self.ball_tex = arcade.load_texture(file_path)

    def spawn_random_sprite(self, w, h, x, y):
        # Create and spawn a new sprite
        ball_sprite = MovingSprite(self.ball_tex, scale=0.01)
        ball_sprite.center_x = x
        ball_sprite.center_y = y
        ball_sprite.set_new_target()
        self.sprite_list.append(ball_sprite)

    def on_update(self, delta_time):
        if self.thingstate:
            self.elapsed_time += delta_time

            if self.elapsed_time >= self.update_interval:
                self.elapsed_time = 0.0
                x = random.randint(0, SCREEN_WIDTH)
                y = random.randint(0, SCREEN_HEIGHT)
                self.spawn_random_sprite(50, 50, x, y)

        # Update all sprites
        self.sprite_list.update()

        # Remove sprites once they reach their target
        for sprite in self.sprite_list[:]:  # Iterate over a copy of the list
            dx = sprite.target_x - sprite.center_x
            dy = sprite.target_y - sprite.center_y
            distance = math.hypot(dx, dy)

            # If sprite is close enough to target, remove it
            if distance < sprite.speed:
                self.sprite_list.remove(sprite)

    def on_draw(self):
        self.clear()
        self.sprite_list.draw()

class visualswindow(UIView):
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

        self.background_color = arcade.color.JET




def main():
    """ Main function """
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, WINDOW_TITLE, resizable=False, center_window=True)
    window.show_view(visualswindow())
    arcade.run()

if __name__ == "__main__":
    main()
