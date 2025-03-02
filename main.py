import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLabel, QFrame, QProgressBar, \
    QTextEdit, QPushButton
from PyQt5.QtGui import QPalette, QColor, QPixmap, QPainter, QTransform
from PyQt5.QtCore import Qt, QTimer
from pymavlink.mavextra import airspeed

import altitude_inducator
import yellow_arrow
from sensorler import *
from ibredoksanderece import NeedleDoksanDerece
from ibreyuzdensifira import NeedleYuzdenSifira
from ibresifirdanyuze import NeedleSifirdanYuze

from ImageLabelClass import *
from frameclass import FrameClass
from labelclass import LabelClass


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



    def create_sekme_2(self):
        tab = QWidget()
        self.o = "images/on.png"
        self.y = "images/yan.png"
        self.u = "images/ust.png"

        self.o_h = 70
        self.y_h = 40
        self.u_h = 58

        self.o_w = 130
        self.y_w = 300
        self.u_w = 300
        self.resim_yolu = "batarya/1.png"
        self.ibre_batarya_100 = ImageLabel(parent=tab, height=180, width=200, x_pos=885, y_pos=340, image_path=self.resim_yolu)
        self.drone_label = ImageLabel(parent=tab, width=1000, height=600, x_pos=680, y_pos=180, image_path="images/drone600_600.png")
        self.logo = ImageLabel(parent=tab, width=300, height=800, x_pos=500, y_pos=800, image_path="images/SONYAKAMOZ1.png")
        self.ibre_devir = ImageLabel(parent=tab, height=200, width=300, x_pos=80, y_pos=20, image_path="images/ibre2.png")
        self.ibre_heading = ImageLabel(parent=tab, height=200, width=300, x_pos=379, y_pos=20, image_path="images/ibre5.png")
        self.ibre_air_speed = ImageLabel(parent=tab, height=200, width=300, x_pos=700, y_pos=20, image_path="images/ibre7.png")
        self.ibre_gps_speed = ImageLabel(parent=tab, height=200, width=300, x_pos=1055, y_pos=20, image_path="images/ibre7.png")
        self.ibre_dikilme = ImageLabel(parent=tab, height=200, width=300, x_pos=1365, y_pos=20, image_path="images/ibre3.png")
        self.ibre_yatis = ImageLabel(parent=tab, height=200, width=300, x_pos=1645, y_pos=20, image_path="images/ibre4.png")
        self.ibre_voltaj = ImageLabel(parent=tab, height=175, width=300, x_pos=680, y_pos=400, image_path="images/deneme.png")
        self.ibre_amper = ImageLabel(parent=tab, height=175, width=300, x_pos=1082, y_pos=400, image_path="images/ibre10.png")
        self.on = ImageLabel( parent= tab, height=self.o_h, width=self.o_w, x_pos=1680, y_pos=109, image_path=self.o)
        self.yan = ImageLabel( parent= tab, height=self.y_h, width=self.y_w, x_pos=1400, y_pos=96, image_path=self.y)
        self.ust = ImageLabel( parent= tab, height=self.u_h, width=self.u_w, x_pos=430, y_pos=85, image_path=self.u)








        self.gaz_label = LabelClass("GAZ",tab,  "white" ,"transparent", "bold", "12" )
        self.gaz_label.move(1300, 300)
        
        self.devir_label = LabelClass("DEVİR",tab, "white" ,"transparent", "bold", "12" )
        self.devir_label.move(158, 220)

        self.heading_label = LabelClass("HEADING",tab, "white" ,"transparent", "bold", "12" )
        self.heading_label.move(453, 220)

        self.airspeed_label = LabelClass("AIRSPEED",tab, "white" ,"transparent", "bold", "12" )
        self.airspeed_label.move(763, 220)

        self.gpsspeed_label = LabelClass("GPSSPEED",tab, "white" ,"transparent", "bold", "12" )
        self.gpsspeed_label.move(1118, 220)

        self.dikilme_label = LabelClass("DIKILME",tab, "white" ,"transparent", "bold", "12" )
        self.dikilme_label.move(1433, 220)

        self.horizon_label = LabelClass("HORIZON",tab, "white" ,"transparent", "bold", "12" )
        self.horizon_label.move(1727, 220)


        self.sicaklik_frame = FrameClass(parent=tab, width=100, height=25,x_pos=1815,y_pos=950)
        self.dis_sicaklik_frame = FrameClass(parent=tab, width=100, height=25,x_pos=1815,y_pos=970)
        self.sistem_zamani = FrameClass(parent=tab, width=125, height=25,x_pos=1810,y_pos=10)
        self.batarya_kalan = FrameClass(parent=tab, width=50, height=25,x_pos=952,y_pos=465)
        self.yukselik_etiketi = FrameClass(parent=tab, width=40, height=20,x_pos=640,y_pos=772)
        self.heading_frame = FrameClass(parent=tab, width=50, height=20,x_pos=550,y_pos=20)
        self.airspeed_frame = FrameClass(parent=tab, width=50, height=20,x_pos=854,y_pos=20)
        self.amper_frame = FrameClass(parent=tab, width=50, height=20,x_pos=1142,y_pos=550)
        self.gpsspeed_frame = FrameClass(parent=tab, width=50, height=20,x_pos=1210,y_pos=20)
        self.voltaj_frame = FrameClass(parent=tab, width=50, height=20,x_pos=741,y_pos=550)






        self.label_sicaklik = LabelClass("SICAKLIK", self.sicaklik_frame, "white" ,"transparent", "bold", "12")
        label_sicaklik_yazi = LabelClass("FCC Sıcaklık", tab, "white","transparent", "bold", "12")
        label_sicaklik_yazi.move(1727, 953)

        self.sayisalverilertext_label = ["CUSTOM MOD:", "VOLTAj:", "AMPER:", "HEADING:", "ARM DURUMU:",
                                         "YERDEN YÜKSEKLİK:", "DENİZ YÜKSEKLİĞİ:", "BATARYA:", "BASE MOD:",
                                         "GPS SPEED:", "AİR SPEED:", "DEVİR:", "GAZ:", "DİKİLME:",
                                         "YATIŞ:", "YUVARLANMA:"]

        for i in range(16):
            sayisal_veriler_label = LabelClass(self.sayisalverilertext_label[i], tab, "white","transparent", "bold", "12" )
            sayisal_veriler_label.move(1420, 300 + i * 30)



        self.sayisalveriler_label = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15",
                                     "16"]
        self.sayisalveriler_labels = []

        for i in range(16):
            label=LabelClass(self.sayisalveriler_label[i], tab, "white","transparent", "bold", "12",  width=100, height=30)
            label.move(1590, 293 + i * 30)
            self.sayisalveriler_labels.append(label)



        self.imu_labels = ["GPS","INS","MAG","AHRS","EKF","PRE","SICAKLIK"]
        self.imu_frames = []
        for i in range(7):

            box = FrameClass(parent=tab, width=100, height=25,x_pos=1200,y_pos=790+ i * 30)
            LabelClass(self.imu_labels[i], box, "white", "transparent", "bold", "12")
            self.imu_frames.append(box)

        self.motor_labels = ["MOTOR 1","MOTOR 2"]
        self.motor_frames = []

        for i in range(2):

            box = FrameClass(parent=tab, width=100, height=25,x_pos=850,y_pos=290+ i * 350)
            LabelClass(self.motor_labels[i], box, "white", "transparent", "bold", "12")
            self.motor_frames.append(box)

        self.motor_labels_2 = ["MOTOR 3","MOTOR 4"]
        self.motor_frames_2 = []
        for i in range(2):

            box = FrameClass(parent=tab, width=100, height=25,x_pos=1005,y_pos=290+ i * 350)
            LabelClass(self.motor_labels_2[i], box, "white", "transparent", "bold", "12")
            self.motor_frames_2.append(box)

        self.motor_bars = []
        for i in range(4):

            box = FrameClass(parent=tab, width=50, height=200,x_pos=873 + i * 59,y_pos=770)
            label = LabelClass(f"Motor {i+1}", tab, "white", "transparent", "bold", "12")
            label.move(873 + i * 59, 770)

            bar = QProgressBar(box)
            bar.setGeometry(5, 5, 40, 190)
            bar.setStyleSheet("QProgressBar { background-color: #222222; border: none; } "
                              "QProgressBar::chunk { background-color: #00FF00; }")
            bar.setOrientation(Qt.Vertical)
            bar.setMaximum(2000)
            bar.setMinimum(1000)

            self.motor_bars.append(bar)



        self.button= QPushButton('AIRCRAFT TYPE',self)
        self.button.setGeometry(100,80,120,40)
        self.button.setStyleSheet("QPushButton { background-color: #222222; }")
        self.button.move(1700, 900)
        self.button.clicked.connect(self.on_button_click)
        self.aircraft_type = 1


        self.label_dis_sicaklik = QLabel(f"{35:.2f}°C", self.dis_sicaklik_frame)
        self.label_dis_sicaklik.setStyleSheet("color: white; font-weight: bold; font-size: 14px;")
        self.label_dis_sicaklik.setAlignment(Qt.AlignCenter)

        self.label_dis_sicaklik_yazi = QLabel("Dış Sıcaklık", tab)
        self.label_dis_sicaklik_yazi.setStyleSheet("color: white; font-weight: bold;")
        self.label_dis_sicaklik_yazi.move(1730, 974)

        self.global_altitude = altitude_inducator.ScaleWidget(tab)
        self.global_altitude.setGeometry(570, 240, 50, 600)

        self.throttle = altitude_inducator.ScaleWidget(tab)
        self.throttle.setGeometry(1300, 300, 50, 400)



        self.label_batarya = QLabel("BATARYA", self.batarya_kalan)
        self.label_batarya.setStyleSheet("color: white; font-weight: bold; font-size: 14px;")
        self.label_batarya.setAlignment(Qt.AlignCenter)


        for i in range(0, 301, 25):
            label = QLabel(str(i), tab)
            label.setStyleSheet("color: white; font-weight: bold; font-size: 10px")
            label.move(550, int(812 - (i * 1.854)))


        for i in range(0, 101, 10):
            label = QLabel(str(i), tab)
            label.setStyleSheet("color: white; font-weight: bold; font-size: 10px")
            label.move(1270, 670 - int((i * 3.5)))



        self.label_yukseklik_etiketi = LabelClass("YUKSEKLIK", tab , "white", "transparent", "bold", "12")
        self.label_yukseklik_etiketi.setAlignment(Qt.AlignCenter)
        self.label_yukseklik_etiketi.move(640,772)


        self.yellow_arrow = yellow_arrow.YellowArrow(tab)
        self.yellow_arrow.setGeometry(100, 100, 100, 80)  # Adjust position and size as needed
        self.yellow_arrow.set_angle(270)
        self.yellow_arrow.move(605,500)



        self.yellow_arrow_throttle = yellow_arrow.YellowArrow(tab)
        self.yellow_arrow_throttle.setGeometry(100, 100, 100, 80)  # Adjust position and size as needed
        self.yellow_arrow_throttle.set_angle(270)
        self.yellow_arrow_throttle.move(1302, 630)



        self.sistem_zamanı_label = LabelClass("ZAMAN", self.sistem_zamani, "white", "transparent", "bold", "12")
        self.sistem_zamanı_label.setAlignment(Qt.AlignCenter)


        self.label_heading = LabelClass("HEADING", self.heading_frame, "white", "transparent", "bold", "12")
        self.label_heading.setAlignment(Qt.AlignCenter)



        self.label_airspeed = LabelClass("AIRSPEED", self.airspeed_frame, "white", "transparent", "bold", "12")
        self.label_airspeed.setAlignment(Qt.AlignCenter)



        self.label_gpsspeed = LabelClass("GPSSPEED", self.gpsspeed_frame, "white", "transparent", "bold", "12")
        self.label_gpsspeed.setAlignment(Qt.AlignCenter)

        self.voltaj_text_label = LabelClass("VOLTAJ", tab, "white", "transparent", "bold", "12")
        self.voltaj_text_label.setAlignment(Qt.AlignCenter)
        self.voltaj_text_label.move(743,530)

        self.amper_text_label = LabelClass("AMPER", tab, "white", "transparent", "bold", "12")
        self.amper_text_label.setAlignment(Qt.AlignRight)
        self.amper_text_label.move(1145, 530)

        self.batarya_text_label = LabelClass("BATARYA", tab, "white", "transparent", "bold", "12")
        self.batarya_text_label.setAlignment(Qt.AlignCenter)
        self.batarya_text_label.move(950, 500)

        self.status_text_box = QTextEdit(tab)
        self.status_text_box.setReadOnly(True)
        self.status_text_box.setStyleSheet("background-color: gray; color: white; font-size: 12px;")
        self.status_text_box.setGeometry(1340, 845, 300, 150)  # (x, y, width, height)


        self.label_voltaj = LabelClass("VOLTAJ", self.voltaj_frame, "white", "transparent", "bold", "12")
        self.label_voltaj.setAlignment(Qt.AlignCenter)



        self.label_amper = LabelClass("AMPER", tab, "white", "transparent", "bold", "12")
        self.label_amper.setAlignment(Qt.AlignCenter)
        self.label_amper.move(1154, 554)

        self.label_yerden = LabelClass("YERDEN", tab, "white", "transparent", "bold", "13")
        self.label_yerden.setAlignment(Qt.AlignCenter)
        self.label_yerden.move(525, 830)



        self.haberlesme_label = LabelClass("HABERLEŞME", tab, "white", "transparent", "bold", "16")
        self.haberlesme_label.setAlignment(Qt.AlignCenter)
        self.haberlesme_label.move(1340, 820)


        self.mode_frame = QLabel(tab)
        self.mode_frame.setGeometry(935, 345, 150, 25)
        self.mode_frame.setStyleSheet("background: transparent;")

        self.label_mode = LabelClass("HEARTBEAT", self.mode_frame, "white", "transparent", "bold", "12")
        self.label_mode.setAlignment(Qt.AlignCenter)

        tab.setStyleSheet("background-color: #000000;")

        self.airspeed_needle = NeedleDoksanDerece(tab)
        self.airspeed_needle.setNeedleSize(80, 5)
        self.airspeed_needle.move(701,22)

        self.gpsspeed_needle = NeedleDoksanDerece(tab)
        self.gpsspeed_needle.setNeedleSize(80, 5)
        self.gpsspeed_needle.move(1056, 22)

        self.devir_needle = NeedleDoksanDerece(tab)
        self.devir_needle.setNeedleSize(80, 5)
        self.devir_needle.move(81, 22)

        self.voltaj_needle = NeedleYuzdenSifira(tab)
        self.voltaj_needle.setNeedleSize(75, 5)
        self.voltaj_needle.move(669, 400)

        self.amper_needle = NeedleSifirdanYuze(tab)
        self.amper_needle.setNeedleSize(75, 5)
        self.amper_needle.move(1070, 400)

        self.box_loop_dizi = []




















        for i in range(16):
            box_loop = QFrame(tab)
            box_loop.setFrameShape(QFrame.Box)
            box_loop.setStyleSheet("background-color: #000000; border: 1px solid white;")
            box_loop.setFixedSize(12, 12)
            box_loop.move(1385, 302 + i * 30)
            self.box_loop_dizi.append(box_loop)




       

       
       
       

        self.update
        return tab

















    def update_progress_bars(self, data):
        for i, bar in enumerate(self.motor_bars):
            bar.setValue(data[f"servo{i+1}"])





    def update_temperature(self, temperature):
        self.label_sicaklik.setText(f"{temperature:.2f}°C")
        if 30 < temperature < 40:
            self.label_sicaklik.setStyleSheet("background-color: #00FF00;")
            self.imu_frames[6].setStyleSheet("background-color: #00FF00; border: 2px solid white;")
        elif temperature < 30:
            self.label_sicaklik.setStyleSheet("background-color: #FF0000;")
            self.imu_frames[6].setStyleSheet("background-color: #FF0000; border: 2px solid white;")

    def update_altitude(self, relative_alt):
        global_yukseklik = int(relative_alt)
        self.label_yukseklik_etiketi.setText(f"{global_yukseklik}")
        yeni_y = 819 - (global_yukseklik * 1.9)
        yeni_y = max(50, min(yeni_y, 819))
        self.label_yukseklik_etiketi.move(640, int(yeni_y-8))
        self.yukselik_etiketi.move(638, int(yeni_y-10))
        self.yellow_arrow.move(572, int(yeni_y - 40))
        self.sayisalveriler_labels[5].setText(f"{relative_alt}")

        if relative_alt <5:
            self.box_loop_dizi[13].setStyleSheet("background-color: #FF0000; border: 1px solid white;")
        elif relative_alt >=5:
            self.box_loop_dizi[13].setStyleSheet("background-color: #00FF00; border: 1px solid white;")


    def update_throttle(self, chan3_raw):
        throttle = int(chan3_raw)
        yeni_y = 630 - (throttle * 3.58)
        yeni_y = max(50, min(yeni_y, 630))
        self.yellow_arrow_throttle.move(1302, int(yeni_y)+12)
        self.sayisalveriler_labels[12].setText(f"{throttle}")

    def update_arm(self, base_mode):

        if base_mode == True:
            self.motor_frames[0].setStyleSheet("background-color: #00FF00; border: 2px solid white;")
            self.motor_frames[1].setStyleSheet("background-color: #00FF00; border: 2px solid white;")
            self.motor_frames_2[0].setStyleSheet("background-color: #00FF00; border: 2px solid white;")
            self.motor_frames_2[1].setStyleSheet("background-color: #00FF00; border: 2px solid white;")
        elif base_mode == False:
            self.motor_frames[0].setStyleSheet("background-color: #FF0000; border: 2px solid white;")
            self.motor_frames[1].setStyleSheet("background-color: #FF0000; border: 2px solid white;")
            self.motor_frames_2[0].setStyleSheet("background-color: #FF0000; border: 2px solid white;")
            self.motor_frames_2[1].setStyleSheet("background-color: #FF0000; border: 2px solid white;")
        self.sayisalveriler_labels[8].setText(f"{base_mode}")
    def updated_ins(self, ins_healthy):

        if ins_healthy == True:
            self.imu_frames[1].setStyleSheet("background-color: #00FF00; border: 1px solid white;")

        elif ins_healthy == False:
            self.imu_frames[1].setStyleSheet("background-color: #FF0000; border: 1px solid white;")


    def updated_mag(self, mag_healthy):

        if mag_healthy == True:
            self.imu_frames[2].setStyleSheet("background-color: #00FF00; border: 1px solid white;")

        elif mag_healthy == False:
            self.imu_frames[2].setStyleSheet("background-color: #FF0000; border: 1px solid white;")


    def updated_ahrs(self, ahrs_healthy):
        if ahrs_healthy == True:
            self.imu_frames[3].setStyleSheet("background-color: #00FF00; border: 1px solid white;")

        elif ahrs_healthy == False:
            self.imu_frames[3].setStyleSheet("background-color: #FF0000; border: 1px solid white;")


    def updated_ekf(self, ekf_healthy):
        if ekf_healthy == True:
            self.imu_frames[4].setStyleSheet("background-color: #00FF00; border: 1px solid white;")

        elif ekf_healthy == False:
            self.imu_frames[4].setStyleSheet("background-color: #FF0000; border: 1px solid white;")


    def updated_pre(self, pre_healthy):
        if pre_healthy == True:
            self.imu_frames[5].setStyleSheet("background-color: #00FF00; border: 1px solid white;")

        elif pre_healthy == False:
            self.imu_frames[5].setStyleSheet("background-color: #FF0000; border: 1px solid white;")

    def updated_system_time(self, time_unix_usec, time_boot_ms):
        self.label_sistem_zamani.setText(f"{time_unix_usec}, {time_boot_ms}")

    def add_status_message(self, message):
        """STATUSTEXT mesajlarını ekler ve en son mesaja kaydırır"""
        self.status_text_box.append(message)

        # Otomatik olarak en son mesaja kaydır
        scrollbar = self.status_text_box.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())


    def updated_gps_count(self, satellite_count):
        if satellite_count > 9:
            self.imu_frames[0].setStyleSheet("background-color: #00FF00; border: 1px solid white;")
        elif satellite_count < 10:
            self.imu_frames[0].setStyleSheet("background-color: #FF0000; border: 1px solid white;")


    def updated_battery(self, voltage,current,remaining):

        self.label_batarya.setText(f"%{remaining}")
        self.label_voltaj.setText(f"{voltage}")
        self.label_amper.setText(f"{current}")
        self.sayisalveriler_labels[1].setText(f"{voltage}")
        self.sayisalveriler_labels[2].setText(f"{current}")
        self.sayisalveriler_labels[7].setText(f"{remaining}")

        self.voltaj_needle.setAirspeed(voltage)
        self.amper_needle.setAirspeed(current)


        image_index = 15 - int((remaining / 100.0) * 15)
        image_index = max(1, min(image_index, 15))  # 1 ile 15 arasında sınırla

        self.resim_yolu = f"batarya/{image_index}.png"

        self.update_battery_image()

        if voltage <= 19.5:
            self.box_loop_dizi[9].setStyleSheet("background-color: #FF0000; border: 1px solid white;")
        elif 19.5 < voltage <= 20:
            self.box_loop_dizi[9].setStyleSheet("background-color: #FFFF00; border: 1px solid white;")
        elif voltage > 20:
            self.box_loop_dizi[9].setStyleSheet("background-color: #00FF00; border: 1px solid white;")

        if current < 45:
            self.box_loop_dizi[10].setStyleSheet("background-color: #00FF00; border: 1px solid white;")
        elif current >= 45:
            self.box_loop_dizi[10].setStyleSheet("background-color: #FF0000; border: 1px solid white;")

        if remaining < 30:
            self.box_loop_dizi[15].setStyleSheet("background-color: #FF0000; border: 1px solid white;")
        elif remaining >= 40:
            self.box_loop_dizi[15].setStyleSheet("background-color: #00FF00; border: 1px solid white;")



    def update_battery_image(self):
        new_pixmap = QPixmap(self.resim_yolu)
        scaled_pixmap = new_pixmap.scaled(180, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        self.ibre_batarya_100.setPixmap(scaled_pixmap)




    def updated_vfr(self,heading, airspeed, groundspeed, altitude, climb, throttle):

        self.label_heading.setText(f"{heading}")
        self.label_airspeed.setText(f"{airspeed}")
        self.label_gpsspeed.setText(f"{groundspeed}")
        self.sayisalveriler_labels[3].setText(f"{heading}")
        self.sayisalveriler_labels[10].setText(f"{airspeed}")
        self.sayisalveriler_labels[9].setText(f"{groundspeed}")
        self.airspeed_needle.setAirspeed(airspeed)
        self.gpsspeed_needle.setAirspeed(groundspeed)
        self.sayisalveriler_labels[6].setText(f"{altitude}")



        pixmap = QPixmap("images/ibre5.png")
        scaled_pixmap = pixmap.scaled(200, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        transform = QTransform()
        cx, cy = scaled_pixmap.width() / 2, scaled_pixmap.height() / 2

        transform.translate(cx, cy)
        transform.rotate(-heading)
        transform.translate(-cx, -cy)

        rotated_pixmap = scaled_pixmap.transformed(transform, Qt.SmoothTransformation)

        self.ibre_heading.setPixmap(rotated_pixmap)
        self.ibre_heading.setFixedSize(rotated_pixmap.size())


        label_x = 330 - rotated_pixmap.width() // 2 + 161
        label_y = 20 - rotated_pixmap.height() // 2 + 98
        self.ibre_heading.move(label_x, label_y)

        if groundspeed > 25:
            self.box_loop_dizi[1].setStyleSheet("background-color: #FF0000; border: 1px solid white;")

        elif groundspeed < 25:
            self.box_loop_dizi[1].setStyleSheet("background-color: #00FF00; border: 1px solid white;")



        if airspeed > 25:
            self.box_loop_dizi[2].setStyleSheet("background-color: #FF0000; border: 1px solid white;")
            
        elif airspeed < 25:
            self.box_loop_dizi[2].setStyleSheet("background-color: #00FF00; border: 1px solid white;")


    def mete_updated(self, modes):
        try:

            mode_text = ""
            if modes == 0:
                mode_text = "STABILIZE"
            elif modes == 1:
                mode_text = "ACRO"
            elif modes == 2:
                mode_text = "ALT_HOLD"
            elif modes == 3:
                mode_text = "AUTO"
            elif modes == 4:
                mode_text = "GUIDED"
            elif modes == 5:
                mode_text = "LOITER"
            elif modes == 6:
                mode_text = "RTL"
            elif modes == 7:
                mode_text = "CIRCLE"
            elif modes == 9:
                mode_text = "LAND"
            else:
                mode_text = f"UNKNOWN ({mode_text})"

            self.label_mode.setText(f"{mode_text}")
            self.sayisalveriler_labels[0].setText(f"{mode_text}")
        except Exception as e:
            print(f"Error in heartbeat_guncelleme: {e}")

    def updated_attitude(self, roll, pitch, yaw):
        self.sayisalveriler_labels[13].setText(f"{int(pitch)}")
        self.sayisalveriler_labels[14].setText(f"{int(roll)}")
        self.sayisalveriler_labels[15].setText(f"{int(yaw)}")

        original_pixmap = QPixmap("images/yan.png")
        scaled_pixmap = original_pixmap.scaled(125, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        # Transform ile döndürme işlemi
        transform = QTransform()
        transform.rotate(roll)  # Negatif yön, çünkü burun yukarı açıldığında resim aşağı kaymalı




        # Yeni döndürülmüş pixmap oluştur (Ölçek korunuyor)
        rotated_pixmap = scaled_pixmap.transformed(transform, Qt.SmoothTransformation)

        self.yan_goruntu.setStyleSheet("background-color: transparent;")
        self.yan_goruntu.setPixmap(rotated_pixmap)

        original_pixmap_2 = QPixmap("images/on.png")
        scaled_pixmap_2 = original_pixmap_2.scaled(125, 500, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        # Transform ile döndürme işlemi
        transform_2 = QTransform()
        transform_2.rotate(yaw)



        # Yeni döndürülmüş pixmap oluştur (Ölçek korunuyor)
        rotated_pixmap_2 = scaled_pixmap_2.transformed(transform_2, Qt.SmoothTransformation)
        self.on_goruntu.move(1685, 110)
        self.on_goruntu.setStyleSheet("background-color: transparent;")
        self.on_goruntu.setPixmap(rotated_pixmap_2)

    def update_all(self):
        self.update()





    def on_button_click(self):
        if self.aircraft_type == 1:
            self.o = "images/drone_on.png"
            self.y = "images/drone_yan.png"
            self.u = "images/drone_ust.png"
            self.o_h = 810
            self.y_h = 150
            self.u_h = 78
            self.o_w = 150
            self.y_w = 600
            self.u_w = 320
            self.aircraft_type = 2
            print(self.aircraft_type)
        else:
            self.o = "images/on.png"
            self.y = "images/yan.png"
            self.u = "images/ust.png"
            self.o_h = 630
            self.y_h = 40
            self.u_h = 58
            self.o_w = 130
            self.y_w = 300
            self.u_w = 300
            self.aircraft_type = 1
            print(self.aircraft_type)
        self.update_images()


    def update_images(self):
        # on_goruntu resmini güncelle
        # on_goruntu resmini güncelle
        new_pixmap_o = QPixmap(self.o)
        scaled_pixmap_o = new_pixmap_o.scaled(self.o_w, self.o_h, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.on.setPixmap(scaled_pixmap_o)

        # yan_goruntu resmini güncelle
        new_pixmap_y = QPixmap(self.y)
        scaled_pixmap_y = new_pixmap_y.scaled(self.y_w, self.y_h, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.yan.setPixmap(scaled_pixmap_y)

        # ust_goruntu resmini güncelle
        new_pixmap_u = QPixmap(self.u)
        scaled_pixmap_u = new_pixmap_u.scaled(self.u_w, self.u_h, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.ust.setPixmap(scaled_pixmap_u)




if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())