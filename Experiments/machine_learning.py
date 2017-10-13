from Window.DeviceWindow import *
from Window.LineEdit import *
from Experiments.DataAnalysis import *
from Tools.record import *
from ContactForceGui.app import *
from sklearn.svm import SVR


class SvmParameterLayout(QWidget):
    gamma_line = None
    c_line = None

    def __init__(self):
        super(SvmParameterLayout, self).__init__()
        self.gamma_line = LabelOnSpinBox(label='Gamma 1/n',
                                         val=1024,
                                         maximum=8192)
        self.c_line = LabelOnSpinBox(label='C',
                                     val=int(1e3),
                                     maximum=1e5)

        layout = QVBoxLayout()

        layout.addWidget(QLabel("<b>SVM関連(｀･ω･´)</b>"))
        layout.addWidget(self.gamma_line)
        layout.addWidget(self.c_line)
        layout.addStretch()
        layout.setContentsMargins(QMargins(0, 0, 0, 0))
        self.setLayout(layout)

    def get_gamma(self):
        return self.gamma_line.get_value()

    def get_c(self):
        return self.c_line.get_value()


class SvmToolWindowFFT(FFTRecordWindow):
    data_ana = None
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
    log_cnt = 0

    def __init__(self, parent=None):
        super(SvmToolWindowFFT, self).__init__(parent=parent)
        self.setWindowTitle("SVM Manager")

        self.data_ana_checkbox = QCheckBox(text="データ解析ツール")
        self.data_ana_checkbox.toggled.connect(self.start_data_ana)
        self.log_check_box = QCheckBox(text="推定値保存")
        self.calc_button = QPushButton("演算開始")
        self.start_estimate_button = QPushButton("推定開始")
        self.calc_button.clicked.connect(self.calc_svm)
        self.start_estimate_button.clicked.connect(self.start_estimate)

        self.ai_control = AiControlView()
        self.ao_control = AoControlView()

        self.file_name = QLabel("Out:result_0.csv")

        self.z_reg_label = QLabel("")
        self.x_reg_label = QLabel("")
        self.y_reg_label = QLabel("")

        self.z_estimate_label = QLabel("")
        self.x_estimate_label = QLabel("")
        self.y_estimate_label = QLabel("")

        self.svm_para_panel = SvmParameterLayout()

        self.svm_panel = QVBoxLayout()
        self.svm_panel.addWidget(self.data_ana_checkbox)
        self.svm_panel.addWidget(self.log_check_box)
        self.svm_panel.addWidget(self.calc_button)
        self.svm_panel.addWidget(self.start_estimate_button)
        self.svm_panel.addWidget(self.file_name)
        self.svm_panel.addWidget(self.z_reg_label)
        self.svm_panel.addWidget(self.x_reg_label)
        self.svm_panel.addWidget(self.y_reg_label)
        self.svm_panel.addWidget(self.z_estimate_label)
        self.svm_panel.addWidget(self.x_estimate_label)
        self.svm_panel.addWidget(self.y_estimate_label)
        self.svm_panel.addStretch()

        self.main_layout.addWidget(self.ai_control)
        self.main_layout.addWidget(self.ao_control)
        self.main_layout.addWidget(self.svm_para_panel)
        self.main_layout.addLayout(self.svm_panel)
        self.setLayout(self.main_layout)

        self.start_estimate_button.setEnabled(False)
        self.calc_button.setEnabled(False)
        self.data_ana = DataAnalysis()

    def start_data_ana(self):
        if self.data_ana_checkbox.isChecked():
            self.data_ana.show()
        else:
            self.data_ana.hide()

    def set_device(self, device):
        super(SvmToolWindowFFT, self).set_device(device)
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
        super(SvmToolWindowFFT, self).record()
        z, x, y = self.contact_force_view.get_force()
        z = round(z, 1)
        x = round(x, 1)
        y = round(y, 1)
        force_sr = pd.Series([z, x, y])

        self.force_data = self.force_data.append(force_sr, ignore_index=True)

    def calc_svm(self):
        self.fft_data_np = self.fft_data
        self.force_z_np = np.array(self.force_data[0])
        self.force_x_np = np.array(self.force_data[1])
        self.force_y_np = np.array(self.force_data[2])

        C = int(self.svm_para_panel.get_c())
        gamma = self.svm_para_panel.get_gamma()

        self.svr_z = SVR(kernel='rbf', C=C, gamma=float(1/gamma))
        self.svr_z.fit(self.fft_data_np, self.force_z_np)
        self.svr_x = SVR(kernel='rbf', C=C, gamma=float(1/gamma))
        self.svr_x.fit(self.fft_data_np, self.force_x_np)
        self.svr_y = SVR(kernel='rbf', C=C, gamma=float(1/gamma))
        self.svr_y.fit(self.fft_data_np, self.force_y_np)

        self.calc_button.setText("再演算")

        self.z_reg_label.setText("Z_Score:" + str(round(self.svr_z.score(self.fft_data_np, self.force_z_np), 5)))
        self.x_reg_label.setText("X_Score:" + str(round(self.svr_x.score(self.fft_data_np, self.force_x_np), 5)))
        self.y_reg_label.setText("Y_Score:" + str(round(self.svr_y.score(self.fft_data_np, self.force_y_np), 5)))
        self.start_estimate_button.setEnabled(True)
        zscore = self.svr_z.score(self.fft_data_np, self.force_z_np)
        xscore = self.svr_x.score(self.fft_data_np, self.force_x_np)
        yscore = self.svr_y.score(self.fft_data_np, self.force_y_np)
        self.reg_score = zscore, xscore, yscore

    def stop_record(self):
        super(SvmToolWindowFFT, self).stop_record()
        self.calc_button.setEnabled(True)

    def start_estimate(self):
        self.log_check_box.setEnabled(False)
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
        self.z_force_e = self.svr_z.predict(fft_data.reshape(1, -1))
        self.x_force_e = self.svr_x.predict(fft_data.reshape(1, -1))
        self.y_force_e = self.svr_y.predict(fft_data.reshape(1, -1))
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
        self.log_check_box.setEnabled(True)
        self.record_button.setEnabled(True)
        self.estimate_update.stop()
        self.start_estimate_button.setText("推定開始")
        self.start_estimate_button.disconnect()
        self.start_estimate_button.clicked.connect(self.start_estimate)

        if self.log_check_box.isChecked():
            self.log_data_df['SVM_C'] = self.svm_para_panel.get_c()
            self.log_data_df['SVM_gamma'] = self.svm_para_panel.get_gamma()
            self.log_data_df['LearningSamples'] = self.force_data.size
            self.log_data_df['Score_Z'] = self.reg_score[0]
            self.log_data_df['Score_X'] = self.reg_score[1]
            self.log_data_df['Score_Y'] = self.reg_score[2]
            name = 'result_' + str(self.log_cnt) + '.csv'
            self.log_data_df.to_csv(name)
            self.log_cnt += 1
            name = 'Out:result_' + str(self.log_cnt) + '.csv'
            self.file_name.setText(name)

    def write_csv(self):
        super(SvmToolWindowFFT, self).write_csv()
        self.force_data.to_csv('force.csv')

    def clear_data(self):
        super(SvmToolWindowFFT, self).write_csv()
        self.calc_button.setEnabled(False)
        self.start_estimate_button.setEnabled(False)
        self.record_button.setEnabled(True)
        self.force_data = pd.DataFrame()
