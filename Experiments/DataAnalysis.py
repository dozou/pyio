from Window.DeviceWindow import *
from Window.LineEdit import *
from Experiments.DataAnalysis import *
import pandas as pd


class DataAnalysis(QWidget):

    def __init__(self):
        super(DataAnalysis, self).__init__()

        read_button = QPushButton("読み出し")

        main_layout = QHBoxLayout()
        main_layout.addWidget(QLabel("test"))

        self.setLayout(main_layout)

    def set_data(self):
        print("")

