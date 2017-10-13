import copy
import sys
import importlib as il
import numpy as np
import math
#import ContactForceGui.libPyCFS as cfs
from SignalProcessing.move_mean import *
from GraphicsItem.arrow import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class ForceXYZ:
    z = 0.0
    x = 0.0
    y = 0.0


class ForceView(QGraphicsItem):
    xforce = 0.0
    yforce = 0.0
    zforce = 0.0
    estimate_point = QPointF()
    estimate_force = ForceXYZ()
    estimate_force_z = 0.00
    circle_size = 0.00
    force_point = QPointF()
    target_point = QPointF()
    target_force = ForceXYZ()
    force_factor = 20
    point_factor = 40
    test = False

    def __init__(self):
        super(ForceView, self).__init__()
        self.target_point.setX(1280//2-self.point_factor*self.target_force.x)
        self.target_point.setY(720//2-self.point_factor*self.target_force.y)
        self.mean_z = MoveMean(3)
        self.mean_x = MoveMean(3)
        self.mean_y = MoveMean(3)
        self.test = QPolygonF()
        # self.arrow = DrawArrow(QPointF(1280/2, 720/2))
        self.force_mouse_point = QPointF(1280/2, 720/2)
        self.rect = QPolygonF()

    def paint(self, painter, option, widget):
        # if abs(self.estimate_force.x) > 1.0:
        #     move = (self.estimate_force.x * (self.estimate_force.x**2))/6
        #     if move > 4:
        #         move = 4
        #     self.force_mouse_point.setX(self.force_mouse_point.x() + move)
        #
        # if abs(self.estimate_force.y) > 1.0:
        #     move = (self.estimate_force.y * (self.estimate_force.y**2))/6
        #     if move > 4:
        #         move = 4
        #     self.force_mouse_point.setY(self.force_mouse_point.y() - move)
        #
        # if abs(self.estimate_force.z) > 4.0:
        #     self.test.append(self.force_mouse_point)
        #
        # if abs(self.estimate_force.z) > 8.0:
        #     self.force_mouse_point.setX(1280/2)
        #     self.force_mouse_point.setY(720/2)

        qpen = QPen()
        qpen.setWidth(10)
        qpen.setColor(Qt.black)
        qpen.setCapStyle(Qt.RoundCap)
        painter.setPen(qpen)
        painter.drawPoints(self.test)
        qpen.setColor(Qt.red)
        qpen.setWidth(10)
        qpen.setCapStyle(Qt.RoundCap)
        painter.setPen(qpen)
        painter.drawPoint(self.force_mouse_point)

        qpen.setColor(Qt.black)
        qpen.setWidth(3)
        qpen.setCapStyle(Qt.RoundCap)
        painter.setPen(qpen)
        # self.arrow.angle = self.xforce/5
        #self.arrow.head_length(float(self.circle_size))
        # self.arrow.head_size(abs(float(self.zforce))+1)
        # self.arrow.size = 1
        # self.arrow.update_point()
        # painter.drawPolygon(self.arrow.points)
        # for xy, z in self.locus_xy.value:
        #     painter.drawEllipse(xy, z+40, z+40)

        qpen.setWidth(3)
        qpen.setColor(Qt.blue)
        painter.setPen(qpen)
        painter.drawEllipse(self.force_point, self.circle_size+40, self.circle_size+40)

        qpen.setColor(Qt.black)
        painter.setPen(qpen)
        self.target_point.setX(700//2-self.point_factor*self.target_force.x)
        self.target_point.setY(500//2-self.point_factor*self.target_force.y)
        self.targetforce = self.target_force.z * self.force_factor
        #painter.drawEllipse(self.target_point, self.targetforce+20, self.targetforce+20)

        text_point = QPointF()
        text_point.setX(self.force_point.x())
        text_point.setY(self.force_point.y())
        zforce_txt = "Z:" + str('%03.3f'%self.zforce)
        xforce_txt = "X:" + str('%03.3f'%self.xforce)
        yforce_txt = "Y:" + str('%03.3f'%self.yforce)
        text_point.setX(text_point.x()+self.circle_size+40)
        painter.drawText(text_point, zforce_txt)
        text_point.setY(text_point.y()+12)
        painter.drawText(text_point, xforce_txt)
        text_point.setY(text_point.y()+12)
        painter.drawText(text_point, yforce_txt)

        self.estimate_of_circle(painter=painter, qpen=qpen)

    def estimate_of_circle(self, painter, qpen):
        qpen.setColor(Qt.red)
        painter.setPen(qpen)
        painter.drawEllipse(self.estimate_point, self.estimate_force_z+40, self.estimate_force_z+40)

    def update_estimate_force(self):
        self.estimate_force_z = self.force_factor * abs(self.estimate_force.z)
        estimate_point = QPointF()
        estimate_point.setX(1280//2+(self.point_factor * self.estimate_force.x))
        estimate_point.setY(720//2-(self.point_factor * self.estimate_force.y))
        self.estimate_point = estimate_point

    def set_estimate_force(self, force):
        z, x, y = force
        # self.estimate_force.z = self.mean_z.push(z)
        # self.estimate_force.x = self.mean_x.push(x)
        # self.estimate_force.y = self.mean_y.push(y)
        self.estimate_force.z = z
        self.estimate_force.x = x
        self.estimate_force.y = y

    def boundingRect(self):
        return QRectF(0, 0, 1280, 720)

    def updateCircle(self, z_force, x_force=0, y_force=0):
        self.xforce = x_force
        self.yforce = y_force
        self.zforce = z_force

        self.circle_size = (self.force_factor * abs(z_force))
        xy = QPoint()
        xy.setX(1280//2+(self.point_factor * x_force))
        xy.setY(720//2-(self.point_factor * y_force))
        self.force_point = xy
        self.update()

    def update_target_circle(self, z_force, x_force, y_force):
        self.target_force.x = x_force
        self.target_force.y = y_force
        self.target_force.z = z_force

    def reset_points(self):
        self.test.clear()

    def reset_mouse_point(self):
        self.force_mouse_point.setX(1280/2)
        self.force_mouse_point.setY(720/2)
        self.estimate_force.z = 0.0
        self.estimate_force.x = 0.0
        self.estimate_force.y = 0.0


class ContactForceViewer(QGraphicsView):
    def __init__(self, parent=None):
        super(ContactForceViewer, self).__init__(parent)
        scene = QGraphicsScene(self)
        self.viewer = ForceView()

        scene.addItem(self.viewer)
        #scene.setMinimumRenderSize()
        scene.setSceneRect(0, 0, 1280, 720)

        self.setScene(scene)
        self.setCacheMode(QGraphicsView.CacheBackground)
        self.setWindowTitle("ContactForceGui")
        self.cfs = il.import_module('ContactForceGui.libPyCFS')
        self.ENUM = self.cfs.axis
        self.forcedevice = self.cfs.PyCFS()
        self.auto()

    def open_device(self, devname):
        self.forcedevice.openDevice(devname)
        self.forcedevice.startPolling()
        self.forcedevice.resetOffset()

    def close_device(self):
        self.forcedevice.closeDevice()

    def auto(self):
        self.timer = QTimer()
        self.timer.setInterval(10)
        self.timer.timeout.connect(self.timeout)
        self.timer.start()

    def timeout(self):
        z_force = self.forcedevice.getForce(self.ENUM.Z_FORCE)
        x_force = self.forcedevice.getForce(self.ENUM.X_FORCE)
        y_force = self.forcedevice.getForce(self.ENUM.Y_FORCE)
        #y_force = 0
        self.viewer.updateCircle(z_force=z_force,
                                 x_force=x_force,
                                 y_force=y_force)
        self.viewer.update_estimate_force()

    def stop(self):
        if self.timer:
            self.timer.stop()
            self.timer = None


class ContactForceMain(QWidget):
    def __init__(self, parent=None):
        super(ContactForceMain, self).__init__(parent)
        self.setMinimumSize(QSize(1380, 820))
        self.setWindowTitle("ContactForceGuiTool")

        #Setting Tool layout
        set_layout = QVBoxLayout()
        self.device_name_text = QLabel("Enter to connect!")
        self.deviceName_textbox = QLineEdit("/dev/tty.usbmodem15010191")
        self.deviceName_textbox.returnPressed.connect(self.open_device)
        self.targetX_text = QLabel("X Force:0")
        self.targetX_slider = QSlider(Qt.Horizontal)
        self.targetX_slider.setRange(-10, 10)
        self.targetX_slider.valueChanged.connect(self.changed_target)
        self.targetY_text = QLabel("Y Force:0")
        self.targetY_slider = QSlider(Qt.Horizontal)
        self.targetY_slider.setRange(-10, 10)
        self.targetY_slider.valueChanged.connect(self.changed_target)
        self.targetForce_text = QLabel("Force:0")
        self.targetForce_slider = QSlider(Qt.Horizontal)
        self.targetForce_slider.setRange(0, 10)
        self.targetForce_slider.valueChanged.connect(self.changed_target)
        self.device_connect = QPushButton("Connect")
        self.device_connect.clicked.connect(self.open_device)

        set_layout.addWidget(self.device_name_text)
        set_layout.addWidget(self.deviceName_textbox)
        set_layout.addWidget(self.targetX_text)
        set_layout.addWidget(self.targetX_slider)
        set_layout.addWidget(self.targetY_text)
        set_layout.addWidget(self.targetY_slider)
        set_layout.addWidget(self.targetForce_text)
        set_layout.addWidget(self.targetForce_slider)
        set_layout.addWidget(self.device_connect)
        set_layout.addStretch()

        layout = QHBoxLayout()
        self.view = ContactForceViewer()
        layout.addWidget(self.view)
        #layout.addLayout(set_layout)
        self.setLayout(layout)
        self.open_device()

    def open_device(self):
        self.view.close_device()
        self.view.open_device(self.deviceName_textbox.text())
        self.device_connect.setText("Disconnect")
        self.device_connect.disconnect()
        self.device_connect.clicked.connect(self.close_device)

    def close_device(self):
        self.view.close_device()
        self.device_connect.setText("Connect")
        self.device_connect.disconnect()
        self.device_connect.clicked.connect(self.open_device)

    def changed_target(self):
        self.view.viewer.update_target_circle(
            x_force=self.targetX_slider.value()*(-1),
            y_force=self.targetY_slider.value(),
            z_force=self.targetForce_slider.value())

        target_x = "X Force:" + str(self.targetX_slider.value()*(-1))
        target_y = "Y_Force:" + str(self.targetY_slider.value())
        target_force = "Force:" + str(self.targetForce_slider.value())
        self.targetX_text.setText(target_x)
        self.targetY_text.setText(target_y)
        self.targetForce_text.setText(target_force)

    def get_force(self):
        return (self.view.forcedevice.getForce(self.view.ENUM.Z_FORCE),
                self.view.forcedevice.getForce(self.view.ENUM.X_FORCE),
                self.view.forcedevice.getForce(self.view.ENUM.Y_FORCE))

    def set_estimate(self, force):
        self.view.viewer.set_estimate_force(force)

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_R:
            self.view.viewer.reset_points()

        if event.key() == Qt.Key_C:
            self.view.viewer.reset_mouse_point()

    def hideEvent(self, a0: QHideEvent):
        self.close_device()
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    main_window = ContactForceMain()
    main_window.show()
    sys.exit(app.exec_())
