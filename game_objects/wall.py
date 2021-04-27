from engine.game_object import GameObject


class Wall(GameObject):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, "Wall",
                         "./textures/sprites/wall.png", 2, 0)
