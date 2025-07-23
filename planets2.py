import arcade
from util import *

# Define screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Good Arcade View Ex"
GRAVITY = 25

class Planet:
    def __init__(self, x, y, mass):
        self.pos = (x, y)
        self.mass = mass
        self.vel = (0, 0)

    def draw(self):
        x, y = self.pos
        arcade.draw_circle_filled(center_x=x, center_y=y, radius=20, color=arcade.color.BLUE)

    def move(self, elapsed):
        self.pos = vec_add(self.pos, vec_mult(elapsed, self.vel))

class MyGameWindow(arcade.Window):
    """
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
        planet1 = Planet(SCREEN_WIDTH // 2 + 150, SCREEN_HEIGHT // 2 + 10, 5)
        planet1.vel = (0, 50)
        planet2 = Planet(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 40, 5)
        planet2.vel = (0, -50)
        planet3 = Planet(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 500)
        self.planets = [planet1, planet2, planet3]

    def on_draw(self):
        """
        Called whenever the window needs to be drawn.
        This is where all the drawing commands go.
        """
        # Clear the screen to the background color
        self.clear()
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
                    dv = vec_sub(p2.pos, p1.pos)
                    d = vec_mag(dv)
                    force = p1.mass * p2.mass * GRAVITY / (d**2)
                    df1 = vec_mult(force/p1.mass, vec_norm(dv))
                    df2 = vec_mult(force/p2.mass, vec_norm(dv))
                    if d > 25:
                        p1.vel = vec_add(p1.vel, df1)
                        p2.vel = vec_sub(p2.vel, df2)

        for p in self.planets:
            p.move(elapsed_time)


    # def on_key_press(self, key, modifiers):
    #     """
    #     Called whenever a key is pressed.
    #     """
    #     if key == arcade.key.LEFT:
    #         self.player_x -= self.player_speed
    #     elif key == arcade.key.RIGHT:
    #         self.player_x += self.player_speed
    #     elif key == arcade.key.UP:
    #         self.player_y += self.player_speed
    #     elif key == arcade.key.DOWN:
    #         self.player_y -= self.player_speed

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
