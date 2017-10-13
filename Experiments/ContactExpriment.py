#coding:utf-8
from PyQt5.QtChart import *
from Window.DeviceWindow import *
from Window.LineEdit import *
from Tools.record import *
from PyQt5.QtWidgets import *
from SignalProcessing.fft import *
import numpy as np
import pandas as pd


class ContactForceRecord(RecordWindow):
    data_cnt = 0
    contact_force_view = None
    force_values = None

    def __init__(self, parent=None, device=None):
        super(ContactForceRecord, self).__init__(parent, device)

    def set_force(self, force):
        self.contact_force_view = force

    def start_record(self):
        if self.size_checkbox.isChecked():
            size = self.size_line.get_value()
            self.force_values = np.empty((size, 3), float)
        else:
            self.force_values = np.empty((0, 3), float)
        super(ContactForceRecord, self).start_record()

    def rec_update(self):
        z, x, y = self.contact_force_view.get_force()
        z = round(z, 3)
        x = round(x, 3)
        y = round(y, 3)
        force = np.array([z, x, y])
        if self.size_checkbox.isChecked():
            if self.size_line.get_value() <= self.data_cnt:
                self.stop_record()
                return
            self.force_values[self.data_cnt] = force
        else:
            force = np.array([[z, x, y]])
            self.wave_data = np.append(self.force_values, force, axis=0)
        super(ContactForceRecord, self).rec_update()

    def get_force(self):
        return self.contact_force_view.get_force()

    def write_csv(self):
        super(ContactForceRecord, self).write_csv()
        force_file_name = self.file_name_line.get_value()
        self.force_values = pd.DataFrame(self.force_values)
        self.force_values.to_csv(force_file_name + '_force.csv')

