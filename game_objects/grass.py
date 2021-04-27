from engine.game_object import GameObject


class Grass(GameObject):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, "Grass",
                         "./textures/sprites/grass.png", 1, 0)
