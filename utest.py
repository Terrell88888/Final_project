import unittest
from main import SnakeGame, LevelManager


class TestSnakeGame(unittest.TestCase):
    def setUp(self):
        self.game = SnakeGame("C:\\Users\\Terrell\\Downloads\\1.png")
        self.level_manager = LevelManager()

    def test_food_generation(self):
        self.game.generate_food_position()
        x, y = self.game.food_position
        self.assertTrue(100 <= x <= 1000, "Food x-coordinate out of bounds")
        self.assertTrue(100 <= y <= 600, "Food y-coordinate out of bounds")

    def test_score_update(self):
        initial_score = self.game.score
        self.game.score += 1
        self.assertEqual(
            self.game.score,
            initial_score + 1,
            "Score did not update correctly")

    def test_collision_with_self(self):
        self.game.snake_body = [[100, 100], [120, 100], [
            140, 100], [140, 120], [120, 120], [100, 120]]
        # The head returns to the starting position
        self.game.last_head_position = [100, 100]
        self.game.check_collisions(level_config={})  # No obstacles
        self.assertTrue(self.game.game_over, "Self-collision not detected")

    def test_collision_with_obstacle(self):
        obstacle = (200, 200, 50, 50)
        # Snake's head moves into the obstacle's range
        self.game.snake_body = [[210, 210]]
        self.game.last_head_position = [210, 210]
        self.game.check_collisions(level_config={"obstacles": [obstacle]})
        self.assertTrue(self.game.game_over, "Obstacle collision not detected")

    def test_level_completion(self):
        current_level_config = self.level_manager.get_current_level_config()
        target_score = current_level_config["target_score"]
        self.assertFalse(
            self.level_manager.is_level_completed(
                self.game.score),
            "Level marked as completed prematurely")
        self.game.score = target_score
        self.assertTrue(
            self.level_manager.is_level_completed(
                self.game.score),
            "Level not marked as completed")

    def test_next_level(self):
        initial_level = self.level_manager.current_level
        self.assertTrue(
            self.level_manager.next_level(),
            "Failed to switch to the next level")
        self.assertEqual(
            self.level_manager.current_level,
            initial_level + 1,
            "Level did not increment correctly")
        # Test if it stops progressing after the last level
        while self.level_manager.next_level():
            pass
        self.assertFalse(
            self.level_manager.next_level(),
            "Switched to a non-existent level")

    def test_reset_game(self):
        self.game.snake_body = [[100, 100], [120, 100], [140, 100]]
        self.game.score = 10
        self.game.game_over = True
        self.game.reset_game(reset_score=True)
        self.assertEqual(len(self.game.snake_body), 0, "Snake body not reset")
        self.assertEqual(self.game.score, 0, "Score not reset")
        self.assertFalse(self.game.game_over, "Game over status not reset")


if __name__ == "__main__":
    unittest.main()
