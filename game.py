import arcade
import os

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Move Sprite with Keyboard Example"
SCREEN_BUFFER = 50

CHARACTER_SCALING = 0.5

MOVEMENT_SPEED = 5

# Player class (controls movement and stuff?)
class Player(arcade.Sprite):

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.left < 0:
            self.left = 0
        elif self.right > SCREEN_WIDTH - 1:
            self.right = SCREEN_WIDTH - 1

        if self.bottom < SCREEN_BUFFER:
            self.bottom = SCREEN_BUFFER
        elif self.top > SCREEN_HEIGHT - SCREEN_BUFFER:
            self.top = SCREEN_HEIGHT - SCREEN_BUFFER
    
class MyGame(arcade.Window):

    def __init__(self, width, height, title):
        """
        Initializer
        """

        # Call the parent class initializer
        super().__init__(width, height, title)

        # lets the computer know where all of the files are located
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        # variable that holds the player sprite
        self.player_sprite = None

        # list of players
        self.player_list = None

    def setup(self):
        """
        Call this function to set up the game again
        """

        # Set up the sprite list
        self.player_list = arcade.SpriteList()

        # Setup the player
        image_source = ":resources:images/space_shooter/playerShip1_orange.png"
        self.player_sprite = Player(image_source, CHARACTER_SCALING)
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 128
        self.player_sprite.turn_right(90)
        self.player_list.append(self.player_sprite)

    def on_draw(self):
        """ renders the screen """

        arcade.start_render()

        # draws the player to the screen
        self.player_list.draw()
    
    def on_update(self, delta_time):
        """ Movement and Game Logic """

        self.player_list.update()

    def on_key_press(self, key, modifiers):

        if key == arcade.key.W:
            self.player_sprite.change_y = MOVEMENT_SPEED
        elif key == arcade.key.S:
            self.player_sprite.change_y = -MOVEMENT_SPEED
        elif key == arcade.key.D:
            self.player_sprite.change_x = MOVEMENT_SPEED
        elif key == arcade.key.A:
            self.player_sprite.change_x = -MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        if key == arcade.key.W or key == arcade.key.S:
            self.player_sprite.change_y = 0
        elif key == arcade.key.A or key == arcade.key.D:
            self.player_sprite.change_x = 0


def main():
    """ main method """
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()