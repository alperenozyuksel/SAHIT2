from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt5.QtGui import QPainter, QPen, QBrush
from PyQt5.QtCore import Qt, QTimer
from dronekit import connect
import sys, math


class AirspeedGauge(QWidget):
    def __init__(self):
        super().__init__()
        self.airspeed = 0  # Başlangıçta 0 airspeed
        self.setWindowTitle("Airspeed Gauge")
        self.resize(300, 300)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(100)  # 100 ms'de bir yenile

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        self.drawGauge(qp)
        qp.end()

    def drawGauge(self, qp):
        center_x, center_y = 150, 150
        radius = 100

        qp.setRenderHint(QPainter.Antialiasing)
        qp.setPen(QPen(Qt.black, 3))
        qp.setBrush(QBrush(Qt.white))
        qp.drawEllipse(center_x - radius, center_y - radius, radius * 2, radius * 2)

        # İbreyi çiz
        qp.setPen(QPen(Qt.red, 5))
        angle = -135 + (self.airspeed * 270 / 50)  # 0-100 airspeed aralığı
        radian = math.radians(angle)
        x = center_x + radius * 0.8 * math.cos(radian)
        y = center_y + radius * 0.8 * math.sin(radian)
        qp.drawLine(center_x, center_y, x, y)

    def setAirspeed(self, value):
        self.airspeed = min(max(value, 0), 100)  # 0-100 arası sınırla
        self.update()


# DroneKit bağlantısı
vehicle = connect('127.0.0.1:14550', wait_ready=True)


def update_airspeed():
    gauge.setAirspeed(vehicle.airspeed)
    QTimer.singleShot(500, update_airspeed)


app = QApplication(sys.argv)
gauge = AirspeedGauge()
gauge.show()
update_airspeed()
sys.exit(app.exec_())
