from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi


class Screen_ToolSelection(QWidget):
    parent = None

    btn_imgtopdf: QPushButton

    def __init__(self, parent=None):
        super(Screen_ToolSelection, self).__init__()

        self.parent = parent

        loadUi("ui/screen_toolselection.ui", self)

        self.btn_imgtopdf.clicked.connect(self.click_imgtopdf)

    def click_imgtopdf(self):
        self.parent.central_widget.setCurrentWidget(self.parent.screen_imgtopdf)
