from engine.animation import Animation
from engine import game_data
from engine.vector import Vector


class AnimationWinner(Animation):
    def __init__(self):
        sprites = ["./textures/animations/winner.png"]
        super().__init__(
            Vector((game_data.game_place_offset
                    + game_data.map_width) / 2 - 94,
                   game_data.game_place_offset + game_data.map_height - 40),
            sprites, -2, AnimationWinner.upd)

    @staticmethod
    def upd(anim: Animation):
        if anim.position.y > (game_data.game_place_offset
                              + game_data.map_height) / 2 - 20:
            anim.position.y -= 2
        else:
            game_data.game_end = True
