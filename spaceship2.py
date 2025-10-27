import arcade, math, random
from util import Vector

# Define screen dimensions
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Bad Arcade View Ex"
GRAVITY = 25

# Computes planet 1 pulling on planet 2
def compute_gravity(pos1, pos2, mass1, mass2, elapsed_time):
    gravity_factor = 0.0003
    v = pos1 - pos2
    n = v.normalize()
    d = v.magnitude()
    force = n * (mass1 * mass2 * (d ** 0.5) * gravity_factor * elapsed_time)
    return force

def random_vector():
    angle = random.randint(0, 360)
    mag = random.randint(50, 100)
    x = mag * math.cos(angle*math.pi/180)
    y = mag * math.sin(angle*math.pi/180)
    return Vector(x, y)

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
        self.counter = 0
        self.angle = 0
        
    # def update(self, elapsed_time):
    #     x, y = self.position
    #     if x < 0 or x > SCREEN_WIDTH or y < 0 or y > SCREEN_HEIGHT:
    #         self.kill()
    #         return
    #     self.position = (self.vel.x+x, self.vel.y+y)

    def update_bullets_and_rotation(self, keys, elapsed_time):
        # self.counter += 1
        # if arcade.key.SPACE in keys and self.counter % 30 == 0:
        #     self.new_bullet()
        if arcade.key.LEFT in keys:
            self.angle -= 2
        if arcade.key.RIGHT in keys:
            self.angle += 2
        
        for b in self.bullet_list:
            # update the velocity by multiplying by 1.01
            mag = b.vel.magnitude()
            mag2 = mag * 1.01
            u = b.vel.normalize()
            b.vel = u * mag2
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
        spaceship = Spaceship(Vector(SCREEN_WIDTH // 2 + 150, SCREEN_HEIGHT // 2 + 10), 
                              random_vector(), 30)
        self.planets = [spaceship]
        for planet in range(5):
            self.planets.append(Planet(Vector(SCREEN_WIDTH // 2 + random.randint(-500, 500), 
                                              SCREEN_HEIGHT // 2 + random.randint(-400, 400)), 
                                              random_vector(), 40))
        self.planets_list = arcade.SpriteList()
        for p in self.planets:
            self.planets_list.append(p)
            
        self.center_planet = Planet(Vector(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), Vector(0, 0), 150)
        self.center_list = arcade.SpriteList()
        self.center_list.append(self.center_planet)

        self.keys_held = set()
        self.win = False

    def on_draw(self):
        """
        Called whenever the window needs to be drawn.
        This is where all the drawing commands go.
        """
        self.clear()
        self.planets_list.draw()
        self.center_list.draw()
        # change
        self.planets_list[0].draw_bullets()

        if self.win:
            self.clear()
            arcade.draw_text("You win!", SCREEN_WIDTH//2, SCREEN_HEIGHT//2, arcade.color.GREEN)

    def on_update(self, elapsed_time):
        """
        All the game logic goes here. This method is called every frame.
        'delta_time' is the time in seconds since the last update.
        """
        # change
        for i in range(len(self.planets_list)):
            for j in range(len(self.planets_list)):
                # considering self.planets[i] pulling on self.planets[j]
                if i == j:
                    continue
                # Computes planet 1 pulling on planet 2
                # def compute_gravity(pos1, pos2, mass1, mass2, elapsed_time):
                # change
                p1 = self.planets_list[i]
                # change
                p2 = self.planets_list[j]
                x1, y1 = p1.position
                x2, y2 = p2.position
                f = compute_gravity(Vector(x1, y1), Vector(x2, y2), p1.mass, p2.mass, elapsed_time)
                # planet 2 velocity changes by the force on it
                p2.vel += f
        # now we need to compute the center planet pulling on each of the other planetsd
        # change
        for i in range(len(self.planets_list)):
            p1 = self.center_planet
            # change
            p2 = self.planets_list[i]
            x1, y1 = p1.position
            x2, y2 = p2.position
            f = compute_gravity(Vector(x1, y1), Vector(x2, y2), p1.mass, p2.mass, elapsed_time)
            p2.vel += f
        for p in self.planets_list:
            p.update(elapsed_time)
        # change
        self.planets_list[0].update_bullets_and_rotation(self.keys_held, elapsed_time)
        for planet in self.planets_list[1:]:
            if arcade.check_for_collision_with_list(planet, self.planets[0].bullet_list):
                print("collision detected")
                planet.kill()
                break

        if len(self.planets_list) == 1:
            self.win = True
        
    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP:
            self.planets_list[0].new_bullet()
        if key == arcade.key.ESCAPE:
            arcade.close_window()
        else:
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
