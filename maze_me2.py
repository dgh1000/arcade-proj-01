import arcade
import arcade.shape_list as SL

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 1000
SCREEN_TITLE = "maze"

class GreenSquare(arcade.Sprite):
    def __init__(self, scale, init_pos):
        img = "green-square.png"
        super().__init__(img, scale)
        self.position = init_pos

class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.SKY_BLUE)
        self.green_square = GreenSquare(0.1, (SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        self.maze = arcade.SpriteList()
        self.maze.append(self.green_square)

    def on_draw(self):
        self.clear()
        self.maze.draw()

if __name__ == "__main__":
    MyGame()
    arcade.run()
