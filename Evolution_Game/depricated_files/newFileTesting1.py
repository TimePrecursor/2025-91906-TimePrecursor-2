import math
import os
import random
import time

import numpy
import arcade
from arcade.gui import UIView, UIAnchorLayout
from pyglet.math import clamp

import Evolution_Game.windows.stage2_files.live_food_stats as live
from Evolution_Game.windows.stage2_files.environmentSetupMkII import tree_list

# Game constants
SPRITE_SCALING = 0.15
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 600
NORMAL_SPEED = 3
BOUNDARY_MARGIN = 50
MIN_HUNGER = 10
MAX_HUNGER = 100
MIN_STAMINA = 10


class Animal(arcade.Sprite):
    def __init__(self, image_path, x, y, scale=1.0):
        super().__init__()
        self.texture = arcade.load_texture(image_path)
        self.center_x = x
        self.center_y = y
        self.scale = scale
        self.angle = 0
        self.fleeing = False
    
    def calculate_angle(self, x1, y1, x2, y2):
        """Calculate angle between two points in degrees"""
        dx = x2 - x1
        dy = y2 - y1
        return math.degrees(math.atan2(-dy, dx))
    
    def detect_predator(self, predator_pos, prey_pos):
        """Calculate angle for prey to detect predator"""
        x1, y1 = prey_pos
        x2, y2 = predator_pos
        angle = self.calculate_angle(x1, y1, x2, y2)
        return (angle - 90) % 360
    
    def get_movement_vector(self, angle_degrees, magnitude):
        """Convert angle to x,y movement vector"""
        angle_radians = math.radians(angle_degrees)
        opposite = magnitude * math.sin(angle_radians)
        adjacent = magnitude * math.cos(angle_radians)
        return [opposite, adjacent]
    
    def process_ai(self, predator_pos, prey_pos, prey_sprite, predator_sprite, 
                   vision_range, awareness, dt):
        """Handle prey AI behavior"""
        angle_deg = self.detect_predator(predator_pos, prey_pos)
        distance = arcade.get_distance_between_sprites(prey_sprite, predator_sprite)
        
        if distance < (vision_range * awareness):
            self.fleeing = True
            change_x, change_y = self.get_movement_vector(angle_deg, 10)
            return True, angle_deg, change_x, change_y
        else:
            self.wander()
            return False, 0, 0, 0
    
    def wander(self):
        """Random wandering behavior for prey"""
        # Just generate random movement - would be expanded in real implementation
        x = numpy.random.normal(scale=1)


class Player(arcade.Sprite):
    def __init__(self):
        """Initialize the player sprite"""
        super().__init__(scale=0.2)
        self.center_x = 0
        self.center_y = 0
        self.change_y = 0
        self.change_x = 0


