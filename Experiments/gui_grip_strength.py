from Window.DeviceWindow import *
from Window.LineEdit import *
from Experiments.DataAnalysis import *
from Tools.record import *
from GraphicsItem.arrow import *
from GraphicsItem.tranceform import *
from sklearn.svm import SVR
from TweModule.TweLiteBasic import *
import math


class GripperGame(QGraphicsItem):
    def __init__(self, width: int, height: int):
        super(GripperGame, self).__init__()
        self.window_size = None
        self.grip_force = 0.0
        self.width = width
        self.height = height
        draw_scale = QPolygonF()
        draw_scale.append(QPointF(0, 70))
        draw_scale.append(QPointF(5, -5))
        draw_scale.append(QPointF(-5, -5))
        self.target = QRectF(0, 0, self.width, self.height)
        self.source = QRectF(0, 0, 2084, 2084)
        self.image = QImage("GraphicsItem/scale.png")
        self.scales = []
        rect_size = 460
        self.rect_angle = QRectF((self.width-rect_size)/2, (self.height-rect_size)/2, rect_size, rect_size )

        self.arrow_estimate = TranceForm(draw_scale, QPointF(self.width / 2, self.height / 2))

    def paint(self, painter: QtGui.QPainter, option, widget):
        qpen = QPen()
        qpen.setWidth(1)
        qpen.setColor(Qt.black)
        painter.setPen(qpen)

        painter.drawImage(self.target, self.image, self.source)
        font = QFont("Times", 70, QFont.Bold)
        painter.setFont(font)
        painter.drawText(self.width/2-50, self.height/2-150, "%0.1f" % self.grip_force)

        qpen.setWidth(15)
        qpen.setColor(Qt.blue)
        painter.setPen(qpen)
        painter.drawArc(self.rect_angle, -180 * 16, (self.grip_force*1.8) * (-16))

        self.arrow_estimate.size = 5.0
        self.arrow_estimate.angle = ((self.grip_force * 1.8) - 90) * math.pi / 180
        self.arrow_estimate.update_point()

        qbrush = QBrush()
        arrow_path = QPainterPath()
        arrow_path.addPolygon(self.arrow_estimate.points)
        qbrush.setColor(Qt.red)
        qbrush.setStyle(Qt.SolidPattern)
        painter.fillPath(arrow_path, qbrush)

    def boundingRect(self):
        return QRectF(0, 0, self.width, self.height)


class GripStrengthViewer(QGraphicsView):
    def __init__(self):
        super(GripStrengthViewer, self).__init__()
        self.setFixedSize(800, 800)
        self.grip_force = 0.0
        scene = QGraphicsScene()
        scene.setSceneRect(0, 0, self.width(), self.height())
        self.grip_game = GripperGame(self.width(), self.height())
        self.grip_game.window_size = self.size()
        scene.addItem(self.grip_game)
        self.setCacheMode(QGraphicsView.CacheBackground)
        self.setScene(scene)

    def set_grip_force(self, estimate_force, truth_force):
        self.grip_force = estimate_force
        self.grip_game.grip_force = estimate_force
        self.grip_game.update()
