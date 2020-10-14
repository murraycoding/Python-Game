# Python-Game

## Game Overview
This game will be a side view space shooter game. The player may move forward or back and up and down within the play field. The player will use weapons and sheilds to attack other enemies and defend itself against attacks from other enemies. Each level will be a set length and the playable area will move along the level.

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
