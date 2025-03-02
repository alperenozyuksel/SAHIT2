from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


class ImageLabel(QLabel):
    def __init__(self, parent, width, height, x_pos, y_pos, image_path):
        super().__init__(parent)
        self.image_path = image_path
        self.width = width
        self.height = height
        self.x_pos = x_pos
        self.y_pos = y_pos

        pixmap = QPixmap(image_path)
        scaled_pixmap = pixmap.scaled(width, height, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        self.setPixmap(scaled_pixmap)

        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("background-color: transparent;")

        self.move(x_pos, y_pos)




