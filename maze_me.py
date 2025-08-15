"""
arrow keys move a little box one step per press. holding down
does nothing
"""
import arcade
from util import *
from arcade.shape_list import ShapeElementList, create_ellipse_filled

# Define screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Maze"

def make_vehicle(x, y):
    size = 50
    texture = arcade.Texture.create_empty("circle_texture", (size, size))

    # Step 2: Draw onto the texture using the Pyglet image buffer
    from arcade.shape_list import ShapeElementList, create_ellipse_filled
    shape_list = ShapeElementList()
    shape_list.append(create_ellipse_filled(size/2, size/2, size, size, arcade.color.BLUE))

    # Render the shapes into the texture's image
    image = arcade.get_image(shape_list, size, size)
    texture = arcade.Texture("circle_texture", image=image)

    # Step 3: Make the sprite from that texture
    sprite = arcade.Sprite(center_x=400, center_y=300)
    sprite.texture = texture
    return sprite

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
        arcade.set_background_color(arcade.color.BLACK)

        # Initialize game state variables
        self.pos = Vector(SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
        self.keys_held = set()
        self.vehicle_sprite = make_vehicle(SCREEN_WIDTH//2, SCREEN_HEIGHT//2)

    def on_draw(self):
        """
        Called whenever the window needs to be drawn.
        This is where all the drawing commands go.
        """
        # Clear the screen to the background color
        self.clear()
        # arcade.draw_lbwh_rectangle_filled(self.pos.x, self.pos.y, 20, 20, arcade.color.BLUE)
        arcade.draw_sprite(self.vehicle_sprite)


    def on_update(self, elapsed_time):
        """
        All the game logic goes here. This method is called every frame.
        'delta_time' is the time in seconds since the last update.
        """
        if arcade.key.UP in self.keys_held:
            self.pos += Vector(0, 1)
        if arcade.key.DOWN in self.keys_held:
            self.pos += Vector(0, -1)
        if arcade.key.LEFT in self.keys_held:
            self.pos += Vector(-1, 0)
        if arcade.key.RIGHT in self.keys_held:
            self.pos += Vector(1, 0)
            

    def on_key_press(self, key, modifiers):
        """
        Called when the user releases a key.
        """
        self.keys_held.add(key)
        # In this simple example, we don't need to do anything on key release

    def on_key_release(self, key, modifiers):
        if key in self.keys_held:
            self.keys_held.remove(key)      

def main():
    """ Main function to start the game """
    game = MyGameWindow(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.run()

if __name__ == "__main__":
    print("Arcade version", arcade.__version__)
    main()
