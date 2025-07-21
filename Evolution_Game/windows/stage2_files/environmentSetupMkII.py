import math
import arcade
import random
import os

tree_list = arcade.SpriteList()
TREE_SPREAD_DISTANCE = 100  # how far apart trees must be
NUMBER_OF_TREES = 11  # how many trees
MAX_ATTEMPTS_PER_TREE = 5  # tries before skipping
scenery_assets = [
    "bolder.png", "bush.png", "lake1.png", "lake3.png", "lake4.png", "meat.png",
    "rock1.png", "rock2.png", "rock3.png", "rock4.png", "rock5.png", "tree1.png"
]

class EnvironmentSetup(arcade.Sprite):
    tree_locations = []
    def asset_paths(self, name="tree1.png"):
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        path = os.path.join(project_root, "assets", "images", "scenery", f"{name}")
        return path

    def is_far_enough(self, x, y):
        """ Check if (x,y) is far enough from existing trees """
        for tree in tree_list:
            if math.hypot(tree.center_x - x, tree.center_y - y) < TREE_SPREAD_DISTANCE:
                return False
        return True

    def create_random_trees(self, tree_texture_path, x_max=1000, y_max=600):
        """Actually spawn the trees, nicely spread """
        skipped_trees = 0
        for _ in range(NUMBER_OF_TREES):
            placed = False
            for attempt in range(MAX_ATTEMPTS_PER_TREE):
                random_x = random.randint(10, x_max-10)
                random_y = random.randint(10, y_max-10)
                if self.is_far_enough(random_x, random_y):
                    tree = arcade.Sprite(tree_texture_path, scale=0.35)
                    tree.center_x = random_x
                    tree.center_y = random_y
                    self.tree_locations.append({"center_x":random_x,"center_y":random_y})
                    tree_list.append(tree)
                    placed = True
                    break
            if not placed:
                skipped_trees += 1
        if skipped_trees > 1:
            print(f"Skipped a tree after too many attempts. x{skipped_trees}")
        else:
            print("Skipped a tree after too many attempts.")