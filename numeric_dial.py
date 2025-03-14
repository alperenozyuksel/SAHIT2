from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QFont
from PyQt5.QtCore import Qt
import math

class NumericDial(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(400, 400)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setFont(QFont("Arial", 12))

        center_x, center_y = self.width() // 2, self.height() // 2
        radius = min(center_x, center_y) - 20

        for angle in range(0, 360, 30):  # 30 derece aralıklarla
            radian = math.radians(angle)
            x = center_x + int(math.cos(radian) * radius)
            y = center_y + int(math.sin(radian) * radius)

            painter.drawText(x - 10, y + 5, str(angle))
