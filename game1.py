import arcade
import random

# Game constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Catch the Falling Apples!"
BASKET_WIDTH = 100
BASKET_HEIGHT = 20
APPLE_SIZE = 20
FALL_SPEED = 5
APPLE_RATE = 2  # The rate at which apples spawn (frames per apple)

class Basket(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.width = BASKET_WIDTH
        self.height = BASKET_HEIGHT
        self.center_x = SCREEN_WIDTH // 2
        self.center_y = 50
        self.color = arcade.color.BLUE

    def update(self):
        """Handle movement of the basket."""
        if self.left < 0:
            self.center_x = self.width // 2
        elif self.right > SCREEN_WIDTH:
            self.center_x = SCREEN_WIDTH - self.width // 2

class Apple(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.width = APPLE_SIZE
        self.height = APPLE_SIZE
        self.center_x = random.randint(0, SCREEN_WIDTH)
        self.center_y = SCREEN_HEIGHT
        self.color = arcade.color.RED
        self.change_y = -FALL_SPEED

    def update(self):
        """Move the apple down and check if it falls off the screen."""
        self.center_y += self.change_y

        # If the apple goes off the screen, reset it at the top
        if self.top < 0:
            self.center_x = random.randint(0, SCREEN_WIDTH)
            self.center_y = SCREEN_HEIGHT

class CatchApplesGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.basket = Basket()
        self.apples = arcade.SpriteList()
        self.score = 0
        self.game_over = False
        self.apple_spawn_timer = 0

    def setup(self):
        """Set up the game, this is called once when the game starts."""
        self.basket = Basket()
        self.apples = arcade.SpriteList()
        self.score = 0
        self.game_over = False
        self.apple_spawn_timer = 0

    def on_draw(self):
        """Render the screen."""
        arcade.start_render()
        self.basket.draw()
        self.apples.draw()

        # Draw the score
        score_text = f"Score: {self.score}"
        arcade.draw_text(score_text, 10, SCREEN_HEIGHT - 30, arcade.color.WHITE, 20)

        # Draw Game Over text if the game is over
        if self.game_over:
            arcade.draw_text("Game Over!", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, arcade.color.RED, 30)

    def on_update(self, delta_time):
        """Update game logic."""
        if self.game_over:
            return

        self.basket.update()

        # Spawn apples
        self.apple_spawn_timer += 1
        if self.apple_spawn_timer >= APPLE_RATE:
            self.apple_spawn_timer = 0
            apple = Apple()
            self.apples.append(apple)

        # Update apples
        self.apples.update()

        # Check for collisions with basket
        for apple in self.apples:
            if apple.collides_with_sprite(self.basket):
                self.score += 1
                apple.center_x = random.randint(0, SCREEN_WIDTH)
                apple.center_y = SCREEN_HEIGHT
            elif apple.bottom < 0:
                self.game_over = True

    def on_key_press(self, symbol, modifiers):
        """Handle key presses to move the basket."""
        if symbol == arcade.key.LEFT:
            self.basket.center_x -= 10
        elif symbol == arcade.key.RIGHT:
            self.basket.center_x += 10

if __name__ == "__main__":
    window = CatchApplesGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()
