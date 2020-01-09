"""
    TODO: intro to class and tool usage

"""
# PyQt5 Gui components
import PIL
from PyQt5 import QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
# External modules
from PIL import Image, ImageOps
from PyPDF2 import PdfFileMerger
# Python modules
from datetime import datetime
import os
# Memory management and debugging modules
import gc
from guppy import hpy

h = hpy()


# This thread handles all the conversion heavy weight
class ThreadPDF(QThread):
    # Signals
    signal_progress = pyqtSignal(int)
    signal_message = pyqtSignal([str], [str, int])  # Overloaded to accept different types of params
    signal_toggle_ui = pyqtSignal(bool)

    BATCH_SIZE = 15  # note: 25 is an arbitrary threshold that works on my machine, need further testing

    def __init__(self, save_path, file_name, listFiles_paths, option_orientation, option_page_size, option_margin_size):
        """ Thread object constructor
            params:
            save_path       Directory where the resulting PDF file will be saved
            file_name       Final name of the PDF file
            listFiles_paths List containing the paths of all the Image files for the PDF
        """
        QThread.__init__(self)
        # Set thread variables
        self.save_path = save_path
        self.file_name = file_name
        self.paths = listFiles_paths
        self.option_orientation = option_orientation
        self.option_page_size = option_page_size
        self.option_margin_size = option_margin_size
        self.progress = 0

    def __del__(self):
        self.wait()

    def run(self):
        self.process_pdf()

    # Process every image into a single PDF file, cutting the load into batches if necessary
    def process_pdf(self):
        # Signal info to the main thread
        self.progress = 0
        self.signal_progress.emit(self.progress)
        self.signal_message.emit(f"Now processing {len(self.paths)} images into {self.file_name}.pdf")

        # If there are too many items in the list, separate into batches
        if len(self.paths) > self.BATCH_SIZE:
            # determine the total number of iterations (number of batches)
            _iterations = len(self.paths) // self.BATCH_SIZE  # int division
            _rem = len(self.paths) % self.BATCH_SIZE
            if _rem > 0: _iterations += 1  # the remainder will be another batch

            part_paths = []  # Stores where each part is located, used to join them later

            # Generate and save PDF chunks in a temporal folder
            for i in range(0, _iterations):
                # Signal info to the main thread
                self.progress = int(i / _iterations * 100)
                self.signal_progress.emit(self.progress)
                current_msg = f"Now working on part {i + 1} of {_iterations}"
                self.signal_message.emit(current_msg)

                # determine the batch length
                batch_length = self.BATCH_SIZE if len(self.paths) - self.BATCH_SIZE * i > self.BATCH_SIZE else len(self.paths) - self.BATCH_SIZE * i
                # function handles the conversion from path strings to image array
                pdf_images = self.convert_batch(start_i=self.BATCH_SIZE * i, length=batch_length, total_parts=_iterations, current_msg=current_msg)
                # add this iteration's part path to the part path list
                part_path = f"_TEMP/{self.file_name}_{i}.pdf"
                part_paths.append(part_path)
                # saves the part as a pdf
                pdf_images[0].save(part_path, save_all=True, append_images=pdf_images[1:])

                # flag the space as empty and call the garbage collector to free the memory used by the part
                # note: Somehow just one part can use more than 500MB of ram and the next statement keeps an additional bit of memory free at all times
                # noinspection PyUnusedLocal
                pdf_images = None
                gc.collect()

            # Signal info to the main thread
            self.signal_message.emit(f"Now merging into {self.file_name}.pdf")

            # PDF merge process start
            pdf_merger = PdfFileMerger()
            # append each part to the merger
            for part_path in part_paths:
                pdf_merger.append(part_path)
            # save to the final PDF
            pdf_merger.write(f"{self.save_path}/{self.file_name}.pdf")
            pdf_merger.close()

            # Signal info to the main thread
            self.signal_message.emit(f"Deleting {len(part_paths)} temporal files")

            # Delete the PDF part files
            for part_path in part_paths:
                os.remove(part_path)

        # for lists of less than 'self.BATCH_SIZE' items, do just one batch
        else:
            # Signal info to the main thread
            current_msg = f"Now working on {self.file_name}.pdf"
            self.signal_message.emit(current_msg)

            # function handles the conversion from paths strings to image array
            pdf = self.convert_batch(length=len(self.paths), current_msg=current_msg)
            if isinstance(pdf, list):
                # turn image array into the final PDF
                pdf[0].save(f"{self.save_path}/{self.file_name}.pdf", save_all=True, append_images=pdf[1:])
            else:
                # turn image into the final PDF
                pdf.save(f"{self.save_path}/{self.file_name}.pdf", save_all=True)

        # Signal info to the main thread
        self.signal_message[str, int].emit(f"File successfully saved to {self.save_path}\\{self.file_name}.pdf", 2000)
        self.signal_toggle_ui.emit(True)
        # One last call to the garbage collector
        gc.collect()

    # Helper function that turns a single batch of image paths into a image array
    def convert_batch(self, start_i=0, length=BATCH_SIZE, total_parts=1, current_msg=""):
        # converted image array, will return this
        image_list = []

        for i in range(start_i, start_i + length):
            # Signal info to the main thread
            progress_part = (i - start_i + 1) / length
            progress_overall = self.progress + int(progress_part * 100 / total_parts)
            self.signal_progress.emit(progress_overall)
            self.signal_message.emit(f"{current_msg}... {progress_part * 100:.2f}%")

            # convert from path string to image
            img = Image.open(self.paths[i])

            img = self.modify_image(img)

            # append the image to the array
            image_list.append(img)

        # more than one image, return the array
        if len(image_list) > 1:
            return image_list
        # if just one image, return it
        else:
            return image_list[0]

    # Helper function that applies all image modifiers from UI
    def modify_image(self, im):
        # Margin sizes in px
        # note: arbitrary values, google better ones
        margin_SMALL = 150
        margin_LARGE = 300

        # Sizes at print dpi (300)
        size_A4 = (2480, 3508)
        size_USLETTER = (2550, 3300)

        # Rotate image to better fit portrait or landscape orientation
        if self.option_orientation == "PORTRAIT":
            if im.width > im.height:
                im = im.rotate(90, PIL.Image.NEAREST, expand=1)
        else:
            if im.width < im.height:
                im = im.rotate(90, PIL.Image.NEAREST, expand=1)

        # Add margins
        if self.option_margin_size != 'NOMARGIN':
            margin = 0
            if self.option_margin_size == 'SMALL':
                margin = margin_SMALL
            elif self.option_margin_size == 'LARGE':
                margin = margin_LARGE
            im = ImageOps.expand(im, border=margin, fill='white')

        # Resize to fit page
        if self.option_page_size != "FIT":
            desired_width, desired_height = (im.width, im.height)

            if self.option_page_size == "A4":
                desired_width, desired_height = size_A4 if self.option_orientation == "PORTRAIT" else (size_A4[1], size_A4[0])
                pass
            elif self.option_page_size == 'USLETTER':
                desired_width, desired_height = size_USLETTER if self.option_orientation == "PORTRAIT" else (size_USLETTER[1], size_USLETTER[0])
                pass

            scale_factor = min(desired_width / im.width, desired_height / im.height)
            new_size = (int(im.width * scale_factor), int(im.height * scale_factor))
            im = im.resize(new_size, Image.ANTIALIAS)

        return im


