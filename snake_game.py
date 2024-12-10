import cv2
import math
import random
import numpy as np
from cvzone.HandTrackingModule import HandDetector
import cvzone
import time


class SnakeGame:
    def __init__(self, food_image_path):
        """Initialize the Snake game"""
        self.snake_body = []  # Coordinates of all points in the snake's body
        self.segment_lengths = []  # Distance between each pair of adjacent points
        self.total_length = 0  # Current total length of the snake
        self.max_length = 50  # Maximum allowable length of the snake
        self.last_head_position = 0, 0  # Last position of the snake's head

        # Load and resize the food image
        self.food_image = cv2.imread(food_image_path, cv2.IMREAD_UNCHANGED)
        if self.food_image.shape[2] == 3:
            self.food_image = cv2.cvtColor(self.food_image, cv2.COLOR_BGR2BGRA)

        # Initial food size
        self.food_image = self.resize_image(
            self.food_image, (50, 50))
        self.food_height, self.food_width, _ = self.food_image.shape
        self.food_position = 0, 0
        self.generate_food_position()

        # Game state
        self.score = 0  # Accumulated total score
        self.high_score = 0  # Highest score
        self.game_over = False

    def generate_food_position(self):
        """Randomly generate the food position"""
        self.food_position = random.randint(
            100, 1000), random.randint(
            100, 600)

    def reset_game(self, reset_score=True):
        """Reset the game state"""
        self.snake_body = []
        self.segment_lengths = []
        self.total_length = 0
        self.max_length = 50
        self.last_head_position = 0, 0
        if reset_score:
            self.score = 0  # Reset the score
        self.game_over = False
        self.generate_food_position()

    def update(self, frame, head_position, level_config, current_level):
        """
        Update the game state
        Attributes:
            frame: Current frame image
            head_position: Current position of the snake's head
            level_config: Current level configuration
            current_level: Current level number
        """
        if self.game_over:
            self.display_game_over(frame)
        else:
            self.move_snake(head_position)
            self.check_collisions(level_config)
            self.draw_snake(frame)
            self.display_food(frame)
            self.display_score(frame, current_level)
            self.draw_obstacles(frame, level_config.get("obstacles", []))
        return frame

    def move_snake(self, head_position):
        """
        Control the movement of the snake
        Attributes:
            head_position: Current position of the snake's head
        """
        px, py = self.last_head_position
        cx, cy = head_position
        self.snake_body.append([cx, cy])
        distance = math.hypot(cx - px, cy - py)
        self.segment_lengths.append(distance)
        self.total_length += distance
        self.last_head_position = cx, cy

        # Limit the length of the snake, remove extra points
        if self.total_length > self.max_length:
            for i, segment in enumerate(self.segment_lengths):
                self.total_length -= segment
                self.segment_lengths.pop(i)
                self.snake_body.pop(i)
                if self.total_length <= self.max_length:
                    break

    def check_collisions(self, level_config):
        """
        Check if the snake collides with food, obstacles, or itself
        Attributes:
            level_config: Current level configuration
        """
        # Check if the snake eats the food
        food_x, food_y = self.food_position
        head_x, head_y = self.last_head_position
        if food_x - self.food_width // 2 < head_x < food_x + self.food_width // 2 and \
           food_y - self.food_height // 2 < head_y < food_y + self.food_height // 2:
            self.generate_food_position()
            self.max_length += level_config.get("food_length_bonus", 50)
            self.score += level_config.get("food_score", 1)

        # Check if the snake collides with itself
        if len(self.snake_body) > 2:
            body_points = np.array(
                self.snake_body[:-2], np.int32).reshape((-1, 1, 2))
            min_distance = cv2.pointPolygonTest(
                body_points, (head_x, head_y), True)
            if -1 <= min_distance <= 1:
                self.update_high_score()
                self.game_over = True

        # Check if the snake collides with obstacles
        for obstacle in level_config.get("obstacles", []):
            ox, oy, ow, oh = obstacle
            if ox < head_x < ox + ow and oy < head_y < oy + oh:
                self.update_high_score()
                self.game_over = True

    def update_high_score(self):
        """Update the highest score"""
        if self.score > self.high_score:
            self.high_score = self.score

    def draw_snake(self, frame):
        """Draw the snake's body"""
        if self.snake_body:
            for i, point in enumerate(self.snake_body):
                if i != 0:
                    cv2.line(frame, tuple(
                        self.snake_body[i - 1]), tuple(self.snake_body[i]), (0, 0, 255), 20)
            cv2.circle(frame, tuple(
                self.snake_body[-1]), 20, (255, 0, 0), cv2.FILLED)

    def display_food(self, frame):
        """Display the food"""
        food_x, food_y = self.food_position
        frame = cvzone.overlayPNG(
            frame,
            self.food_image,
            (food_x - self.food_width // 2, food_y - self.food_height // 2))

    def display_score(self, frame, current_level):
        """Display the score and level"""
        cvzone.putTextRect(
            frame, f'Score: {self.score}', [
                50, 80], scale=2, thickness=2, offset=5, colorT=(
                0, 255, 0), colorR=(
                50, 50, 50))
        cvzone.putTextRect(
            frame, f'High Score: {self.high_score}', [
                50, 130], scale=2, thickness=2, offset=5, colorT=(
                0, 255, 0), colorR=(
                50, 50, 50))
        cvzone.putTextRect(frame,
                           f'Level: {current_level + 1}',
                           [50,
                            180],
                           scale=2,
                           thickness=2,
                           offset=5, colorT=(0, 255, 0), colorR=(50, 50, 50))

    def display_game_over(self, frame):
        """Display the game over screen"""
        cvzone.putTextRect(
            frame, "Game Over", [
                400, 300], scale=5, thickness=5, offset=10, colorT=(
                0, 0, 255), colorR=(
                50, 50, 50))
        cvzone.putTextRect(
            frame, f'Your Score: {self.score}', [
                400, 400], scale=3, thickness=3, offset=10, colorT=(
                0, 0, 255), colorR=(
                50, 50, 50))
        cvzone.putTextRect(
            frame, f'High Score: {self.high_score}', [
                400, 470], scale=3, thickness=3, offset=10, colorT=(
                0, 0, 255), colorR=(
                50, 50, 50))
        cvzone.putTextRect(
            frame, "Press 'r' to Restart", [
                400, 540], scale=2, thickness=2, offset=5, colorT=(
                0, 255, 0), colorR=(
                50, 50, 50))
        cvzone.putTextRect(
            frame, "Press 'b' to Return to Menu", [
                400, 570], scale=2, thickness=2, offset=5, colorT=(
                0, 255, 0), colorR=(
                50, 50, 50))

    def draw_obstacles(self, frame, obstacles):
        """Draw obstacles"""
        for obstacle in obstacles:
            x, y, w, h = obstacle
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), -1)

    @staticmethod
    def resize_image(image, size):
        """Resize the image"""
        return cv2.resize(image, size)


