"""

"""

import random
import arcade
import math
from util import *

# --- Constants ---
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = "Spaceship Example"

class Asteroid(arcade.Sprite):

    def __init__(self, init_pos, angle, vel):
        img = "asteroid.png"
        super().__init__(img, 0.2)
        self.position = init_pos[0], init_pos[1]
        self.angle_radians = (angle - 90) * math.pi / 180
        self.vel_x = vel * math.cos(self.angle_radians)
        self.vel_y = -vel * math.sin(self.angle_radians)

    def update(self, dtime):
        x, y = self.position
        self.position = x+self.vel_x, y+self.vel_y
        if self.position[0] < 0 or self.position[0] > WINDOW_WIDTH:
            self.kill()
        if self.position[1] < 0 or self.position[1] > WINDOW_HEIGHT:
            self.kill()

class Bullet(arcade.Sprite):

    def __init__(self, init_pos, angle, vel):
        super().__init__("bullet.png", 0.2)
        self.position = init_pos[0], init_pos[1]
        self.angle_radians = (angle - 90) * math.pi / 180
        self.vel_x = vel * math.cos(self.angle_radians)
        self.vel_y = -vel * math.sin(self.angle_radians)

    def update(self, dtime):
        x, y = self.position
        self.position = x+self.vel_x, y+self.vel_y
        if self.position[0] < 0 or self.position[0] > WINDOW_WIDTH:
            self.kill()
        if self.position[1] < 0 or self.position[1] > WINDOW_HEIGHT:
            self.kill()

class GameView(arcade.View):

    def __init__(self):
        """ Initializer """
        # Call the parent class initializer
        super().__init__()

        # Variables that will hold sprite lists
        self.spaceship_list = None
        self.bullet_list = None
        self.asteroid_list = None

        # Create a variable to hold the player sprite
        self.spaceship_sprite = None

        # Hide the mouse cursor while it's over the window
        self.window.set_mouse_visible(False)

        self.background_color = arcade.color.BLACK
        
        self.keys_down = set()

        self.angle = 0

    def setup(self):
        """ Set up the game and initialize the variables. """

        # Create the sprite lists

        self.spaceship_sprite = arcade.Sprite("spaceship.png", scale=0.1)
        self.spaceship_sprite.position = WINDOW_WIDTH//2, WINDOW_HEIGHT//2
        self.spaceship_list = arcade.SpriteList()
        self.spaceship_list.append(self.spaceship_sprite)
        self.asteroid_list = arcade.SpriteList()
        self.asteroid_list.append(Asteroid((300,300), 0, 1))

        # Set up the bullet
        # self.bullet_sprite = Bullet((300, 300), 0, 2)
        self.bullet_list = arcade.SpriteList()
        # self.bullet_list.append(self.bullet_sprite)


    def on_draw(self):
        """ Draw everything """

        # Clear the screen to only show the background color
        self.clear()

        # Draw the sprites
        self.spaceship_list.draw()
        self.bullet_list.draw()
        self.asteroid_list.draw()

    def handle_collisions(self):
        for b in self.bullet_list:
            cols = arcade.check_for_collision_with_list(b, self.asteroid_list)
            for a in cols:
                a.remove_from_sprite_lists()

    def new_asteroid(self):
        i = random.randint(0, 3)
        n = None
        if i == 0:
            # add along bottom border
            n = Vector(random.randint(0, WINDOW_WIDTH), 0)
        elif i == 1:
            # along top border
            n = Vector(random.randint(0, WINDOW_WIDTH), WINDOW_HEIGHT)
        elif i == 2:
            # add along left border
            n = Vector(0, random.randint(0, WINDOW_HEIGHT))
        else:
            # add along right border
            n = Vector(WINDOW_WIDTH, random.randint(0, WINDOW_HEIGHT))
        center = Vector(WINDOW_WIDTH//2, WINDOW_HEIGHT//2)
        d = center - n
        a = d.angle() * 180 / math.pi
        self.asteroid_list.append(Asteroid((n.x, n.y), a, 1))

    def update_spaceship():
        pass

    def on_update(self, delta_time):
        self.handle_collisions()

        """ Movement and game logic """
        self.bullet_list.update()
        if arcade.key.LEFT in self.keys_down:
            self.angle -= 2
        if arcade.key.RIGHT in self.keys_down:
            self.angle += 2
        self.spaceship_sprite.angle = self.angle
        self.asteroid_list.update()

        if 1 == random.randint(0, 45):
            self.new_asteroid()

    def on_key_press(self, key, modifier):
        if key == arcade.key.ESCAPE:
            arcade.close_window()
        elif key == arcade.key.SPACE:
            b = Bullet((WINDOW_WIDTH//2, WINDOW_HEIGHT//2), self.spaceship_sprite.angle, 2)
            self.bullet_list.append(b)
        else:
            self.keys_down.add(key)

    def on_key_release(self, key, modifier):
        if key in self.keys_down:
            self.keys_down.remove(key)


def main():
    """ Main function """
    # Create a window class. This is what actually shows up on screen
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)

    # Create and setup the GameView
    game = GameView()
    game.setup()

    # Show GameView on screen
    window.show_view(game)

    # Start the arcade game loop
    arcade.run()


if __name__ == "__main__":
    main()