# coding:utf-8
import os
import sys
import json
import time
import datetime
from PyQt5.QtWidgets import QWidget, QApplication, QLabel
from PyQt5.QtWidgets import QPushButton, QVBoxLayout
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QTimer
from PyQt5.Qt import Qt
from yapsy.PluginManager import PluginManager
from pybration.Util import System
from pybration.DataSturucture import DataContainer
from pybration.Tools.Json import get_default_param
from pybration.Window.SettingWindow import SettingWindow


class MainWindow(QWidget):
    face_data = ["（｀･ω･´）", "（｀･ω･´）", "（&nbsp;&nbsp;&nbsp;&nbsp;｀･ω）",
                 "（&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;｀･）",
                 "（&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;）",
                 "（･`&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;）",
                 "（ω･`&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;）", "（&nbsp;´･ω･`&nbsp;）"]  # 前を向いてる顔になった時に時刻表示

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        # self.data = DataContainer()
        self.setWindowFlags(Qt.Dialog)
        self.system = System()
        self.data = self.system.load_param()

        self.setWindowTitle("Pybration")
        self.face = QLabel()

        self.face.setFixedHeight(20)  # 高さ固定
        self.face.setText(self.face_data[0])

        """
        プラグインの初期化
        """
        self.plugin_manager = PluginManager()
        plugin_dir = [os.path.join(os.path.dirname(__file__), "Plugins")]
        plugin_dir.extend(self.data.parameter['System']['plugin_folder'])
        self.plugin_manager.setPluginPlaces(self.system.check_dir_str(plugin_dir))
        self.plugin_manager.collectPlugins()

        self.plugin_button = []
        self.plugin_start_func = []
        self.external_setting_windows = []

        """プラグインの呼び込み順番を修正"""
        plugins = []
        for i in self.plugin_manager.getAllPlugins():
            plugins.append((i.name, i))
        plugins = sorted(plugins)
        plugins = [i[1] for i in plugins]

        for i, plugin in enumerate(plugins):
            print("LOAD_PLUGIN(v" + str(plugin.version) + "): " + str(plugin.name))
            if not self.data.parameter['Plugins'].get(plugin.name):
                self.data.parameter['Plugins'][str(plugin.name)] = {}

            """プラグインの初期化"""
            plugin.plugin_object.init(self.data)

            """プラグインボタンの表示設定"""
            if plugin.plugin_object.enable_button():
                button = QPushButton(str(plugin.name))
                button.clicked.connect(plugin.plugin_object.clicked)
                self.plugin_button.append(button)

            """プラグイン設定項目の追加"""
            if plugin.plugin_object.enable_setting_window():
                self.external_setting_windows.append(plugin.plugin_object.get_setting_window())

        """
        設定ウィンドウの初期化
        """
        self.setting_manager = SettingWindow(parent=self.parent(),
                                             data=self.data,
                                             window=self.external_setting_windows)
        self.setting_manager_button = QPushButton("設定")
        self.setting_manager_button.clicked.connect(self.setting_manager.show)

        self.date = QLabel()
        # self.date.setFrameStyle( QFrame.Panel | Qt.QFrame.Sunken ) # 枠表示
        self.date.setFixedHeight(20 * 2)  # 高さ固定
        self.update_layout()

        # self.wait_0_microsecond()

        self.timer = QTimer()
        self.timer.setInterval(125)
        self.timer.timeout.connect(self.timeout)
        self.timer.start()
        self.face_rote = 0

    def update_layout(self):
        layout = QVBoxLayout()
        layout.addWidget(self.face)
        layout.addWidget(self.setting_manager_button)
        for i in range(len(self.plugin_button)):
            layout.addWidget(self.plugin_button[i])
        layout.addWidget(self.date)
        self.setLayout(layout)

    """
        ショボーンを回転させるためのメソッドです
        125[msec]間隔で更新しています
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
        # d = datetime.datetime.today()
        d = datetime.datetime.now()
        day_time_str = d.strftime("%Y-%m-%d %H:%M:%S")
        self.date.setText('<div>'
                          + '<center>'
                          + day_time_str
                          + '</center>'
                          + '</div>'
                          )

    """
    時刻表示のタイミングを(無理やり)合わせるためのメソッド
    """

    def wait_0_microsecond(self):
        print("Adjust the time... Please Waiting...")
        wait_s = 0.0000001
        wait_count = 0
        while True:
            d = datetime.datetime.today()
            if d.microsecond == 0.0:
                print("wait : " + str(wait_count))
                break

            time.sleep(wait_s)
            wait_count += 1

    def closeEvent(self, a0):
        for dev in self.data.device:
            if dev.is_open():
                dev.close_device()
        if not os.path.exists(os.environ['HOME']+"/.pybration"):
            os.mkdir(os.environ['HOME']+"/.pybration")
        fw = open(os.environ['HOME']+"/.pybration/param.json", 'w')
        json.dump(self.data.parameter, fw, indent=4)
        quit()


def main():
    myApp = QApplication(sys.argv)
    myWindow = MainWindow()
    myWindow.show()
    return myApp.exec()


if __name__ == "__main__":
    main()
