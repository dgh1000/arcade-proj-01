import arcade
from util import *
from copy import copy

# Define screen dimensions
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Bad Arcade View Ex"
GRAVITY = 25

# Computes planet 1 pulling on planet 2
def compute_gravity(pos1, pos2, mass1, mass2, elapsed_time):
    gravity_factor = 0.0005
    v = pos1 - pos2
    n = v.normalize()
    d = v.magnitude()
    force = n * (mass1 * mass2 * (d ** 0.5) * gravity_factor * elapsed_time)
    return force

class Movable(arcade.Sprite):

    def __init__(self, img, scale, pos, vel, mass):
        super().__init__(img, scale)
        self.position = (pos.x, pos.y)
        self.vel = vel
        self.mass = mass

    def update(self, delta_time):
        v = self.vel*delta_time
        x, y = self.position
        self.position = (x+v.x, y+v.y)
        if x < 0 or x > SCREEN_WIDTH or y < 0 or y > SCREEN_HEIGHT:
            self.kill()
        
            
                  
class Spaceship(Movable):
    def __init__(self, pos, vel, mass):
        super().__init__("spaceship.png", 0.1, pos, vel, mass)
        self.bullet_list = arcade.SpriteList()
        
    # def update(self, elapsed_time):
    #     x, y = self.position
    #     if x < 0 or x > SCREEN_WIDTH or y < 0 or y > SCREEN_HEIGHT:
    #         self.kill()
    #         return
    #     self.position = (self.vel.x+x, self.vel.y+y)

    def update_bullets(self, keys, elapsed_time):
        if arcade.key.SPACE in keys:
            self.new_bullet()
        for b in self.bullet_list:
            b.update(elapsed_time)



    def new_bullet(self):
        angle_radians = (-self.angle+90)*math.pi/180
        vel_x = 60 * math.cos(angle_radians)
        vel_y = 60 * math.sin(angle_radians)
        x, y = self.position
        self.bullet_list.append(Movable("bullet.png", 0.2, Vector(x, y), Vector(vel_x, vel_y), 0))

    def draw_bullets(self):
        self.bullet_list.draw()


        

class Planet(Movable):
    def __init__(self, pos, vel, mass):
        super().__init__("asteroid.png", 0.3, pos, vel, mass)

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
        arcade.set_background_color(arcade.color.BLACK)

        # Initialize game state variables

        planet1 = Spaceship(Vector(SCREEN_WIDTH // 2 + 150, SCREEN_HEIGHT // 2 + 10), 
                         Vector(0, 50), 30)
        planet2 = Planet(Vector(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 40), 
                         Vector(0, -50), 40)
        planet3 = Planet(Vector(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 - 40), 
                         Vector(0, 70), 50)
        self.center_planet = Planet(Vector(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), 
                                    Vector(0, 0), 150)
        self.planets = [planet1, planet2, planet3]
        self.planets_list = arcade.SpriteList()
        for p in self.planets:
            self.planets_list.append(p)
        self.center_list = arcade.SpriteList()
        self.center_list.append(self.center_planet)

        self.keys_held = set()

    def on_draw(self):
        """
        Called whenever the window needs to be drawn.
        This is where all the drawing commands go.
        """
        self.clear()
        self.planets_list.draw()
        self.center_list.draw()
        # self.planets[0].draw_bullets()

    def on_update(self, elapsed_time):
        """
        All the game logic goes here. This method is called every frame.
        'delta_time' is the time in seconds since the last update.
        """
        for i in range(len(self.planets)):
            for j in range(len(self.planets)):
                # considering self.planets[i] pulling on self.planets[j]
                if i == j:
                    continue
                # Computes planet 1 pulling on planet 2
                # def compute_gravity(pos1, pos2, mass1, mass2, elapsed_time):
                p1 = self.planets[i]
                p2 = self.planets[j]
                x1, y1 = p1.position
                x2, y2 = p2.position
                f = compute_gravity(Vector(x1, y1), Vector(x2, y2), p1.mass, p2.mass, elapsed_time)
                # planet 2 velocity changes by the force on it
                p2.vel += f
        # now we need to compute the center planet pulling on each of the other planetsd
        for i in range(len(self.planets)):
            p1 = self.center_planet
            p2 = self.planets[i]
            x1, y1 = p1.position
            x2, y2 = p2.position
            f = compute_gravity(Vector(x1, y1), Vector(x2, y2), p1.mass, p2.mass, elapsed_time)
            p2.vel += f
        for p in self.planets:
            p.update(elapsed_time)
        # self.planets[0].update_bullets(self.keys_held, elapsed_time)
        
    def on_key_press(self, key, modifiers):
        self.keys_held.add(key)

    def on_key_release(self, key, modifiers):
        if key in self.keys_held:
            self.keys_held.remove(key)

def main():
    """ Main function to start the game """
    game = MyGameWindow(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.run()

if __name__ == "__main__":
    main()
