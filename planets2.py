import arcade
from util import *
from copy import copy

# Define screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Bad Arcade View Ex"
GRAVITY = 25

class Planet:
    def __init__(self, x, y, mass, color):
        self.pos = Vector(x, y)
        self.mass = mass
        self.vel = Vector(0, 0)
        self.color = color
        self.lastpos = []

    def draw(self):
        x, y = (self.pos.x, self.pos.y)
        # self.vel is current velocity as vector. find velocity as a scalar
        # x and y component. magnitude of the vector
        # not tracking the color as its on variable
        # we're not incrementing or decrementing it when the speed changes
        s = self.vel.magnitude()
        # compute a green component of the color
        r = int(s)
        c = (r,5,5)

        arcade.draw_circle_filled(center_x=x, center_y=y, radius=20, color=c)
        # for pos in self.lastpos:
        #     x = pos.x
        #     y = pos.y
        #     arcade.draw_circle_filled(center_x=x, center_y=y, radius=10, color=arcade.color.GRAY)

    def move(self, elapsed):
        # keep track of last three positions by saving self.pos first
        # a list to keep track of these positions
            
        self.lastpos.append(copy(self.pos))
        if len(self.lastpos) > 20:
            del self.lastpos[0]
        self.pos += self.vel * elapsed

    def set_vel(self, vel):
        self.vel = vel

# inherits from a class provided by the game engine
# we're making a game that has a main window
class MyGameWindow(arcade.Window):
    """
    Here's another note.
    Main application class that inherits directly from arcade.Window.
    This class will handle all drawing and updating logic.
    """

    def __init__(self, width, height, title):
        """
        Initializer for the game window.
        Sets up the window and any initial game state.
        """
        super().__init__(width, height, title)

        # Set the background color
        arcade.set_background_color(arcade.color.WHITE)

        # Initialize game state variables
        planet1 = Planet(SCREEN_WIDTH // 2 + 150, SCREEN_HEIGHT // 2 + 10, 50, arcade.color.BLUE)
        planet1.vel = Vector(0, 50)
        planet2 = Planet(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 40, 50, arcade.color.RED)
        planet2.vel = Vector(0, -50)
        planet3 = Planet(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 500, arcade.color.ORANGE)
        self.planets = [planet1, planet2, planet3]

    def on_draw(self):
        """
        Called whenever the window needs to be drawn.
        This is where all the drawing commands go.
        """
        # Clear the screen to the background color
        # self.clear()
        for p in self.planets:
            p.draw()

    def on_update(self, elapsed_time):
        """
        All the game logic goes here. This method is called every frame.
        'delta_time' is the time in seconds since the last update.
        """
        for i in range(len(self.planets)):
            for j in range(len(self.planets)):
                if i != j:
                    p1 = self.planets[i]
                    p2 = self.planets[j]
                    dv = p2.pos - p1.pos
                    d = dv.magnitude()
                    force = p1.mass * p2.mass * GRAVITY / (d**2)
                    df1 = dv.normalize() * (force / p1.mass)
                    if d > 25:
                        p1.set_vel(p1.vel+df1)

        for p in self.planets:
            p.move(elapsed_time)

    def on_key_release(self, key, modifiers):
        """
        Called when the user releases a key.
        """
        # In this simple example, we don't need to do anything on key release
        pass

def main():
    """ Main function to start the game """
    game = MyGameWindow(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.run()

if __name__ == "__main__":
    main()
