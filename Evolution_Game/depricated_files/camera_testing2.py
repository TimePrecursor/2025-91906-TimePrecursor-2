import arcade
import os

# --- Constants ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
MOVEMENT_SPEED = 5
WORLD_WIDTH = SCREEN_WIDTH * 3  # Total width of the game world
TILE_SIZE = 64
CAMERA_MARGIN = 100  # Distance from edge to start scrolling


class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Scrolling Background Example")
        arcade.set_background_color(arcade.color.AIR_SUPERIORITY_BLUE)

        # Cameras
        self.camera = None
        self.gui_camera = None

        # Game world
        self.player_list = None
        self.tile_list = None
        self.player_sprite = None

        # Scroll tracking
        self.view_left = 0
        self.pressed_keys = set()

        # Background
        self.sky_texture = None

    def setup(self):
        # Initialize sprite lists
        self.player_list = arcade.SpriteList()
        self.tile_list = arcade.SpriteList()

        # Set up cameras
        self.camera = arcade.Camera2D()
        self.gui_camera = arcade.Camera2D()

        # Load background tile
        # Update this path to match where your background image is located
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        image_folder = os.path.join(project_root, "assets", "images", "animal_textures_fixed")
        file_name = "backgroundtileable.jpg"
        file_path = os.path.join(image_folder, file_name)

        try:
            self.sky_texture = arcade.load_texture(file_path)
            self.tile_width = self.sky_texture.width
            self.tile_height = self.sky_texture.height
        except Exception as e:
            print(f"Error loading texture: {e}")
            # Fallback texture size if loading fails
            self.tile_width = 256
            self.tile_height = 256
            self.sky_texture = None

        # Create player
        self.player_sprite = arcade.SpriteSolidColor(30, 30, arcade.color.BLUE)
        self.player_sprite.center_x = 100
        self.player_sprite.center_y = SCREEN_HEIGHT // 2
        self.player_list.append(self.player_sprite)

        # Make floor tiles across the world width
        for x in range(0, WORLD_WIDTH, TILE_SIZE):
            tile = arcade.SpriteSolidColor(TILE_SIZE, TILE_SIZE, arcade.color.DARK_GREEN)
            tile.center_x = x + TILE_SIZE // 2
            tile.center_y = TILE_SIZE // 2
            self.tile_list.append(tile)

    def on_draw(self):
        self.clear()

        # Use the camera
        self.camera.use()

        # Draw tiled background
        if self.sky_texture:
            # Calculate how many tiles we need based on view
            start_x = int(self.view_left // self.tile_width) * self.tile_width
            end_x = start_x + SCREEN_WIDTH + self.tile_width

            for x in range(start_x, end_x, self.tile_width):
                # Using the LBWH format (Left, Bottom, Width, Height)
                arcade.draw_texture_rect(
                    texture=self.sky_texture,
                    rect=arcade.LBWH(
                        left=x,
                        bottom=0,
                        width=self.tile_width,
                        height=SCREEN_HEIGHT
                    )
                )

        # Draw world elements
        self.tile_list.draw()
        self.player_list.draw()

    def on_update(self, delta_time):
        # Process player movement
        self.player_sprite.change_x = 0

        if arcade.key.RIGHT in self.pressed_keys:
            self.player_sprite.change_x = MOVEMENT_SPEED
        elif arcade.key.LEFT in self.pressed_keys:
            self.player_sprite.change_x = -MOVEMENT_SPEED

        # Update player position
        self.player_list.update()

        # Keep player within world boundaries
        if self.player_sprite.left < 0:
            self.player_sprite.left = 0
        elif self.player_sprite.right > WORLD_WIDTH:
            self.player_sprite.right = WORLD_WIDTH

        # --- Manage scrolling ---

        # Scroll right
        right_boundary = self.view_left + SCREEN_WIDTH - CAMERA_MARGIN
        if self.player_sprite.right > right_boundary:
            self.view_left += self.player_sprite.right - right_boundary

        # Scroll left
        left_boundary = self.view_left + CAMERA_MARGIN
        if self.player_sprite.left < left_boundary:
            self.view_left -= left_boundary - self.player_sprite.left

        # Keep view_left within valid bounds
        if self.view_left < 0:
            self.view_left = 0
        elif self.view_left > WORLD_WIDTH - SCREEN_WIDTH:
            self.view_left = WORLD_WIDTH - SCREEN_WIDTH

        # Update camera position
        self.camera.viewport_left = self.view_left
        self.camera.viewport_bottom = 0

    def on_key_press(self, key, modifiers):
        self.pressed_keys.add(key)

    def on_key_release(self, key, modifiers):
        self.pressed_keys.discard(key)


def main():
    game = MyGame()
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()