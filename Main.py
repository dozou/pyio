#coding:utf-8
import sys
import os
from yapsy.PluginManager import PluginManager
from yapsy.PluginInfo import PluginInfo
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        manager = PluginManager()

        manager.setPluginPlaces([os.path.join(os.path.dirname(__file__), "Plugins")])
        manager.collectPlugins()
        print(os.path.dirname(__file__))
        print(str(len(manager.getAllPlugins())))
        face_data = ["(｀･ω･´)", "( ｀･ω)", "( 　｀･)", "(　　　　)", "(･`　 )", "(ω･` )", "(´･ω･`)"]  # 後ろがおになった時に時刻表示
        self.setWindowTitle("Pybration")
        self.face = QLabel()
        self.face.setText(face_data[0])
        self.device_maneger_button = QPushButton("設定")
        self.plugin_button = []
        for plugin in manager.getAllPlugins():
            self.plugin_button.append(QPushButton(str(plugin.name)))
        self.update_layout()

    def update_layout(self):
        layout = QVBoxLayout()
        layout.addWidget(self.face)
        layout.addWidget(self.device_maneger_button)
        for i in range(len(self.plugin_button)):
            layout.addWidget(self.plugin_button[i])

        self.setLayout(layout)


if __name__ == "__main__":
    myApp = QApplication(sys.argv)
    myWindow = MainWindow()
    myWindow.show()
    myApp.exec_()
    sys.exit(0)
