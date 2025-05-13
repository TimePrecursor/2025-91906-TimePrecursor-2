import math
import arcade
import random
import os

tree_list = arcade.SpriteList()
TREE_SPREAD_DISTANCE = 100  # how far apart trees must be
NUMBER_OF_TREES = 5  # how many trees
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
        print(path)
        return path

    def is_far_enough(self, x, y):
        """ Check if (x,y) is far enough from existing trees """
        for tree in tree_list:
            if math.hypot(tree.center_x - x, tree.center_y - y) < TREE_SPREAD_DISTANCE:
                return False
        return True

    def create_random_trees(self, tree_texture_path, x_max=1000, y_max=600):
        """ Actually spawn the trees, nicely spread """
        for _ in range(NUMBER_OF_TREES):
            placed = False
            for attempt in range(MAX_ATTEMPTS_PER_TREE):
                random_x = random.randint(10, x_max-10)
                random_y = random.randint(10, y_max-10)
                if self.is_far_enough(random_x, random_y):
                    tree = arcade.Sprite(tree_texture_path, scale=0.1)
                    tree.center_x = random_x
                    tree.center_y = random_y
                    self.tree_locations.append({"center_x":random_x,"center_y":random_y})
                    tree_list.append(tree)
                    placed = True
                    print("made a tree")
                    break
            if not placed:
                print("Skipped a tree after too many attempts.")



    # def treelocations(self, tree_locations=None):
    #     print(tree_locations)
    #     return(tree_locations)
    #     # print(self.tree_locations)

# window = arcade.Window(1280, 720, "Tree Spread Example")
# environment = EnvironmentSetup()
# window.background_color = arcade.color.AMAZON
# # Where your tree image is
# tree_image_path = "tree1.png"  # Or wherever you store it
#
# # Call this ONCE to create the trees
# environment.create_random_trees(EnvironmentSetup.asset_paths(EnvironmentSetup))
#
# @window.event
# def on_draw():
#     window.clear()
#     environment.draw_trees()
#
# arcade.run()

