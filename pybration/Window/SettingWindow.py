from pybration.Window.LineEdit import *
# from pybration.Window.DeviceWindow import *
from pybration.DataSturucture import DataContainer
from PyQt5.QtChart import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class ManageWorkDirecory(QWidget):
    def __init__(self):
        super(ManageWorkDirecory, self).__init__()
        layout = QVBoxLayout()

        change_dir_button = QPushButton("変更")

        layout.addWidget(QLabel("<b>作業ディレクトリ</b>"))
        layout.addWidget(change_dir_button)
        layout.addStretch()
        self.setLayout(layout)


class SettingWindow(QWidget):

    def __init__(self, parent, data:DataContainer):
        super(SettingWindow, self).__init__(parent=parent)
        self.setWindowTitle("設定")
        # self.device_manager = DeviceManagerWindow()
        # self.directory_manager = ManageWorkDirecory()

        main_layout = QHBoxLayout()
        #main_layout.addWidget(self.directory_manager)
        # main_layout.addWidget(self.device_manager)

        self.setLayout(main_layout)



