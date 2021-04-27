from bonuses.clock import BonusClock
from game_objects.enemy import Enemy
from engine.vector import Vector
from engine import game_data
import unittest


class TestsBonusClock(unittest.TestCase):
    def test_destroy(self):
        game_data.map_width = 500
        game_data.map_height = 500
        bonus_clock = BonusClock()
        x, y = 25, 25
        for i in range(0, 3):
            pos = Vector(x, y)
            Enemy(pos)
            x += 50
            y += 50
        bonus_clock.destroy(True)
        for game_object in game_data.game_objects:
            if game_object.name == "Bonus":
                self.assertIn(bonus_clock.id, game_data.for_destroy)
            else:
                self.assertTrue(game_object.is_frozen)
