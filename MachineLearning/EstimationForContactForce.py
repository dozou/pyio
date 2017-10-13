from Window.DeviceWindow import *
from Window.LineEdit import *
from Tools.record import *
from ContactForceGui.app import *
from sklearn.ensemble import GradientBoostingRegressor


class EstimationForContactForce(FFTRecordWindow):
    svm_para_panel = None
    contact_force_view = None
    z_force_e = None
    x_force_e = None
    y_force_e = None
    estimate_update = None
    estimate_force = False
    reg_score = None
    ao_control = None
    ai_control = None
    force_data = pd.DataFrame()
    log_data_df = pd.DataFrame()
    log_data_sr = pd.Series()

    def __init__(self, parent=None):
        super(EstimationForContactForce, self).__init__(parent=parent)
        self.setWindowTitle("MachineLearning Manager")

        self.log_check_box = QCheckBox(text="推定値保存")
        self.calc_button = QPushButton("演算開始")
        self.start_estimate_button = QPushButton("推定開始")
        self.calc_button.clicked.connect(self.calc_svm)
        self.start_estimate_button.clicked.connect(self.start_estimate)

        self.ai_control = AiControlView()
        self.ao_control = AoControlView()

        self.z_reg_label = QLabel("")
        self.x_reg_label = QLabel("")
        self.y_reg_label = QLabel("")

        self.z_estimate_label = QLabel("")
        self.x_estimate_label = QLabel("")
        self.y_estimate_label = QLabel("")

        self.ml_panel = QVBoxLayout()
        self.ml_panel.addWidget(self.log_check_box)
        self.ml_panel.addWidget(self.calc_button)
        self.ml_panel.addWidget(self.start_estimate_button)
        self.ml_panel.addWidget(self.z_reg_label)
        self.ml_panel.addWidget(self.x_reg_label)
        self.ml_panel.addWidget(self.y_reg_label)
        self.ml_panel.addWidget(self.z_estimate_label)
        self.ml_panel.addWidget(self.x_estimate_label)
        self.ml_panel.addWidget(self.y_estimate_label)
        self.ml_panel.addStretch()

        self.main_layout.addWidget(self.ai_control)
        self.main_layout.addWidget(self.ao_control)
        self.main_layout.addLayout(self.ml_panel)
        self.setLayout(self.main_layout)

        self.start_estimate_button.setEnabled(False)
        self.calc_button.setEnabled(False)

    def set_device(self, device):
        self.fft_func.set_device(device)
        self.ao_control.set_device(device)
        self.ai_control.set_device(device)

    def set_force(self, force):
        self.contact_force_view = force

    def get_estimate_force(self):
        return (self.z_force_e,
                self.x_force_e,
                0,
                self.estimate_force)

    def record(self):
        fft = self.fft_func.get()
        fft_sr = pd.Series(fft)

        z, x, y = self.contact_force_view.get_force()
        z = round(z, 1)
        x = round(x, 1)
        y = round(y, 1)
        force_sr = pd.Series([z, x, y])

        self.fft_data = self.fft_data.append(fft_sr, ignore_index=True)
        self.force_data = self.force_data.append(force_sr, ignore_index=True)

    def calc_svm(self):
        self.fft_data_np = np.array(self.fft_data)
        self.force_z_np = np.array(self.force_data[0])
        self.force_x_np = np.array(self.force_data[1])
        self.force_y_np = np.array(self.force_data[2])

        C = int(self.svm_para_panel.get_c())
        gamma = self.svm_para_panel.get_gamma()

        self.ml_z = GradientBoostingRegressor()
        self.ml_z.fit(self.fft_data_np, self.force_z_np)
        self.ml_x = GradientBoostingRegressor()
        self.ml_x.fit(self.fft_data_np, self.force_x_np)
        self.ml_y = GradientBoostingRegressor()
        self.ml_y.fit(self.fft_data_np, self.force_y_np)

        self.calc_button.setText("再演算")

        self.z_reg_label.setText("Z_Score:" + str(round(self.ml_z.score(self.fft_data_np, self.force_z_np), 5)))
        self.x_reg_label.setText("X_Score:" + str(round(self.ml_x.score(self.fft_data_np, self.force_x_np), 5)))
        self.y_reg_label.setText("Y_Score:" + str(round(self.ml_y.score(self.fft_data_np, self.force_y_np), 5)))
        self.start_estimate_button.setEnabled(True)

    def stop_record(self):
        super(EstimationForContactForce, self).stop_record()
        self.calc_button.setEnabled(True)

    def start_estimate(self):
        self.record_button.setEnabled(False)
        self.estimate_update = QTimer()
        self.estimate_update.setInterval(50)
        self.estimate_update.timeout.connect(self.update_estimate)
        self.estimate_update.start()
        self.start_estimate_button.disconnect()
        self.start_estimate_button.setText("推定停止")
        self.start_estimate_button.clicked.connect(self.stop_estimate)

        if self.log_check_box.isChecked():
            self.log_data_df = pd.DataFrame(columns=['Estimate_Z',
                                                  'Estimate_X',
                                                  'Estimate_Y',
                                                  'True_Z',
                                                  'True_X',
                                                  'True_Y'])

    def update_estimate(self):
        fft_data = self.fft_func.get()
        fft_data = np.array(fft_data)
        self.z_force_e = self.ml_z.predict(fft_data.reshape(1, -1))
        self.x_force_e = self.ml_x.predict(fft_data.reshape(1, -1))
        self.y_force_e = self.ml_y.predict(fft_data.reshape(1, -1))
        z, x, y = self.contact_force_view.get_force()

        z_estimate = "Z: "
        x_estimate = "X: "
        y_estimate = "Y: "
        z_estimate += str(round(self.z_force_e[0], 3))
        x_estimate += str(round(self.x_force_e[0], 3))
        y_estimate += str(round(self.y_force_e[0], 3))

        self.z_estimate_label.setText(z_estimate)
        self.x_estimate_label.setText(x_estimate)
        self.y_estimate_label.setText(y_estimate)

        self.estimate_force = True
        force = (self.z_force_e[0], self.x_force_e[0], self.y_force_e[0], True)
        self.contact_force_view.set_estimate(force)

        if self.log_check_box.isChecked():
            log_data_sr = pd.Series([self.z_force_e,
                                     self.x_force_e,
                                     self.y_force_e,
                                     z,
                                     x,
                                     y], index=self.log_data_df.columns)
            self.log_data_df = self.log_data_df.append(log_data_sr, ignore_index=True)

        self.z_reg_label.setText("Z_Size:" + str(self.z_force_e.size))
        self.x_reg_label.setText("X_Size:" + str(self.x_force_e.size))
        self.y_reg_label.setText("Y_Size:" + str(self.y_force_e.size))

    def stop_estimate(self):
        self.record_button.setEnabled(True)
        self.estimate_update.stop()
        self.start_estimate_button.setText("推定開始")
        self.start_estimate_button.disconnect()
        self.start_estimate_button.clicked.connect(self.start_estimate)

        if self.log_check_box.isChecked():
            self.log_data_df['SVM_C'] = self.svm_para_panel.get_c()
            self.log_data_df['SVM_gamma'] = self.svm_para_panel.get_gamma()
            self.log_data_df['LearningSamples'] = self.force_data.size
            self.log_data_df.to_csv('result.csv')

    def write_csv(self):
        self.fft_data.to_csv('fft.csv')
        self.force_data.to_csv('force.csv')

    def clear_data(self):
        self.calc_button.setEnabled(False)
        self.start_estimate_button.setEnabled(False)
        self.record_button.setEnabled(True)
        self.fft_data = pd.DataFrame()
        self.force_data = pd.DataFrame()