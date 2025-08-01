"""

"""

import random
import arcade

# --- Constants ---
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = "Spaceship Example"


class GameView(arcade.View):

    def __init__(self):
        """ Initializer """
        # Call the parent class initializer
        super().__init__()

        # Variables that will hold sprite lists
        self.spaceship_list = None

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
        self.spaceship_list = arcade.SpriteList()

        # Set up the player
        # Character image from kenney.nl
        img = "spaceship.png"
        self.spaceship_sprite = arcade.Sprite(img, scale=0.1)
        self.spaceship_sprite.position = WINDOW_WIDTH//2, WINDOW_HEIGHT//2
        self.spaceship_list.append(self.spaceship_sprite)


    def on_draw(self):
        """ Draw everything """

        # Clear the screen to only show the background color
        self.clear()

        # Draw the sprites
        self.spaceship_list.draw()

    def on_update(self, delta_time):
        """ Movement and game logic """
        if arcade.key.LEFT in self.keys_down:
            self.angle -= 2
        if arcade.key.RIGHT in self.keys_down:
            self.angle += 2

        self.spaceship_sprite.angle = self.angle

    def on_key_press(self, key, modifier):
        self.keys_down.add(key)

    def on_key_release(self, key, modifier):
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