class LevelManager:
    def __init__(self):
        """Initialize level management"""
        self.levels = [
            {
                "target_score": 10,
                "food_score": 1,
                "food_length_bonus": 50,
                "obstacles": [],  # No obstacles
                "food_size": (70, 70)
            },
            {
                "target_score": 25,
                "food_score": 1,
                "food_length_bonus": 40,
                "obstacles": [(300, 300, 50, 50)],  # An obstacle
                "food_size": (60, 60)
            },
            {
                "target_score": 50,
                "food_score": 1,
                "food_length_bonus": 30,
                # Two obstacles
                "obstacles": [(200, 200, 70, 70), (500, 500, 50, 50)],
                "food_size": (50, 50)
            },
            {
                "target_score": 100,
                "food_score": 1,
                "food_length_bonus": 20,
                # Three obstacles
                "obstacles": [(100, 100, 100, 100), (400, 400, 60, 60), (700, 300, 80, 80)],
                "food_size": (45, 45)
            }
        ]
        self.current_level = 0

    def get_current_level_config(self):
        """Get the current level configuration"""
        return self.levels[self.current_level]

    def is_level_completed(self, score):
        """Check if the level is completed"""
        return score >= self.levels[self.current_level]["target_score"]

    def next_level(self):
        """Switch to the next level"""
        if self.current_level < len(self.levels) - 1:
            self.current_level += 1
            return True
        return False

    def reset_levels(self):
        """Reset all levels"""
        self.current_level = 0


