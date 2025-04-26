import arcade
import os

# --- Constants ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
MOVEMENT_SPEED = 5
SCROLL_LIMIT = SCREEN_WIDTH * 2
TILE_SIZE = 64


class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Scrolling Background Example")
        arcade.set_background_color(arcade.color.AIR_SUPERIORITY_BLUE)

        # Cameras
        self.camera = arcade.Camera2D()
        self.gui_camera = arcade.Camera2D()

        # Game world
        self.player_list = arcade.SpriteList()
        self.tile_list = arcade.SpriteList()
        self.player_sprite = None

        # Scroll tracking
        self.world_scroll = 0
        self.pressed_keys = set()

        # Background
        self.sky_texture = None

    def setup(self):
        # Load background tile
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        image_folder = os.path.join(project_root, "assets", "images", "animal_textures_fixed")
        file_name = "backgroundtileable.jpg"
        file_path = os.path.join(image_folder, file_name)
        self.sky_texture = arcade.load_texture(file_path)  # Must exist in folder
        self.tile_width = self.sky_texture.width
        self.tile_height = self.sky_texture.height

        # Create player
        self.player_sprite = arcade.SpriteCircle(15, arcade.color.BLUE)
        self.player_sprite.center_x = 100
        self.player_sprite.center_y = SCREEN_HEIGHT // 2
        self.player_list.append(self.player_sprite)

        # Make floor tiles 3x screen width
        for x in range(-TILE_SIZE, SCREEN_WIDTH * 3, TILE_SIZE):
            tile = arcade.SpriteSolidColor(TILE_SIZE, TILE_SIZE, arcade.color.DARK_GREEN)
            tile.center_x = x + TILE_SIZE // 2
            tile.center_y = TILE_SIZE // 2
            self.tile_list.append(tile)

    def on_draw(self):
        self.clear()
        self.camera.use()

        # Tiled background (scrolls with camera)
        # Adjust the background position based on camera's position
        for x in range(-self.tile_width, SCREEN_WIDTH * 3, self.tile_width):
            arcade.draw_texture_rect(
                texture=self.sky_texture,  # Your background texture
                rect=arcade.LBWH(
                    x - (self.world_scroll % self.tile_width),  # Adjusted position for scrolling
                    0,  # Align with the bottom of the screen
                    self.tile_width,
                    SCREEN_HEIGHT
                )
            )

        # World
        self.tile_list.draw()
        self.player_list.draw()

    def on_update(self, delta_time):

        CAMERA_MARGIN = 100

        # --- Scroll the screen ---
        screen_left = self.camera.viewport_left
        screen_right = self.camera.viewport_left + self.width

        # Move camera right if player is too close to right edge
        if self.player_sprite.right > screen_right - CAMERA_MARGIN:
            self.world_scroll += MOVEMENT_SPEED

        # Move camera left if player is too close to left edge
        if self.player_sprite.left < screen_left + CAMERA_MARGIN:
            self.world_scroll -= MOVEMENT_SPEED

        # Optional: Stop scrolling after 2x screen width
        max_scroll = SCREEN_WIDTH * 2
        if self.world_scroll > max_scroll:
            self.world_scroll = max_scroll
        if self.world_scroll < 0:
            self.world_scroll = 0

        # Player movement input
        self.player_sprite.change_x = 0
        if arcade.key.RIGHT in self.pressed_keys:
            self.player_sprite.change_x = MOVEMENT_SPEED
        elif arcade.key.LEFT in self.pressed_keys:
            self.player_sprite.change_x = -MOVEMENT_SPEED

        # Prevent player from moving off the screen
        if self.player_sprite.left < 0:
            self.player_sprite.left = 0
        if self.player_sprite.right > SCREEN_WIDTH:
            self.player_sprite.right = SCREEN_WIDTH

        self.player_list.update()

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
