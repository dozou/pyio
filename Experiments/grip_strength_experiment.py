from Window.DeviceWindow import *
from Window.LineEdit import *
from Experiments.DataAnalysis import *
from Tools.record import *
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import GridSearchCV
from SignalProcessing.fft import *
from SignalProcessing.move_mean import *
from Experiments.gui_grip_strength import *
from TweModule.TweLiteBasic import *


class TweDevices(TweLiteBasic):
    def __init__(self, record_device=None):
        super(TweDevices, self).__init__("/dev/tty.usbserial-MWHCYFV")

    def get_grip_force(self):
        volt = self.device_io.vin / 1000.0
        vout = self.device_io.ai[0] / 1000.0
        if volt - vout == 0:
            return 0
        r2 = (2960 * vout) / (volt - vout)
        grip_force = (r2 - 196) / 163.8
        return grip_force


class MachineLearningControlLayout(QWidget):
    calc_button = None
    estimate_button = None

    def __init__(self):
        super(MachineLearningControlLayout, self).__init__()
        layout = QVBoxLayout()

        self.pre_process_button = QPushButton("前処理")
        self.calc_button = QPushButton("演算開始")
        self.estimate_button = QPushButton("推定開始")
        self.viewer_button = QPushButton("表示")
        self.estimate_onoff_check = QCheckBox("log更新停止")
        self.estimate_onoff_check.setChecked(True)

        layout.addWidget(QLabel("<b>操作</b>"))
        layout.addWidget(self.pre_process_button)
        layout.addWidget(self.calc_button)
        layout.addWidget(self.estimate_button)
        layout.addWidget(self.viewer_button)
        layout.addWidget(self.estimate_onoff_check)
        layout.addStretch()

        self.setLayout(layout)


class GripStrengthRecord(RecordWindow):
    def __init__(self, record_device, twe_device: TweDevices):
        super(GripStrengthRecord, self).__init__(device=record_device)
        self.twe_device = twe_device
        self.force_values = None
        #self.twe_device.start()

    def start_record(self):
        if self.size_checkbox.isChecked():
            size = self.size_line.get_value()
            self.force_values = np.empty((size, 1), float)
        else:
            self.force_values = np.empty((0, 1), float)
        super(GripStrengthRecord, self).start_record()

    def stop_record(self):
        super(GripStrengthRecord, self).stop_record()

    def rec_update(self):
        vout = self.twe_device.device_io.ai[0] / 1000.0
        volt = self.twe_device.device_io.vin / 1000.0
        r2 = (2960 * vout) / (volt - vout)
        grip_force = (r2 - 196) / 163.8 * 9.8

        if self.size_checkbox.isChecked():
            if self.size_line.get_value() <= self.data_cnt:
                self.stop_record()
                return
            self.force_values[self.data_cnt] = grip_force
        else:
            self.wave_data = np.append(self.force_values, grip_force, axis=0)

        super(GripStrengthRecord, self).rec_update()
        # print("Voltage %d Grip = %d" % (self.twe_device.device_io.vin, r2))

    def write_csv(self):
        super(GripStrengthRecord, self).write_csv()
        force_file_name = self.file_name_line.get_value()
        self.force_values = pd.DataFrame(self.force_values)
        self.force_values.to_csv(force_file_name + '_force.csv')


class GripStrengthForEnsemble(QWidget):
    def __init__(self, parent=0, device=None):
        super(GripStrengthForEnsemble, self).__init__(parent=parent)
        self.twe_device = TweDevices(record_device=device)
        self.twe_device.start()
        self.record_window = GripStrengthRecord(record_device=device, twe_device=self.twe_device)
        self.ai_device = device
        self.viewer = GripStrengthViewer()
        self.control_panel = MachineLearningControlLayout()
        self.control_panel.pre_process_button.clicked.connect(self.pre_process)
        self.control_panel.calc_button.clicked.connect(self.train_learn)
        self.control_panel.estimate_button.clicked.connect(self.start_estimate)
        self.control_panel.viewer_button.clicked.connect(self.viewer.show)
        self.console_window = QTextBrowser()
        self.console_window.setReadOnly(True)
        scroll_bar = self.console_window.verticalScrollBar()
        scroll_bar.setValue(scroll_bar.maximum())
        layout = QHBoxLayout()
        layout.addWidget(self.record_window)
        layout.addWidget(self.control_panel)
        layout.addWidget(self.console_window)
        # layout.addWidget(viewer)
        self.setLayout(layout)

        self.update_timer = QTimer()
        self.control_panel.estimate_button.setEnabled(False)
        self.control_panel.calc_button.setEnabled(False)
        self.train_data = None
        self.estimator = None
        self.result_filter = MoveMean(3)
        self.handle_output("Initialization program....<br>")

    def pre_process(self):
        self.handle_output("Start Preprocess<br>")
        self.control_panel.calc_button.setEnabled(True)
        self.train_data = to_fft2d(self.record_window.wave_data)
        self.train_data = to_psd2d(self.train_data)
        self.train_data = self.train_data[:, 1000//20:3000//20]
        self.handle_output("Compleate Preprocess<br>")

    def train_learn(self):
        self.control_panel.estimate_button.setEnabled(True)
        self.handle_output("Start Calc<br>")
        tuned_parameters = [
            {'n_estimators': [200, 300, 400], 'max_features': [10, 15, 20]}
        ]
        clf = GridSearchCV(
            GradientBoostingRegressor(),  # 識別器
            tuned_parameters,  # 最適化したいパラメータセット
            cv=5,  # 交差検定の回数
            scoring='r2',
            n_jobs=-1,
            verbose=10
        )
        clf.fit(self.train_data, self.record_window.force_values.ravel())
        self.estimator = clf.best_estimator_
        self.handle_output("ChoieParameter:%s <br>" % self.estimator)
        self.handle_output("Finish Calc<br>")

    def start_estimate(self):
        self.control_panel.estimate_button.setText("推定停止")
        self.control_panel.estimate_button.disconnect()
        self.control_panel.estimate_button.clicked.connect(self.stop_estimate)
        self.update_timer = QTimer()
        self.update_timer.setInterval(0)
        self.update_timer.timeout.connect(self.estimate)
        self.update_timer.start()
        self.handle_output("EstimateValue:  Error<br>")

    def stop_estimate(self):
        self.update_timer.stop()
        self.control_panel.calc_button.setEnabled(True)
        self.control_panel.estimate_button.setText("推定開始")
        self.control_panel.estimate_button.disconnect()
        self.control_panel.estimate_button.clicked.connect(self.start_estimate)
        self.handle_output("Stop <br>")

    def estimate(self):
        wave_data = self.ai_device.getAI()
        truth_force = self.twe_device.get_grip_force()
        train_data = to_fft(wave_data)
        train_data = to_psd(train_data)
        train_data = train_data[1000//20:3000//20]
        estimate_value = self.estimator.predict(train_data.reshape(1,-1))
        self.viewer.set_grip_force(self.result_filter.push(estimate_value), truth_force)
        if not self.control_panel.estimate_onoff_check.isChecked():
            self.handle_output("%2f,     %2f<br>" % (estimate_value, estimate_value - truth_force))

    def handle_output(self, text):
        self.console_window.moveCursor(QtGui.QTextCursor.End)
        self.console_window.ensureCursorVisible()
        self.console_window.insertHtml(text)
