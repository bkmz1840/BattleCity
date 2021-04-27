from engine.game_object import GameObject
from engine import game_data
from engine.vector import Vector
from engine.size import Size
from engine.direction import Direction
from animations.anim_tank_death import AnimationTankDeath
from animations.anim_game_over import AnimationGameOver
from game_objects.bullet import Bullet


class Player(GameObject):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, "Player",
                         "./textures/sprites/player_u_1.png", 3, 1,
                         Player.upd)
        self.spawn_position = Vector(x, y)
        self.sprite_u_1 = "./textures/sprites/player_u_1.png"
        self.sprite_r_1 = "./textures/sprites/player_r_1.png"
        self.sprite_d_1 = "./textures/sprites/player_d_1.png"
        self.sprite_l_1 = "./textures/sprites/player_l_1.png"
        self.sprite_u_2 = "./textures/sprites/player_u_2.png"
        self.sprite_r_2 = "./textures/sprites/player_r_2.png"
        self.sprite_d_2 = "./textures/sprites/player_d_2.png"
        self.sprite_l_2 = "./textures/sprites/player_l_2.png"
        self.bullet = None
        self.count_lifes = 2
        self.is_dead = False

    def destroy(self, direction=None):
        self.count_lifes -= 1
        AnimationTankDeath(Vector(
            self.position.x + self.size.width / 4,
            self.position.y + self.size.height / 4))
        if self.count_lifes == 0:
            self.is_dead = True
            AnimationGameOver()
        else:
            self.position = self.spawn_position.copy()
        game_data.for_destroy[self.id] = self

    @staticmethod
    def check_next_step(player, next_position):
        old_position = player.position
        player.position = next_position
        for game_object in game_data.game_objects:
            if game_object.id == player.id \
                    or game_object.name == "Animation":
                continue
            if game_object.name != "Grass" \
                    and player.is_intersect(game_object):
                if game_object.name == "Bonus":
                    game_object.destroy(True)
                    break
                player.position = old_position
                break

    @staticmethod
    def fire(player):
        if player.bullet is None:
            direction_by_sprite = {
                player.sprite_u_1: Direction.Up,
                player.sprite_r_1: Direction.Right,
                player.sprite_d_1: Direction.Down,
                player.sprite_l_1: Direction.Left,
                player.sprite_u_2: Direction.Up,
                player.sprite_r_2: Direction.Right,
                player.sprite_d_2: Direction.Down,
                player.sprite_l_2: Direction.Left
            }
            direction = direction_by_sprite[player.sprite]
            size_by_direction = {
                Direction.Up: Size(12, 10),
                Direction.Right: Size(10, 13),
                Direction.Down: Size(13, 10),
                Direction.Left: Size(10, 13)
            }
            size = size_by_direction[direction]
            position_by_direction = {
                Direction.Up: Vector(
                    player.position.x + player.size.width / 2 -
                    size.width / 2,
                    player.position.y - player.size.height / 2),
                Direction.Down: Vector(
                    player.position.x + player.size.width / 2 -
                    size.width / 2,
                    player.position.y + 3 * player.size.height / 2),
                Direction.Left: Vector(
                    player.position.x - player.size.width / 2,
                    player.position.y + player.size.height / 2 -
                    size.height / 2),
                Direction.Right: Vector(
                    player.position.x + 3 * player.size.width / 2,
                    player.position.y + player.size.height / 2 -
                    size.height / 2)
            }
            position = position_by_direction[direction]
            player.bullet = Bullet(position.x, position.y, size,
                                   direction, False, player=player)
        game_data.is_space_pressed = False

    @staticmethod
    def set_player_sprite(player):
        sprites_by_key = {
            Direction.Up: player.sprite_u_1,
            Direction.Right: player.sprite_r_1,
            Direction.Down: player.sprite_d_1,
            Direction.Left: player.sprite_l_1
        }
        if game_data.pressed_key not in sprites_by_key:
            return False
        sprites_pairs = {
            player.sprite_u_1: player.sprite_u_2,
            player.sprite_r_1: player.sprite_r_2,
            player.sprite_d_1: player.sprite_d_2,
            player.sprite_l_1: player.sprite_l_2
        }
        sprite = sprites_by_key[game_data.pressed_key]
        if player.sprite == sprite:
            player.sprite = sprites_pairs[sprite]
        else:
            player.sprite = sprite
        return True

    @staticmethod
    def upd(player):
        if game_data.is_space_pressed:
            Player.fire(player)
        if not Player.set_player_sprite(player):
            return
        if game_data.pressed_key == Direction.Up \
                and player.position.y - player.speed \
                >= game_data.game_place_offset:
            Player.check_next_step(
                player, Vector(player.position.x,
                               player.position.y - player.speed))
        elif game_data.pressed_key == Direction.Down \
                and player.position.y + player.speed \
                < game_data.map_height - 7:
            Player.check_next_step(
                player, Vector(player.position.x,
                               player.position.y + player.speed))
        elif game_data.pressed_key == Direction.Right \
                and player.position.x + player.speed \
                < game_data.map_width - 7:
            Player.check_next_step(
                player, Vector(player.position.x + player.speed,
                               player.position.y))
        elif game_data.pressed_key == Direction.Left \
                and player.position.x - player.speed \
                >= game_data.game_place_offset:
            Player.check_next_step(
                player, Vector(player.position.x - player.speed,
                               player.position.y))
