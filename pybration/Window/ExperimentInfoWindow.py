# -*- coding: utf-8 -*-
from pybration.DataSturucture import DataContainer
from pybration.Window.LineEdit import LabelOnLineEdit, LabelOnSpinBox
from PyQt5.QtWidgets import QLabel, QWidget, QVBoxLayout


class ExperimentInfoWindow(QWidget):
    def __init__(self, data: DataContainer):
        super().__init__()
        self.my_param = data.parameter["Plugins"]["Experiment"]  # type: dict

        if not self.my_param.get('experiment_id'):
            self.my_param["experiment_id"] = 0
        self.title = QLabel("<h3>実験情報</h3>")
        self.experiment_id = LabelOnSpinBox(label="EID",
                                            val=self.my_param["experiment_id"])
        self.subject_name = LabelOnLineEdit(label="Name",
                                            text="")
        self.add_infos = list()

    def update_layout(self):
        layout = QVBoxLayout()
        layout.addWidget(self.title)
        layout.addWidget(self.experiment_id)
        layout.addWidget(self.subject_name)
        layout.addWidget(self.samples_line)
        for i in self.add_infos:
            layout.addWidget(i)
        layout.addStretch()
        self.setLayout(layout)
