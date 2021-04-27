from PyQt5.QtWidgets import QWidget, QPushButton, QLabel
from PyQt5.QtGui import QPixmap
from menues.levels_select import LevelsSelect


class MainMenu(QWidget):
    def __init__(self):
        super(MainMenu, self).__init__()
        self.setGeometry(0, 0, 700, 500)
        self.setWindowTitle("Battle City")
        self.setStyleSheet("background-color: black;")
        self.level_select = None
        self.init_UI()

    def add_logo(self):
        logo = QPixmap("./textures/battle-city.jpg")
        logo_box = QLabel(self)
        logo_box.setPixmap(logo)
        logo_box.setGeometry(50, 0, 600, 300)

    def init_UI(self):
        self.add_logo()
        bttn_play = QPushButton("Play", self)
        bttn_play.setGeometry(225, 300, 250, 40)
        bttn_play_style_sheet = '''
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
        bttn_play.setStyleSheet(bttn_play_style_sheet)
        bttn_play.clicked.connect(self.click_bttn_play)
        bttn_quit = QPushButton("Quit", self)
        bttn_quit.setGeometry(315, 360, 70, 20)
        bttn_quit_style_sheet = '''
            QPushButton {
                color: white;
                border: 1px solid white;
            }
            QPushButton:hover {
                color: black;
                background-color: #fff;
            }
        '''
        bttn_quit.setStyleSheet(bttn_quit_style_sheet)
        bttn_quit.clicked.connect(self.close)

    def click_bttn_play(self):
        self.close()
        self.level_select = LevelsSelect()
        self.level_select.show()
