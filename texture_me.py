import arcade

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Minimal Texture Example (Arcade 3.x)"

class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.ALMOND)

        # Load an image as a Texture
        self.texture = arcade.load_texture(":resources:images/tiles/grassCenter.png")

    def on_draw(self):
        arcade.start_render()
        # Draw using left, right, width, height version
        arcade.draw_lbwh_rectangle_textured(
            400, 300,  # lower-left corner
            self.texture.width, self.texture.height,
            self.texture
        )

if __name__ == "__main__":
    MyGame()
    arcade.run()
