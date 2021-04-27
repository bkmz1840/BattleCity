from engine.game_object import GameObject
from engine.size import Size
from engine.vector import Vector
from engine.direction import Direction
from engine import game_data
from game_objects.bullet import Bullet
from animations.anim_tank_death import AnimationTankDeath
import random


class Enemy(GameObject):
    def __init__(self, pos):
        self.size_v = Size(35, 30)
        self.size_g = Size(30, 35)
        super().__init__(pos.x, pos.y, self.size_v, "Enemy",
                         "./textures/sprites/enemy_u_1.png", 3, 1,
                         Enemy.upd)
        self.sprite_u_1 = ""
        self.sprite_r_1 = ""
        self.sprite_d_1 = ""
        self.sprite_l_1 = ""
        self.sprite_u_2 = ""
        self.sprite_r_2 = ""
        self.sprite_d_2 = ""
        self.sprite_l_2 = ""
        type_enemy = self.choose_type_enemy()
        if type_enemy == 1:
            self.set_first_type_enemy()
        else:
            self.set_second_type_enemy()
        self.last_step = ""
        self.bullet = None
        self.is_frozen = False
        self.freeze_time = 0

    def choose_type_enemy(self):
        random_int = random.randint(1, 16)
        if random_int == 11:
            return 2
        else:
            return 1

    def set_first_type_enemy(self):
        self.sprite_u_1 = "./textures/sprites/enemy_u_1.png"
        self.sprite_r_1 = "./textures/sprites/enemy_r_1.png"
        self.sprite_d_1 = "./textures/sprites/enemy_d_1.png"
        self.sprite_l_1 = "./textures/sprites/enemy_l_1.png"
        self.sprite_u_2 = "./textures/sprites/enemy_u_2.png"
        self.sprite_r_2 = "./textures/sprites/enemy_r_2.png"
        self.sprite_d_2 = "./textures/sprites/enemy_d_2.png"
        self.sprite_l_2 = "./textures/sprites/enemy_l_2.png"

    def set_second_type_enemy(self):
        self.speed = 2
        self.sprite = "./textures/sprites/enemy_f_u_1.png"
        self.sprite_u_1 = "./textures/sprites/enemy_f_u_1.png"
        self.sprite_r_1 = "./textures/sprites/enemy_f_r_1.png"
        self.sprite_d_1 = "./textures/sprites/enemy_f_d_1.png"
        self.sprite_l_1 = "./textures/sprites/enemy_f_l_1.png"
        self.sprite_u_2 = "./textures/sprites/enemy_f_u_2.png"
        self.sprite_r_2 = "./textures/sprites/enemy_f_r_2.png"
        self.sprite_d_2 = "./textures/sprites/enemy_f_d_2.png"
        self.sprite_l_2 = "./textures/sprites/enemy_f_l_2.png"

    def destroy(self, direction=None):
        game_data.count_enemies_in_game -= 1
        AnimationTankDeath(Vector(
            self.position.x + self.size.width / 4,
            self.position.y + self.size.height / 4))
        game_data.for_destroy[self.id] = self

    @staticmethod
    def fire(enemy, direction):
        if enemy.bullet is None:
            size_by_direction = {
                Direction.Up: Size(12, 10),
                Direction.Right: Size(10, 13),
                Direction.Down: Size(13, 10),
                Direction.Left: Size(10, 13)
            }
            size = size_by_direction[direction]
            position_by_direction = {
                Direction.Up: Vector(
                    enemy.position.x + enemy.size.width / 2 -
                    size.width / 2,
                    enemy.position.y - enemy.size.height / 2),
                Direction.Down: Vector(
                    enemy.position.x + enemy.size.width / 2 -
                    size.width / 2,
                    enemy.position.y + 3 * enemy.size.height / 2),
                Direction.Left: Vector(
                    enemy.position.x - enemy.size.width / 2,
                    enemy.position.y + enemy.size.height / 2 -
                    size.height / 2),
                Direction.Right: Vector(
                    enemy.position.x + 3 * enemy.size.width / 2,
                    enemy.position.y + enemy.size.height / 2 -
                    size.height / 2)
            }
            position = position_by_direction[direction]
            enemy.bullet = Bullet(
                position.x, position.y, size, direction, True, enemy=enemy)

    @staticmethod
    def check_obj_intersect_enemy(
            enemy, available_directions, old_position, game_object):
        if Direction.Up in available_directions:
            enemy.size = enemy.size_v
            if old_position.y - enemy.speed \
                    >= game_data.game_place_offset:
                enemy.position = Vector(
                    old_position.x, old_position.y - enemy.speed)
                if enemy.is_intersect(game_object):
                    available_directions.remove(Direction.Up)
                enemy.position = old_position
            else:
                available_directions.remove(Direction.Up)
        if Direction.Down in available_directions:
            enemy.size = enemy.size_v
            if old_position.y + enemy.speed \
                    < game_data.map_height - 8:
                enemy.position = Vector(
                    old_position.x, old_position.y + enemy.speed)
                if enemy.is_intersect(game_object):
                    available_directions.remove(Direction.Down)
                enemy.position = old_position
            else:
                available_directions.remove(Direction.Down)
        if Direction.Left in available_directions:
            enemy.size = enemy.size_g
            if old_position.x - enemy.speed \
                    >= game_data.game_place_offset:
                enemy.position = Vector(
                    old_position.x - enemy.speed, old_position.y)
                if enemy.is_intersect(game_object):
                    available_directions.remove(Direction.Left)
                enemy.position = old_position
            else:
                available_directions.remove(Direction.Left)
        if Direction.Right in available_directions:
            enemy.size = enemy.size_g
            if old_position.x + enemy.speed \
                    < game_data.map_width - 8:
                enemy.position = Vector(
                    old_position.x + enemy.speed, old_position.y)
                if enemy.is_intersect(game_object):
                    available_directions.remove(Direction.Right)
                enemy.position = old_position
            else:
                available_directions.remove(Direction.Right)

    @staticmethod
    def get_available_directions(enemy):
        available_directions = {Direction.Up, Direction.Right,
                                Direction.Down, Direction.Left}
        old_position = enemy.position
        for game_object in game_data.game_objects:
            if game_object.id == enemy.id \
                    or game_object.name == "Grass" \
                    or game_object.name == "Animation" \
                    or game_object.name == "Bonus":
                continue
            Enemy.check_obj_intersect_enemy(
                enemy, available_directions, old_position, game_object)
            if len(available_directions) == 0:
                return None
        directions = []
        for direction in available_directions:
            directions.append(direction)
        if len(directions) == 0:
            return None
        return directions

    @staticmethod
    def first_behavior(enemy, available_directions):
        if enemy.last_step in available_directions:
            direction = enemy.last_step
        else:
            direction = available_directions[
                random.randint(0, len(available_directions) - 1)]
        enemy.last_step = direction
        Enemy.make_step_by_direction(enemy, direction)

    @staticmethod
    def get_direction_to_obj(enemy, available_directions, obj):
        directions = []
        if enemy.position.x > obj.position.x \
                and Direction.Left in available_directions:
            directions.append(Direction.Left)
        if enemy.position.x < obj.position.x \
                and Direction.Right in available_directions:
            directions.append(Direction.Right)
        if enemy.position.y > obj.position.y \
                and Direction.Up in available_directions:
            directions.append(Direction.Up)
        if enemy.position.y < obj.position.y \
                and Direction.Down in available_directions:
            directions.append(Direction.Down)
        if len(directions) == 0:
            direction = None
        elif len(directions) == 1:
            direction = directions[0]
        elif enemy.last_step in directions:
            direction = enemy.last_step
        else:
            direction = directions[random.randint(0, len(directions) - 1)]
        return direction

    @staticmethod
    def check_enemy_on_line_with_obj(enemy, obj, eps):
        return abs(enemy.position.y - obj.position.y) <= eps \
               and enemy.position.y + enemy.size.height \
               >= obj.position.y + obj.size.height \
               or abs((enemy.position.y + enemy.size.height) -
                      (obj.position.y + obj.size.height)) <= eps \
               and enemy.position.y <= obj.position.y \
               or abs(enemy.position.x - obj.position.x) <= eps \
               and enemy.position.x + enemy.size.width \
               >= obj.position.x + obj.size.width \
               or abs((enemy.position.x + enemy.size.width) -
                      (obj.position.x + obj.size.width)) <= eps \
               and enemy.position.x <= obj.position.x

    @staticmethod
    def move_to_obj(enemy, obj, available_directions):
        if len(available_directions) == 1:
            direction = available_directions[0]
            Enemy.make_step_by_direction(enemy, direction)
            return
        eps = enemy.speed * 3
        if Enemy.check_enemy_on_line_with_obj(enemy, obj, eps):
            if abs(enemy.position.x - obj.position.x) > eps:
                if enemy.position.x > obj.position.x:
                    Enemy.set_sprite(enemy, Direction.Left)
                else:
                    Enemy.set_sprite(enemy, Direction.Right)
            elif abs(enemy.position.y - obj.position.y) > eps:
                if enemy.position.y > obj.position.y:
                    Enemy.set_sprite(enemy, Direction.Up)
                else:
                    Enemy.set_sprite(enemy, Direction.Down)
        else:
            direction = Enemy.get_direction_to_obj(
                enemy, available_directions, obj)
            Enemy.make_step_by_direction(enemy, direction)

    @staticmethod
    def set_sprite(enemy, direction):
        sprites_by_direction = {
            Direction.Up: enemy.sprite_u_1,
            Direction.Right: enemy.sprite_r_1,
            Direction.Down: enemy.sprite_d_1,
            Direction.Left: enemy.sprite_l_1
        }
        sprites_pairs = {
            enemy.sprite_u_1: enemy.sprite_u_2,
            enemy.sprite_r_1: enemy.sprite_r_2,
            enemy.sprite_d_1: enemy.sprite_d_2,
            enemy.sprite_l_1: enemy.sprite_l_2
        }
        sprite = sprites_by_direction[direction]
        if enemy.sprite == sprite:
            enemy.sprite = sprites_pairs[sprite]
        else:
            enemy.sprite = sprite
        if enemy.sprite == enemy.sprite_u_1 \
                or enemy.sprite == enemy.sprite_u_2 \
                or enemy.sprite == enemy.sprite_d_1 \
                or enemy.sprite == enemy.sprite_d_2:
            enemy.size = enemy.size_v
        else:
            enemy.size = enemy.size_g

    @staticmethod
    def make_step_by_direction(enemy, direction):
        if direction is None:
            return
        enemy.last_step = direction
        Enemy.set_sprite(enemy, direction)
        next_position_by_direction = {
            Direction.Up: Vector(enemy.position.x,
                                 enemy.position.y - enemy.speed),
            Direction.Right: Vector(enemy.position.x + enemy.speed,
                                    enemy.position.y),
            Direction.Down: Vector(enemy.position.x,
                                   enemy.position.y + enemy.speed),
            Direction.Left: Vector(enemy.position.x - enemy.speed,
                                   enemy.position.y)
        }
        enemy.position = next_position_by_direction[direction]

    @staticmethod
    def upd(enemy):
        if enemy.is_frozen \
                and enemy.freeze_time < game_data.duration_freeze_time:
            enemy.freeze_time += 1
            return
        enemy.is_frozen = False
        enemy.freeze_time = 0
        available_directions = Enemy.get_available_directions(enemy)
        if available_directions is None:
            return
        if game_data.enemy_behavior == 1:
            Enemy.first_behavior(enemy, available_directions)
        elif game_data.enemy_behavior == 2:
            Enemy.move_to_obj(enemy, game_data.player, available_directions)
        else:
            Enemy.move_to_obj(enemy, game_data.base, available_directions)
        direction_by_sprite = {
            enemy.sprite_u_1: Direction.Up,
            enemy.sprite_u_2: Direction.Up,
            enemy.sprite_r_1: Direction.Right,
            enemy.sprite_r_2: Direction.Right,
            enemy.sprite_d_1: Direction.Down,
            enemy.sprite_d_2: Direction.Down,
            enemy.sprite_l_1: Direction.Left,
            enemy.sprite_l_2: Direction.Left
        }
        direction = direction_by_sprite[enemy.sprite]
        random_int = random.randint(1, 64)
        if random_int == 11:
            Enemy.fire(enemy, direction)
