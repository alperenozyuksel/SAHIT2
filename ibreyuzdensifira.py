from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt
import math


class NeedleYuzdenSifira(QWidget):
    def __init__(self, parent=None, needle_length=30, needle_width=5):
        super().__init__(parent)
        self.airspeed = 0  # Başlangıçta 0 airspeed
        self.needle_length = needle_length  # İbre uzunluğu (sabit)
        self.needle_width = needle_width  # İbre kalınlığı
        self.setFixedSize(200, 200)  # Sabit boyut verebiliriz

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        self.drawNeedle(qp)
        qp.end()

    def drawNeedle(self, qp):
        center_x, center_y = self.width() // 2, self.height() // 2
        radius = self.needle_length  # İbre uzunluğunu sabit tutuyoruz

        qp.setRenderHint(QPainter.Antialiasing)
        qp.setPen(QPen(Qt.red, self.needle_width))

        # Hızı kullanarak ibrenin açısını hesapla
        angle = 382 - (self.airspeed * 382 / 50)  # 0 için 90, 100 için 0 derece
        radian = math.radians(angle)

        # İbreyi çiz
        x = center_x + radius * math.cos(radian)
        y = center_y + radius * math.sin(radian)
        qp.drawLine(center_x, center_y, x, y)

    def setAirspeed(self, value):
        self.airspeed = min(max(value, 0), 100)  # 0-100 arası sınırla
        self.update()

    def setNeedleSize(self, length, width):
        self.needle_length = length
        self.needle_width = width
        self.update()  # İbre boyutunu değiştirdiğimizde widget'ı güncelle

    def sizeHint(self):
        return self.size()
