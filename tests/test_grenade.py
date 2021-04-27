from bonuses.grenade import BonusGrenade
from game_objects.enemy import Enemy
from engine.vector import Vector
from engine import game_data
import unittest


class TestsBonusGrenade(unittest.TestCase):
    def test_destroy(self):
        game_data.map_width = 500
        game_data.map_height = 500
        bonus_grenade = BonusGrenade()
        x, y = 25, 25
        for i in range(0, 3):
            pos = Vector(x, y)
            Enemy(pos)
            x += 50
            y += 50
        bonus_grenade.destroy(True)
        for game_object in game_data.game_objects:
            if game_object.name == "Bonus" or game_object.name == "Enemy":
                self.assertIn(game_object.id, game_data.for_destroy)