# Class for the Image to PDF converter tool
class Screen_ImageToPDF(QWidget):
    # Class global variables
    default_save_path = f"{os.sep.join((os.path.expanduser('~'), 'Desktop'))}"
    allowed_file_extensions = ["png", "jpg", "jpeg", "tif", "tiff", "bmp", "gif"]

    OPTIONS_ORIENTATION = ["PORTRAIT", "LANDSCAPE"]
    OPTIONS_PAGE_SIZE = ["FIT", "A4", "USLETTER"]
    OPTIONS_MARGIN_SIZE = ["NOMARGIN", "SMALL", "LARGE"]

    parent = None
    # Explicit all variable types for items inherited from the .ui file
    listFiles: QListWidget
    btnMakePDF: QPushButton
    btnBrowse: QPushButton
    btnDuplicate: QPushButton
    btnDelete: QPushButton
    btnDeleteAll: QPushButton
    btnBack: QPushButton
    txtFileName: QLineEdit
    statusbar: QStatusBar
    central_widget: QStackedWidget
    comboOrientation: QComboBox
    comboSize: QComboBox
    comboMargin: QComboBox
    progressBar: QProgressBar

    def __init__(self, parent=None):
        super(Screen_ImageToPDF, self).__init__()

        # Set class variables
        self.parent = parent
        self.statusbar = parent.statusbar
        self.central_widget = parent.central_widget
        self.pdf_thread = None

        # noinspection SpellCheckingInspection
        loadUi("ui/screen_imagetopdf.ui", self)  # Load the tool's UI from file

        # Connect all UI items to their respective function
        self.btnMakePDF.clicked.connect(self.click_make_pdf)
        self.btnBrowse.clicked.connect(self.click_browse)
        self.btnDuplicate.clicked.connect(self.click_duplicate)
        self.btnDelete.clicked.connect(self.click_delete)
        self.btnDeleteAll.clicked.connect(self.click_delete_all)
        self.btnBack.clicked.connect(self.click_back)

        # The progress bar should be only visible while working on a file
        self.progressBar.setVisible(False)

    # Helper function to append a '(#)' to the file name until it finds one unused (maybe it's not the best approach)
    def generate_file_name(self, file_name, i=1):
        if os.path.exists(f"{self.default_save_path}/{file_name}({i}).pdf"):
            return self.generate_file_name(file_name, i + 1)
        else:
            return f"{file_name}({i})"

    # Toggles some UI elements while working on a file
    def toggle_ui(self, is_activated):
        # Disable these buttons
        self.btnMakePDF.setDisabled(not is_activated)
        self.btnBack.setDisabled(not is_activated)
        # Show progress bar
        self.progressBar.setVisible(not is_activated)

    # Returns a formatted string from the 'self.allowed_file_extensions' list
    def get_file_filter(self):
        # Output example: "Images (*.png *.jpg *.tif)"
        ext_filter = ""
        for ext in self.allowed_file_extensions:
            ext_filter += f"*.{ext} "
        return f"Images ({ext_filter[:-1]})"

    def click_make_pdf(self):
        # If the Gui's list is empty, do nothing
        if self.listFiles.count() == 0:
            return

        # Read the file name from the text box
        file_name = self.txtFileName.text()
        # Text blank? Generate one based on the date with YearMonthDay_Hour-Minute-Second format
        if file_name == "":
            file_name = datetime.now().strftime("%Y%m%d_%H-%M-%S")
        # Keep on renaming if file exist
        if os.path.exists(f"{self.default_save_path}/{file_name}.pdf"):
            file_name = self.generate_file_name(file_name)

        # Retrieve all paths from the list, they will be set to the pdf thread
        listFiles_paths = []
        for i in range(0, self.listFiles.count()):
            listFiles_paths.append(self.listFiles.item(i).text())
        # Retrieve option values

        # note hete

        option_orientation = self.OPTIONS_ORIENTATION[self.comboOrientation.currentIndex()]
        option_page_size = self.OPTIONS_PAGE_SIZE[self.comboSize.currentIndex()]
        option_margin_size = self.OPTIONS_MARGIN_SIZE[self.comboMargin.currentIndex()]

        # Lock UI elements
        self.toggle_ui(False)

        # Define and start the conversion thread
        self.pdf_thread = ThreadPDF(save_path=self.default_save_path, file_name=file_name, listFiles_paths=listFiles_paths,
                                    option_orientation=option_orientation, option_page_size=option_page_size, option_margin_size=option_margin_size)
        self.pdf_thread.start()
        # Link thread's signals
        self.pdf_thread.signal_progress.connect(self.progressBar.setValue)
        self.pdf_thread.signal_message[str].connect(self.statusbar.showMessage)
        self.pdf_thread.signal_message[str, int].connect(self.statusbar.showMessage)
        self.pdf_thread.signal_toggle_ui.connect(self.toggle_ui)

    def click_browse(self):
        # Open windows' item browser with specifications
        file_names, _selectedFilter = QtWidgets.QFileDialog.getOpenFileNames(caption="Select images",
                                                                             directory=os.sep.join(
                                                                                 (os.path.expanduser('~'), 'Desktop')),
                                                                             filter=self.get_file_filter()
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
        # Clear the fileName field
        self.txtFileName.setText("")

    def click_back(self):
        self.central_widget.removeWidget(self)
