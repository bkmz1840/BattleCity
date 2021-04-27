from game_objects.water import Watter
from engine.vector import Vector
from engine.size import Size
import unittest


class TestsWater(unittest.TestCase):
    def test_init(self):
        cords = Vector(10, 20)
        size = Size(40, 40)
        water = Watter(cords.x, cords.y, size)
        self.assertEqual(water.position.x, cords.x)
        self.assertEqual(water.position.y, cords.y)
        self.assertEqual(water.size.width, size.width)
        self.assertEqual(water.size.height, size.height)
        self.assertEqual(water.speed, 0)
        self.assertEqual(water.sprite, "./textures/sprites/water.png")
        self.assertIsNone(water.upd)
        self.assertEqual(water.name, "Water")
        self.assertEqual(water.drawing_priority, 5)
