import arcade
import arcade.shape_list as SL
import math

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

    # boundary
    for i in range(-12, 13):
        coordinates.append((i, 10))
    for i in range(-12, 13):
        coordinates.append((12, i))
    for i in range(-12, 13):
        coordinates.append((i, -10))
    for i in range(-12, 13):
        coordinates.append((-12, i))

    for i in range(3, 10):
        coordinates.append((i, 0))
    for i in range(10):
        coordinates.append((i, 3))
    # bottom coordinate is (0, -5)
    for i in range(0, -6, -1):
        coordinates.append((3, i))
    for i in range(-2, 3):
        coordinates.append((i, -5))
    for i in range(-3, -9, -1):
        coordinates.append((10, i))
    for i in range(-3, -9, -1):
        coordinates.append((-5, i))
    for i in range(-2, 7):
        coordinates.append((i, 8))

    return coordinates


class GreenSquare(arcade.Sprite):
    def __init__(self, scale, init_pos):
        img = "green-square.png"
        super().__init__(img, scale)
        self.position = init_pos

class Car(arcade.Sprite):
    def __init__(self, scale, init_pos, init_velocity):
        img = "car.png"
        super().__init__(img, scale)
        self.position = init_pos
        self.velocity = init_velocity

    def update(self, keys):
        # degrees rotates clockwise
        angle = self.angle
        # modify the angle to be appropriate for trig
        if arcade.key.UP in keys:
            # accelerate
            self.velocity += 0.1
        if arcade.key.DOWN in keys:
            self.velocity -= 0.1
            if self.velocity < 0:
                self.velocity = 0    
        if arcade.key.RIGHT in keys:
            # turn right
            angle += 2
        if arcade.key.LEFT in keys:
            # turn left
            angle -= 2
            
        self.angle = angle
        x, y = self.position
        trig_angle = -angle
        radians = trig_angle*math.pi/180

        dx = self.velocity * math.cos(radians)
        dy = self.velocity * math.sin(radians)
        x += dx
        y += dy
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

        # create 
        self.init_car_pos = 75, 65
        self.car = Car(0.05, self.init_car_pos, 0)
        self.car_list = arcade.SpriteList()
        self.car_list.append(self.car)
        
        # create flag
        self.flag = arcade.Sprite("flag.png", 0.1)
        self.flag.position = SCREEN_WIDTH-75, SCREEN_HEIGHT-75
        self.flag_list = arcade.SpriteList()
        self.flag_list.append(self.flag)


        self.keys_held = set()
        self.win = False
        self.lose = False
        self.total_time = 0
        self.timer_going = False
        self.best_times = []

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
            self.maze.append(GreenSquare(MAZE_TILE_SIZE/MAZE_TILE_SOURCE_SIZE, (x,y)))

    def on_draw(self):
        # Clear, then draw
        self.clear()
        if self.win:
            arcade.draw_text("YOU WIN!", SCREEN_WIDTH//2, SCREEN_HEIGHT//2, 
                                    arcade.color.GREEN, font_size=50, anchor_x="center", anchor_y="center")
        elif self.lose:
            arcade.draw_text("GAME OVER!", SCREEN_WIDTH//2, SCREEN_HEIGHT//2, 
                                    arcade.color.RED, font_size=50, anchor_x="center", anchor_y="center")
        else:
            self.maze.draw()
            self.car_list.draw()
            self.flag_list.draw()
            # Format the time as seconds with 2 decimal places
        time_string = f"Time: {self.total_time:.2f} seconds"
        arcade.draw_text(time_string, SCREEN_WIDTH//2, SCREEN_HEIGHT - 10, arcade.color.BLUE, 20, anchor_x="center", anchor_y="center")
        for i, time in enumerate(sorted(self.best_times)[:3]):
            arcade.draw_text(f"Best time #{i+1}: {time:.2f} seconds", 10, SCREEN_HEIGHT - 20-(i*30), arcade.color.GOLD, 20)
                
    def on_update(self, delta_time):
        self.car.update(self.keys_held)
        if self.keys_held:
            self.timer_going = True
        if not(self.win or self.lose) and self.timer_going:
            self.total_time += delta_time

        if arcade.key.R in self.keys_held:
            self.win = False
            self.lose = False
            self.total_time = 0
            self.timer_going = False
            self.car.position = self.init_car_pos
            self.car.velocity = 0
            self.car.angle = 0
            return
        
        if arcade.key.ESCAPE in self.keys_held:
            arcade.exit()

        if arcade.check_for_collision_with_list(self.car, self.maze):
            self.lose = True
        # we only set win to True if not currently True
        if arcade.check_for_collision(self.car, self.flag):
            if not self.win:
                self.win = True
                self.best_times.append(self.total_time)
            

    def on_key_press(self, key, modifiers):
        self.keys_held.add(key)

    def on_key_release(self, key, modifiers):
        if key in self.keys_held:
            self.keys_held.remove(key)
    

if __name__ == "__main__":
    MyGame()
    arcade.run()
