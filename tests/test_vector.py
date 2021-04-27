from engine.vector import Vector
import unittest


class TestsVector(unittest.TestCase):
    def test_operations(self):
        vector = Vector(10, 10)
        other_v = Vector(15, 15)
        self.assertEqual(vector.x, 10)
        self.assertEqual(vector.y, 10)
        # __add__
        vector = vector + other_v
        self.assertEqual(vector.x, 25)
        self.assertEqual(vector.y, 25)
        # __iadd__
        vector += other_v
        self.assertEqual(vector.x, 40)
        self.assertEqual(vector.y, 40)
        # __sub__
        vector = vector - other_v
        self.assertEqual(vector.x, 25)
        self.assertEqual(vector.y, 25)
        # __isub__
        vector -= other_v
        self.assertEqual(vector.x, 10)
        self.assertEqual(vector.y, 10)
        # __str__
        self.assertEqual(str(vector), "(10, 10)")

    def test_copy(self):
        vector = Vector(5, 10)
        other_v = vector.copy()
        self.assertFalse(vector == other_v)
        self.assertEqual(other_v.x, 5)
        self.assertEqual(other_v.y, 10)