class GameView1(UIView):
    def __init__(self):
        super().__init__()
        # Timer variables
        self.logic_timer = 0.0
        self.prey_logic_timer = 0
        self.prey_is_alive = True
        
        # Setup environment and UI
        from Evolution_Game.windows.stage2_files.environmentSetupMkII import EnvironmentSetup
        self.environment = EnvironmentSetup()
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.physic_engine = None
        
        # Input tracking
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.shift_pressed = False
        self.ctrl_pressed = False
        self.A_pressed = False
        
        # UI layout
        self.grid = UIAnchorLayout()
        self.manager.add(self.grid)
        
        # Game state
        self.chosen_animal = None
        self.chosen_prey = None
        self.fleeing = False
        self.background_color = arcade.color.AMAZON
        self.NO_SETUP = True
        self.player_list = arcade.SpriteList()
        
        # Player stats
        self.stamina = 0
        self.max_stamina = 0
        self.range = 0
        self.sneak_range = 0
        self.current_range = 0
        self.stat_speed = 0
        self.sprint_speed = 0
        self.metabolism = 0
        self.hunger = MAX_HUNGER
        self.max_hunger = MAX_HUNGER
        self.hunger_ratio = 1.0
        self.max_hunger_ratio = 1.0
        self.stamina_regen_rate = 0

        if not self.NO_SETUP:
            self.setup()
            self.chosen_animal = self.chosen_animal1

    def setup(self):
        """Set up the game and initialize variables"""
        self.NO_SETUP = True
        self.player_list = arcade.SpriteList()
        
        # Load animal selection from cache
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        cache_file_path = os.path.join(project_root, "windows", "stage2_files", "saved_cache", "cache1.txt")
        
        with open(cache_file_path, "r") as f:
            line1 = f.readline().rstrip("\n")
            line2 = f.readline().rstrip("\n")
        
        self.chosen_animal1 = line1
        self.creature_type = line2
        self.cr_index = 0
        
        # Setup player sprite
        self.file_path = os.path.join(project_root, "assets", "images", "animal_textures_fixed", f"{self.chosen_animal1}.png")
        tree_texture_path = self.environment.asset_paths("tree1.png")
        self.environment.create_random_trees(tree_texture_path)
        
        self.player_sprite = Player()
        self.player_sprite.texture = arcade.load_texture(self.file_path)
        self.player_sprite.scale = 0.15
        self.player_sprite.angle = 0
        self.player_list.append(self.player_sprite)
        
        # Load creature stats
        from Evolution_Game.windows.stage2_files.creature_stats import predator_roles
        creature_type = predator_roles[self.creature_type]
        
        if creature_type != self.chosen_animal1:
            self.cr_index = 1
            
        # Set creature stats
        creature_stats = predator_roles[self.creature_type][self.cr_index]
        self.stamina = creature_stats["stamina"]
        self.max_stamina = creature_stats["stamina"]
        self.range = creature_stats["normal_detectable_range"]
        self.sneak_range = creature_stats["sneak_detectable_range"]
        self.current_range = self.range
        self.stat_speed = creature_stats["sprint_speed"]
        self.sprint_speed = self.stat_speed / 2.5
        self.prey_data = live.live_food_stats_list
        self.metabolism = creature_stats["metabolism"]
        
        # Display stats
        stat_list = [
            "Stamina:", 
            "Hunger:", 
            f"Metabolism = {self.metabolism}\nSpeed = {round(self.stat_speed, 1)}\nDetectable Range = {self.range}"
        ]
        self.top_right_info_add(3, stat_list, 300, 40, bold=False)
        
        # Setup prey
        self.spawn_prey()
        self.animal = Animal(self.filefood_path, 0, 0)
        self.player_sprite.center_x=200
        self.player_sprite.center_y=200
        self.setup_done = True

    def spawn_prey(self):
        """Generate and place prey in the game environment"""
        self.load_prey_image()
        
        import Evolution_Game.windows.stage2_files.environmentSetupMkII as enviro_setup
        select_randxy = random.choice(enviro_setup.EnvironmentSetup.tree_locations)
        
        self.animalsprite = Animal(
            self.filefood_path, 
            select_randxy["center_x"], 
            select_randxy["center_y"], 
            scale=0.15
        )
        
        self.player_list.append(self.animalsprite)

    def load_prey_image(self):
        """Load random prey image from available choices"""
        self.prey_choices = []
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        cache_file = os.path.join(project_root, "windows", "stage2_files", "saved_cache", "cache1.txt")
        
        with open(cache_file, "r") as cf:
            for line in cf.readlines():
                if line.startswith("|"):
                    line = line.rstrip("\n").lstrip("|")
                    self.prey_choices = line.split("|")
        
        self.prey_choices.pop(0)
        random_prey = random.choice(self.prey_choices)
        self.chosen_prey = random_prey
        
        self.filefood_path = os.path.join(
            project_root, "assets", "images", "animal_textures_fixed", f"{random_prey}.png"
        )
        
        live.live_food(arcade.load_image(self.filefood_path), scale=1)

    def handle_prey_flee(self, prey_sprite, angle, change_x, change_y):
        """Handle prey fleeing behavior with boundary checking"""
        # Adjust angle to flee away from predator
        angle -= 180
        prey_sprite.angle = angle
        
        # Get current position
        current_x = prey_sprite.center_x
        current_y = prey_sprite.center_y
        
        # Calculate potential new position
        movement_speed = 0.2  # Slowed down movement (1/5)
        new_x = current_x + change_x * movement_speed
        new_y = current_y + change_y * movement_speed
        
        # Check boundaries and adjust movement
        if new_x < BOUNDARY_MARGIN:  # Left boundary
            prey_sprite.change_x = abs(change_x * movement_speed)
        elif new_x > WINDOW_WIDTH - BOUNDARY_MARGIN:  # Right boundary
            prey_sprite.change_x = -abs(change_x * movement_speed)
        else:
            prey_sprite.change_x = change_x * movement_speed
            
        if new_y < BOUNDARY_MARGIN:  # Bottom boundary
            prey_sprite.change_y = abs(change_y * movement_speed)
        elif new_y > WINDOW_HEIGHT - BOUNDARY_MARGIN:  # Top boundary
            prey_sprite.change_y = -abs(change_y * movement_speed)
        else:
            prey_sprite.change_y = change_y * movement_speed

    def stop_fleeing(self, prey_sprite):
        """Stop prey from fleeing"""
        prey_sprite.change_y = 0
        prey_sprite.change_x = 0
        self.fleeing = False

    def is_position_in_bounds(self, position):
        """Check if a position is within game boundaries"""
        x, y = position
        min_bound = BOUNDARY_MARGIN
        max_x = WINDOW_WIDTH - BOUNDARY_MARGIN
        max_y = WINDOW_HEIGHT - BOUNDARY_MARGIN
        
        if (min_bound < x < max_x) and (min_bound < y < max_y):
            return True
        return False

    def update_player_movement(self):
        """Update player movement based on input and stats"""
        # Calculate stamina regeneration rate
        self.stamina_regen_rate = self.sprint_speed / 15
        hunger_decay_rate = self.sprint_speed / 30
        
        # Apply hunger penalty to stamina regeneration
        if self.hunger < 30:
            self.stamina_regen_rate *= 0.5
            
        # Calculate movement direction
        move_x = 0
        move_y = 0
        speed = 0
        
        # Check if any movement keys are pressed
        is_moving = (self.up_pressed or self.down_pressed or 
                     self.left_pressed or self.right_pressed)
        
        # Determine movement speed based on input and stats
        if is_moving:
            if self.shift_pressed and not self.ctrl_pressed:
                # Sprint mode
                if self.stamina > 20 and self.hunger > MIN_HUNGER:
                    speed = self.sprint_speed / 1.25
                    self.stamina -= 0.15
                elif self.stamina > 10 and self.hunger > MIN_HUNGER:
                    speed = self.sprint_speed / 1.5
                    self.stamina -= 0.15
                else:
                    speed = NORMAL_SPEED
            elif self.ctrl_pressed:
                # Sneak mode
                if self.stamina > 20 and self.hunger > MIN_HUNGER:
                    speed = NORMAL_SPEED / 1.5
                    self.stamina -= 0.05
                elif self.stamina > 10 and self.hunger > MIN_HUNGER:
                    speed = NORMAL_SPEED / 2.2
                    self.stamina -= 0.1
                else:
                    speed = NORMAL_SPEED / 2.2
                    self.hunger -= 0.1
                    self.hunger = clamp(self.hunger, MIN_HUNGER, MAX_HUNGER)
            else:
                # Normal movement
                speed = NORMAL_SPEED
        
        # Regenerate stamina if not sprinting/sneaking or not moving
        if (not (self.shift_pressed or self.ctrl_pressed) or not is_moving) and is_moving:
            if self.hunger > MIN_HUNGER and self.stamina < self.max_stamina:
                self.stamina += self.stamina_regen_rate
                self.stamina = clamp(self.stamina, MIN_STAMINA, self.max_stamina)
                self.hunger -= hunger_decay_rate
                self.hunger = clamp(self.hunger, MIN_HUNGER, MAX_HUNGER)
        
        # Get movement direction from input
        if self.up_pressed and self.player_sprite.center_y < (WINDOW_HEIGHT - BOUNDARY_MARGIN):
            move_y += 1
        if self.down_pressed and self.player_sprite.center_y > BOUNDARY_MARGIN:
            move_y -= 1
        if self.left_pressed and self.player_sprite.center_x > BOUNDARY_MARGIN:
            move_x -= 1
        if self.right_pressed and self.player_sprite.center_x < (WINDOW_WIDTH - BOUNDARY_MARGIN):
            move_x += 1
        
        # Normalize direction vector
        magnitude = math.hypot(move_x, move_y)
        if magnitude > 0:
            move_x /= magnitude
            move_y /= magnitude
        
        # Apply final movement
        self.player_sprite.change_x = move_x * speed
        self.player_sprite.change_y = move_y * speed
        
        # Update sprite angle based on movement direction
        self.update_player_angle(move_x, move_y)

    def update_player_angle(self, move_x, move_y):
        """Update player sprite angle based on movement direction"""
        if move_x == 0 and move_y > 0:
            self.player_sprite.angle = 180  # Up
        elif move_x == 0 and move_y < 0:
            self.player_sprite.angle = 0    # Down
        elif move_x < 0 and move_y == 0:
            self.player_sprite.angle = 90   # Left
        elif move_x > 0 and move_y == 0:
            self.player_sprite.angle = 270  # Right
        elif move_x > 0 and move_y > 0:
            self.player_sprite.angle = 225  # Up-Right
        elif move_x < 0 and move_y > 0:
            self.player_sprite.angle = 135  # Up-Left
        elif move_x < 0 and move_y < 0:
            self.player_sprite.angle = 45   # Down-Left
        elif move_x > 0 and move_y < 0:
            self.player_sprite.angle = 315  # Down-Right

    def on_draw(self):
        """Render the screen"""
        self.clear()
        tree_list.draw()
        self.player_list.draw()
        self.manager.draw()
        
        # Draw status bars
        self.draw_hunger_bar(width=self.max_hunger * 2)
        self.draw_stamina_bar(width=self.max_stamina * 4)

    def update_prey_behavior(self):
        """Update prey AI behavior"""
        predator = self.player_sprite
        prey = self.animalsprite
        
        # Get prey stats
        prey_stats = self.prey_data[self.chosen_prey]
        vision_range = prey_stats["vision_range"]
        awareness = prey_stats["awareness"]
        
        # Process AI decision
        is_fleeing, angle, change_x, change_y = self.animal.process_ai(
            predator.position,
            prey.position,
            prey,
            predator,
            vision_range,
            awareness,
            self.logic_timer
        )
        
        if is_fleeing:
            self.fleeing = True
            self.handle_prey_flee(prey, angle, change_x, change_y)

    def on_update(self, delta_time):
        """Update game state for each frame"""
        # Update AI logic at intervals
        self.logic_timer += delta_time
        if self.logic_timer >= 0.25 and not self.fleeing:
            self.update_prey_behavior()
            self.logic_timer = 0.0
            
        # Handle prey fleeing timer
        if self.fleeing:
            self.prey_logic_timer += 1
            if self.prey_logic_timer >= 50:
                self.stop_fleeing(self.animalsprite)
                self.prey_logic_timer = 0
                
        # Update player movement
        self.update_player_movement()

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""
        if key == arcade.key.UP:
            self.up_pressed = True
            # self.movementkey_pressed = True
            self.update_player_movement()
        if key == arcade.key.DOWN:
            self.down_pressed = True
            # self.movementkey_pressed = True
            self.update_player_movement()
        if key == arcade.key.LEFT:
            self.left_pressed = True
            # self.movementkey_pressed = True
            self.update_player_movement()
        if key == arcade.key.RIGHT:
            self.right_pressed = True
            # self.movementkey_pressed = True
            self.update_player_movement()
        if key == arcade.key.LSHIFT:
            self.shift_pressed = True
            self.update_player_movement()
        if key == arcade.key.A:
            # self.renamethis1()
            # live.live_food_functions.load_image(live.live_food_functions)
            live.live_food()
        if key == arcade.key.LCTRL:
            self.ctrl_pressed = True
            self.current_range = self.sneak_range

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key."""
        if key == arcade.key.UP:
            self.up_pressed = False
            self.update_player_movement()
        if key == arcade.key.DOWN:
            self.down_pressed = False
            self.update_player_movement()
        if key == arcade.key.LEFT:
            self.left_pressed = False
            self.update_player_movement()
        if key == arcade.key.RIGHT:
            self.right_pressed = False
            self.update_player_movement()
        if key == arcade.key.LSHIFT:
            self.shift_pressed = False
            self.update_player_movement()
        if key == arcade.key.A:
            self.A_pressed = False
        if key == arcade.key.LCTRL:
            self.ctrl_pressed = False
            self.current_range = self.range

    def top_right_info_add(self, amount=4, text=None, width=200, height=30, font_size=20, bold=True,
                           y_val=(WINDOW_HEIGHT / 2) - 25):
        self.y2 = 60
        for y in range(amount):
            x = y
            if x > 1:
                x *= 1.5
                font_size /= 1.5
            y = arcade.gui.UILabel(
                font_size=font_size,
                text=text[y],
                height=height,
                width=width,
                bold=bold,
                multiline=True
            )
            self.grid.add(y, align_y=y_val - self.y2 * x, align_x=(-WINDOW_WIDTH // 2) + 90)
            self.manager.add(y)
            self.chosen_label = arcade.gui.UILabel(
                font_size=20,
                text=self.chosen_animal1,
                height=20,
                width=200,
                bold=True
            )
            self.grid.add(self.chosen_label, align_y=(WINDOW_HEIGHT / 2) - 25, align_x=0)
            self.manager.add(self.chosen_label)
        """
        #
        # self.health_lab = arcade.gui.UILabel(
        #     font_size=15,
        #     text="Stamina:",
        #     height=40,
        #     width=200,
        #     bold=True
        # )
        # self.grid.add(self.health_lab, align_y=(WINDOW_HEIGHT//2)-25, align_x=(-WINDOW_WIDTH//2)+60)
        # self.manager.add(self.health_lab)
        #
        # self.hunger_lab = arcade.gui.UILabel(
        #     font_size=15,
        #     text="Hunger:",
        #     height=40,
        #     width=200,
        #     bold=True
        # )
        # self.grid.add(self.hunger_lab, align_y=(WINDOW_HEIGHT//2)-85, align_x=(-WINDOW_WIDTH//2)+60)
        # self.manager.add(self.hunger_lab)
        #
        # self.stats_lab = arcade.gui.UILabel(
        #     font_size=12,
        #     text=f"Metabolism = {self.metabolism}\nSpeed = {round(self.stat_speed,ndigits=1)}\nDetectable Range = {self.range}",
        #     height=40,
        #     width=400,
        #     bold=False,
        #     italic=True,
        #     multiline=True
        # )
        # self.grid.add(self.stats_lab, align_x=(-WINDOW_WIDTH // 2) + 100, align_y=(WINDOW_HEIGHT // 2) - 150)
        # self.manager.add(self.stats_lab)
        """

    # def draw_health_bar(self, x=(WINDOW_WIDTH/-2)-100, y=(WINDOW_HEIGHT/2)+200, width=200, height=100):
    def draw_stamina_bar(self, x=(WINDOW_WIDTH // 40), y=WINDOW_HEIGHT - 50, width=None, height=25):
        # Left and right coordinates
        left = x
        right = x + width
        # Correct the Y coordinates
        top = y + height / 2
        bottom = y - height / 2
        # Stamina bar (colored based on health ratio)
        Stamina_ratio = self.stamina / self.max_stamina
        Stamina_right = x + (width * Stamina_ratio)
        color = self.get_Stamina_color()
        arcade.draw_lrbt_rectangle_filled(left, Stamina_right, bottom, top, color)
        # Outline (optional border)
        arcade.draw_lrbt_rectangle_outline(left, right, bottom, top, arcade.color.BLACK, 3)

    def draw_hunger_bar(self, x=(WINDOW_WIDTH // 40), y=WINDOW_HEIGHT - 110, width=None, height=25):
        # Left and right coordinates
        left = x
        right = x + width
        # Correct the Y coordinates
        top = y + height / 2
        bottom = y - height / 2
        # Stamina bar (colored based on a health ratio)
        hunger_ratio = self.hunger / 100
        hunger_right = x + (width * hunger_ratio)
        color = self.get_hunger_color()
        arcade.draw_lrbt_rectangle_filled(left, hunger_right, bottom, top, color)
        # Outline (optional border)
        arcade.draw_lrbt_rectangle_outline(left, right, bottom, top, arcade.color.BLACK, 3)

    def get_Stamina_color(self):
        if self.stamina >= 80:
            return arcade.color.LIGHT_SKY_BLUE
        elif 80 > self.stamina >= 20:
            return arcade.color.YELLOW
        elif self.stamina < 20:
            return arcade.color.RED
        return None

    def get_hunger_color(self):
        if self.hunger >= 80:
            return arcade.color.LIGHT_SKY_BLUE
        elif 80 > self.hunger >= 20:
            return arcade.color.YELLOW
        elif self.hunger < 20:
            return arcade.color.RED
        return None

    # def check_key(self,key):
    #     if key == True:
    #         return True
    #     else:
    #         return False

    def handle_prey_collision(self, prey):
        # Call a helper to execute the async function using asyncio
        self.run_async_task(self.shrink_and_remove_prey(prey))

    def run_async_task(self, coro):
        """Run an async task inside Arcade using the event loop."""
        import asyncio

        # Create or get an existing event loop
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:  # No running loop
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        # Run the coroutine as a task
        loop.create_task(coro)

    async def shrink_and_remove_prey(self, prey):
        # Store original scale
        original_scale = prey.scale
        # Gradually shrink over 2 seconds
        shrink_duration = 1.0  # seconds
        start_time = time.time()

        while time.time() - start_time < shrink_duration:
            elapsed = time.time() - start_time
            progress = elapsed / shrink_duration
            # Calculate new scale (linear interpolation from original to 0)
            prey.scale = original_scale * (1 - progress)
            # Wait for next frame
            await arcade.sleep(1 / 60)

        # Remove the prey and update hunger
        nutritional_value = self.prey_data[prey.creature_type]["nutritional_value"]
        self.hunger = min(self.max_hunger, self.hunger + nutritional_value)
        # Remove prey from sprite lists
        prey.remove_from_sprite_lists()

    def check_prey_collision(self):
        # Get list of all prey that collided with player
        hit_list = arcade.check_for_collision_with_list(
            self.animalsprite,
            self.player_list
        )

        # Handle each collision
        for prey in hit_list:
            if not hasattr(prey, 'is_being_eaten'):  # Prevent multiple collision handling
                prey.is_being_eaten = True
                self.handle_prey_collision(prey)


def main():
    """ Main function """
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT)
    game = GameView1()
    window.show_view(game)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()