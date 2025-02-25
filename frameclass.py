from PyQt5.QtWidgets import QFrame
from PyQt5.QtCore import Qt

class FrameClass(QFrame):
    def __init__(self, parent, width, height, x_pos, y_pos):
        super().__init__(parent)

        self.width = width
        self.height = height
        self.x_pos = x_pos
        self.y_pos = y_pos

        self.setFrameShape(QFrame.Box)
        self.setStyleSheet("background-color: #000000; border: 1px solid white ")
        self.setFixedSize(width, height)
        self.move(x_pos, y_pos)


