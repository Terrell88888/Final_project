# Final_project: Snake Game with Hand Tracking

This project is based on an innovative rendition of the classic Snake game that utilizes computer vision techniques to provide a touchless gaming experience. Built using **OpenCV** and **cvzone**, the project uses real-time gesture tracking to control the movement of Snake. The game introduces a dynamic feature that not only features two modes, Timed Mode and Endless Mode, but also sets up obstacles and food to change as you level up.

## Features

### Hand-Tracking Gameplay
- Use your hand and a webcam to control the snake’s head.
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

### Custom Food Images
- Easily add custom food images with transparent backgrounds for a personalized touch.

### High Score Tracking
- The game keeps track of your all-time highest score, so you can always try to beat your best!


## Installation

### Prerequisites
- Python 3.7 or higher  
- Required libraries:  
  - **OpenCV**  
  - **cvzone**  
  - **numpy**  

### Steps
1. **Clone the repository:**  
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. **Install the required libraries:**  
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your webcam:**  
   Make sure your computer has a webcam connected and ready to use.

4. **Customize food images (optional):**  
   Add your own food images to the project folder and update the file path in the code (`SnakeGame` class) to use them.

## Usage

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

| Level | Target Score | Food Bonus Length | Food Size | Obstacles         |
|-------|--------------|-------------------|-----------|-------------------|
| 1     | 10           | 50                | 70x70     | None              |
| 2     | 25           | 40                | 60x60     | 1 (50x50)         |
| 3     | 50           | 30                | 50x50     | 1 (70x70)         |
| 4     | 100          | 20                | 45x45     | 1 (100x100)       |

---

## Customization

### Food Image  
To customize the food image:  
1. Replace the food image file (update the path in the `SnakeGame` class).  
2. Make sure the new image is a `.png` with a transparent background for the best visual experience.  

### Levels  
To modify the levels, edit the `LevelManager` class to:  
- Add or remove obstacles.  
- Adjust target scores, food bonuses, or food sizes.  

## Dependencies

- **Python**: Core programming language used for the game.  
- **OpenCV**: Handles camera input and graphics rendering.  
- **cvzone**: Simplifies hand detection and overlaying graphics.  
- **numpy**: Supports mathematical computations.  

Install all dependencies with:  
```bash
pip install -r requirements.txt
```

---

## License

This project is licensed under the **MIT License**.

---

## Acknowledgments

- [OpenCV](https://opencv.org/) for providing excellent tools for computer vision.  
- [cvzone](https://github.com/cvzone) for simplifying hand detection and graphic overlays.  

Enjoy playing the Snake Game! 


