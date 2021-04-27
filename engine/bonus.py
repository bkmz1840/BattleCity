from engine.vector import Vector
from engine import game_data
from PyQt5.QtGui import QPixmap


class Bonus:
    def __init__(self, x, y, size, sprite, d_p):
        self.id = game_data.id
        game_data.id += 1
        self.position = Vector(x, y)
        self.size = size
        self.sprite = sprite
        self.name = "Bonus"
        self.drawing_priority = d_p
        self.ticks_alive = 0
        game_data.game_objects.append(self)
        game_data.has_bonus = True

    def update(self):
        self.ticks_alive += 1
        if self.ticks_alive == game_data.duration_bonus:
            self.destroy()

    def draw(self, painter):
        painter.drawPixmap(self.position.x, self.position.y,
                           QPixmap(self.sprite))

    def destroy(self, taken_player=False):
        game_data.for_destroy[self.id] = self
        game_data.has_bonus = False
