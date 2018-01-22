# coding:utf-8
import os
import sys
import json
from yapsy.PluginManager import PluginManager
from pybration.Window.DeviceWindow import *
from pybration.DataSturucture import *
import datetime
import time


class MainWindow(QWidget):
    face_data = ["（｀･ω･´）", "（｀･ω･´）", "（&nbsp;&nbsp;&nbsp;&nbsp;｀･ω）",
                 "（&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;｀･）",
                 "（&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;）",
                 "（･`&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;）",
                 "（ω･`&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;）", "（&nbsp;´･ω･`&nbsp;）"]  # 前を向いてる顔になった時に時刻表示

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.data = DataContainer()
        self.check_json()
        for p in self.data.parameter['System']['plugin_folder']:
            sys.path.append(p)
        self.manager = PluginManager()
        plugin_dir = [os.path.join(os.path.dirname(__file__), "Plugins")]
        plugin_dir.extend(self.data.parameter['System']['plugin_folder'])
        self.manager.setPluginPlaces(plugin_dir)
        self.manager.collectPlugins()
        self.setWindowTitle("Pybration")
        self.face = QLabel()
        self.setting_manager = DeviceManagerWindow(parent=parent, data=self.data)
        # self.face.setFrameStyle( QFrame.Panel | QFrame.Sunken ) # 枠表示
        self.face.setFixedHeight(20)  # 高さ固定
        self.face.setText(self.face_data[0])
        self.device_manager_button = QPushButton("設定")
        self.device_manager_button.clicked.connect(self.setting_manager.show)

        self.plugin_button = []
        self.plugin_start_func = []

        for i, plugin in enumerate(self.manager.getAllPlugins()):
            print("LOAD_PLUGIN:" + str(plugin.name))
            if not self.data.parameter['Plugins'].get(plugin.name):
                self.data.parameter['Plugins'][str(plugin.name)] = {}

            plugin.plugin_object.set_parent_data(self.data)
            if plugin.plugin_object.enable_button():
                button = QPushButton(str(plugin.name))
                button.clicked.connect(plugin.plugin_object.clicked)
                self.plugin_button.append(button)
            else:
                plugin.plugin_object.run()

        self.date = QLabel()
        # self.date.setFrameStyle( QFrame.Panel | QFrame.Sunken ) # 枠表示
        self.date.setFixedHeight(20)  # 高さ固定
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
        layout.addWidget(self.device_manager_button)
        for i in range(len(self.plugin_button)):
            layout.addWidget(self.plugin_button[i])
        layout.addWidget(self.date)
        self.setLayout(layout)

    def check_json(self):
        try:
            print("LOAD_PARAMETER:"+os.environ['HOME']+"/.pybration/param.json")
            param = open(os.environ['HOME']+"/.pybration/param.json", 'r')
        except IOError:
            print("LOAD_PARAMETER:default")
            param = open("./default.json", 'r')
        self.data.parameter = json.load(param)

        if not self.data.parameter['System'].get('setting_folder'):
            self.data.parameter['System']['setting_folder'] = os.environ['HOME']+"/.pybration/"

        if not self.data.parameter['System'].get('plugin_folder'):
            self.data.parameter['System']['plugin_folder'] = []

        if not self.data.parameter['System'].get('work_folder'):
            self.data.parameter['System']['work_folder'] = ""

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
        d = datetime.datetime.today()
        day_time_str = d.strftime("%Y-%m-%d %H:%M:%S")
        self.date.setText('<div>'
                          + day_time_str
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
    myApp.exec_()
    sys.exit(0)


if __name__ == "__main__":
    main()
