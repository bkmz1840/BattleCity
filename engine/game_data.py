# objects
game_objects = []
for_destroy = {}
id = 0
count_enemies = 40
count_enemies_in_game = 0
enemy_behavior = 1
player = None
base = None

# map
map_height = 0
map_width = 0
game_place_offset = 25
game_end = False

# keys
pressed_key = None
is_space_pressed = False

# timings
tick_count = 0
fire_delay = 120
duration_bonus = 750
duration_freeze_time = 600
player_respawn_time = 200

# bonuses
has_bonus = False


def refresh_game_data():
    global game_objects, for_destroy, id,\
        count_enemies_in_game, enemy_behavior, game_end,\
        pressed_key, is_space_pressed, tick_count, has_bonus,\
        player, base
    game_objects = []
    for_destroy = {}
    id = 0
    count_enemies_in_game = 0
    enemy_behavior = 1
    game_end = False
    pressed_key = None
    is_space_pressed = False
    tick_count = 0
    has_bonus = False
    player = None
    base = None
