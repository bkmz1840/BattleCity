from engine.vector import Vector
from engine import game_data
from PyQt5.QtGui import QPixmap


class GameObject:
    def __init__(self, x, y, size, name, sprite, d_p, speed, upd=None):
        self.id = game_data.id
        game_data.id += 1
        self.position = Vector(x, y)
        self.size = size
        self.sprite = sprite
        self.name = name
        self.drawing_priority = d_p
        self.speed = speed
        self.upd = upd
        game_data.game_objects.append(self)

    def update(self):
        if self.upd is not None:
            self.upd(self)

    def draw(self, painter):
        painter.drawPixmap(self.position.x, self.position.y,
                           QPixmap(self.sprite))

    def is_intersect(self, other):
        return not (self.position.x + self.size.width <= other.position.x
                    or self.position.y + self.size.height <= other.position.y
                    or self.position.x >= other.position.x + other.size.width
                    or self.position.y >= other.position.y + other.size.height)

    def destroy(self, direction=None):
        game_data.for_destroy[self.id] = self
