from engine.animation import Animation
from game_objects.enemy import Enemy
from engine import game_data
from engine.vector import Vector
from engine.size import Size


class AnimationSpawnEnemy(Animation):
    def __init__(self, pos, pos_enemy):
        game_data.count_enemies_in_game += 1
        sprites = ["./textures/animations/spawn_enemy_1.png",
                   "./textures/animations/spawn_enemy_2.png",
                   "./textures/animations/spawn_enemy_3.png"]
        self.init_pos = Vector(pos.x + 5, pos.y + 5)
        super().__init__(
            self.init_pos.copy(), sprites, -1, AnimationSpawnEnemy.upd)
        self.size = Size(40, 40)
        self.circles = 0
        self.position_enemy = pos_enemy
        self.name = "AnimationSpawnEnemy"

    def destroy(self):
        Enemy(self.position_enemy)
        game_data.for_destroy[self.id] = self

    @staticmethod
    def upd(anim):
        if anim.circles == 2:
            anim.index_sprite = len(anim.sprites)
            return
        anim.count_updates += 1
        if anim.count_updates % 12 == 0:
            anim.index_sprite += 1
            anim.position.x -= 10
            anim.position.y -= 10
            if anim.index_sprite == len(anim.sprites):
                anim.index_sprite = 0
                anim.circles += 1
                anim.position = anim.init_pos.copy()
