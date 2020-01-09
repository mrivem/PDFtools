import PIL
from PIL import Image, ImageOps
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from Screen_ImageToPDF import Screen_ImageToPDF
import os


class Screen_ToolSelection(QWidget):
    parent = None

    btn_imgtopdf: QPushButton
    btn_none_1: QPushButton
    central_widget: QStackedWidget

    DEBUG_INITIAL_TOOL = ""

    def __init__(self, parent=None):
        super(Screen_ToolSelection, self).__init__()

        self.parent = parent
        self.statusbar = parent.statusbar

        loadUi("ui/screen_toolselection.ui", self)

        self.central_widget = parent.central_widget

        self.btn_imgtopdf.clicked.connect(self.click_imgtopdf)
        self.btn_none_1.clicked.connect(self.click_test)

    def post_load(self):
        if self.DEBUG_INITIAL_TOOL:
            if self.DEBUG_INITIAL_TOOL == "imgtopdf":
                self.click_imgtopdf()

    def click_imgtopdf(self):
        self.screen_imgtopdf = Screen_ImageToPDF(self)
        self.central_widget.addWidget(self.screen_imgtopdf)
        self.central_widget.setCurrentWidget(self.screen_imgtopdf)

    def click_test(self):
        pass
