from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi

from Screen_ImageToPDF import Screen_ImageToPDF
from Screen_MergePDF import Screen_MergePDF
from Screen_PDFToImage import Screen_PDFToImage
from Screen_RotatePDF import Screen_RotatePDF
from Screen_SplitPDF import Screen_SplitPDF


class Screen_ToolSelection(QWidget):
    parent = None

    btn_imagetopdf: QPushButton
    btn_pdftoimage: QPushButton
    btn_pdfmerge: QPushButton
    btn_pdfsplit: QPushButton
    btn_pdfrotate: QPushButton
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
        self.btn_pdfmerge.clicked.connect(self.click_pdfmerge)
        self.btn_pdfsplit.clicked.connect(self.click_pdfsplit)
        self.btn_pdfrotate.clicked.connect(self.click_pdfrotate)

    def post_load(self):
        if self.DEBUG_INITIAL_TOOL:
            if self.DEBUG_INITIAL_TOOL == "imgtopdf":
                self.click_imagetopdf()
            if self.DEBUG_INITIAL_TOOL == "pdftoimage":
                self.click_pdftoimage()
            if self.DEBUG_INITIAL_TOOL == "mergepdf":
                self.click_pdfmerge()
            if self.DEBUG_INITIAL_TOOL == "splitpdf":
                self.click_pdfsplit()
            if self.DEBUG_INITIAL_TOOL == "rotatepdf":
                self.click_pdfrotate()

    def click_imagetopdf(self):
        self.screen_imgtopdf = Screen_ImageToPDF(self)
        self.central_widget.addWidget(self.screen_imgtopdf)
        self.central_widget.setCurrentWidget(self.screen_imgtopdf)

    def click_pdftoimage(self):
        self.screen_pdftoimage = Screen_PDFToImage(self)
        self.central_widget.addWidget(self.screen_pdftoimage)
        self.central_widget.setCurrentWidget(self.screen_pdftoimage)

    def click_pdfmerge(self):
        self.screen_mergepdf = Screen_MergePDF(self)
        self.central_widget.addWidget(self.screen_mergepdf)
        self.central_widget.setCurrentWidget(self.screen_mergepdf)

    def click_pdfsplit(self):
        self.screen_splitpdf = Screen_SplitPDF(self)
        self.central_widget.addWidget(self.screen_splitpdf)
        self.central_widget.setCurrentWidget(self.screen_splitpdf)

    def click_pdfrotate(self):
        self.screen_rotatepdf = Screen_RotatePDF(self)
        self.central_widget.addWidget(self.screen_rotatepdf)
        self.central_widget.setCurrentWidget(self.screen_rotatepdf)
