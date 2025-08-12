"""

"""

import random
import arcade
import math
from util import *

# --- Constants ---
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = "Spaceship Example"

# it IS a sprite. It's both a Sprite and a bullet
# classes: silverware, class of all knives, forks and spoons
# subclass: stainless steel silverware
# subclass: plastic silverware
# instance of subclass plastic. is it also an instance of silverware. yes!
# if something is instance of silverware, is it also an instance of plastic? maybe
# 

class Movable(arcade.Sprite):
    def __init__(self, img, init_pos, vel_x, vel_y):
        super().__init__(img, 0.2)
        self.position = init_pos
        self.vel_x = vel_x 
        self.vel_y = vel_y

    def update(self, delta_time):
        # update the sprite's position. self.vel_x, self.vel_y
        x, y = self.position
        if x < 0 or x > WINDOW_WIDTH or y < 0 or y > WINDOW_HEIGHT:
            self.kill()
            return
        self.position = (self.vel_x+x, self.vel_y+y)
class GameView(arcade.View):

    def __init__(self):
        """ Initializer """
        # Call the parent class initializer
        super().__init__()

        # Variables that will hold sprite lists
        self.spaceship_list = None
        self.bullet_list = None

        # Create a variable to hold the player sprite
        self.spaceship_sprite = None
        self.bullet_sprite = None

        # Hide the mouse cursor while it's over the window
        self.window.set_mouse_visible(False)
        self.background_color = arcade.color.BLACK
        self.keys_down = set()
        self.angle = 0
        self.count = 0
        self.lives = 0

    def setup(self):
        """ Set up the game and initialize the variables. """

        # Create the sprite lists

        # Set up the spaceship
        self.spaceship_sprite = arcade.Sprite("spaceship.png", scale=0.1)
        self.spaceship_sprite.position = WINDOW_WIDTH//2, WINDOW_HEIGHT//2
        self.spaceship_list = arcade.SpriteList()
        self.spaceship_list.append(self.spaceship_sprite)

        # Set up the bullet
        # self.bullet_sprite = Bullet((WINDOW_WIDTH//2, WINDOW_HEIGHT//2), 0, 1)  # arcade.Sprite("bullet.png", scale=0.2)
        self.bullet_list = arcade.SpriteList()

        # asteroid list
        self.asteroid_list = arcade.SpriteList()
        
    def new_bullet(self):
        angle_radians = (-self.spaceship_sprite.angle+90)*math.pi/180
        vel_x = 3 * math.cos(angle_radians)
        vel_y = 3 * math.sin(angle_radians)
        x, y = self.spaceship_sprite.position
        self.bullet_list.append(Movable("bullet.png", (x, y), vel_x, vel_y))

    def new_asteroid(self):
        left = (0, random.randint(0, WINDOW_HEIGHT))
        right = (WINDOW_WIDTH, random.randint(0, WINDOW_HEIGHT))
        top = (random.randint(0, WINDOW_WIDTH), WINDOW_HEIGHT)
        bottom = (random.randint(0, WINDOW_WIDTH), 0)
        # pos1, pos2 = random.choice([left, right, top, bottom])
        p = Vector(*random.choice([left, right, top, bottom]))
        x, y = self.spaceship_sprite.position
        ss = Vector(x, y)
        point = (ss - p).normalize()
        vel_x = point.x
        vel_y = point.y
        self.asteroid_list.append(Movable("asteroid.png", (p.x, p.y), vel_x, vel_y))
        
    def spaceship_update(self):
        if arcade.key.LEFT in self.keys_down:
            self.angle -= 2
        if arcade.key.RIGHT in self.keys_down:
            self.angle += 2
        self.spaceship_sprite.angle = self.angle

    def check_bullet_collisions(self):
        need_removal = []
        for asteroid in self.asteroid_list:
            collisions = arcade.check_for_collision_with_list(asteroid, self.bullet_list)
            for bullet in collisions:
                print(f"Bullet hit asteroid! asteroid at {asteroid.center_x}, {asteroid.center_y}, Bullet at {bullet.center_x}, {bullet.center_y}")
                need_removal.append(asteroid)
                need_removal.append(bullet)
        for remove in need_removal:
            remove.remove_from_sprite_lists()

    def check_spaceship_collisions(self):
        collisions = arcade.check_for_collision_with_list(self.spaceship_sprite, self.asteroid_list)
        for asteroid in collisions:
            asteroid.remove_from_sprite_lists()
            self.lives -= 1

    def on_draw(self):
        """ Draw everything """
        # Clear the screen to only show the background color
        self.clear()
        arcade.draw_text(f"Lives: {self.lives}", 10, WINDOW_HEIGHT-30, arcade.color.WHITE, font_size=20)
        # Draw the sprites
        self.spaceship_list.draw()
        self.bullet_list.draw()
        self.asteroid_list.draw()
        if self.lives == 0:
            arcade.draw_text("GAME OVER", WINDOW_WIDTH//2, WINDOW_HEIGHT//2, arcade.color.RED, font_size=50, anchor_x="center", anchor_y="center")

    def on_update(self, delta_time):
        """ Movement and game logic """
        if self.lives != 0:
            self.count += 1
            if self.count % 120 == 0:
                # print("check")
                self.new_asteroid()
            self.spaceship_update()
            self.bullet_list.update()
            self.asteroid_list.update()
            self.check_bullet_collisions()
            self.check_spaceship_collisions()


    def on_key_press(self, key, modifier):
        if key == arcade.key.ESCAPE:
            arcade.exit()
        elif key == arcade.key.SPACE:
            self.new_bullet()
        else:
            self.keys_down.add(key)

    def on_key_release(self, key, modifier):
        if key in self.keys_down:
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