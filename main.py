import sys
from io import BytesIO

import requests

from PyQt5.QtGui import QPixmap, QImage, QKeyEvent
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QMainWindow
from PyQt5 import uic
from PyQt5.Qt import *

SCREEN_SIZE = [600, 450]


class Map(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui_file.ui", self)
        self.setWindowTitle('Отображение карты')
        self.initUI()

        self.map_zoom = 5
        self.map_ll = [37.9777751, 55.757718]
        self.map_l = "map"
        self.refresh_map()

    def refresh_map(self):
        map_params = {
            "ll": f"{self.map_ll[0]},{self.map_ll[1]}",
            "l": self.map_l,
            "z": self.map_zoom,
            "size": "600,450"
        }
        response = requests.get("http://static-maps.yandex.ru/1.x/", params=map_params)
        self.image.setPixmap(QPixmap.fromImage(QImage.fromData(response.content)))

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_PageUp and self.map_zoom < 18:
            self.map_zoom += 1
        elif key == Qt.Key_PageDown and self.map_zoom > 0:
            self.map_zoom -= 1
        self.refresh_map()

    def initUI(self):
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(600, 450)
        layout = QVBoxLayout()
        layout.addWidget(self.image, alignment=Qt.AlignCenter)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Map()
    ex.show()
    sys.exit(app.exec())
