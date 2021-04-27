from game_objects.enemy import Enemy
from engine import game_data
from engine.vector import Vector
from engine.size import Size
from engine.direction import Direction
import unittest


class TestsEnemy(unittest.TestCase):
    def check_obj_position(self, obj, position):
        self.assertEqual(obj.position.x, position.x)
        self.assertEqual(obj.position.y, position.y)

    def test_fire(self):
        game_data.game_objects.clear()
        game_data.for_destroy.clear()
        cords = Vector(55, 55)
        enemy = Enemy(cords)
        Enemy.fire(enemy, Direction.Up)
        objs = ["Enemy", "Bullet"]
        i = 0
        size_bullet_u = Size(12, 10)
        id = 0
        for game_object in game_data.game_objects:
            self.assertEqual(game_object.name, objs[i])
            if game_object.name == "Bullet":
                self.assertEqual(Direction.Up, game_object.direction)
                self.assertEqual(game_object.size.height,
                                 size_bullet_u.height)
                self.assertEqual(game_object.size.width,
                                 size_bullet_u.width)
                self.check_obj_position(game_object, Vector(65, 37.5))
                id = game_object.id
            i += 1
        self.assertEqual(enemy.bullet.id, id)
