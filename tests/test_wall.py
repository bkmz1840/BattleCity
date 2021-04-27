from game_objects.wall import Wall
from engine.vector import Vector
from engine.size import Size
import unittest


class TestsWall(unittest.TestCase):
    def test_init(self):
        cords = Vector(10, 20)
        size = Size(40, 40)
        wall = Wall(cords.x, cords.y, size)
        self.assertEqual(wall.position.x, cords.x)
        self.assertEqual(wall.position.y, cords.y)
        self.assertEqual(wall.size.width, size.width)
        self.assertEqual(wall.size.height, size.height)
        self.assertEqual(wall.speed, 0)
        self.assertEqual(wall.sprite, "./textures/sprites/wall.png")
        self.assertIsNone(wall.upd)
        self.assertEqual(wall.name, "Wall")
        self.assertEqual(wall.drawing_priority, 2)
