# -*- coding: utf-8 -*-
from pybration.DataSturucture import DataContainer
from pybration.Window.LineEdit import LabelOnLineEdit, LabelOnSpinBox
from PyQt5.QtWidgets import QLabel, QWidget, QVBoxLayout, QPushButton


class ExperimentInfoWindow(QWidget):
    def __init__(self, data: DataContainer, parent=None):
        super().__init__(parent=parent)
        if not data.parameter["Plugins"].get("Experiment"):
            data.parameter["Plugins"]["Experiment"] = {}
        self.my_param = data.parameter["Plugins"]["Experiment"]  # type: dict
        self.data = data

        if not self.my_param.get('experiment_id'):
            self.my_param["experiment_id"] = 0
        self.title = QLabel("<h3>実験情報</h3>")
        self.experiment_id = LabelOnSpinBox(label="EID",
                                            val=self.my_param["experiment_id"])
        self.experiment_id.LineEdit.valueChanged.connect(self.update_info)
        self.subject_name = LabelOnLineEdit(label="Name",
                                            text="")
        self.subject_name.LineEdit.textChanged.connect(self.update_info)
        self.success_button = QPushButton("Success")
        self.add_info = list()
        self.layout_v_box = QVBoxLayout(self)  # type: QVBoxLayout
        self.update_info()

    def update_layout(self):
        self.layout_v_box.addWidget(self.title)
        self.layout_v_box.addWidget(self.experiment_id)
        self.layout_v_box.addWidget(self.subject_name)
        for i, obj in enumerate(self.add_info):
            self.layout_v_box.addWidget(self.add_info[i])
        self.layout_v_box.addWidget(self.success_button)
        self.layout_v_box.addStretch()
        self.setLayout(self.layout_v_box)

    def update_info(self):
        if not self.data.parameter.get("ExperimentInfo"):
            self.data.parameter['ExperimentInfo'] = {}
        exp_data = self.data.parameter['ExperimentInfo']
        exp_data['experiment_id'] = self.experiment_id.get_value()
        exp_data['subject_name'] = self.subject_name.get_value()
