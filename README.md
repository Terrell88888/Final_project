# Final_project: Snake Game（Hand Tracking Version)

This project is based on an innovative rendition of the classic Snake game that utilizes computer vision techniques to provide a touchless gaming experience. Built using **OpenCV** and **cvzone**, the project uses real-time gesture tracking to control the movement of Snake. The game introduces a dynamic feature that not only features two modes, Timed Mode and Endless Mode, but also sets up obstacles and food to change as you level up.

## Features

### Hand-Tracking Gameplay
- Use your index finger and a webcam to control the snake’s head.
- Your hand movements guide the snake’s direction in real time.

### Dynamic Levels
- Multiple levels that get more challenging as you progress.
- Watch out for obstacles, longer snake lengths, and smaller food targets!

### Game Modes
- **Timed Mode**: Race against the clock to score as much as possible before time runs out.
- **Endless Mode**: Play at your own pace with no time limits.

### Interactive Graphics
- Smooth, real-time snake movement and food generation.
- Cool visual effects for scoring, level-ups, and the game-over screen.

### High Score Tracking
- The game keeps track of your all-time highest score, so you can always try to beat your best!


## Requirements

The project requires the following Python libraries:

- **cvzone**: Version 1.6.1
- **numpy**: Version 2.2.0
- **opencv-python**: Version 4.10.0.84

These dependencies are listed in the requirements.txt file.

### Running the Program

1. **Clone the repository:**  
   ```bash
   git clone https://github.com/Terrell88888/Final_project.git
   cd Final_project
   ```

2. **Install the required libraries:**  
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your webcam:**  
   Make sure your computer has a webcam connected and ready to use.

## How to Play

1. **Run the game:**  
   ```bash
   python snake_game.py
   ```

2. **Start Menu:**  
   - **Press `1`**: Start the game in Timed Mode.  
   - **Press `2`**: Start the game in Endless Mode.  
   - **Press `ESC`**: Exit the game.  

3. **Controls:**  
   - Move your hand to guide the snake.  
   - Collect food to increase your score.  
   - Avoid obstacles and make sure not to collide with yourself!  

4. **During Gameplay:**  
   - **Press `r`**: Restart the current game.  
   - **Press `b`**: Return to the start menu (available only after the game ends).  

## Game Details

### Levels  
Each level is defined by:  
- **Target Score**: The score required to move to the next level.  
- **Obstacles**: The number and size of obstacles increase as you progress.  
- **Food Size**: Food gets smaller with each new level, making it harder to collect. 

| Level | Target Score | Food Bonus Length | Food Size | Obstacles |
|-------|--------------|-------------------|-----------|-----------|
| 1     | 10           | 50                | 70x70     | None      |
| 2     | 25           | 40                | 60x60     | 1         |
| 3     | 50           | 30                | 50x50     | 2         |
| 4     | 100          | 20                | 45x45     | 3         |

--- 

Enjoy playing the Snake Game! 


