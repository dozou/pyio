# -*- coding: utf-8 -*-
from pybration.DataSturucture import DataContainer
from PyQt5.QtWidgets import QGroupBox, QVBoxLayout,QWidget
from PyQt5.Qt import Qt


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

    def __init__(self, parent, data: DataContainer, window):
        super(SettingWindow, self).__init__(parent=parent)
        self.setWindowTitle("設定")
        self.setContentsMargins(10,10,10,10)
        # self.device_manager = DeviceManagerWindow()

        main_layout = QVBoxLayout()
        # self.setWindowFlags(Qt.Window)

        for i in window:  # type:QGroupBox
            # i.setWindowFlags(Qt.MSWindowsFixedSizeDialogHint)
            main_layout.addWidget(i)

        main_layout.addStretch()
        self.setLayout(main_layout)



