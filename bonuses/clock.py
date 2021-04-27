from engine.bonus import Bonus
from engine import game_data
from engine.size import Size
import random


class BonusClock(Bonus):
    def __init__(self):
        super().__init__(
            random.randint(game_data.game_place_offset, game_data.map_width),
            random.randint(game_data.game_place_offset, game_data.map_height),
            Size(15, 16),
            "./textures/bonuses/clock.png", 0)

    def destroy(self, taken_player=False):
        if taken_player:
            for game_object in game_data.game_objects:
                if game_object.name == "Enemy":
                    game_object.is_frozen = True
        game_data.for_destroy[self.id] = self
        game_data.has_bonus = False
