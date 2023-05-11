from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel

from view import font_title, palette_title


class Title(QLabel):
    def __init__(self, text: str):
        super().__init__(text)
        self.setFont(font_title)
        self.setPalette(palette_title)
        self.setAlignment(Qt.AlignCenter)
