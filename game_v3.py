from math import sin, cos, radians
from random import randint
import arcade
import os
import random
from arcade.color import SCARLET
import time

from arcade.gui import UIManager
from arcade.sprite_list import check_for_collision, check_for_collision_with_list

# Verison 3.0
# This version of the game will have:
# -> A view for the start of the game (done)
# -> A Button to start the wave (or just a time delay) (time delay done)
# -> Logic to end the wave and start a new wave (done)
# -> View to show the score and health 
# -> Log to end the game at zero health (done)
# -> View for game over (done)

# CONSTANTS
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Move Sprite with Keyboard Example"
SCREEN_BUFFER = 50
SCREEN_UPPERBOUND = SCREEN_HEIGHT - SCREEN_BUFFER
SCREEN_LOWERBOUND = SCREEN_BUFFER

CHARACTER_SCALING = 0.5
LASER_SCALING = 0.4
ENEMY_SCALING = 0.5

PLAYER_SPEED = 5
ENEMY_SPEED = 2
LASER_SPEED = 8
LASER_DAMAGE = 3

ENEMY_HEALTH = 20
ENEMY_VALUE = 5

POWER_UP_SCALE = 0.5

# CLASS: Player

class Player(arcade.Sprite):

    # initialize player
    def __init__(self, filename, scale, health, speed, weapon, shield=None, weapon_time=0):
        super().__init__(filename, scale)
        self.health = health
        self.speed = speed
        self.weapon = weapon
        self.sheild = shield
        self.weapon_time = weapon_time

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

    def __init__(self, filename, scale, display_time):
        super().__init__(filename, scale)
        self.display_time = display_time
        self.time_existed = 0
    
    def spawn(self, x_pos, y_pos):
        self.center_x = x_pos
        self.center_y = y_pos

    def drop(self, x_pos, y_pos):
        self.center_x = x_pos
        self.center_y = y_pos

    def on_update(self, delta_time):
        self.time_existed += delta_time
        if self.time_existed > self.display_time:
            self.remove_from_sprite_lists()
    
# Health class
class Health(Power_Up):

    def __init__(self):
        super().__init__(filename=':resources:images/items/keyGreen.png',scale=POWER_UP_SCALE, display_time = 5)
        self.power = 10
    
    def spawn(self):
        self.center_x = random.randint(300, SCREEN_WIDTH-50)
        self.center_y = random.randint(SCREEN_BUFFER+50, SCREEN_HEIGHT-SCREEN_BUFFER-50)

class double_laser_powerup(Power_Up):

    def __init__(self):
        super().__init__(filename=':resources:images/items/coinSilver.png',scale=POWER_UP_SCALE,display_time = 5)

class spread_laser_powerup(Power_Up):

    def __init__(self):
        super().__init__(filename=':resources:images/items/coinGold.png',scale=POWER_UP_SCALE,display_time = 5)

# Starting Weapon
class Player_Laser_Basic(Laser):

    def __init__(self, angle=0):
        super().__init__(filename=':resources:images/space_shooter/laserBlue01.png', scale=LASER_SCALING, damage=LASER_DAMAGE*3, speed=LASER_SPEED)
        self.angle = angle
        self.turn_left(self.angle)

    def update(self):
        self.center_x += self.speed*cos(radians(self.angle))
        self.center_y += self.speed*sin(radians(self.angle))
        

# Basic Enemy Laser
class Enemy_Laser_Basic(Laser):

    def __init__(self, damage):
        super().__init__(filename=':resources:images/space_shooter/laserBlue01.png', scale=LASER_SCALING, damage = LASER_DAMAGE, speed=LASER_SPEED)
        self.turn_right(180)
        self.damage = damage

    def update(self):
        self.center_x -= self.speed

# Player double laser
class Player_Double_Laser():

    def __init__(self, effect_time=10):
        self.effect_time = effect_time

    def fire(self, x_pos, y_pos):
        laser_1 = Player_Laser_Basic()
        laser_1.fire(x_pos, y_pos - 20)
        laser_2 = Player_Laser_Basic()
        laser_2.fire(x_pos, y_pos + 20)
        return [laser_1,laser_2]

# Player spread laser
class Player_Spread_Laser():

    def __init__(self, effect_time=10):
        self.effect_time = effect_time

    def fire(self, x_pos, y_pos):
        laser_1 = Player_Laser_Basic(8)
        laser_1.fire(x_pos, y_pos)
        laser_2 = Player_Laser_Basic(4)
        laser_2.fire(x_pos, y_pos)
        laser_3 = Player_Laser_Basic(0)
        laser_3.fire(x_pos, y_pos)
        laser_4 = Player_Laser_Basic(-4)
        laser_4.fire(x_pos, y_pos)
        laser_5 = Player_Laser_Basic(-8)
        laser_5.fire(x_pos, y_pos)
        return [laser_1,laser_2,laser_3,laser_4,laser_5]

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
class Enemy_Basic(Enemy):

    def __init__(self):
        super().__init__(filename=':resources:images/enemies/mouse.png', scale=ENEMY_SCALING, speed = random.randint(60,120)*ENEMY_SPEED/100, health=ENEMY_HEALTH, value=ENEMY_VALUE)
    
    def update(self):
        self.center_x -= self.speed

