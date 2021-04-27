from game_objects.bullet import Bullet
from engine.vector import Vector
from engine.size import Size
from engine.direction import Direction
from engine import game_data
from game_objects.player import Player
from game_objects.wall import Wall
from bonuses.clock import BonusClock
import unittest


class TestsBullet(unittest.TestCase):
    def test_init(self):
        cords = Vector(10, 20)
        size = Size(12, 10)
        bullet = Bullet(cords.x, cords.y, size, Direction.Up, False)
        self.assertEqual(bullet.position.x, cords.x)
        self.assertEqual(bullet.position.y, cords.y)
        self.assertEqual(bullet.size.width, size.width)
        self.assertEqual(bullet.size.height, size.height)
        self.assertEqual(bullet.speed, 3)
        self.assertEqual(bullet.sprite, "./textures/sprites/bullet_u.png")
        self.assertIsNotNone(Bullet.upd)
        self.assertEqual(bullet.name, "Bullet")
        self.assertEqual(bullet.drawing_priority, 4)

    def find_bullet(self):
        for game_object in game_data.game_objects:
            if game_object.name == "Bullet":
                return game_object
        return None

    def test_destroy(self):
        game_data.game_objects.clear()
        cords = Vector(10, 20)
        size_p = Size(30, 30)
        player = Player(cords.x, cords.y, size_p)
        Player.fire(player)
        bullet = self.find_bullet()
        self.assertIsNotNone(bullet)
        self.assertIsNotNone(player.bullet)
        bullet.destroy()
        self.assertEqual(game_data.game_objects[-1].name, "Animation")
        self.assertIn(bullet.id, game_data.for_destroy)
        self.assertIsNone(player.bullet)

    def check_obj_position(self, obj, vector):
        self.assertEqual(obj.position.x, vector.x)
        self.assertEqual(obj.position.y, vector.y)

    def test_upd(self):
        game_data.game_objects.clear()
        game_data.for_destroy.clear()
        game_data.map_width = 500
        game_data.map_height = 500
        cords_p = Vector(50, 50)
        size_p = Size(30, 30)
        player = Player(cords_p.x, cords_p.y, size_p)
        cords = Vector(200, 200)
        size = Size(12, 10)
        bullet = Bullet(cords.x, cords.y, size, Direction.Up, False, player=player)
        player.bullet = bullet
        BonusClock()
        Bullet.upd(bullet)
        self.check_obj_position(bullet, Vector(200, 197))
        self.assertEqual(len(game_data.for_destroy), 0)
        wall = Wall(200, 196, Size(40, 40))
        Bullet.upd(bullet)
        self.check_obj_position(bullet, Vector(200, 194))
        self.assertIn(bullet.id, game_data.for_destroy)
        self.assertNotIn(wall.id, game_data.for_destroy)
        game_data.game_objects.pop()
        game_data.for_destroy.clear()
        player.position = Vector(200, 192)
        Bullet.upd(bullet)
        self.check_obj_position(bullet, Vector(200, 191))
        self.assertIn(bullet.id, game_data.for_destroy)
        self.assertIn(player.id, game_data.for_destroy)
        size_by_direction = {
            Direction.Up: Size(12, 10),
            Direction.Right: Size(10, 13),
            Direction.Down: Size(13, 10),
            Direction.Left: Size(10, 13)
        }
        # r
        bullet.direction = Direction.Right
        bullet.size = size_by_direction[bullet.direction]
        game_data.game_objects.pop(0)
        game_data.for_destroy.clear()
        Bullet.upd(bullet)
        self.check_obj_position(bullet, Vector(203, 191))
        # d
        bullet.direction = Direction.Down
        bullet.size = size_by_direction[bullet.direction]
        Bullet.upd(bullet)
        self.check_obj_position(bullet, Vector(203, 194))
        # l
        bullet.direction = Direction.Left
        bullet.size = size_by_direction[bullet.direction]
        Bullet.upd(bullet)
        self.check_obj_position(bullet, Vector(200, 194))
        bullet.position = Vector(26, 26)
        bullet.direction = Direction.Up
        bullet.size = size_by_direction[bullet.direction]
        Bullet.upd(bullet)
        self.assertIn(bullet.id, game_data.for_destroy)
