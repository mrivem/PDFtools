"""
TODO intro and info here

Todo:
    Document code
"""
import gc
import os
from datetime import datetime

from PyPDF2 import PdfFileMerger
from PyQt5 import QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi


class Thread_Merge(QThread):
    # Signals
    signal_progress = pyqtSignal(int)
    signal_message = pyqtSignal([str], [str, int])
    signal_toggle_ui = pyqtSignal(bool)

    def __init__(self, save_path, output_file_name, listFiles_paths):
        QThread.__init__(self)
        self.save_path = save_path
        self.file_name = output_file_name
        self.paths = listFiles_paths

    def __del__(self):
        self.wait()

    def run(self):
        progress = 0
        self.signal_progress.emit(progress)
        self.signal_message.emit(f"Starting merging process.")

        pdf_merger = PdfFileMerger()
        i = 1
        for path in self.paths:
            progress = int(i / len(self.paths) * 100)
            self.signal_progress.emit(progress)
            self.signal_message.emit(f"Now merging {i} of {len(self.paths)}: {path}")

            pdf_merger.append(path)
            i += 1
        self.signal_message.emit(f"Writing final PDF to destination.. this might take a while for large files.")
        pdf_merger.write(os.path.join(self.save_path, f"{self.file_name}.PDF"))
        pdf_merger.close()

        self.signal_message[str, int].emit(f"{len(self.paths)} files merged successfully into {self.file_name}.PDF", 2000)
        self.signal_toggle_ui.emit(True)

        gc.collect()


class Screen_MergePDF(QWidget):
    # Class global variables
    parent = None
    default_save_path = f"{os.sep.join((os.path.expanduser('~'), 'Desktop'))}"
    allowed_file_extensions = ["pdf"]
    merge_thread = None

    # Explicit all variable types for items inherited from the .ui file
    central_widget: QStackedWidget
    statusbar: QStatusBar

    listFiles: QListWidget
    progressBar: QProgressBar
    btnBrowse: QPushButton
    btnMerge: QPushButton
    btnDelete: QPushButton
    btnDeleteAll: QPushButton
    btnBack: QPushButton
    txtFileName: QLineEdit

    def __init__(self, parent=None):
        super(Screen_MergePDF, self).__init__()

        self.parent = parent
        self.statusbar = parent.statusbar
        self.central_widget = parent.central_widget

        loadUi("ui/screen_mergepdf.ui", self)

        # Connect all UI items to their respective function
        self.btnMerge.clicked.connect(self.click_merge)
        self.btnBrowse.clicked.connect(self.click_browse)
        self.btnDelete.clicked.connect(self.click_delete)
        self.btnDeleteAll.clicked.connect(self.click_delete_all)
        self.btnBack.clicked.connect(self.click_back)

        # The progress bar should be only visible while working on the PDFs
        self.progressBar.setVisible(False)

    def click_merge(self):
        # If the Gui's list is empty, do nothing
        if self.listFiles.count() == 0:
            return
        # Read the file name from the text box
        output_file_name = self.txtFileName.text()
        # Text blank? Generate one based on the date with YearMonthDay_Hour-Minute-Second format
        if output_file_name == "":
            output_file_name = datetime.now().strftime("%Y%m%d_%H-%M-%S")

        # Keep on renaming if file exist
        if os.path.exists(f"{self.default_save_path}/{output_file_name}.pdf"):
            output_file_name = self.generate_file_name(output_file_name)

        # Retrieve all paths from the list, they will be set to the pdf thread
        listFiles_paths = []
        for i in range(0, self.listFiles.count()):
            listFiles_paths.append(self.listFiles.item(i).text())

        # Lock UI elements
        self.toggle_ui(False)

        # Define and start the merging thread
        self.merge_thread = Thread_Merge(save_path=self.default_save_path, output_file_name=output_file_name, listFiles_paths=listFiles_paths)
        self.merge_thread.start()
        # Link thread's signals
        self.merge_thread.signal_progress.connect(self.progressBar.setValue)
        self.merge_thread.signal_message[str].connect(self.statusbar.showMessage)
        self.merge_thread.signal_message[str, int].connect(self.statusbar.showMessage)
        self.merge_thread.signal_toggle_ui.connect(self.toggle_ui)

    # Toggles some UI elements while working on a file
    def toggle_ui(self, is_activated):
        # Disable these buttons
        self.btnMerge.setDisabled(not is_activated)
        self.btnBack.setDisabled(not is_activated)
        # Show progress bar
        self.progressBar.setVisible(not is_activated)

    # Helper function to append a '(#)' to the file name until it finds one unused (maybe it's not the best approach)
    def generate_file_name(self, file_name, i=1):
        if os.path.exists(f"{self.default_save_path}/{file_name}({i}).pdf"):
            return self.generate_file_name(file_name, i + 1)
        else:
            return f"{file_name}({i})"

    def click_browse(self):
        # Open windows' item browser with specifications
        file_names, _selectedFilter = QtWidgets.QFileDialog.getOpenFileNames(caption="Select images",
                                                                             directory=os.sep.join(
                                                                                 (os.path.expanduser('~'), 'Desktop')),
                                                                             filter="PDF files(*.pdf)"
                                                                             )
        # Add items to the list
        self.listFiles.addItems(file_names)

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
        del self
