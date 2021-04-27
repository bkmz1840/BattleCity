from engine.animation import Animation
from engine import game_data
from engine.vector import Vector


class AnimationGameOver(Animation):
    def __init__(self):
        sprites = ["./textures/animations/game_over.png"]
        super().__init__(
            Vector((game_data.game_place_offset
                    + game_data.map_width) / 2 - 94,
                   game_data.game_place_offset + game_data.map_height - 114),
            sprites, -2, AnimationGameOver.upd)

    @staticmethod
    def upd(anim: Animation):
        if anim.position.y > (game_data.game_place_offset
                              + game_data.map_height) / 2 - 57:
            anim.position.y -= 2
        else:
            game_data.game_end = True
