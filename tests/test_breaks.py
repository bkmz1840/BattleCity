from game_objects.breaks import Breaks
from engine.vector import Vector
from engine.size import Size
from engine.direction import Direction
from engine import game_data
import unittest


class TestsBreaks(unittest.TestCase):
    def test_init(self):
        cords = Vector(10, 20)
        size = Size(40, 40)
        breaks = Breaks(cords.x, cords.y, size)
        self.assertEqual(breaks.position.x, cords.x)
        self.assertEqual(breaks.position.y, cords.y)
        self.assertEqual(breaks.size.width, size.width)
        self.assertEqual(breaks.size.height, size.height)
        self.assertEqual(breaks.speed, 0)
        self.assertEqual(breaks.sprite, "./textures/sprites/breaks.png")
        self.assertIsNone(breaks.upd)
        self.assertEqual(breaks.name, "Breaks")
        self.assertEqual(breaks.drawing_priority, 2)

    def test_destroy(self):
        cords = Vector(10, 20)
        size = Size(40, 40)
        breaks = Breaks(cords.x, cords.y, size)
        sprite_v = "./textures/sprites/breaks_v.png"
        sprite_g = "./textures/sprites/breaks_g.png"
        size_v = Size(40, 20)
        size_g = Size(20, 40)
        # u
        breaks.destroy(Direction.Up)
        self.assertEqual(breaks.position.x, cords.x)
        self.assertEqual(breaks.position.y, cords.y)
        self.assertEqual(breaks.sprite, sprite_g)
        self.assertEqual(breaks.size.height, size_g.height)
        self.assertEqual(breaks.size.width, size_g.width)
        # d
        breaks = Breaks(cords.x, cords.y, size)
        breaks.destroy(Direction.Down)
        self.assertEqual(breaks.position.x, cords.x)
        self.assertEqual(breaks.position.y, cords.y + size_g.height)
        self.assertEqual(breaks.sprite, sprite_g)
        self.assertEqual(breaks.size.height, size_g.height)
        self.assertEqual(breaks.size.width, size_g.width)
        # r
        breaks = Breaks(cords.x, cords.y, size)
        breaks.destroy(Direction.Right)
        self.assertEqual(breaks.position.x, cords.x + size_v.width)
        self.assertEqual(breaks.position.y, cords.y)
        self.assertEqual(breaks.sprite, sprite_v)
        self.assertEqual(breaks.size.height, size_v.height)
        self.assertEqual(breaks.size.width, size_v.width)
        # l
        breaks = Breaks(cords.x, cords.y, size)
        breaks.destroy(Direction.Left)
        self.assertEqual(breaks.position.x, cords.x)
        self.assertEqual(breaks.position.y, cords.y)
        self.assertEqual(breaks.sprite, sprite_v)
        self.assertEqual(breaks.size.height, size_v.height)
        self.assertEqual(breaks.size.width, size_v.width)
        id = breaks.id
        breaks.destroy()
        self.assertIn(id, game_data.for_destroy)
