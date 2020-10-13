import arcade
import os
import random
from arcade.color import SCARLET

from arcade.gui import UIManager

# CONSTANTS
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Move Sprite with Keyboard Example"
SCREEN_BUFFER = 50

CHARACTER_SCALING = 0.5
LASER_SCALING = 0.4
ENEMY_SCALING = 0.5

PLAYER_SPEED = 5
ENEMY_SPEED = 2
LASER_SPEED = 8
LASER_DAMAGE = 10

ENEMY_HEALTH = 10
ENEMY_VALUE = 5

POWER_UP_SCALE = 0.5

# CLASS: Player

class Player(arcade.Sprite):

    # initialize player
    def __init__(self, filename, scale, health, speed, weapon, shield=None):
        super().__init__(filename, scale)
        self.health = health
        self.speed = speed
        self.weapon = weapon
        self.sheild = shield

    # handles movement of player
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

# Generic Weapon Class
class Laser(arcade.Sprite):

    def __init__(self, filename, scale, damage, speed):
        super().__init__(filename, scale)
        self.damage = damage
        self.speed = speed
    
    def fire(self, x_pos, y_pos):
        self.center_x = x_pos
        self.center_y = y_pos

# base class for all pick up things (shields, weapon bonus, health, etc.)
class Power_Up(arcade.Sprite):

    def __init__(self, filename, scale, display_time, effect_time):
        super().__init__(filename, scale)
        self.display_time = display_time
        self.effect_time = effect_time
        self.time_existed = 0
    
    def spawn(self):
        self.center_x = random.randint(300, SCREEN_WIDTH-50)
        self.center_y = random.randint(SCREEN_BUFFER+50, SCREEN_HEIGHT-SCREEN_BUFFER-50)

    def drop(self, x_pos, y_pos):
        self.center_x = x_pos
        self.center_y = y_pos

    def update(self, delta_time):
        self.time_existed += delta_time
        if self.time_existed > self.display_time:
            self.remove_from_sprite_lists()
    
# Health class
class Health(Power_Up):

    def __init__(self):
        super().__init__(filename=':resources:images/items/keyGreen.png',scale=POWER_UP_SCALE, display_time = 5, effect_time = None)
        self.power = 10

# Starting Weapon
class Player_Laser_Basic(Laser):

    def __init__(self):
        super().__init__(filename=':resources:images/space_shooter/laserBlue01.png', scale=LASER_SCALING, damage=LASER_DAMAGE, speed=LASER_SPEED)

    def update(self):
        self.center_x += self.speed

# Basic Enemy Laser
class Enemy_Laser_Basic(Laser):

    def __init__(self):
        super().__init__(filename=':resources:images/space_shooter/laserBlue01.png', scale=LASER_SCALING, damage=LASER_DAMAGE, speed=LASER_SPEED)

    def update(self):
        self.center_x -= self.speed

# Player double laser
class Player_Double_Laser():

    def fire(self, x_pos, y_pos):
        laser_1 = Player_Laser_Basic()
        laser_1.fire(x_pos, y_pos - 20)
        laser_2 = Player_Laser_Basic()
        laser_2.fire(x_pos, y_pos + 20)
        return [laser_1,laser_2]
        
# Enemy Class
class Enemy(arcade.Sprite):

    def __init__(self, filename, scale, speed, health, value):
        super().__init__(filename, scale)
        self.speed = speed
        self.health = health
        self.value = value
    
    def spawn(self):
        self.center_x = SCREEN_WIDTH - 20
        self.center_y = random.randint(SCREEN_BUFFER+50, SCREEN_HEIGHT-SCREEN_BUFFER-50)

# Basic Enemy
class Enemy_Green_Fish(Enemy):

    def __init__(self):
        super().__init__(filename=':resources:images/enemies/fishGreen.png', scale=ENEMY_SCALING, speed = random.randint(60,120)*ENEMY_SPEED/100, health=ENEMY_HEALTH, value=ENEMY_VALUE)
    
    def update(self):
        self.center_x -= self.speed

# Bee Enemy
class Enemy_Bee(Enemy):
    
    def __init__(self):
        super().__init__(filename=':resources:images/enemies/bee.png',scale=ENEMY_SCALING,speed=1.5*ENEMY_SPEED, health=20, value=10)

    def update(self):
        self.center_x -= self.speed

