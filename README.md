# Python-Game

## Game Overview
This game is a space shooter game. At the current moment in development, directions and a tutorial are not built-in to the game itself. Please read below for controls and an overview of the game.

### Object of the game
The object of the game is to defeat enemies and avoid taking damage to survive wave after wave of enemies. As the player, you can **move up, down, left and right** over the whole game screen by using the **mouse** or the **WASD** keys. To **attack** enemies you can fire your laser by pressing the **enter** key or clicking the **left mouse button**.

### Enemies
Each wave will have a set number of enemies. There are three types of enemies in the game:

- Mouse (5 points): This enemy moves in a straight line.
- Fish (10 points): This enemy moves in a wave pattern and may drop a silver coin.
- Bees (15 points): This enemy moves in a zig-zag pattern

All enemies have randomized movement within their type of movement. The mice move at randomized speeds, the fish all move with different amplitudes of the wave and move up and down through the wave at a different speed and the bees move at a random zig zag pattern. Each bee will turn around at a random place on the screen. All enemies also fire their lasers at random times. This randomness make each game different and exciting! The coins refered to in the enemy description are weapon upgrades (see that section for more information). Please note that those enemies have just a random chance of dropping the coins for the upgrade.

While each game is different, the constant in the game is the number of enemies per wave. Each wave has a set number of enemies. The number of enemies left in the wave can be found at the top left corner of the screen. Please not the number indicates the number of enemies left to be spawned on screen so it does not include the ones already on screen. Each wave the enemies become more difficult too. The enemy speed and health goes up each wave.

### Weapon upgrades
Weapon Upgrades come in the form of silver or gold coins dropped by certain enemies. Collecting a coin will grant you a temporary weapon upgrade! The silver coins result in a double laser where two lasers will fire with each click of the mouse (or enter button). The gold coins will grant you a spread laser! The spread laser fires 5 lasers at once in a burst pattern all shooting out in different directions. Each coin will only be available for pick up for short time and the weapon upgrades also only last for a short time so use them wisely!

### Extra health
Randomly on screen, green keys will appear. Each one of these keys will grant the player 10 extra health. Each key will only be available on screen for a short time.

### Game Over
Once the players health reaches 0, the game is over. The game over screen will show the player score and the leaderboard for the game. If the player has scored high enough to be counted in the leaderboard, their name will display in the leaderboard.

### Leaderboard
Within the game, there should be a csv file to contain the leaderboard. If you are running this code on your own loacal machine. Make sure to have the csv file in place so the game can record the high scores.

## What this game is missing
At this point in development, the game is perfectly playable in its final form (for now). In the future, I would like to add some "polish" to the game. For example, the leaderboard just displays as plain text on the screen instead of in a nicely formatted table. The background also is just a plain play background instead of a cool space theme. The enemies are also just stock images from the Python Arcade library. These are all things I plan to change when I do work on the game again.

My challenge to myself was to learn a game library and make a playable game during the month of October working mostly just during my extra time on weekdays. Next month I have a new project to work on but I do plan to go back to this to give the game more "polish". Below you can read about the humble benginnings of the game in the development updates.

## Game Development Updates

### October 5, 2020
The game window opens and the player ship renders to the screen. It can then move up, down, left and right. It also limits itself to the edges of the screen. I have also made the player stop before the top and bottom of the screens to leave space for a UI for game information.

### October 6, 2020
The player can now shoot lasers and the lasers are removed from the game once they are off screen. By the end of the day, enemies were generated with a random position on the right hand side of the screen with a random speed. The player is also able to shoot the enemies and they would disappear once shot. If any enemy was shot, then a new random enemy was generate on the left hand side of the screen.

### October 7, 2020
Before, enemies were only eliminated by being shot. Now, if an enemy moves past the player (off screen to the left) then it is considered "eliminated" and a new enemy appears on the right hand side of the screen. As of right now, only 10 randomly generated enemies are on screen at once. The enemies can also fire back at the player. If an enemy laser hits the player, it is removed from the screen and an action can occur (such as damage to the player). 

### October 8, 2020
The player now can pick up extra health, the health will generate randomly on screen and be erased after 5 seconds. A new enemy class was also introduced. I also created a generic power up class for later use in weapon upgrades.

### October 9, 2020
Weapons Upgrades planned and enemy types also planned. Next week, I plan to impliment these and create an end game sequence. Also started thinking about how to up the difficulty over time.

### October 13, 2020
Added double laser to the game. It is set as the default weapon just to test.
By the end of the day, I was able to get the double laser to be as a weapon upgrade. If the player kills the Bee enemy. There is a chance they will drop a silver coin. If the player moves over to the silver coin, the weapon will change to a double laser. The  silver coin will automatically disapear after a set time. Right now, the weapon stays on double. I am hoping to solve the weapon cooldown period tomorrow.

### October 14, 2020
Finished adding the double laser update. When a player picks up the silver coin, they will have a double laser but only for a set time. After that, the players weapon reverts to a single laser. Added spread laser to the game and the on press enter function now checks for the spread laser.

### October 15, 2020
Wave enemy is complete. The enemy will move in a wave pattern with a random speed and wave height. Eventually this type of enemy will take multiple hits to kill but for now it is still just a one hit kill. The enemy health update will come as a separate update to effect all enemies.

### October 16, 2020
ZigZag enemy was added to the game. This is the last planned enemy type. Now, the logic comes about what enemy will come and how often it will show up.

### October 19, 2020
Enemy update #1 complete all enemies drop the right weapons and all movement is complete for all enemies.

### October 20, 2020
Enemy update #2 is complete. All enemies now have health and drop weapon upgrades when they die. Early stages of wave updates are also in place for the wave mechanic to be introduced tomorrow.

### October 21, 2020
Final details of wave mechanics complete. The only thing left to do is add the logic to start a new wave once the old save is completed.

### October 22, 2020
Added logic for a game over at zero health and a game over screen. Working on the "next wave" mechanic yet.

### October 26, 2020
Added mouse controls for the game. Move the mouse to move the ship and press the left mouse key for firing the weapon.

### October 27, 2020
Added a leaderboard and score now displays after the player dies. The leaderboard functionality of posting to the leaderboard has not been finalized yet.

### October 28, 2020
Leaderboard logic is complete except for displaying the leaderboard when the game ends (or begins). Users will enter their name at the start of the game and the game will check their score against the current leaderboard. If it should be placed in the leaderboard, it will insert the name and score in the appropriate place in the leaderboard. This is all via reading an external csv file.
