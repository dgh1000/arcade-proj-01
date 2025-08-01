"""
arrow keys move a little box one step per press. holding down
does nothing
"""
import arcade
from util import *

# Define screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Bad Arcade View Ex"

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
        self.pos = Vector(SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
        self.keys_down = set()

    def on_draw(self):
        """
        Called whenever the window needs to be drawn.
        This is where all the drawing commands go.
        """
        # Clear the screen to the background color
        self.clear()
        arcade.draw_xywh_rectangle_filled(self.pos.x, self.pos.y, 20, 20, arcade.color.BLUE)

    def on_update(self, elapsed_time):
        """
        All the game logic goes here. This method is called every frame.
        'delta_time' is the time in seconds since the last update.
        """
        if arcade.key.UP in self.keys_down:
            self.pos += Vector(0, 1)
        elif arcade.key.DOWN in self.keys_down:
            self.pos += Vector(0, -1)
        elif arcade.key.RIGHT in self.keys_down:
            self.pos += Vector(1, 0)
        elif arcade.key.LEFT in self.keys_down:
            self.pos += Vector(-1, 0)
        

    def on_key_press(self, key, modifiers):
        """
        Called when the user releases a key.
        """
        if key == arcade.key.ESCAPE:
            arcade.close_window()
        # In this simple example, we don't need to do anything on key release
        self.keys_down.add(key)

    def on_key_release(self, key, modifiers):
        self.keys_down.remove(key)

def main():
    """ Main function to start the game """
    game = MyGameWindow(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.run()

if __name__ == "__main__":
    main()
