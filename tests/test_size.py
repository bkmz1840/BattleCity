from engine.size import Size
import unittest


class TestsSize(unittest.TestCase):
    def test_init(self):
        size = Size(500, 600)
        self.assertEqual(size.height, 500)
        self.assertEqual(size.width, 600)
