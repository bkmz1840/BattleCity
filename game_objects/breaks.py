from engine.game_object import GameObject
from engine import game_data
from engine.size import Size
from engine.vector import Vector
from engine.direction import Direction


class Breaks(GameObject):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, "Breaks",
                         "./textures/sprites/breaks.png", 2, 0)
        self.is_broken = False

    def destroy(self, direction=None):
        sprite_v = "./textures/sprites/breaks_v.png"
        sprite_g = "./textures/sprites/breaks_g.png"
        if self.is_broken:
            game_data.for_destroy[self.id] = self
            return
        size_v = Size(40, 20)
        size_g = Size(20, 40)
        if direction == Direction.Up:
            self.sprite = sprite_g
            self.size = size_g
            self.is_broken = True
        elif direction == Direction.Down:
            self.position = Vector(
                self.position.x, self.position.y + size_g.height)
            self.sprite = sprite_g
            self.size = size_g
            self.is_broken = True
        elif direction == Direction.Left:
            self.sprite = sprite_v
            self.size = size_v
            self.is_broken = True
        elif direction == Direction.Right:
            self.position = Vector(
                self.position.x + size_v.width, self.position.y)
            self.sprite = sprite_v
            self.size = size_v
            self.is_broken = True
