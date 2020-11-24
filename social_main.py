"""
Social game modified from example
"""
import arcade
import os
import math
import json
import random as rand
import sys


SPRITE_SCALING = 0.5

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Move Sprite by Angle Example"

MOVEMENT_SPEED = 2
ANGLE_SPEED = 2


class Player(arcade.Sprite):
    """ Player class """

    def __init__(self, image, scale):
        """ Set up the player """

        # Call the parent init
        super().__init__(image, scale)

        # Create a variable to hold our speed. 'angle' is created by the parent
        self.speed = 0

        # get ready to record the actions
        self.d_angle_hist = []
        self.speed_hist = []

    def update(self):
        # Convert angle in degrees to radians.
        angle_rad = math.radians(self.angle)

        # Rotate the ship
        self.angle += self.change_angle

        # Use math to find our change based on our speed and angle
        self.center_x += -self.speed * math.sin(angle_rad)
        self.center_y += self.speed * math.cos(angle_rad)

        # record the actions
        self.d_angle_hist.append(self.change_angle)
        self.speed_hist.append(self.speed)


class Actor(arcade.Sprite):
    """ Actor class ( Previous Players) """

    def __init__(self, image, scale, histories):
        """ Set up the Actor """

        # Call the parent init
        super().__init__(image, scale)

        # Create a variable to hold our speed. 'angle' is created by the parent
        self.speed = 0
        self.counter = 0
        self.histories = histories
        self.init_pos = histories['init_pos']

    def update(self):

        # extract actions or stay still
        if self.counter < len(self.histories['d_angle']):
            d_angle = self.histories['d_angle'][self.counter]
            speed = self.histories['speed'][self.counter]
            # print('move', self.histories['d_angle'][self.counter])
        else:
            d_angle = speed = 0

        # Convert angle in degrees to radians.
        angle_rad = math.radians(self.angle)

        # Rotate the ship
        self.angle += d_angle

        # Use math to find our change based on our speed and angle
        self.center_x += -speed * math.sin(angle_rad)
        self.center_y += speed * math.cos(angle_rad)
        self.counter += 1



class SocialGame(arcade.Window):
    """
    Main application class.
    """

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

        # Set up the player info
        self.player_sprite = None

        self.player_init = None

        self.scene_name = ""

        self.scene_hist = {}

        # Set the background color
        arcade.set_background_color(arcade.color.BLACK)

    def setup(self, load_file = "", actor_name = ""):
        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.actor_list = arcade.SpriteList()

        # Set up the player actor yea it's blue what do you want
        self.player_sprite = Player("./resources/playerShip1_blue.png", SPRITE_SCALING)

        self.player_sprite.player_init = (int(SCREEN_WIDTH * rand.random()), int(SCREEN_HEIGHT * rand.random()))
        self.player_sprite.center_x = self.player_sprite.player_init[0]
        self.player_sprite.center_y = self.player_sprite.player_init[1]
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

    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        arcade.start_render()

        # Draw all the sprites.
        self.player_list.draw()
        self.actor_list.draw()

    def on_update(self, delta_time):
        """ Movement and game logic """

        # Call update on all sprites (The sprites don't do much in this
        # example though.)
        self.player_list.update()
        self.actor_list.update()

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        # Forward/back
        if key == arcade.key.UP:
            self.player_sprite.speed = MOVEMENT_SPEED
        elif key == arcade.key.DOWN:
            self.player_sprite.speed = -MOVEMENT_SPEED

        # Rotate left/right
        elif key == arcade.key.LEFT:
            self.player_sprite.change_angle = ANGLE_SPEED
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_angle = -ANGLE_SPEED

        elif key == arcade.key.ESCAPE:
            self.on_exit_save()
            sys.exit(0)


    def on_exit_save(self):

        if len(self.scene_name) > 0:
            player_dict = {'name': self.player_sprite.actor_name, "d_angle": self.player_sprite.d_angle_hist,
                           'speed': self.player_sprite.speed_hist, "init_pos": self.player_sprite.player_init}

            self.scene_hist[self.player_sprite.actor_name] = player_dict

            with open(self.scene_name, 'w') as fp:
                json.dump(self.scene_hist, fp)
        else:
            pass


    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player_sprite.speed = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_angle = 0


def main():
    """ Main method """

    print("input scene name")
    scene_name = input()

    print("input actor name")
    action_name = input()

    window = SocialGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup("./saved_scene/" + scene_name + ".json", action_name)
    arcade.run()


if __name__ == "__main__":
    main()