# Main Game Class
class MyGame(arcade.Window):

    def __init__(self, width, height, title):
        """ Initialize Game """
        super().__init__(width, height, title)

        # lets the computer know where all of the files are located
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        # Game Variables

        # Sprite Lists
        self.player_sprite = None
        self.player_laser_list = None
        self.enemy_list = None          # List of enemies
        self.enemy_laser_list = None    # enemy lasers
        self.health_list = None

        # score variable
        self.score = 0

    # sets up a new game
    def setup(self):
        """ Call this function to set up a new game """

        # Resets player
        image_source = ":resources:images/space_shooter/playerShip1_orange.png"
        self.player_sprite = Player(image_source, CHARACTER_SCALING, 100, PLAYER_SPEED, Player_Double_Laser())
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 128
        self.player_sprite.turn_right(90)

        # Sets up the sprite lists
        self.player_laser_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.enemy_laser_list = arcade.SpriteList()
        self.health_list = arcade.SpriteList()

        # resets the score to 0
        self.score = 0

    # Custom Game Methods

    # checks for collisions for all player lasers
    def process_player_lasers(self):
        """ checks for collision from player lasers to all enemies """

        # updates the player's laser list
        self.player_laser_list.update()

        # checks all lasers for collision
        for laser in self.player_laser_list:

            # list of all enemies who have been hit
            hit_list = arcade.check_for_collision_with_list(laser, self.enemy_list)

            # removes lasers that have been in a collision
            if len(hit_list) > 0:
                laser.remove_from_sprite_lists()
            
            # removes enemy from game and adds value to score
            for enemy in hit_list:
                self.score += enemy.value
                enemy.remove_from_sprite_lists()

            # removes laser from list if it is off screen
            if laser.center_x > SCREEN_WIDTH:
                laser.remove_from_sprite_lists()

    # checks for collision between enemy lasers and player
    def process_enemy_lasers(self):
        """ checks for collisions from all enemy lasers to player """

        # updates the position of all enemy lasers
        self.enemy_laser_list.update()

        # checks all enemy lasers
        for laser in self.enemy_laser_list:

            # checks for collision
            hit = arcade.check_for_collision(laser, self.player_sprite)

            if hit:
                laser.remove_from_sprite_lists()
                self.player_sprite.health -= laser.damage
                print('Enemy hit a player')

    def enemy_logic(self, delta_time):
        """ logic to determine when enemies shoot """

        # logic to have the enemies fire
        for enemy in self.enemy_list:

            odds = 200
            adj_odds = int(odds*(1/60)/delta_time)
            bee_odds = int(3*odds*(1/60)/delta_time)
            
            # generates laser to be fired
            if random.randrange(adj_odds) == 0:
                laser = Enemy_Laser_Basic()
                laser.fire(enemy.center_x,enemy.center_y)
                self.enemy_laser_list.append(laser)

            # removes an enemy if they fall off screen to the left
            if enemy.center_x < 0:
                enemy.remove_from_sprite_lists()
            
            if random.randrange(bee_odds) == 0:
                enemy = Enemy_Bee()
                enemy.spawn()
                self.enemy_list.append(enemy)

    def health_logic(self, delta_time):
        """ logic to deistribute health on the board """

        odds = 475
        adj_odds = int(odds*(1/60)/delta_time)

        # generates a new health and adds it to sprite list
        if random.randrange(adj_odds) == 0:
            health = Health()
            health.spawn()
            self.health_list.append(health)

        # checks for collsions and adds health to player
        for health in self.health_list:

            # collision check
            hit = arcade.check_for_collision(self.player_sprite, health)

            # if there is a hit, add health
            if hit:
                self.player_sprite.health += health.power
                health.remove_from_sprite_lists()
            
            #updates the time on all health objects
            health.update(delta_time)

    # UPDATE METHOD
    def on_update(self, delta_time):
        """ Movement and Game Logic """

        # updates all sprites
        self.player_sprite.update()
        self.enemy_list.update()
        self.process_player_lasers()
        self.process_enemy_lasers()
        self.health_logic(delta_time)
        

        # maintains 10 enemies on the screen at all times
        if len(self.enemy_list) < 10:
            enemy = Enemy_Green_Fish()
            enemy.spawn()
            self.enemy_list.append(enemy)
        
        
        # logic to have enemies fire
        self.enemy_logic(delta_time)
    
    # DRAW METHOD
    def on_draw(self):
        """ renders the screen """

        arcade.start_render()

        # draws the player and the lasers to the screen
        self.player_sprite.draw()
        self.player_laser_list.draw()
        self.enemy_list.draw()
        self.enemy_laser_list.draw()
        self.health_list.draw()

        # draws the score to the screen
        score_output = f'Score: {self.score}'
        arcade.draw_text(score_output, 20, SCREEN_HEIGHT-40, arcade.color.WHITE)

        # draws the health to the screen
        health_output = f'Health: {self.player_sprite.health}'
        arcade.draw_text(health_output, 100, SCREEN_HEIGHT-40, arcade.color.WHITE)

    def on_key_press(self, key, modifiers):
        
        # Start moving player
        if key == arcade.key.W:
            self.player_sprite.change_y = PLAYER_SPEED
        elif key == arcade.key.S:
            self.player_sprite.change_y = -PLAYER_SPEED
        elif key == arcade.key.D:
            self.player_sprite.change_x = PLAYER_SPEED
        elif key == arcade.key.A:
            self.player_sprite.change_x = -PLAYER_SPEED

        # creates a laser
        if key == arcade.key.ENTER:
            lasers = Player_Double_Laser().fire(self.player_sprite.center_x, self.player_sprite.center_y)
            self.player_laser_list.append(lasers[0])
            self.player_laser_list.append(lasers[1])
    
    def on_key_release(self, key, modifiers):

        # stop moving player
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
        