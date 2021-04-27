from engine.game_object import GameObject
from animations.anim_game_over import AnimationGameOver


class Base(GameObject):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, "Base",
                         "./textures/sprites/base.png", 2, 0)
        self.sprite_broken = "./textures/sprites/base_broken.png"

    def destroy(self, direction=None):
        if self.sprite != self.sprite_broken:
            self.sprite = self.sprite_broken
            AnimationGameOver()
