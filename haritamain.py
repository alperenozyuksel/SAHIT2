import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLabel, QFrame, QProgressBar, \
    QTextEdit
from PyQt5.QtGui import QPalette, QColor, QPixmap, QPainter, QTransform
from PyQt5.QtCore import Qt, QTimer
import altitude_inducator
import yellow_arrow
from sensorler import *
from ibredoksanderece import NeedleDoksanDerece
from ibreyuzdensifira import NeedleYuzdenSifira
from ibresifirdanyuze import NeedleSifirdanYuze
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtWebEngineWidgets import QWebEngineSettings




class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()



        self.setWindowTitle("ŞAHİT")
        self.setGeometry(100, 100, 1920, 1080)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("black"))
        self.setPalette(palette)

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.tabs.addTab(self.create_map_tab("Harita"), "Harita")
        self.tabs.addTab(self.create_sekme_2(), "Sekme 2")
        self.tabs.addTab(self.create_tab("Sekme 3"), "Sekme 3")



        self.mavlink_thread = MAVLinkDataThread()
        self.mavlink_thread.ins_health_updated.connect(self.updated_ins)
        self.mavlink_thread.mag_health_updated.connect(self.updated_mag)
        self.mavlink_thread.ahrs_health_updated.connect(self.updated_ahrs)
        self.mavlink_thread.ekf_health_updated.connect(self.updated_ekf)
        self.mavlink_thread.pre_health_updated.connect(self.updated_pre)
        self.mavlink_thread.battery_updated.connect(self.updated_battery)
        self.mavlink_thread.temperature_updated.connect(self.update_temperature)
        self.mavlink_thread.armed_status_updated.connect(self.update_arm)
        self.mavlink_thread.altitude_updated.connect(self.update_altitude)
        self.mavlink_thread.status_text_updated.connect(self.add_status_message)
        self.mavlink_thread.pwm_updated.connect(self.update_progress_bars)
        self.mavlink_thread.gps_satellite_updated.connect(self.updated_gps_count)
        self.mavlink_thread.vfr_hud_updated.connect(self.updated_vfr)
        self.mavlink_thread.throttle_updated.connect(self.update_throttle)
        self.mavlink_thread.msg_mode_updated.connect(self.mete_updated)
        self.mavlink_thread.attitude_updated.connect(self.updated_attitude)
        self.mavlink_thread.start()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_all)  # Her zamanlayıcıda yeniden çiz
        self.timer.start(100)  # Her 100ms'de bir
    def create_tab(self, title):
        tab = QWidget()
        tab_layout = QVBoxLayout()
        label = QLabel(title)
        label.setStyleSheet("color: white; font-size: 24px;")
        tab_layout.addWidget(label)
        tab.setLayout(tab_layout)
        tab.setStyleSheet("background-color: #000000;")
        return tab

    def create_map_tab(self, title):
        tab = QWidget()
        tab_layout = QVBoxLayout()

        # Başlık etiketi (label)
        label = QLabel(title)
        label.setStyleSheet("color: white; font-size: 18px;")
        label.setAlignment(Qt.AlignTop)
        tab_layout.addWidget(label, alignment=Qt.AlignTop)  # Başlığı yukarı hizala

        # Harita için Frame oluştur
        map_frame = QFrame()
        map_frame.setStyleSheet("background-color: #2E2E2E; border: 1px solid #444;")  # Frame stilini ayarla
        map_frame_layout = QVBoxLayout(map_frame)
        map_frame_layout.setContentsMargins(0, 0, 0, 0)  # Kenar boşluklarını kaldır

        # QWebEngineView (Harita Görüntüleme)
        self.map_view = QWebEngineView()
        self.map_view.settings().setAttribute(QWebEngineSettings.JavascriptEnabled, True)
        self.map_view.settings().setAttribute(QWebEngineSettings.LocalStorageEnabled, True)
        self.map_view.settings().setAttribute(QWebEngineSettings.PluginsEnabled, True)

        # JavaScript hatalarını konsolda görmek için
        self.map_view.page().javaScriptConsoleMessage = (
            lambda level, message, line, sourceID: print(f"JS Error [{level}]: {message} (Line {line})")
        )

        # HTML İçeriği (Aynı)
        html_content = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>Harita</title>
                <meta charset="utf-8" />
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <link rel="stylesheet" href="https://unpkg.com/leaflet/dist/leaflet.css" />
                <script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>
                <style>
                    html, body { height: 100%; margin: 0; padding: 0; }
                    #map { height: calc(100% - 50px); width: 100vw; }
                </style>
            </head>
            <body>
                <div id="map"></div>
                <script>
                    var map = L.map('map').setView([51.505, -0.09], 13);
                    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                        attribution: '&copy; OpenStreetMap contributors'
                    }).addTo(map);
                </script>
            </body>
            </html>
        """

        self.map_view.setHtml(html_content)

        # Harita görünümünü frame içine ekle
        map_frame_layout.addWidget(self.map_view)

        # Frame'i ana layout'a ekle
        tab_layout.addWidget(map_frame)

        # Tab'ı yerleşimle düzenle
        tab.setLayout(tab_layout)
        tab.setStyleSheet("background-color: #000000;")  # Arka plan rengi

        return tab