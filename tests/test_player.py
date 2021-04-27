from game_objects.player import Player
from engine.vector import Vector
from engine.size import Size
from game_objects.wall import Wall
from animations.anim_bullet import AnimationBullet
from bonuses.clock import BonusClock
from engine import game_data
from engine.direction import Direction
import unittest


class TestsPlayer(unittest.TestCase):
    def test_init(self):
        cords = Vector(10, 55)
        size = Size(30, 30)
        player = Player(cords.x, cords.y, size)
        self.check_obj_position(player, cords)
        self.assertEqual(player.size.width, size.width)
        self.assertEqual(player.size.height, size.height)
        self.assertEqual(player.speed, 1)
        self.assertEqual(player.sprite, "./textures/sprites/player_u_1.png")
        self.assertEqual(player.upd, Player.upd)
        self.assertEqual(player.name, "Player")
        self.assertEqual(player.drawing_priority, 3)

    def test_destroy(self):
        game_data.game_objects.clear()
        game_data.for_destroy.clear()
        cords = Vector(55, 55)
        size = Size(30, 30)
        player = Player(cords.x, cords.y, size)
        player.destroy()
        i = 0
        names_obj = ["Player", "Animation", "Animation"]
        for game_object in game_data.game_objects:
            self.assertEqual(game_object.name, names_obj[i])
            i += 1
        self.assertIn(player.id, game_data.for_destroy)

    def check_obj_position(self, obj, vector):
        self.assertEqual(obj.position.x, vector.x)
        self.assertEqual(obj.position.y, vector.y)

    def test_check_next_step(self):
        game_data.game_objects.clear()
        game_data.for_destroy.clear()
        game_data.map_width = 500
        game_data.map_height = 500
        x = [10, 50, 90]
        y = [90, 10, 90]
        size = Size(40, 40)
        for i in range(0, len(x)):
            Wall(x[i], y[i], size)
        AnimationBullet(Vector(5, 5))
        bonus_clock = BonusClock()
        bonus_clock.position = Vector(35, 65)
        cords = Vector(55, 55)
        size = Size(30, 30)
        player = Player(cords.x, cords.y, size)
        n_p_1 = Vector(55, 49)  # u
        n_p_2 = Vector(55, 91)  # d
        n_p_3 = Vector(91, 55)  # r
        n_p_4 = Vector(49, 55)  # l
        Player.check_next_step(player, n_p_1)
        self.check_obj_position(player, cords)
        Player.check_next_step(player, n_p_2)
        self.check_obj_position(player, n_p_2)
        Player.check_next_step(player, n_p_3)
        self.check_obj_position(player, n_p_3)
        Player.check_next_step(player, n_p_4)
        self.check_obj_position(player, n_p_4)
        self.assertIn(bonus_clock.id, game_data.for_destroy)

    def test_fire(self):
        game_data.game_objects.clear()
        game_data.for_destroy.clear()
        cords = Vector(55, 55)
        size = Size(30, 30)
        player = Player(cords.x, cords.y, size)
        Player.fire(player)
        objs = ["Player", "Bullet"]
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
                self.check_obj_position(game_object, Vector(65, 40))
                id = game_object.id
            i += 1
        self.assertEqual(player.bullet.id, id)

    def test_upd(self):
        game_data.game_objects.clear()
        game_data.for_destroy.clear()
        game_data.map_height = 500
        game_data.map_width = 500
        cords = Vector(55, 55)
        size = Size(30, 30)
        player = Player(cords.x, cords.y, size)
        game_data.is_space_pressed = True
        Player.upd(player)
        names_obj = ["Player", "Bullet"]
        i = 0
        for game_object in game_data.game_objects:
            self.assertEqual(game_object.name, names_obj[i])
            i += 1
        self.assertFalse(game_data.is_space_pressed)
        self.assertIsNotNone(player.bullet)
        # u
        game_data.pressed_key = Direction.Up
        Player.upd(player)
        self.assertEqual(player.sprite, player.sprite_u_2)
        self.check_obj_position(player, Vector(55, 54))
        Player.upd(player)
        self.assertEqual(player.sprite, player.sprite_u_1)
        self.check_obj_position(player, Vector(55, 53))
        # r
        game_data.pressed_key = Direction.Right
        Player.upd(player)
        self.assertEqual(player.sprite, player.sprite_r_1)
        self.check_obj_position(player, Vector(56, 53))
        # d
        game_data.pressed_key = Direction.Down
        Player.upd(player)
        self.assertEqual(player.sprite, player.sprite_d_1)
        self.check_obj_position(player, Vector(56, 54))
        # l
        game_data.pressed_key = Direction.Left
        Player.upd(player)
        self.assertEqual(player.sprite, player.sprite_l_1)
        self.check_obj_position(player, Vector(55, 54))
