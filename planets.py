import math
import arcade
from util import *

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Arcade View Example"
GRAVITY = 25

class Planet:
    def __init__(self, x, y, mass):
        self.pos = (x, y)
        self.mass = mass
        self.vel = (0, 0)

    def draw(self):
        x, y = self.pos
        arcade.draw_circle_filled(center_x=x, center_y=y, radius=20, color=arcade.color.BLUE)

    def move(self, elapsed):
        self.pos = vec_add(self.pos, vec_mult(elapsed, self.vel))

# --- Main Menu View ---
class MainMenuView(arcade.View):
    def on_show_view(self):
        arcade.set_background_color(arcade.color.AZURE)

    def on_draw(self):
        self.clear()
        arcade.draw_text("Main Menu", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50,
                         arcade.color.BLACK, font_size=30, anchor_x="center")
        arcade.draw_text("Click to Start", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 50,
                         arcade.color.GRAY, font_size=20, anchor_x="center")

    def on_mouse_press(self, x, y, button, modifiers):
        game_view = GameView()
        self.window.show_view(game_view)

# --- Game View ---
class GameView(arcade.View):

    def __init__(self):
        super().__init__()
        planet1 = Planet(SCREEN_WIDTH // 2 + 150, SCREEN_HEIGHT // 2 + 10, 5)
        planet1.vel = (0, 50)
        planet2 = Planet(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 40, 5)
        planet2.vel = (0, -50)
        planet3 = Planet(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 500)
        self.planets = [planet1, planet2, planet3]

    
    def on_show_view(self):
        arcade.set_background_color(arcade.color.WHITE)

    def on_update(self, elapsed_time):
        for i in range(len(self.planets)):
            for j in range(len(self.planets)):
                if i != j:
                    p1 = self.planets[i]
                    p2 = self.planets[j]
                    dv = vec_sub(p2.pos, p1.pos)
                    d = vec_mag(dv)
                    force = p1.mass * p2.mass * GRAVITY / (d**2)
                    df1 = vec_mult(force/p1.mass, vec_norm(dv))
                    df2 = vec_mult(force/p2.mass, vec_norm(dv))
                    if d > 25:
                        p1.vel = vec_add(p1.vel, df1)
                        p2.vel = vec_sub(p2.vel, df2)

        for p in self.planets:
            p.move(elapsed_time)
        

    def on_draw(self):
        self.clear()
        # arcade.draw_text("Game Screen", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
        #                  arcade.color.WHITE, font_size=30, anchor_x="center")
        for p in self.planets:
            p.draw()

    def on_key_press(self, symbol, modifiers):
        # Press ESC to go back to menu
        if symbol == arcade.key.ESCAPE:
            menu_view = MainMenuView()
            self.window.show_view(menu_view)

# --- Main Function ---
def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    menu_view = MainMenuView()
    game_view = GameView()
    window.show_view(menu_view)
    arcade.run()

if __name__ == "__main__":
    main()
