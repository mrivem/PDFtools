"""
TODO intro and info here

Todo:
    Document code
"""

import os

import PyPDF2
from PyQt5 import QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi


class Thread_Rotate(QThread):
    # Signals
    signal_message = pyqtSignal([str], [str, int])
    signal_toggle_ui = pyqtSignal(bool)

    def __init__(self, save_path, input_file, rotation):
        QThread.__init__(self)
        self.save_path = save_path
        self.input_file = input_file
        self.rotation = rotation

    def __del__(self):
        self.wait()

    def run(self):
        self.signal_message.emit(f"Now rotating {self.input_file} by {self.rotation}°")

        out_file_name = f"{os.path.splitext(os.path.split(self.input_file)[1])[0]}_rotated{self.rotation}.PDF"

        pdfReader = PyPDF2.PdfFileReader(self.input_file)
        pdfWriter = PyPDF2.PdfFileWriter()

        num_pages = pdfReader.getNumPages()
        for page_num in range(num_pages):
            self.signal_message.emit(f"Rotating page {page_num} of {num_pages}")
            page = pdfReader.getPage(page_num)
            page.rotateClockwise(self.rotation)
            pdfWriter.addPage(page)

        self.signal_message.emit(f"Saving the rotated PDF file")
        with open(os.path.join(self.save_path, out_file_name), "wb") as out_file:
            pdfWriter.write(out_file)
            out_file.close()

        self.signal_message[str, int].emit(f"File rotated successfully!", 2000)
        self.signal_toggle_ui.emit(True)


class Screen_RotatePDF(QWidget):
    # Class global variables
    parent = None
    default_save_path = f"{os.sep.join((os.path.expanduser('~'), 'Desktop'))}"
    rotate_thread = None

    # Explicit all variable types for items inherited from the .ui file
    central_widget: QStackedWidget
    statusbar: QStatusBar

    btnBack: QPushButton
    btnRotate: QPushButton
    btnBrowse: QPushButton
    txtInput: QLineEdit
    comboRotation: QComboBox

    def __init__(self, parent=None):
        # noinspection PyArgumentList
        super(Screen_RotatePDF, self).__init__()

        self.parent = parent
        self.statusbar = parent.statusbar
        self.central_widget = parent.central_widget

        loadUi("ui/screen_rotatepdf.ui", self)

        self.btnRotate.clicked.connect(self.click_rotate)
        self.btnBrowse.clicked.connect(self.click_browse)
        self.btnBack.clicked.connect(self.click_back)

    def click_rotate(self):
        if self.txtInput.text() == "":
            return

        input_file = self.txtInput.text()

        # Get rotation
        rotation_index = self.comboRotation.currentIndex()
        # 90 clockwise
        if rotation_index == 0:
            rotation = 90
        # 90 counter clockwise
        elif rotation_index == 1:
            rotation = 270
        # 180 vertical flip
        else:
            rotation = 180

        # Lock UI elements
        self.toggle_ui(False)

        self.rotate_thread = Thread_Rotate(save_path=self.default_save_path, input_file=input_file, rotation=rotation)
        self.rotate_thread.start()
        # Link thread's signals
        self.rotate_thread.signal_message[str].connect(self.statusbar.showMessage)
        self.rotate_thread.signal_message[str, int].connect(self.statusbar.showMessage)
        self.rotate_thread.signal_toggle_ui.connect(self.toggle_ui)

    def toggle_ui(self, is_activated):
        # Disable these buttons
        self.btnRotate.setDisabled(not is_activated)
        self.btnBack.setDisabled(not is_activated)

    def click_browse(self):
        # Open windows' item browser with specifications
        file_name, _selectedFilter = QtWidgets.QFileDialog.getOpenFileName(caption="Select images",
                                                                           directory=os.sep.join(
                                                                               (os.path.expanduser('~'), 'Desktop')),
                                                                           filter="PDF files(*.pdf)"
                                                                           )
        # If nothing was selected, do nothing
        if not file_name:
            return
        # Set the path to the input path box
        self.txtInput.setText(file_name)

    def click_back(self):
        self.central_widget.removeWidget(self)
        del self
