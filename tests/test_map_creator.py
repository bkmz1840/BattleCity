from engine.map_creator import MapCreator
from engine import game_data
from game_objects import *
import unittest


class TestsMapCreator(unittest.TestCase):
    def setUp(self):
        self.map_creator = MapCreator()

    def test_create_game_object_by_symbol(self):
        s1 = "#"
        s2 = "P"
        s3 = "E"
        s4 = "9"
        x, y = 0, 0
        # empty_cell
        game_data.game_objects.clear()
        self.map_creator.create_game_object_by_symbol(s1, x, y)
        self.assertEqual(len(game_data.game_objects), 0)
        # player
        self.map_creator.create_game_object_by_symbol(s2, x, y)
        self.assertEqual(len(game_data.game_objects), 1)
        obj = game_data.game_objects[0]
        self.assertEqual(obj.position.x, 32.5)
        self.assertEqual(obj.position.y, 32.5)
        self.assertEqual(obj.size.height, 30)
        self.assertEqual(obj.size.width, 30)
        self.assertTrue(isinstance(obj, player.Player))
        self.assertEqual(game_data.player, obj)
        self.assertRaises(SystemError, self.map_creator
                          .create_game_object_by_symbol, s2, x + 1, y + 1)
        game_data.game_objects.clear()
        # base
        self.map_creator.create_game_object_by_symbol(s3, x, y)
        self.assertEqual(len(game_data.game_objects), 1)
        obj = game_data.game_objects[0]
        self.assertEqual(obj.position.x, 25)
        self.assertEqual(obj.position.y, 25)
        self.assertEqual(obj.size.height, 40)
        self.assertEqual(obj.size.width, 40)
        self.assertTrue(isinstance(obj, base.Base))
        self.assertEqual(game_data.base, obj)
        self.assertRaises(SystemError, self.map_creator
                          .create_game_object_by_symbol, s3, x + 1, y + 1)
        game_data.game_objects.clear()
        # other game object
        self.map_creator.create_game_object_by_symbol(s4, x, y)
        self.assertEqual(len(game_data.game_objects), 1)
        self.assertTrue(isinstance(game_data.game_objects[0], wall.Wall))

    def test_create_map(self):
        game_data.refresh_game_data()
        path = "./maps/test_map.txt"
        self.map_creator.create_map(path)
        self.assertEqual(len(game_data.game_objects), 34)
        self.assertEqual(game_data.map_width, 520)
        self.assertEqual(game_data.map_height, 520)
