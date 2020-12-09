from social_main import Player
from social_main import Actor
from social_main import SocialGame

import arcade
import os
import math
import json
import random as rand
import sys
import numpy as np
import argparse



SPRITE_IMAGE_SIZE = 128
SPRITE_SCALING = 0.25
SPRITE_SIZE = SPRITE_IMAGE_SIZE * SPRITE_SCALING

# SPRITE_SCALING = 0.5

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Move Sprite Social"

MOVEMENT_SPEED = 2
ANGLE_SPEED = 2


class Robot(Player):
    """ Robot class """
    def __init__(self, image, scale, hist):
        """ Set up the Robot """

        # Call the parent init
        super().__init__(image, scale)

        self.x_hist = hist[0]
        self.y_hist = hist[1]
        self.t_hist = np.degrees(hist[2])
        self.counter = 0

    def update(self):

        if self.counter >= len(self.x_hist):
            self.angle =    self.t_hist[-1]
            self.center_x = self.x_hist[-1]
            self.center_y = self.y_hist[-1]
        else:
            self.angle = self.t_hist[self.counter]
            self.center_x = self.x_hist[self.counter]
            self.center_y = self.y_hist[self.counter]
            self.counter += 1




class SocialReplay(SocialGame):

    def __init__(self, width, height, title):
        """
        Initializer
        """

        # Call the parent class initializer
        super().__init__(width, height, title)

        # Set the working directory (where we expect to find files) to the same
        # directory this .py file is in. You can leave this out of your own
        # code, but it is needed to easily run the examples using "python -m"
        # as mentioned at the top of this program.
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        # Variables that will hold sprite lists
        self.player_list = None
        self.actor_list = None
        self.wall_list = None
        self.interest_list = None

        # Set up the player info
        self.player_sprite = None
        self.player_init = None
        self.player_order = None

        # set up scene info
        self.scene_name = ""
        self.scene_hist = {}

        # Set the background color
        arcade.set_background_color(arcade.color.BLACK)


    def setup(self, load_file="", actor_name="r", hist =[]):
        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.actor_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.interest_list = arcade.SpriteList()

        # Set up the player actor yea it's blue what do you want
        self.player_sprite = Robot("./resources/playerShip1_blue.png", SPRITE_SCALING, hist)

        self.player_sprite.player_init = (int(SCREEN_WIDTH * rand.random()), int(SCREEN_HEIGHT * rand.random()))
        self.player_sprite.center_x = hist[0][0]
        self.player_sprite.center_y = hist[0][1]
        self.player_sprite.actor_name = actor_name
        self.player_list.append(self.player_sprite)

        if len(load_file) == 0:
            print("no scene read")
            pass
        else:
            self.scene_name = load_file
            print("opening scene " + load_file)
            try:
                f = open(load_file)
                hist = json.load(f)
                self.scene_hist = hist
                for actor_name in hist:
                    actor_sprite = Actor(":resources:images/space_shooter/playerShip2_orange.png", SPRITE_SCALING,
                                         hist[actor_name])
                    actor_sprite.center_x = int(hist[actor_name]["init_pos"][0])
                    actor_sprite.center_y = int(hist[actor_name]["init_pos"][1])
                    self.actor_list.append(actor_sprite)
            except FileNotFoundError:
                print("no scene found")
                sys.exit(0)

        self.player_order = len(self.actor_list)

        self.setupRoom1()

    def setupRoom1(self):

        wall_res = ":resources:images/tiles/dirtCenter.png"
        # Wall 1
        for lenghts in np.arange(0, SCREEN_HEIGHT / 3, SPRITE_SIZE):
            wall_sprite = arcade.Sprite(wall_res, SPRITE_SCALING)
            wall_sprite.center_x = SCREEN_WIDTH / 3
            wall_sprite.center_y = lenghts
            self.wall_list.append(wall_sprite)

        wall_sprite = arcade.Sprite(wall_res, SPRITE_SCALING)
        wall_sprite.center_x = SCREEN_WIDTH / 3
        wall_sprite.center_y = SCREEN_HEIGHT / 3
        self.wall_list.append(wall_sprite)

        # Wall 2
        for lenghts in np.arange(SCREEN_WIDTH, 2 * SCREEN_WIDTH / 3, -SPRITE_SIZE):
            wall_sprite = arcade.Sprite(wall_res, SPRITE_SCALING)
            wall_sprite.center_x = lenghts
            wall_sprite.center_y = 2 * SCREEN_HEIGHT / 3
            self.wall_list.append(wall_sprite)

        wall_sprite = arcade.Sprite(wall_res, SPRITE_SCALING)
        wall_sprite.center_x = 2 * SCREEN_WIDTH / 3
        wall_sprite.center_y = 2 * SCREEN_HEIGHT / 3
        self.wall_list.append(wall_sprite)

        # Wall 3
        for lenghts in np.arange(0, SCREEN_WIDTH / 2, SPRITE_SIZE):
            wall_sprite = arcade.Sprite(wall_res, SPRITE_SCALING)
            wall_sprite.center_x = lenghts
            wall_sprite.center_y = 2 * SCREEN_HEIGHT / 3
            self.wall_list.append(wall_sprite)

        wall_sprite = arcade.Sprite(wall_res, SPRITE_SCALING)
        wall_sprite.center_x = SCREEN_WIDTH / 2
        wall_sprite.center_y = 2 * SCREEN_HEIGHT / 3
        self.wall_list.append(wall_sprite)

        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite,
                                                         self.wall_list)

        wat_sprite = arcade.Sprite(":resources:images/items/gemBlue.png", SPRITE_SCALING)
        wat_sprite.center_x = SCREEN_WIDTH / 6
        wat_sprite.center_y = SCREEN_HEIGHT / 6
        self.interest_list.append(wat_sprite)

        fir_sprite = arcade.Sprite(":resources:images/items/gemRed.png", SPRITE_SCALING)
        fir_sprite.center_x = 5 * SCREEN_WIDTH / 6
        fir_sprite.center_y = SCREEN_HEIGHT / 2
        self.interest_list.append(fir_sprite)

        tab_sprite = arcade.Sprite(":resources:images/items/gemGreen.png", SPRITE_SCALING)
        tab_sprite.center_x = SCREEN_WIDTH / 4
        tab_sprite.center_y = 5 * SCREEN_HEIGHT / 6
        self.interest_list.append(tab_sprite)

    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        arcade.start_render()

        # Draw all the sprites.
        self.player_list.draw()
        self.actor_list.draw()
        self.wall_list.draw()
        self.interest_list.draw()
        pass

    def on_update(self, delta_time):
        """ Movement and game logic """

        # Call update on all sprites (The sprites don't do much in this
        # example though.)
        self.player_list.update()
        self.actor_list.update()

    def on_key_press(self, key, modifiers):
        pass

    def on_exit_save(self):
        pass

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """
        pass


def main_replay(scene, robot):
    """ Main method """

    if scene is None:
        print("input scene name (use first if you don't know what to do) ")
        scene = input()

    if robot is None:
        print("input actor name (can over write existing actor) ")
        robot = input()


    load_file = "./saved_scene_tasks_order/" + scene + ".json"
    load_file_r = "./saved_results/" + robot + ".json"

    # tune some things here I guess
    exist = True
    repeat = False

    if len(load_file) == 0:
        pass
    else:
        try:
            f = open(load_file)
            hist = json.load(f)
            res = not hist
            if res:
                exist = False
        except FileNotFoundError:
            print("no scene found")
            sys.exit(0)


    if len(load_file_r) == 0:
        pass
    else:
        try:
            f = open(load_file_r)
            hist_robot = json.load(f)
            res = not hist_robot
            if res:
                exist = False
        except FileNotFoundError:
            print("no scene found")
            sys.exit(0)

    print("Press enter to start now")
    input()


    window = SocialReplay(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

    # print(len(hist_robot['hist']))

    window.setup("./saved_scene_tasks_order/" + scene + ".json", robot, hist_robot['hist'])

    print("use ARROWS to move and ESC to save!")
    arcade.run()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Play spaceship game.')
    parser.add_argument('--scene', help='scene name')
    parser.add_argument('--robot', help='robot name')
    args = parser.parse_args()
    main_replay(args.scene, args.robot)
