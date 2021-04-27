from PyQt5.QtGui import QPixmap
from engine import game_data


class Animation:
    def __init__(self, pos, sprites, d_p, upd):
        self.id = game_data.id
        game_data.id += 1
        self.position = pos
        self.sprites = sprites
        self.name = "Animation"
        self.drawing_priority = d_p
        self.upd = upd
        self.index_sprite = 0
        self.count_updates = 0
        game_data.game_objects.append(self)

    def update(self):
        self.upd(self)

    def draw(self, painter):
        if self.index_sprite == len(self.sprites):
            self.destroy()
            return
        painter.drawPixmap(self.position.x, self.position.y,
                           QPixmap(self.sprites[self.index_sprite]))

    def destroy(self):
        game_data.for_destroy[self.id] = self
