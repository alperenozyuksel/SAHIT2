from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QPen, QFont
from PyQt5.QtCore import Qt, QPointF
import math

class NumberDial(QWidget):
    def __init__(self, parent, width, height, x_pos, y_pos, start_angle, end_angle, num_steps):
        super().__init__(parent)
        self.width = width
        self.height = height
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.start_angle = start_angle
        self.end_angle = end_angle
        self.num_steps = num_steps
        self.value = 0  # İbrenin gösterdiği değer

        self.setGeometry(x_pos, y_pos, width, height)
        self.setStyleSheet("background-color: transparent;")

    def set_value(self, value):
        self.value = value
        self.update()  # Widget'ı yeniden çiz

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Çemberin boyutları
        radius = min(self.width, self.height) // 2 - 20
        center = QPointF(self.width // 2, self.height // 2)

        # Sayıları çiz
        self.draw_numbers(painter, center, radius)

        # İbrenin kendisini çiz
        self.draw_needle(painter, center, radius)

    def draw_numbers(self, painter, center, radius):
        font = QFont("Arial", 8)
        painter.setFont(font)
        painter.setPen(QPen(Qt.white, 2))  # Sayıların rengi ve kalınlığı

        for i in range(self.num_steps + 1):
            value = i * (100 // self.num_steps)  # 0'dan 100'e kadar sayılar
            angle = self.start_angle + (self.end_angle - self.start_angle) * (i / self.num_steps)
            angle_rad = math.radians(angle)

            # Sayının konumu (çemberin dışına yerleştir)
            text_radius = radius + 25  # Çemberin dışına yerleştir
            text_point = QPointF(
                center.x() + text_radius * math.cos(angle_rad),
                center.y() - text_radius * math.sin(angle_rad)
            )

            # Sayıyı çiz (merkeze hizala)
            text_rect = painter.fontMetrics().boundingRect(str(value))
            text_point.setX(text_point.x() - text_rect.width() / 2)
            text_point.setY(text_point.y() + text_rect.height() / 4)
            painter.drawText(text_point, str(value))

    def draw_needle(self, painter, center, radius):
        painter.setPen(QPen(Qt.red, 3))
        angle = self.start_angle + (self.end_angle - self.start_angle) * (self.value / 100)
        angle_rad = math.radians(angle)

        # İbrenin uç noktası
        needle_point = QPointF(
            center.x() + radius * 0.8 * math.cos(angle_rad),
            center.y() - radius * 0.8 * math.sin(angle_rad)
        )

        # İbrenin merkezden uca çizgisi
        painter.drawLine(center, needle_point)