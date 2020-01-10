"""
TODO intro and info here

Todo:
    DPI selection in gui ?
    Specify output folder in gui
    Separate large files in batches (maybe every 50 pages? clear temp folder in between)
    Add and test more file formats for the output
"""
import os

from PyQt5 import QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from pdf2image import pdf2image


# This thread handles the conversion from PDF to Image files
class Thread_Images(QThread):
    # Signals
    signal_progress = pyqtSignal(int)
    signal_message = pyqtSignal([str], [str, int])
    signal_toggle_ui = pyqtSignal(bool)

    def __init__(self, save_path, listFiles_paths, option_output_format):
        """ Thread object constructor
            params:
            save_path
            listFiles_paths
            option_output_format
        """
        QThread.__init__(self)
        # Set thread variables
        self.save_path = save_path
        self.paths = listFiles_paths
        self.option_output_format = option_output_format
        self.progress = 0
        self.message = ""
        pass

    def __del__(self):
        self.wait()

    def run(self):
        # Create the _TEMP folder if it doesn't exist
        if not os.path.exists("_TEMP"):
            os.mkdir("_TEMP")

        # Loop through list and process each pdf
        for i in range(len(self.paths)):
            self.progress = int(i / len(self.paths) * 100)
            self.convert_pdf(self.paths[i])

        self.signal_toggle_ui.emit(True)

    def convert_pdf(self, path):
        # This file paths
        this_file_prefix = os.path.splitext(os.path.split(path)[1])[0]
        this_save_path = os.path.join(self.save_path, this_file_prefix)

        # Create the output folder if it doesn't exist
        if not os.path.exists(this_save_path):
            os.mkdir(this_save_path)

        # Signal info to the main thread
        self.signal_progress.emit(self.progress)
        self.signal_message.emit(f"Now reading pages from {path}.. this might take a while")

        # Convert the pdf into an array of images (stored in the _TEMP folder)
        images = pdf2image.convert_from_path(path, dpi=72, output_folder="_TEMP")

        # Save each Image
        counter = 1
        for img in images:
            # Signal info to the main thread
            self.signal_message.emit(f"From {path}: Saving page {counter} of {len(images)}")
            this_progress = int((counter / len(images) * 100) / len(self.paths))
            this_total_progress = self.progress + this_progress
            self.signal_progress.emit(this_total_progress)

            # Save the image
            img.save(os.path.join(this_save_path, f"{this_file_prefix}_{counter}.{self.option_output_format}"), self.option_output_format)
            img.close()
            counter += 1

        self.signal_message.emit(f"Clearing the _TEMP folder...")
        for temp_file in os.listdir("_TEMP"):
            os.remove(os.path.join("_TEMP", temp_file))
        self.signal_message[str, int].emit(f"{path} processed successfully into {len(images)} images.", 2000)


# Class for the PDF to Image converter tool
class Screen_PDFToImage(QWidget):
    # Class global variables
    parent = None
    default_save_path = f"{os.sep.join((os.path.expanduser('~'), 'Desktop'))}"
    allowed_file_extensions = ["pdf"]
    image_thread = None
    # Explicit all variable types for items inherited from the .ui file
    central_widget: QStackedWidget
    statusbar: QStatusBar
    listFiles: QListWidget
    progressBar: QProgressBar
    btnBrowse: QPushButton
    btnGetImages: QPushButton
    btnDelete: QPushButton
    btnDeleteAll: QPushButton
    btnDuplicate: QPushButton
    btnBack: QPushButton
    comboFormat: QComboBox
    txtPrefix: QLineEdit

    def __init__(self, parent=None):
        # noinspection PyArgumentList
        super(Screen_PDFToImage, self).__init__()

        # Set class variables
        self.parent = parent
        self.statusbar = parent.statusbar
        self.central_widget = parent.central_widget

        # noinspection SpellCheckingInspection
        loadUi("ui/screen_pdftoimage.ui", self)  # Load the tool's UI from file

        # Connect all UI items to their respective function
        self.btnGetImages.clicked.connect(self.click_get_images)
        self.btnBrowse.clicked.connect(self.click_browse)
        self.btnDuplicate.clicked.connect(self.click_duplicate)
        self.btnDelete.clicked.connect(self.click_delete)
        self.btnDeleteAll.clicked.connect(self.click_delete_all)
        self.btnBack.clicked.connect(self.click_back)

        # The progress bar should be only visible while working on the images
        self.progressBar.setVisible(False)

    def click_get_images(self):
        # If the Gui's list is empty, do nothing
        if self.listFiles.count() == 0:
            return

        # Retrieve all paths from the list, they will be set to the pdf thread
        listFiles_paths = []
        for i in range(0, self.listFiles.count()):
            listFiles_paths.append(self.listFiles.item(i).text())
        # Retrieve UI options
        option_output_format = self.comboFormat.currentText()
        # Lock UI elements
        self.toggle_ui(False)

        # Define and start the conversion thread
        self.image_thread = Thread_Images(save_path=f"{self.default_save_path}", listFiles_paths=listFiles_paths,
                                          option_output_format=option_output_format)
        self.image_thread.start()
        # Link thread's signals
        self.image_thread.signal_progress.connect(self.progressBar.setValue)
        self.image_thread.signal_message[str].connect(self.statusbar.showMessage)
        self.image_thread.signal_message[str, int].connect(self.statusbar.showMessage)
        self.image_thread.signal_toggle_ui.connect(self.toggle_ui)
        pass

    def toggle_ui(self, is_active):
        self.btnGetImages.setDisabled(not is_active)
        self.btnBack.setDisabled(not is_active)
        self.progressBar.setVisible(not is_active)
        pass

    def click_browse(self):
        # Open windows' item browser with specifications
        file_names, _selectedFilter = QtWidgets.QFileDialog.getOpenFileNames(caption="Select images",
                                                                             directory=os.sep.join(
                                                                                 (os.path.expanduser('~'), 'Desktop')),
                                                                             filter="PDF files(*.pdf)"
                                                                             )
        # Add items to the list
        self.listFiles.addItems(file_names)

    def click_duplicate(self):
        # Get selected items
        selected_items = self.listFiles.selectedItems()
        # No selection ? do nothing
        if not selected_items:
            return
        #
        for item in selected_items:
            # Add the item to the list
            self.listFiles.addItem(item.text())

    def click_delete(self):
        # Get selected items
        selected_items = self.listFiles.selectedItems()
        # No selection ? do nothing
        if not selected_items:
            return
        #
        for item in selected_items:
            # Remove the item from the list
            self.listFiles.takeItem(self.listFiles.row(item))

    def click_delete_all(self):
        # Remove every item from the file list
        for i in range(0, self.listFiles.count()):
            self.listFiles.takeItem(0)

    def click_back(self):
        self.central_widget.removeWidget(self)
