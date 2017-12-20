# coding:utf-8
import sys
import os
from yapsy.PluginManager import PluginManager
from yapsy.PluginInfo import PluginInfo
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import datetime


class MainWindow(QWidget):
    face_data = ["（｀･ω･´）", "（&nbsp;&nbsp;&nbsp;&nbsp;｀･ω）", "（&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;｀･）",
                 "（&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;）",
                 "（･`&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;）",
                 "（ω･`&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;）", "（&nbsp;´･ω･`&nbsp;）"]  # 後ろがおになった時に時刻表示

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        manager = PluginManager()

        manager.setPluginPlaces([os.path.join(os.path.dirname(__file__), "Plugins")])
        manager.collectPlugins()
        print(os.path.dirname(__file__))
        print(str(len(manager.getAllPlugins())))
        self.setWindowTitle("Pybration")
        self.face = QLabel()
        # self.face.setFrameStyle( QFrame.Panel | QFrame.Sunken ) # 枠表示
        self.face.setFixedHeight(20)  # 高さ固定
        self.face.setText(self.face_data[0])
        self.device_maneger_button = QPushButton("設定")
        self.plugin_button = []
        for plugin in manager.getAllPlugins():
            self.plugin_button.append(QPushButton(str(plugin.name)))
        self.date = QLabel()
        # self.date.setFrameStyle( QFrame.Panel | QFrame.Sunken ) # 枠表示
        self.date.setFixedHeight(20)  # 高さ固定
        self.update_layout()

        self.timer = QTimer()
        self.timer.setInterval(200)
        self.timer.timeout.connect(self.timeout)
        self.timer.start()
        self.face_rote = 0

    def update_layout(self):
        layout = QVBoxLayout()
        layout.addWidget(self.face)
        layout.addWidget(self.device_maneger_button)
        for i in range(len(self.plugin_button)):
            layout.addWidget(self.plugin_button[i])
        layout.addWidget(self.date)
        self.setLayout(layout)

    """
        ショボーンを回転させるためのメソッドです
        200[msec]間隔で更新しています
    """

    def timeout(self):
        if len(self.face_data) == self.face_rote:
            self.face_rote = 0
        self.face.setText('<div align="center">'  # Qtスバラ！！HTML指定できるんすよ！！
                          + self.face_data[self.face_rote]
                          + '</div>'
                          )

        if self.face_rote == 0:
            self.time_draw()

        self.face_rote += 1

    """
    時刻表示のためのメソッド
    """

    def time_draw(self):
        d = datetime.datetime.today()
        # daystr = d.strftime("%Y-%m-%d %H:%M:%S")
        daystr = d.strftime("%Y-%m-%d %H:%M")
        self.date.setText('<div>'
                          + daystr
                          + '</div>'
                         )

if __name__ == "__main__":
    myApp = QApplication(sys.argv)
    myWindow = MainWindow()
    myWindow.show()
    myApp.exec_()
    sys.exit(0)
