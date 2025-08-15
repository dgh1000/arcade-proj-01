import arcade
import arcade.shape_list as SL

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 1000
SCREEN_TITLE = "maze"
MAZE_TILE_SIZE = 50
MAZE_TILE_SOURCE_SIZE = 200


def create_maze():
    # create coordinates of their centers
    # assuming they have size (1, 1)
    # (0, 0), (1, 0), (2, 0) through (9,0)
    coordinates = []
    for i in range(10):
        coordinates.append((i, 0))
    return coordinates


class GreenSquare(arcade.Sprite):
    def __init__(self, scale, init_pos):
        img = "green-square.png"
        super().__init__(img, scale)
        self.position = init_pos

class Car(arcade.Sprite):
    def __init__(self, scale, init_pos):
        img = "car.png"
        super().__init__(img, scale)
        self.position = init_pos

    def update_position(self, x, y):
        # this gets called with x, y = 500, 600
        # self.rotation = 
        #   right: 0
        #   left: 180
        #   up: -90
        #   down: 90
        cur_x, cur_y = self.position
        if x > cur_x:
            self.angle = 0
        if x < cur_x:
            self.angle = 180
        if y > cur_y:
            self.angle = -90
        if y < cur_y:
            self.angle = 90

        self.position = x, y
    
class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.SKY_BLUE)

        # create maze
        # self.green_square = GreenSquare(0.3, (SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        self.maze = arcade.SpriteList()
        self.create_maze()
        # self.maze.append(self.green_square)

        # create car
        self.car = Car(0.05, (100, 100))
        self.car_list = arcade.SpriteList()
        self.car_list.append(self.car)
        
        self.keys_held = set()

    def create_maze(self):
        coords = create_maze()
        # this is the size we want it to be in the game
        # MAZE_TILE_SIZE = 50
        # this is size of square in png file
        # MAZE_TILE_SOURCE_SIZE = 200
        for x, y in coords:
            # first param to GreenSquare if scale factor. multiply size of png file
            # by this scale factor
            # maze coords: 0, 0 is the center of the screen. they are one unit
            # 0, 1 is just to the right of 0, 0. size 50
            # 0, 0 and 0, 1: we want the sprites at (0,400) & (0, 450)
            x = x * MAZE_TILE_SIZE + SCREEN_WIDTH//2
            y = y * MAZE_TILE_SIZE + SCREEN_HEIGHT//2
            self.maze.append(GreenSquare(MAZE_TILE_SIZE/MAZE_TILE_SOURCE_SIZE, (x,y)))

    def on_draw(self):
        self.clear()
        self.maze.draw()
        self.car_list.draw()

    def on_update(self, delta_time):
        x, y = self.car.position
        if arcade.key.UP in self.keys_held:
            y += 2
        if arcade.key.DOWN in self.keys_held:
            y -= 2
        if arcade.key.RIGHT in self.keys_held:
            x += 2
        if arcade.key.LEFT in self.keys_held:
            x -= 2

        self.car.update_position(x, y)

        if arcade.check_for_collision_with_list(self.car, self.maze):
            arcade.exit()


    def on_key_press(self, key, modifiers):
        self.keys_held.add(key)

    def on_key_release(self, key, modifiers):
        if key in self.keys_held:
            self.keys_held.remove(key)
    

if __name__ == "__main__":
    MyGame()
    arcade.run()
