from engine.game_object import GameObject
from engine.vector import Vector
from engine.direction import Direction
from engine import game_data
from animations.anim_bullet import AnimationBullet


class Bullet(GameObject):
    def __init__(self, x, y, size, direction,
                 is_enemy_bullet, player=None, enemy=None):
        super().__init__(x, y, size, "Bullet",
                         "./textures/sprites/bullet_u.png", 4, 3,
                         Bullet.upd)
        self.direction = direction
        sprites_by_direction = {
            Direction.Up: "./textures/sprites/bullet_u.png",
            Direction.Right: "./textures/sprites/bullet_r.png",
            Direction.Down: "./textures/sprites/bullet_d.png",
            Direction.Left: "./textures/sprites/bullet_l.png"
        }
        self.sprite = sprites_by_direction[direction]
        self.not_breakable_objects = {"Grass", "Water", "Wall"}
        self.is_enemy_bullet = is_enemy_bullet
        self.enemy = enemy
        self.player = player

    def destroy(self, direction=None):
        AnimationBullet(Vector(
            self.position.x - self.size.width / 2,
            self.position.y - self.size.height / 2))
        game_data.for_destroy[self.id] = self
        if self.is_enemy_bullet:
            self.enemy.bullet = None
        else:
            self.player.bullet = None

    @staticmethod
    def make_step(bullet):
        if bullet.direction == Direction.Up:
            bullet.position.y -= bullet.speed
            if bullet.position.y < game_data.game_place_offset:
                bullet.position.y += bullet.speed
                bullet.destroy()
        elif bullet.direction == Direction.Right:
            bullet.position.x += bullet.speed
            if bullet.position.x > game_data.map_width + 13:
                bullet.position.x -= bullet.speed
                bullet.destroy()
        elif bullet.direction == Direction.Down:
            bullet.position.y += bullet.speed
            if bullet.position.y > game_data.map_height + 13:
                bullet.position.y -= bullet.speed
                bullet.destroy()
        elif bullet.direction == Direction.Left:
            bullet.position.x -= bullet.speed
            if bullet.position.x < game_data.game_place_offset:
                bullet.position.x += bullet.speed
                bullet.destroy()

    @staticmethod
    def upd(bullet):
        Bullet.make_step(bullet)
        for game_object in game_data.game_objects:
            if game_object.id == bullet.id \
                    or game_object.name == "Animation" \
                    or game_object.name == "Bonus":
                continue
            if bullet.is_intersect(game_object):
                if game_object.name == "Enemy" and bullet.is_enemy_bullet:
                    break
                if game_object.name == "Wall":
                    bullet.destroy()
                elif game_object.name not in bullet.not_breakable_objects:
                    if game_object.name == "Breaks":
                        game_object.destroy(bullet.direction)
                    else:
                        game_object.destroy()
                    bullet.destroy()
                break
