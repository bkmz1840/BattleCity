from game_objects.grass import Grass
from engine.vector import Vector
from engine.size import Size
import unittest


class TestsGrass(unittest.TestCase):
    def test_init(self):
        cords = Vector(10, 20)
        size = Size(40, 40)
        grass = Grass(cords.x, cords.y, size)
        self.assertEqual(grass.position.x, cords.x)
        self.assertEqual(grass.position.y, cords.y)
        self.assertEqual(grass.size.width, size.width)
        self.assertEqual(grass.size.height, size.height)
        self.assertEqual(grass.speed, 0)
        self.assertEqual(grass.sprite, "./textures/sprites/grass.png")
        self.assertIsNone(grass.upd)
        self.assertEqual(grass.name, "Grass")
        self.assertEqual(grass.drawing_priority, 1)
