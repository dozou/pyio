from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import math

class DrawArrow:
    angle = 0.0
    size = 1.0

    def __init__(self, point: QPointF):
        self.draw_point = point
        self.shape_points = QPolygonF()
        self.shape_points.append(QPointF(0, 50))
        self.shape_points.append(QPointF(-10, 20))
        self.shape_points.append(QPointF(-5, 20))
        self.shape_points.append(QPointF(-5, -20))
        self.shape_points.append(QPointF(5, -20))
        self.shape_points.append(QPointF(5, 20))
        self.shape_points.append(QPointF(10, 20))
        self.points = QPolygonF()
        self.local_changed_points = QPolygonF(self.shape_points)
        for i in self.shape_points:
            self.points.append(i)

        self.angle = 0.0
        self.update_point()

    def head_size(self, size: float):
        self.local_changed_points.replace(0, QPointF(self.local_changed_points[0].x(),
                                                     self.local_changed_points[0].y()*size))
        self.local_changed_points.replace(1, QPointF(self.local_changed_points[1].x()*size,
                                                     self.local_changed_points[1].y()))
        self.local_changed_points.replace(6, QPointF(self.local_changed_points[6].x()*size,
                                                     self.local_changed_points[6].y()))

    def head_length(self, length: float):
        changed_point_indexs = [0, 1, 2, 5, 6]
        for i in changed_point_indexs:
            self.local_changed_points.replace(i, QPointF(self.local_changed_points[i].y(),
                                                         self.local_changed_points.y() * length))

    def update_point(self):
        # ---形状変形後の全体操作を行う（移動・回転・拡大）---
        for i, point in enumerate(self.local_changed_points):
            point.setX(point.x() * self.size)  # 拡大縮小
            point.setY(point.y() * self.size)
            rotated_point = QPointF()
            rotated_point.setX(point.x() * math.cos(self.angle) - point.y() * math.sin(self.angle))  # 回転
            rotated_point.setY(point.x() * math.sin(self.angle) + point.y() * math.cos(self.angle))
            self.points.replace(i, self.draw_point - rotated_point)  # 座標合わせ
            self.local_changed_points.replace(i, self.shape_points[i])  # 初期化
