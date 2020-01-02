"""
    TODO: my intro and personal data

"""
# PyQt5 Gui components
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
# External modules
from PIL import Image
from PyPDF2 import PdfFileMerger
# Python modules
from datetime import datetime
import os
# Memory management and debugging modules
import gc
from guppy import hpy

h = hpy()


class Screen_ImageToPDF(QWidget):
    default_save_path = f"{os.sep.join((os.path.expanduser('~'), 'Desktop'))}"
    allowed_file_extensions = ["png", "jpg", "jpeg", "tif", "tiff", "bmp", "gif"]

    listFiles: QListWidget
    btnMakePDF: QPushButton
    btnBrowse: QPushButton
    btnDuplicate: QPushButton
    btnDelete: QPushButton
    btnDeleteAll: QPushButton
    btnBack: QPushButton
    txtFileName: QLineEdit

    parent = None

    def __init__(self, parent=None):
        super(Screen_ImageToPDF, self).__init__()
        
        self.parent = parent

        loadUi("ui/screen_imagetopdf.ui", self)

        self.btnMakePDF.clicked.connect(self.click_make_pdf)
        self.btnBrowse.clicked.connect(self.click_browse)
        self.btnDuplicate.clicked.connect(self.click_duplicate)
        self.btnDelete.clicked.connect(self.click_delete)
        self.btnDeleteAll.clicked.connect(self.click_delete_all)
        self.btnBack.clicked.connect(self.click_back)

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

        # If there are too many items in the list, separate into batches
        # note: 25 is an arbitrary threshold that works on my machine, need further testing
        if self.listFiles.count() > 25:
            # determine the total number of iterations (number of batches)
            _iterations = self.listFiles.count() // 25  # int division
            _rem = self.listFiles.count() % 25
            if _rem > 0: _iterations += 1  # the remainder will be another batch

            part_paths = []  # Stores where each part is located, used to join them later

            # Generate and save PDF chunks in a temporal folder
            for i in range(0, _iterations):
                # determine the batch length
                batch_length = 25 if self.listFiles.count() - 25 * i > 25 else self.listFiles.count() - 25 * i
                # function handles the conversion from paths strings to image array
                pdf_imgs = self.convert_batch(start_i=25 * i, length=batch_length)
                # this iteration's part path, also added to the part path list
                part_path = f"_TEMP/{file_name}_{i}.pdf"
                part_paths.append(part_path)
                # saves the part as a pdf
                pdf_imgs[0].save(part_path, save_all=True, append_images=pdf_imgs[1:])
                # flag the space as empty and call the garbage collector to free the memory used by the part
                # note: Somehow just one part can use more than 1GB of ram
                pdf_imgs = None
                gc.collect()

            # PDF merge process start
            pdf_merger = PdfFileMerger()
            # append each part to the merger
            for part_path in part_paths:
                pdf_merger.append(part_path)
            # save to the final PDF
            pdf_merger.write(f"{self.default_save_path}/{file_name}.pdf")
            pdf_merger.close()

            # Delete the PDF part files
            for part_path in part_paths:
                os.remove(part_path)

        # for lists of less than 25 items, do just one batch
        else:
            # function handles the conversion from paths strings to image array
            pdf = self.convert_batch(length=self.listFiles.count())

            if isinstance(pdf, list):
                # turn image array into the final PDF
                pdf[0].save(f"{self.default_save_path}/{file_name}.pdf", save_all=True, append_images=pdf[1:])
            else:
                # turn image into the final pdf
                pdf.save(f"{self.default_save_path}/{file_name}.pdf", save_all=True)

    # todo, document this
    def convert_batch(self, start_i=0, length=25):
        # converted image array, will return this
        image_list = []

        for i in range(start_i, start_i + length):
            # grab the item and extract the path
            list_item = self.listFiles.item(i)
            item_path = list_item.text()
            # convert from path string to image
            img = Image.open(item_path)
            img_converted = img.convert('RGB')
            # append the image to the array
            image_list.append(img_converted)

        # more than one image, return the array
        if len(image_list) > 1:
            return image_list
        # if just one image, return it
        else:
            return image_list[0]

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
                                                                             filter=self.get_file_filter()
                                                                             )
        # Add items to the list
        self.listFiles.addItems(file_names)

    def get_file_filter(self):
        # Output example: "Images (*.png *.jpg *.tif)"
        ext_filter = ""
        for ext in self.allowed_file_extensions:
            ext_filter += f"*.{ext} "
        return f"Images ({ext_filter[:-1]})"

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
        for i in range(0, self.listFiles.count()):
            ire = self.listFiles.takeItem(0)
            print(f"{ire.text()}")

    def click_back(self):
        self.parent.central_widget.setCurrentWidget(self.parent.screen_toolselection)
