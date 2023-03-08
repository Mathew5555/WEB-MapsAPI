import sys
from io import BytesIO
import requests
from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap, QImage, QKeyEvent
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QMainWindow
from PyQt5 import uic
from PyQt5.Qt import *
import geocoder

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
        self.delta = 0.001
        self.pt = 0
        self.refresh_map()

    def refresh_map(self):
        map_params = {
            "ll": f"{self.map_ll[0]},{self.map_ll[1]}",
            "l": self.map_l,
            "z": self.map_zoom,
            "size": "600,450"
        }
        if self.pt:
            map_params["pt"] = self.pt
        response = requests.get("http://static-maps.yandex.ru/1.x/", params=map_params)
        self.image.setPixmap(QPixmap.fromImage(QImage.fromData(response.content)))

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_PageUp and self.map_zoom < 18:
            self.map_zoom += 1
        elif key == Qt.Key_PageDown and self.map_zoom > 0:
            self.map_zoom -= 1
        elif key == Qt.Key_Left and self.map_ll[0] > -180:
            self.map_ll[0] -= (self.delta * (18 - self.map_zoom) ** 2)
        elif key == Qt.Key_Right and self.map_ll[0] < 180:
            self.map_ll[0] += (self.delta * (18 - self.map_zoom) ** 2)
        elif key == Qt.Key_Up and self.map_ll[0] < 90:
            self.map_ll[1] += (self.delta * (18 - self.map_zoom) ** 2)
        elif key == Qt.Key_Down and self.map_ll[0] > -90:
            self.map_ll[1] -= (self.delta * (18 - self.map_zoom) ** 2)
        self.refresh_map()

    def change_map(self):
        self.pushButton.setStyleSheet("#pushButton" + self.style_button[0] + "#pushButton" + self.style_button[1])
        self.pushButton_1.setStyleSheet("#pushButton_1" + self.style_button[0] + "#pushButton_1" + self.style_button[1])
        self.pushButton_2.setStyleSheet("#pushButton_2" + self.style_button[0] + "#pushButton_2" + self.style_button[1])
        if self.sender().text() == "Схема":
            self.pushButton.setStyleSheet(self.style_button[2])
            self.map_l = "map"
        elif self.sender().text() == "Спутник":
            self.pushButton_1.setStyleSheet(self.style_button[2])
            self.map_l = "sat"
        else:
            self.pushButton_2.setStyleSheet(self.style_button[2])
            self.map_l = "sat,skl"
        self.setFocus()
        self.refresh_map()

    def find_place(self):
        self.setFocus()
        toponym_to_find = self.find_Edit.text()
        if toponym_to_find:
            self.map_ll = list(geocoder.get_coordinates(toponym_to_find))
            # ll, spn = geocoder.get_ll_span(toponym_to_find)
            self.map_zoom = 16
            self.pt = f"{self.map_ll[0]},{self.map_ll[1]},pm2rdm"
            self.refresh_map()

    def func_reset(self):
        self.find_Edit.setText("")
        self.setFocus()
        self.pt = ""
        self.refresh_map()

    def initUI(self):
        self.pushButton.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.pushButton_1.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.pushButton_2.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.findButton.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.reset.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.find_Edit.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.style_button = [''' {background-color: rgb(199, 199, 199);
                                  font: 12pt "MS Shell Dlg 2";
                                  border-radius: 10px;
                                  border: 2px solid blue;
                                  color: blue;}''', ''':hover {background-color: rgb(0, 255, 0);}''',
                             '''background-color: rgb(0, 255, 0);
                             font: 12pt "MS Shell Dlg 2";
                             border-radius: 10px;
                             border: 2px solid blue;
                             color: blue;''']
        self.pushButton.setStyleSheet(self.style_button[2])
        self.pushButton.clicked.connect(self.change_map)
        self.pushButton_1.clicked.connect(self.change_map)
        self.pushButton_2.clicked.connect(self.change_map)
        self.findButton.clicked.connect(self.find_place)
        self.reset.clicked.connect(self.func_reset)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Map()
    ex.show()
    sys.exit(app.exec())