# Bee Enemy
class Enemy_Wave(Enemy):
    
    def __init__(self):
        super().__init__(filename=':resources:images/enemies/fishGreen.png',scale=ENEMY_SCALING,speed=1.5*ENEMY_SPEED, health=ENEMY_HEALTH*1.5, value=10)
        self.time_on_screen = 0
        self.wave_speed = random.randint(5*ENEMY_SPEED,15*ENEMY_SPEED)/10
        self.wave_height = random.randint(5*ENEMY_SPEED,15*ENEMY_SPEED)/10

    def on_update(self, delta_time):
        self.time_on_screen += delta_time
        self.center_x -= self.speed
        self.center_y += self.wave_height*sin(self.wave_speed*self.time_on_screen)


class Enemy_ZigZag(Enemy):

    def __init__(self):
        super().__init__(filename=':resources:images/enemies/bee.png',scale=ENEMY_SCALING,speed=4*ENEMY_SPEED, health=ENEMY_HEALTH*2, value=10)
        self.time_on_screen = 0
        self.turn_angle = random.randint(20,50)
        self.going_up = True
        self.turn_height = randint(50, SCREEN_HEIGHT-50)

    def update(self):
        # constant movement horizontally
        self.center_x -= ENEMY_SPEED*cos(radians(self.turn_angle))
        
        # handles movement up and down
        if self.going_up:
            self.center_y += ENEMY_SPEED*sin(radians(self.turn_angle))
        else: 
            self.center_y -= ENEMY_SPEED*sin(radians(self.turn_angle))

        # determines when the enemies turn
        # up to down
        if int(self.center_y) in range(SCREEN_UPPERBOUND - 10, SCREEN_UPPERBOUND + 10) or (self.going_up and int(self.center_y) in range(self.turn_height - 10, self.turn_height + 10)):
            self.going_up = False
        elif int(self.center_y) in range(SCREEN_LOWERBOUND - 10, SCREEN_LOWERBOUND + 10) or (not(self.going_up) and int(self.center_y) in range(self.turn_height - 10, self.turn_height + 10)):
            self.going_up = True


# start screen view
class Start_Screen_View(arcade.View):

    # on show method
    def on_show(self):
        """ This is run once when we switch to this view """
        arcade.set_background_color(arcade.csscolor.BLACK)

        # Resets the viewport if needed
        arcade.set_viewport(0, SCREEN_WIDTH-1, 0, SCREEN_HEIGHT-1)

    # on draw method
    def on_draw(self):
        """ This view is runs normally when this view is active """
        arcade.start_render()
        # Draw some text below
        arcade.draw_text("Click to advance", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2-75, arcade.color.WHITE, font_size=20, anchor_x="center")

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        """ if the user presses the mouse button, start the game """
        game_view = MyGame()
        game_view.setup()
        self.window.show_view(game_view)

