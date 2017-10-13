from Window.DeviceWindow import *
from Window.LineEdit import *
from enum import Enum
from Experiments.ContactExpriment import *
from Experiments.DataAnalysis import *
from Experiments.lpc import *
from Tools.record import *
from ContactForceGui.app import *
from sklearn.svm import SVR
# import Experiments.libPyShared as ps
import importlib as il


class ThreeAxis(Enum):
    Z = 0
    X = 1
    Y = 2


class SvmParameterLayout(QWidget):
    gamma_line = None
    c_line = None

    def __init__(self):
        super(SvmParameterLayout, self).__init__()
        self.gamma_line = LabelOnSpinBox(label='Gamma 1/n',
                                         val=2048,
                                         maximum=8192)
        self.c_line = LabelOnSpinBox(label='C',
                                     val=int(1e3),
                                     maximum=1e5)

        layout = QVBoxLayout()


        layout.addWidget(QLabel("<b>SVM関連(｀･ω･´)</b>"))
        layout.addWidget(self.gamma_line)
        layout.addWidget(self.c_line)
        layout.addStretch()
        self.setLayout(layout)

    def get_gamma(self):
        return self.gamma_line.get_value()

    def get_c(self):
        return self.c_line.get_value()


class MachineLearningControlLayout(QWidget):
    calc_button = None
    estimate_button = None

    def __init__(self):
        super(MachineLearningControlLayout, self).__init__()
        layout = QVBoxLayout()

        self.only_x_calc_check = QCheckBox(text="Z軸のみ演算")
        self.lpc_button = QPushButton("LPC変換")
        self.calc_button = QPushButton("演算開始")
        self.estimate_button = QPushButton("推定開始")

        layout.addWidget(QLabel("<b>操作</b>"))
        layout.addWidget(self.only_x_calc_check)
        layout.addWidget(self.lpc_button)
        layout.addWidget(self.calc_button)
        layout.addWidget(self.estimate_button)
        layout.addStretch()

        self.setLayout(layout)


class ContactForceForSVR(QWidget):
    ai_device = None
    recoder_widget = None
    force_window = None
    parameter_widget = None
    control_widget = None
    calc_button = None
    estimate_button = None
    svr = []
    update_timer = None
    lpc_order = 300

    def __init__(self, parent=None, device=None, force=None):
        super(ContactForceForSVR, self).__init__(parent)
        self.setWindowTitle("SVR Manager")
        layout = QHBoxLayout()

        self.ai_device = device
        self.recoder_widget = ContactForceRecord(parent=parent, device=device)
        self.recoder_widget.set_force(force)
        self.parameter_widget = SvmParameterLayout()
        self.control_widget = MachineLearningControlLayout()
        self.force_window = force

        self.log_data_df = pd.DataFrame()
        self.update_cnt = 0
        self.lpc_data = None

        layout.addWidget(self.recoder_widget)
        layout.addWidget(self.parameter_widget)
        layout.addWidget(self.control_widget)
        self.setLayout(layout)

        self.only_y_calc_check = self.control_widget.only_x_calc_check
        self.lpc_calc_button = self.control_widget.lpc_button
        self.calc_button = self.control_widget.calc_button
        self.estimate_button = self.control_widget.estimate_button

        self.lpc_calc_button.clicked.connect(self.lpc_convert)
        self.calc_button.clicked.connect(self.learning_data)
        self.estimate_button.clicked.connect(self.start_estimate)
        self.estimate_button.setEnabled(False)
        self.calc_button.setEnabled(False)
        self.ps = il.import_module('Experiments.libPyShared')
        self.force_shared = self.ps.PyShared()
        self.force_shared.init(True)

    def lpc_convert(self):
        self.calc_button.setEnabled(True)
        #  LPCに変換
        nfft = self.ai_device.get_sample_num()
        wave_data_np = self.recoder_widget.wave_data
        lpc_data = np.copy(wave_data_np)
        for i, data in enumerate(wave_data_np):
            r = auto_correlate(data)
            a, e = levinson_durbin(r, self.lpc_order)
            w, h = scipy.signal.freqz(np.sqrt(e), a, nfft, "whole")
            lpc_data[i] = [np.sqrt(b.real**2 + b.imag**2) for b in h]

        self.lpc_data = [ans[:nfft//2] for ans in lpc_data]

    def learning_data(self):
        self.estimate_button.setEnabled(True)

        force_data = self.recoder_widget.force_values

        # 学習するよ
        c = int(self.parameter_widget.get_c())
        gamma = self.parameter_widget.get_gamma()
        self.svr = []
        force_data = force_data.T

        print("-------Starting Learning-------")
        print("Gamma="+str(gamma))
        print("C="+str(c))
        self.svr = []
        for i in range(len(ThreeAxis)):
            self.svr.append(SVR(kernel='rbf', C=c, gamma=float(1/gamma)))
            if self.only_y_calc_check.isChecked():
                self.svr[2].fit(self.lpc_data, force_data[0])
                print(ThreeAxis(0).name + "_Score=" + str(self.svr[2].score(self.lpc_data, force_data[0])))
                break
            else:
                self.svr[i].fit(self.lpc_data, force_data[i])
                print(ThreeAxis(i).name+"_Score="+str(self.svr[i].score(self.lpc_data, force_data[i])))
        print("-----------Compleate-----------")

    def start_estimate(self):
        self.calc_button.setEnabled(False)
        self.estimate_button.setText("推定停止")
        self.estimate_button.disconnect()
        self.estimate_button.clicked.connect(self.stop_estimate)
        self.update_timer = QTimer()
        self.update_timer.setInterval(0)
        self.update_timer.timeout.connect(self.update_estimate)
        self.update_timer.start()
        self.log_data_df = pd.DataFrame()

    def update_estimate(self):
        # LPC変換
        nfft = self.ai_device.get_sample_num()
        wave_data = self.ai_device.getAI()
        (z, x, y) = self.recoder_widget.get_force()
        r = auto_correlate(wave_data)
        a, e = levinson_durbin(r, self.lpc_order)
        w, h = scipy.signal.freqz(np.sqrt(e), a, nfft, "whole")
        lpc_data = [np.sqrt(i.real**2 + i.imag**2) for i in h]
        lpc_data = np.array(lpc_data[0:nfft//2])
        force = [
            self.svr[ThreeAxis.Z.value].predict(lpc_data.reshape(1, -1))[0],
            self.svr[ThreeAxis.X.value].predict(lpc_data.reshape(1, -1))[0],
            self.svr[ThreeAxis.Y.value].predict(lpc_data.reshape(1, -1))[0],
            z,
            x,
            y
        ]
        self.force_shared.set(float(abs(force[0])), float(force[1]), float(force[2]))
        self.force_window.set_estimate([force[0], force[1], force[2]])
        log_data_sr = pd.Series(force,
                                index=["Z", "X", "Y", "TrueZ", "TrueX", "TrueY"],
                                name=self.update_cnt)
        print("Z=%f, X=%f, Y=%f" % (force[0], force[1], force[2]))
        self.log_data_df = self.log_data_df.append(log_data_sr)
        self.update_cnt += 1

    def stop_estimate(self):
        self.calc_button.setEnabled(True)
        self.estimate_button.setText("推定開始")
        self.estimate_button.disconnect()
        self.estimate_button.clicked.connect(self.start_estimate)
        self.update_timer.stop()
        self.log_data_df.to_csv("result.csv")

