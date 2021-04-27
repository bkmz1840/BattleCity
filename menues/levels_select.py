from PyQt5.QtWidgets import QWidget, QPushButton
from os import listdir, path
from menues.game_place import GamePlace
from menues import main_menu
from engine.vector import Vector


class LevelsSelect(QWidget):
    def __init__(self):
        super(LevelsSelect, self).__init__()
        self.maps = {}
        self.count_maps = 0
        self.game_place = None
        self.main_menu = None
        self.upload_maps()
        self.move(0, 0)
        self.resize(300, self.count_maps * 50 + 50)
        self.setStyleSheet("background-color: #000;")
        self.setWindowTitle("Maps")
        self.init_bttns_maps()

    def upload_maps(self):
        path_to_maps = "./maps"
        maps_names = [f
                      for f in listdir(path_to_maps)
                      if path.isfile(path.join(path_to_maps, f))]
        self.count_maps = len(maps_names)
        for map_name in maps_names:
            name = map_name[:map_name.find(".txt")]
            self.maps[name] = path_to_maps + "/" + map_name

    def init_bttns_maps(self):
        start_pos = Vector(25, 25)
        bttn_style_sheet = '''
            QPushButton {
                color: white;
                font-size: 30px;
                border: 1px solid white;
            }
            QPushButton:hover {
                color: black;
                background-color: #fff;
            }
        '''
        for map_name in self.maps:
            bttn = QPushButton(map_name.replace("_", " "), self)
            bttn.setGeometry(start_pos.x, start_pos.y, 250, 40)
            bttn.setStyleSheet(bttn_style_sheet)
            bttn.clicked.connect(self.bttn_map_pushed)
            start_pos.y += 50
        bttn_back = QPushButton("Back", self)
        bttn_back.setGeometry(300 - 75, start_pos.y, 70, 20)
        bttn_back_style_sheet = '''
            QPushButton {
                color: white;
                border: 1px solid white;
            }
            QPushButton:hover {
                color: black;
                background-color: #fff;
            }
        '''
        bttn_back.setStyleSheet(bttn_back_style_sheet)
        bttn_back.clicked.connect(self.bttn_back_pushed)

    def bttn_map_pushed(self):
        bttn_text = self.sender().text().replace(" ", "_")
        path_to_map = self.maps[bttn_text]
        self.close()
        self.game_place = GamePlace(path_to_map)
        self.game_place.show()

    def bttn_back_pushed(self):
        self.close()
        self.main_menu = main_menu.MainMenu()
        self.main_menu.show()
