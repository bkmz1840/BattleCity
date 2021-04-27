from game_objects import *
from engine import game_data
from engine.size import Size


class MapCreator:
    def __init__(self):
        self.size = 40
        self.size_player = Size(30, 30)
        self.game_objects = {
            "4": lambda x, y, size: breaks.Breaks(x, y, size),
            "9": lambda x, y, size: wall.Wall(x, y, size),
            "A": lambda x, y, size: water.Watter(x, y, size),
            "B": lambda x, y, size: grass.Grass(x, y, size),
            "P": lambda x, y, size: player.Player(x, y, size),
            "E": lambda x, y, size: base.Base(x, y, size)
        }

    def create_map(self, path_to_map):
        with open(path_to_map) as file:
            rows = file.read().split("\n")
        for x in range(0, len(rows[0])):
            for y in range(0, len(rows)):
                self.create_game_object_by_symbol(
                    rows[y][x], x, y)
        game_data.map_height = len(rows) * self.size
        game_data.map_width = len(rows[0]) * self.size

    def create_game_object_by_symbol(self, symbol, x, y):
        if symbol not in self.game_objects:
            return
        if symbol == "P":
            if game_data.player is not None:
                raise SystemError("Player have already exist")
            obj = self.game_objects[symbol](
                game_data.game_place_offset + x * self.size
                + self.size_player.width / 4,
                game_data.game_place_offset + y * self.size
                + self.size_player.height / 4,
                self.size_player)
            game_data.player = obj
            return
        obj = self.game_objects[symbol](
            game_data.game_place_offset + x * self.size,
            game_data.game_place_offset + y * self.size,
            Size(self.size, self.size))
        if symbol == "E":
            if game_data.base is not None:
                raise SystemError("Base have already exist")
            game_data.base = obj
