import cv2
import math
import random
import numpy as np
from cvzone.HandTrackingModule import HandDetector
import cvzone


class SnakeGame:
    def __init__(self, food_image_path):
        """
        Initialize the Snake game
        :param food_image_path: Path to the food image
        """
        self.snake_body = []  # Coordinates of all points in the snake body
        self.segment_lengths = []  # Distance between adjacent points
        self.total_length = 0  # Current total length of the snake
        self.max_length = 50  # Maximum allowed length of the snake
        self.last_head_position = 0, 0  # Last position of the snake's head

        # Load and resize the food image
        self.food_image = cv2.imread(food_image_path, cv2.IMREAD_UNCHANGED)
        if self.food_image.shape[2] == 3:  # Add alpha channel if not present
            self.food_image = cv2.cvtColor(self.food_image, cv2.COLOR_BGR2BGRA)

        # Initial size of the food
        self.food_image = self.resize_image(
            self.food_image, (50, 50))  # Default width and height 50
        self.food_height, self.food_width, _ = self.food_image.shape
        self.food_position = 0, 0
        self.generate_food_position()

        # Game state
        self.score = 0  # Total score
        self.high_score = 0  # Highest score
        self.game_over = False

    def generate_food_position(self):
        """Generate a random position for the food"""
        self.food_position = random.randint(
            100, 1000), random.randint(
            100, 600)

    def reset_game(self, reset_score=True):
        """
        Reset the game state
        :param reset_score: Whether to reset the score, default is True
        """
        self.snake_body = []
        self.segment_lengths = []
        self.total_length = 0
        self.max_length = 50
        self.last_head_position = 0, 0
        if reset_score:
            self.score = 0  # Reset score
        self.game_over = False
        self.generate_food_position()

    def update(self, frame, head_position, level_config, current_level):
        """
        Update the game state
        :param frame: Current frame image
        :param head_position: Current position of the snake's head
        :param level_config: Current level configuration
        :param current_level: Current level number
        :return: Updated frame image
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
        :param head_position: Current position of the snake's head
        """
        px, py = self.last_head_position
        cx, cy = head_position
        self.snake_body.append([cx, cy])
        distance = math.hypot(cx - px, cy - py)
        self.segment_lengths.append(distance)
        self.total_length += distance
        self.last_head_position = cx, cy

        # Limit the length of the snake and remove extra points
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
        :param level_config: Current level configuration
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
                self.snake_body[-1]), 20, (0, 255, 0), cv2.FILLED)

    def display_food(self, frame):
        """Display the food"""
        food_x, food_y = self.food_position
        frame = cvzone.overlayPNG(
            frame,
            self.food_image,
            (food_x - self.food_width // 2, food_y - self.food_height // 2))

    def display_score(self, frame, current_level):
        """Display the score and current level"""
        cvzone.putTextRect(
            frame, f'Score: {self.score}', [
                50, 80], scale=3, thickness=3, offset=10)
        cvzone.putTextRect(frame, f'High Score: {self.high_score}', [
                           50, 150], scale=3, thickness=3, offset=10)
        cvzone.putTextRect(frame,
                           f'Level: {current_level + 1}',
                           [50,
                            220],
                           scale=3,
                           thickness=3,
                           offset=10)

    def display_game_over(self, frame):
        """Display the game over screen"""
        cvzone.putTextRect(
            frame, "Game Over", [
                300, 400], scale=7, thickness=5, offset=20)
        cvzone.putTextRect(
            frame, f'Your Score: {self.score}', [
                300, 550], scale=7, thickness=5, offset=20)
        cvzone.putTextRect(frame, f'High Score: {self.high_score}', [
                           300, 700], scale=7, thickness=5, offset=20)

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
        """
        Initialize the level manager
        """
        self.levels = [
            {
                "target_score": 10, "food_score": 1, "food_length_bonus": 50, "obstacles": [], "food_size": (
                    70, 70)}, {
                "target_score": 25, "food_score": 1, "food_length_bonus": 40, "obstacles": [
                    (300, 300, 50, 50)], "food_size": (
                        60, 60)}, {
                            "target_score": 50, "food_score": 1, "food_length_bonus": 30, "obstacles": [
                                (200, 200, 70, 70)], "food_size": (
                                    50, 50)}, {
                                        "target_score": 100, "food_score": 1, "food_length_bonus": 20, "obstacles": [
                                            (100, 100, 100, 100)], "food_size": (
                                                45, 45)}, ]
        self.current_level = 0

    def get_current_level_config(self):
        """Get the configuration of the current level"""
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


def main():
    """
    Main function
    """
    cap = cv2.VideoCapture(0)
    cap.set(3, 1280)
    cap.set(4, 720)
    detector = HandDetector(detectionCon=0.8, maxHands=1)

    game = SnakeGame("C:\\Users\\Terrell\\Downloads\\1.png")
    level_manager = LevelManager()

    while True:
        success, frame = cap.read()
        frame = cv2.flip(frame, 1)
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

        cv2.imshow("Snake Game", frame)
        key = cv2.waitKey(1)

        if key == ord('r'):
            game.reset_game(reset_score=True)
            level_manager.reset_levels()
        elif key == 27:  # ESC key to exit
            break

        if not game.game_over and level_manager.is_level_completed(game.score):
            if level_manager.next_level():
                game.reset_game(reset_score=False)
            else:
                game.update_high_score()
                game.game_over = True

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

import cv2
import math
import random
import numpy as np
from cvzone.HandTrackingModule import HandDetector
import cvzone


class SnakeGame:
    def __init__(self, food_image_path):
        """
        Initialize the Snake game
        :param food_image_path: Path to the food image
        """
        self.snake_body = []  # Coordinates of all body points of the snake
        self.segment_lengths = []  # Distance between each pair of adjacent points
        self.total_length = 0  # Total current length of the snake
        self.max_length = 50  # Maximum allowable length of the snake
        self.last_head_position = 0, 0  # Last position of the snake's head

        # Load and resize the food image
        self.food_image = cv2.imread(food_image_path, cv2.IMREAD_UNCHANGED)
        if self.food_image.shape[2] == 3:  # Add alpha channel if not present
            self.food_image = cv2.cvtColor(self.food_image, cv2.COLOR_BGR2BGRA)

        # Initial food size
        self.food_image = self.resize_image(
            self.food_image, (50, 50))  # Default width and height 50
        self.food_height, self.food_width, _ = self.food_image.shape
        self.food_position = 0, 0
        self.generate_food_position()

        # Game state
        self.score = 0  # Accumulated total score
        self.high_score = 0  # Highest score
        self.game_over = False

    def generate_food_position(self):
        """Randomly generate food position"""
        self.food_position = random.randint(
            100, 1000), random.randint(
            100, 600)

    def reset_game(self, reset_score=True):
        """
        Reset the game state
        :param reset_score: Whether to reset the score, default is True
        """
        self.snake_body = []
        self.segment_lengths = []
        self.total_length = 0
        self.max_length = 50
        self.last_head_position = 0, 0
        if reset_score:
            self.score = 0  # Reset score
        self.game_over = False
        self.generate_food_position()

    def update(self, frame, head_position, level_config, current_level):
        """
        Update the game state
        :param frame: Current frame image
        :param head_position: Current position of the snake's head
        :param level_config: Current level configuration
        :param current_level: Current level number
        :return: Updated frame image
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
        Control the snake's movement
        :param head_position: Current position of the snake's head
        """
        px, py = self.last_head_position
        cx, cy = head_position
        self.snake_body.append([cx, cy])
        distance = math.hypot(cx - px, cy - py)
        self.segment_lengths.append(distance)
        self.total_length += distance
        self.last_head_position = cx, cy

        # Limit the snake's length and remove extra points
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
        :param level_config: Current level configuration
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
                self.snake_body[-1]), 20, (0, 255, 0), cv2.FILLED)

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
                50, 80], scale=3, thickness=3, offset=10)
        cvzone.putTextRect(frame, f'High Score: {self.high_score}', [
                           50, 150], scale=3, thickness=3, offset=10)
        cvzone.putTextRect(frame,
                           f'Level: {current_level + 1}',
                           [50, 220],
                           scale=3,
                           thickness=3,
                           offset=10)

    def display_game_over(self, frame):
        """Display the game over screen"""
        cvzone.putTextRect(
            frame, "Game Over", [
                300, 400], scale=7, thickness=5, offset=20)
        cvzone.putTextRect(
            frame, f'Your Score: {self.score}', [
                300, 550], scale=7, thickness=5, offset=20)
        cvzone.putTextRect(frame, f'High Score: {self.high_score}', [
                           300, 700], scale=7, thickness=5, offset=20)

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
        """
        Initialize level management
        """
        self.levels = [
            {"target_score": 10, "food_score": 1, "food_length_bonus": 50, "obstacles": [], "food_size": (70, 70)},
            {"target_score": 25, "food_score": 1, "food_length_bonus": 40, "obstacles": [(300, 300, 50, 50)], "food_size": (60, 60)},
            {"target_score": 50, "food_score": 1, "food_length_bonus": 30, "obstacles": [(200, 200, 70, 70)], "food_size": (50, 50)},
            {"target_score": 100, "food_score": 1, "food_length_bonus": 20, "obstacles": [(100, 100, 100, 100)], "food_size": (45, 45)},
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


def main():
    """
    Main function
    """
    cap = cv2.VideoCapture(0)
    cap.set(3, 1280)
    cap.set(4, 720)
    detector = HandDetector(detectionCon=0.8, maxHands=1)

    game = SnakeGame("food.png")
    level_manager = LevelManager()

    while True:
        success, frame = cap.read()
        frame = cv2.flip(frame, 1)
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

        cv2.imshow("Snake Game", frame)
        key = cv2.waitKey(1)

        if key == ord('r'):
            game.reset_game(reset_score=True)
            level_manager.reset_levels()
        elif key == 27:  # ESC key to exit
            break

        if not game.game_over and level_manager.is_level_completed(game.score):
            if level_manager.next_level():
                game.reset_game(reset_score=False)
            else:
                game.update_high_score()
                game.game_over = True

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
