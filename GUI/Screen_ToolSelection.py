from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi

from Screen_ImageToPDF import Screen_ImageToPDF
from Screen_PDFToImage import Screen_PDFToImage


class Screen_ToolSelection(QWidget):
    parent = None

    btn_imagetopdf: QPushButton
    btn_pdftoimage: QPushButton
    central_widget: QStackedWidget

    DEBUG_INITIAL_TOOL = ""

    def __init__(self, parent=None):
        super(Screen_ToolSelection, self).__init__()

        self.parent = parent
        self.statusbar = parent.statusbar

        loadUi("ui/screen_toolselection.ui", self)

        self.central_widget = parent.central_widget

        self.btn_imagetopdf.clicked.connect(self.click_imagetopdf)
        self.btn_pdftoimage.clicked.connect(self.click_pdftoimage)

    def post_load(self):
        if self.DEBUG_INITIAL_TOOL:
            if self.DEBUG_INITIAL_TOOL == "imgtopdf":
                self.click_imagetopdf()
            if self.DEBUG_INITIAL_TOOL == "pdftoimage":
                self.click_pdftoimage()

    def click_imagetopdf(self):
        self.screen_imgtopdf = Screen_ImageToPDF(self)
        self.central_widget.addWidget(self.screen_imgtopdf)
        self.central_widget.setCurrentWidget(self.screen_imgtopdf)

    def click_pdftoimage(self):
        self.screen_pdftoimage = Screen_PDFToImage(self)
        self.central_widget.addWidget(self.screen_pdftoimage)
        self.central_widget.setCurrentWidget(self.screen_pdftoimage)

    def click_test(self):
        pass