class Game_Over_View(arcade.View):
    """ view to show when the game is over """

    def __init__(self):
        """ this is run once when we switch to this view """
        super().__init__()

        # resets the viewport
        arcade.set_viewport(0, SCREEN_WIDTH - 1, 0, SCREEN_HEIGHT - 1)

    def on_draw(self):
        """ draw this view """
        arcade.start_render()
        arcade.draw_text("Game Over Click to advance", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2-75, arcade.color.WHITE, font_size=20, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """ if the user presses the mouse button, restart the game """
        game_view = MyGame()
        game_view.setup()
        self.window.show_view(game_view)


# Main Game Class
class MyGame(arcade.View):

    def __init__(self):
        """ Initialize Game """
        super().__init__()
        self.window.set_mouse_visible(False)

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
        self.double_laser_upgrade_list = None
        self.spread_laser_upgrade_list = None

        # score variable
        self.score = 0

        # wave information
        self.wave_number = 0
        self.num_basic_enemies = 0
        self.num_wave_enemies = 0
        self.num_zigzag_enemies = 0

    # sets up a new game
    def setup(self):
        """ Call this function to set up a new game """

        # Resets player
        image_source = ":resources:images/space_shooter/playerShip1_orange.png"
        self.player_sprite = Player(image_source, CHARACTER_SCALING, 100, PLAYER_SPEED, Player_Laser_Basic())
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 128
        self.player_sprite.turn_right(90)

        # Sets up the sprite lists
        self.player_laser_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.enemy_laser_list = arcade.SpriteList()
        self.health_list = arcade.SpriteList()
        self.double_laser_upgrade_list = arcade.SpriteList()
        self.spread_laser_upgrade_list = arcade.SpriteList()

        # resets the score to 0
        self.score = 0

        self.wave_creation()

    # Custom Game Methods

    def wave_creation(self):
        """ method to determine how many of each enemy will be in the wave"""

        # adds one to the wave number
        self.wave_number += 1
        wave_modifier = (1+self.wave_number/10)**2

        # updates the enemy health/power/speed/etc.
        ENEMY_SPEED = 2 * wave_modifier
        ENEMY_HEALTH = 20 * wave_modifier

        # sleeps for 5 seconds to give the player an indication of the next wave
        print('program is sleeping')
        time.sleep(1)

        # determines the number of enemies in the wave
        self.num_basic_enemies = self.wave_number*10
        self.num_wave_enemies = self.wave_number*5
        self.num_zigzag_enemies = self.wave_number*3

        

    # checks for next wave
    def check_next_wave(self):
        """ checks to see if the game is ready for the next wave """
        if len(self.enemy_list) == 0 and self.score > 0 and self.num_basic_enemies == 0 and self.num_wave_enemies == 0 and self.num_zigzag_enemies ==0:
            self.wave_creation()


    # checks for player collisions with other things
    def process_player_actions(self, delta_time):
        """ checks to see if the player has collided with stuff and handles logic """

        weapon_upgrade = None

        # checks to see if the player has hit any of the health upgrades or weapon upgrades
        double_laser_hit_list = check_for_collision_with_list(self.player_sprite, self.double_laser_upgrade_list)
        spread_laser_hit_list = check_for_collision_with_list(self.player_sprite, self.spread_laser_upgrade_list)
        health_list_hit_list = check_for_collision_with_list(self.player_sprite, self.health_list)

        if len(double_laser_hit_list) > 0:
            weapon_upgrade = Player_Double_Laser()
            for laser in double_laser_hit_list:
                laser.remove_from_sprite_lists()
        
        elif len(spread_laser_hit_list) > 0:
            weapon_upgrade = Player_Spread_Laser()
            for laser in spread_laser_hit_list:
                laser.remove_from_sprite_lists()
        
        elif len(health_list_hit_list) > 0:
            for health in health_list_hit_list:
                self.player_sprite.health += health.power
                health.remove_from_sprite_lists()

        if isinstance(weapon_upgrade, Player_Double_Laser) or isinstance(weapon_upgrade, Player_Spread_Laser):
            self.player_sprite.weapon = weapon_upgrade
            self.player_sprite.weapon_time = weapon_upgrade.effect_time

        # checks for player collision with any enemies
        for enemy in self.enemy_list:
            if check_for_collision(enemy, self.player_sprite):
                self.player_sprite.health -= 5
                enemy.remove_from_sprite_lists()

        # calculates weapon upgrade effect time
        self.player_sprite.weapon_time -= delta_time

        # takes weapon away if time is over
        if self.player_sprite.weapon_time < 0:
            self.player_sprite.weapon = Player_Laser_Basic()

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
                
                # random number of weapon upgrade logic
                rand_num = random.randrange(1,101)

                self.score += enemy.value
                enemy.health -= laser.damage

                if enemy.health <= 0:
                    # logic to occur after an enemy is eliminated

                    # dropping weapon upgrades
                    if isinstance(enemy, Enemy_Wave):
                        # subtracts one from the count
                        if rand_num < 60:
                            # drops a double laser
                            double_laser = double_laser_powerup()
                            double_laser.spawn(enemy.center_x, enemy.center_y)
                            self.double_laser_upgrade_list.append(double_laser)
                    elif isinstance(enemy, Enemy_ZigZag):
                        # subtracts one from the count
                        if rand_num < 40:
                            # drops a spread laser
                            spread_laser = spread_laser_powerup()
                            spread_laser.spawn(enemy.center_x, enemy.center_y)
                            self.spread_laser_upgrade_list.append(spread_laser)

                    # removed from the game
                    enemy.remove_from_sprite_lists()
                
            # removes laser from list if it is off screens
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

    def enemy_logic(self, delta_time):
        """ logic to determine when enemies shoot """

        odds = 100
        basic_enemy_odds = random.randrange(int(odds*(1/60)/delta_time))
        wave_enemy_odds = random.randrange(int(2*odds*(1/60)/delta_time))
        zigzag_enemy_odds = random.randrange(int(2*odds*(1/60)/delta_time))

        # basic enemies
        if self.num_basic_enemies > 0:
            if basic_enemy_odds == 0:
                enemy = Enemy_Basic()
                enemy.spawn()
                self.enemy_list.append(enemy)
                self.num_basic_enemies -= 1
        
        if self.num_wave_enemies > 0:
            if wave_enemy_odds == 0:
                enemy = Enemy_Wave()
                enemy.spawn()
                self.enemy_list.append(enemy)
                self.num_wave_enemies -= 1
        
        if self.num_zigzag_enemies > 0:
            if zigzag_enemy_odds == 0:
                enemy = Enemy_ZigZag()
                enemy.spawn()
                self.enemy_list.append(enemy)
                self.num_zigzag_enemies -= 1


        # logic to have the enemies fire
        for enemy in self.enemy_list:

            laser_odds = int(odds*(1/60)/delta_time)
            
            # generates laser to be fired
            if random.randrange(laser_odds) == 0:
                laser = Enemy_Laser_Basic(damage=LASER_DAMAGE*self.wave_number)
                laser.fire(enemy.center_x,enemy.center_y)
                self.enemy_laser_list.append(laser)

            # removes an enemy if they fall off screen to the left
            if enemy.center_x < 0:
                enemy.remove_from_sprite_lists()

    def power_up_logic(self, delta_time):
        """ logic to timeout all of the powerups on the board """

        # check to see if any power ups need to be removed due to time
        for double_laser in self.double_laser_upgrade_list:
            double_laser.on_update(delta_time)

        for spread_laser in self.spread_laser_upgrade_list:
            spread_laser.on_update(delta_time)

    def health_logic(self, delta_time):
        """ logic to deistribute health on the board """

        odds = 300
        adj_odds = int(odds*(1/60)/delta_time)

        # generates a new health and adds it to sprite list
        if random.randrange(adj_odds) == 0:
            health = Health()
            health.spawn()
            self.health_list.append(health)

        self.health_list.on_update(delta_time)

    # game over checker method
    def check_game_over(self):
        if self.player_sprite.health <= 0:
            game_over_view = Game_Over_View()
            self.window.show_view(game_over_view)

    # UPDATE METHOD
    def on_update(self, delta_time):
        """ Movement and Game Logic """

        # updates all sprites
        self.player_sprite.update()
        self.enemy_list.update()
        self.enemy_list.on_update(delta_time)
        self.process_player_lasers()
        self.process_enemy_lasers()
        self.health_logic(delta_time)
        self.process_player_actions(delta_time)
        self.power_up_logic(delta_time)
        
        # logic to have enemies fire
        self.enemy_logic(delta_time)

        # logic to check to see if the player has died
        self.check_game_over()

        # checks for the next wave
        self.check_next_wave()
    
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
        self.double_laser_upgrade_list.draw()
        self.spread_laser_upgrade_list.draw()

        # draws the score to the screen
        score_output = f'Score: {self.score}'
        arcade.draw_text(score_output, 20, SCREEN_HEIGHT-40, arcade.color.WHITE)

        # draws the health to the screen
        health_output = f'Health: {self.player_sprite.health}'
        arcade.draw_text(health_output, 100, SCREEN_HEIGHT-40, arcade.color.WHITE)

        #wave information to screenwwwww
        basic_enemy_output = f'Mice: {self.num_basic_enemies}'
        wave_enemy_output = f'Fish: {self.num_wave_enemies}'
        zigzag_enemy_output = f'Bees: {self.num_zigzag_enemies}'
        arcade.draw_text(basic_enemy_output, SCREEN_WIDTH - 250, SCREEN_HEIGHT-40, arcade.color.WHITE)
        arcade.draw_text(wave_enemy_output, SCREEN_WIDTH - 175, SCREEN_HEIGHT-40, arcade.color.WHITE)
        arcade.draw_text(zigzag_enemy_output, SCREEN_WIDTH - 100, SCREEN_HEIGHT-40, arcade.color.WHITE)

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
            if isinstance(self.player_sprite.weapon, Player_Double_Laser):
                lasers = Player_Double_Laser().fire(self.player_sprite.center_x, self.player_sprite.center_y)
                self.player_laser_list.append(lasers[0])
                self.player_laser_list.append(lasers[1])
            elif isinstance(self.player_sprite.weapon, Player_Spread_Laser):
                lasers = Player_Spread_Laser().fire(self.player_sprite.center_x, self.player_sprite.center_y)
                for laser in lasers:
                    self.player_laser_list.append(laser)
            else:
                laser = Player_Laser_Basic()
                laser.fire(self.player_sprite.center_x, self.player_sprite.center_y)
                self.player_laser_list.append(laser)

    def on_key_release(self, key, modifiers):

        # stop moving player
        if key == arcade.key.W or key == arcade.key.S:
            self.player_sprite.change_y = 0
        elif key == arcade.key.A or key == arcade.key.D:
            self.player_sprite.change_x = 0

def main():
    """ main method """
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    start_view = Start_Screen_View()
    window.show_view(start_view)
    arcade.run()

if __name__ == "__main__":
    main()
        
