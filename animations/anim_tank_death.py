from engine.animation import Animation


class AnimationTankDeath(Animation):
    def __init__(self, pos):
        sprites = ["./textures/animations/tank_1.png",
                   "./textures/animations/tank_2.png"]
        super().__init__(pos, sprites, -1, AnimationTankDeath.upd)

    @staticmethod
    def upd(anim):
        anim.count_updates += 1
        if anim.count_updates % 10 == 0:
            anim.index_sprite += 1
            anim.position.x -= 10
            anim.position.y -= 10
