from PyQt5.QtWidgets import QFrame, QLabel
from PyQt5.QtCore import Qt

class LabelClass(QLabel):
    def __init__(self, text, parent, color, bg_color, font_weight, font_size, width=None, height=None):
        super().__init__(text, parent)

        self.color = color
        self.bg_color = bg_color
        self.font_size = font_size
        self.font_weight = font_weight

        self.setStyleSheet(f"color: {self.color}; background-color: {self.bg_color}; font-weight: {self.font_weight}; font-size: {self.font_size}px;")
        self.setAlignment(Qt.AlignCenter)

        if width and height:
            self.setFixedSize(width, height)