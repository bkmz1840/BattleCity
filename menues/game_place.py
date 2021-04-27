from PyQt5.QtWidgets import QWidget, QPushButton
from PyQt5.QtGui import QPaintEvent, QPainter, QBrush,\
    QColor, QKeyEvent, QPixmap
from PyQt5.QtCore import QTimer, Qt
from engine.direction import Direction
from engine.map_creator import MapCreator
from engine.vector import Vector
from engine.icon_enemy import IconEnemy
from engine import game_data
from animations.anim_spawn_enemy import AnimationSpawnEnemy
from animations.anim_winner import AnimationWinner
from bonuses import *
import random
from menues import levels_select


class GamePlace(QWidget):
    def __init__(self, path_to_map):
        game_data.refresh_game_data()
        super(GamePlace, self).__init__()
        self.move(0, 0)
        self.setWindowTitle("Battle City")
        self.setStyleSheet("background-color: #E1E1E1;")
        self.icons_enemies = []
        self.load_map(path_to_map)
        self.init_bttn_stop()
        self.resize(game_data.game_place_offset + 100 +
                    game_data.map_width,
                    game_data.game_place_offset * 2 +
                    game_data.map_height)
        self.key_pressed = set()
        self.tick_circles = 0
        random.seed()
        self.bonuses = [
            lambda: grenade.BonusGrenade(),
            lambda: clock.BonusClock()
        ]
        self.level_select = None
        self.winner_animation = None
        self.is_respawn_player = False
        self.spawn_player_ticks = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.timer_tick)
        self.timer.start()

    def load_map(self, path_to_map):
        map_creator = MapCreator()
        map_creator.create_map(path_to_map)
        pos = Vector(
            game_data.game_place_offset * 2 +
            game_data.map_width + 10,
            game_data.game_place_offset)
        for i in range(0, game_data.count_enemies):
            self.icons_enemies.append(
                IconEnemy(pos, QPixmap("./textures/icon_enemy.png")))
            pos = pos.copy()
            if i % 2 == 0:
                pos.x += 15
            else:
                pos.x -= 15
                pos.y += 15

    def init_bttn_stop(self):
        bttn_stop = QPushButton("Pause", self)
        bttn_stop.setGeometry(
            game_data.game_place_offset + 100 +
            game_data.map_width - 75,
            game_data.game_place_offset * 2 +
            game_data.map_height - 25,
            70, 20)
        bttn_stop_style_sheet = '''
                    QPushButton {
                        background-color: white;
                        color: black;
                        border: 1px solid black;
                    }
                    QPushButton:hover {
                        background-color: black;
                        color: white;
                    }
                '''
        bttn_stop.setStyleSheet(bttn_stop_style_sheet)
        bttn_stop.clicked.connect(self.bttn_stop_pushed)
        bttn_stop.setFocusPolicy(Qt.NoFocus)

    def get_position_for_enemy(self):
        available_x = set()
        for x in range(
                game_data.game_place_offset,
                game_data.map_width):
            available_x.add(x)
        skip_objects = {"Player", "Animation", "Bullet", "Grass"}
        for game_object in game_data.game_objects:
            if game_object.name in skip_objects:
                continue
            if game_data.game_place_offset \
                    <= game_object.position.y < 40:
                for x in range(
                        game_object.position.x,
                        game_object.position.x +
                        game_object.size.height):
                    if x not in available_x:
                        continue
                    available_x.remove(x)
        available_positions = []
        for x in available_x:
            available_positions.append(
                Vector(x, game_data.game_place_offset))
        if len(available_positions) == 0:
            return None
        random.seed()
        return available_positions[random.randint(
            0, len(available_positions) - 1)]

    def spawn_enemy(self):
        if self.tick_circles > 5 \
                and game_data.count_enemies_in_game < 8 \
                and len(self.icons_enemies) > 0:
            position_enemy = self.get_position_for_enemy()
            if position_enemy is not None:
                AnimationSpawnEnemy(
                    position_enemy, position_enemy.copy())
                self.icons_enemies.pop()
                self.tick_circles = 0

    def spawn_bonus(self):
        random_int = random.randint(1, 4096)
        if random_int == 11 and not game_data.has_bonus:
            self.bonuses[random.randint(0, len(self.bonuses) - 1)]()

    def draw_icons(self, painter):
        for icon in self.icons_enemies:
            painter.drawPixmap(icon.position.x, icon.position.y,
                               icon.pixmap)
        icon_life = QPixmap("./textures/icon_life.png")
        icon_count_player_lifes = {
            0: QPixmap("./textures/zero_life.png"),
            1: QPixmap("./textures/one_life.png"),
            2: QPixmap("./textures/two_lifes.png")
        }
        x = game_data.game_place_offset + game_data.map_width + 15
        y = game_data.game_place_offset * 2 \
            + game_data.count_enemies / 2 * 15 + 50
        painter.drawPixmap(x, y, icon_life)
        painter.drawPixmap(
            x + 45, y,
            icon_count_player_lifes[game_data.player.count_lifes])

    def respawn_player(self):
        if self.spawn_player_ticks >= game_data.player_respawn_time:
            game_data.game_objects.append(game_data.player)
            self.is_respawn_player = False
            self.spawn_player_ticks = 0
        else:
            self.spawn_player_ticks += 1

    def check_count_enemy_icons(self):
        if len(self.icons_enemies) == game_data.count_enemies - 10 \
                and game_data.player is not None:
            game_data.enemy_behavior = 2
        if len(self.icons_enemies) == game_data.count_enemies - 20 \
                and game_data.base is not None:
            game_data.enemy_behavior = 3
        if len(self.icons_enemies) == 0 \
                and game_data.count_enemies_in_game == 0 \
                and self.winner_animation is None:
            self.winner_animation = AnimationWinner()

    def paintEvent(self, event: QPaintEvent):
        if game_data.game_end:
            self.timer.stop()
            self.close_game_place()
        game_data.game_objects.sort(key=lambda game_obj:
                                    game_obj.drawing_priority)
        painter = QPainter()
        painter.begin(self)
        self.draw_icons(painter)
        self.check_count_enemy_icons()
        painter.setBrush(QBrush(QColor(0, 0, 0, 255)))
        painter.drawRect(game_data.game_place_offset,
                         game_data.game_place_offset,
                         game_data.map_width, game_data.map_height)
        for game_object in reversed(game_data.game_objects):
            if game_object.id in game_data.for_destroy:
                if game_object.name == "Player" \
                        and not game_object.is_dead:
                    self.is_respawn_player = True
                game_data.game_objects.remove(game_object)
                game_data.for_destroy.pop(game_object.id)
                continue
            game_object.update()
            game_object.draw(painter)
            self.spawn_enemy()
        if self.is_respawn_player:
            self.respawn_player()
        self.spawn_bonus()
        painter.end()

    def keyPressEvent(self, key: QKeyEvent):
        keys = {
            "w": Direction.Up,
            "ц": Direction.Up,
            "d": Direction.Right,
            "в": Direction.Right,
            "s": Direction.Down,
            "ы": Direction.Down,
            "a": Direction.Left,
            "ф": Direction.Left,
            "k": "space",
            "л": "space"
        }
        key_code = key.text()
        if key_code not in keys:
            return
        if key_code == "k" or key_code == "л":
            game_data.is_space_pressed = True
            return
        self.key_pressed.add(key_code)
        game_data.pressed_key = keys[key_code]

    def keyReleaseEvent(self, key: QKeyEvent):
        keys = {
            "w": Direction.Up,
            "ц": Direction.Up,
            "d": Direction.Right,
            "в": Direction.Right,
            "s": Direction.Down,
            "ы": Direction.Down,
            "a": Direction.Left,
            "ф": Direction.Left
        }
        key_code = key.text()
        if key_code in self.key_pressed:
            self.key_pressed.remove(key_code)
            if len(self.key_pressed) == 0:
                game_data.pressed_key = None
            else:
                game_data.pressed_key = keys[min(self.key_pressed)]

    def timer_tick(self):
        game_data.tick_count += 1
        if game_data.tick_count % 60 == 0:
            self.tick_circles += 1
        self.update()

    def bttn_stop_pushed(self):
        bttn = self.sender()
        text = bttn.text()
        if text == "Pause":
            self.timer.stop()
            bttn.setText("Continue")
        else:
            self.timer.start()
            bttn.setText("Pause")

    def close_game_place(self):
        self.close()
        self.level_select = levels_select.LevelsSelect()
        self.level_select.show()
