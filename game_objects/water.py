from engine.game_object import GameObject


class Watter(GameObject):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, "Water",
                         "./textures/sprites/water.png", 5, 0)