def display_start_menu(frame):
    """Display the start menu"""
    cvzone.putTextRect(
        frame, "Snake Game", [
            400, 200], scale=5, thickness=5, offset=20, colorT=(
            0, 0, 255), colorR=(
                50, 50, 50))
    cvzone.putTextRect(
        frame, "Press 1: Timed Mode", [
            400, 350], scale=3, thickness=3, offset=10, colorT=(
            0, 255, 0), colorR=(
                50, 50, 50))
    cvzone.putTextRect(
        frame, "Press 2: Endless Mode", [
            400, 450], scale=3, thickness=3, offset=10, colorT=(
            0, 255, 0), colorR=(
                50, 50, 50))
    cvzone.putTextRect(
        frame, "Press ESC: Quit", [
            400, 550], scale=3, thickness=3, offset=10, colorT=(
            0, 255, 0), colorR=(
                50, 50, 50))


def main():
    """Main function"""
    cap = cv2.VideoCapture(0)
    cap.set(3, 1280)
    cap.set(4, 720)
    detector = HandDetector(detectionCon=0.8, maxHands=1)

    game = SnakeGame("food.png")
    level_manager = LevelManager()

    game_mode = None
    start_time = None
    time_limit = 60  # Time limit for timed mode

    while True:
        success, frame = cap.read()
        frame = cv2.flip(frame, 1)

        if game_mode is None:
            # Display the main menu
            display_start_menu(frame)
        else:
            # Game logic
            hands, frame = detector.findHands(frame, flipType=False)
            if hands:
                landmarks = hands[0]['lmList']
                head_position = landmarks[8][0:2]
                level_config = level_manager.get_current_level_config()

                # Dynamically adjust food size
                food_size = level_config.get(
                    "food_size", (70, 70))  # Default size enlarged to (70, 70)
                game.food_image = game.resize_image(game.food_image, food_size)
                game.food_height, game.food_width, _ = game.food_image.shape

                frame = game.update(
                    frame,
                    head_position,
                    level_config,
                    level_manager.current_level)

            if game_mode == "timed":
                # Countdown for timed mode
                if not game.game_over:
                    elapsed_time = time.time() - start_time
                    remaining_time = max(0, time_limit - int(elapsed_time))
                else:
                    remaining_time = 0  # Remaining time fixed to 0 after the game is over

                # Flashing logic (Time less than 10 seconds)
                if remaining_time <= 10:
                    if int(elapsed_time * 2) % 2 == 0:
                        cvzone.putTextRect(
                            frame, f"Time Left: {remaining_time}s", [
                                50, 230], scale=2, thickness=2, offset=5, colorT=(
                                0, 0, 255), colorR=(
                                50, 50, 50))
                else:
                    # Normal time display
                    cvzone.putTextRect(
                        frame, f"Time Left: {remaining_time}s", [
                            50, 230], scale=2, thickness=2, offset=5, colorT=(
                            0, 255, 0), colorR=(
                            50, 50, 50))

                if remaining_time == 0:
                    game.update_high_score()
                    game.game_over = True

        # Key press events
        key = cv2.waitKey(1)
        # Time Mode
        if key == ord('1') and game_mode is None:
            game_mode = "timed"
            start_time = time.time()
        # Infinite Time Mode
        elif key == ord('2') and game_mode is None:
            game_mode = "endless"
        # Restart the Game
        elif key == ord('r') and game_mode is not None:
            game.reset_game(reset_score=True)
            level_manager.reset_levels()
            if game_mode == "timed":
                start_time = time.time()
        # Return to main menu
        elif key == ord('b') and game.game_over:
            game_mode = None
            game.reset_game(reset_score=True)
            level_manager.reset_levels()
        # ESC key to exit
        elif key == 27:
            break

        if game_mode is not None and not game.game_over and level_manager.is_level_completed(
                game.score):
            if level_manager.next_level():
                game.reset_game(reset_score=False)
            else:
                game.update_high_score()
                game.game_over = True

        cv2.imshow("Snake Game", frame)

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
