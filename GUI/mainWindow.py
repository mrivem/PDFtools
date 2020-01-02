"""
    TODO: my intro and personal data

"""
# PyQt5 Gui components
from PyQt5 import QtCore, QtGui, QtWidgets
# My custom Gui components
from GUI.ListFileEdit import ListFileEdit
# External modules
from PIL import Image
from PyPDF2 import PdfFileMerger
# Python modules
from datetime import datetime
import os
# Memory management modules
import gc
from guppy import hpy

h = hpy()


class Ui_MainWindow(object):
    default_save_path = f"{os.sep.join((os.path.expanduser('~'), 'Desktop'))}"
    allowed_file_extensions = ["png", "jpg", "jpeg", "tif", "tiff", "bmp", "gif"]

    debug = True

    # noinspection PyAttributeOutsideInit
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 660)
        MainWindow.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setAcceptDrops(True)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLeft = QtWidgets.QVBoxLayout()
        self.verticalLeft.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLeft.setObjectName("verticalLeft")
        self.lblFiles = QtWidgets.QLabel(self.centralwidget)
        self.lblFiles.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.lblFiles.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.lblFiles.setObjectName("lblFiles")
        self.verticalLeft.addWidget(self.lblFiles)
        self.listFiles = ListFileEdit(self, self.centralwidget)
        self.listFiles.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listFiles.sizePolicy().hasHeightForWidth())
        self.listFiles.setSizePolicy(sizePolicy)
        self.listFiles.setAcceptDrops(True)
        self.listFiles.setDragEnabled(True)
        self.listFiles.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
        self.listFiles.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.listFiles.setAlternatingRowColors(True)
        self.listFiles.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.listFiles.setObjectName("listFiles")
        self.verticalLeft.addWidget(self.listFiles)
        self.horizontalLayout.addLayout(self.verticalLeft)
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout.addWidget(self.line)
        self.verticalRight = QtWidgets.QVBoxLayout()
        self.verticalRight.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.verticalRight.setObjectName("verticalRight")
        self.lblSelFiles_2 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblSelFiles_2.sizePolicy().hasHeightForWidth())
        self.lblSelFiles_2.setSizePolicy(sizePolicy)
        self.lblSelFiles_2.setObjectName("lblSelFiles_2")
        self.verticalRight.addWidget(self.lblSelFiles_2)
        self.btnBrowse = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnBrowse.sizePolicy().hasHeightForWidth())
        self.btnBrowse.setSizePolicy(sizePolicy)
        self.btnBrowse.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedKingdom))
        self.btnBrowse.setObjectName("btnBrowse")
        self.verticalRight.addWidget(self.btnBrowse)
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.line_2.sizePolicy().hasHeightForWidth())
        self.line_2.setSizePolicy(sizePolicy)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalRight.addWidget(self.line_2)
        self.lblSelFiles = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblSelFiles.sizePolicy().hasHeightForWidth())
        self.lblSelFiles.setSizePolicy(sizePolicy)
        self.lblSelFiles.setObjectName("lblSelFiles")
        self.verticalRight.addWidget(self.lblSelFiles)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.gridLayout.setObjectName("gridLayout")
        self.btnMoveUp = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnMoveUp.sizePolicy().hasHeightForWidth())
        self.btnMoveUp.setSizePolicy(sizePolicy)
        self.btnMoveUp.setObjectName("btnMoveUp")
        self.gridLayout.addWidget(self.btnMoveUp, 0, 0, 1, 1)
        self.btnMoveDown = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnMoveDown.sizePolicy().hasHeightForWidth())
        self.btnMoveDown.setSizePolicy(sizePolicy)
        self.btnMoveDown.setObjectName("btnMoveDown")
        self.gridLayout.addWidget(self.btnMoveDown, 1, 0, 1, 1)
        self.btnDelete = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnDelete.sizePolicy().hasHeightForWidth())
        self.btnDelete.setSizePolicy(sizePolicy)
        self.btnDelete.setObjectName("btnDelete")
        self.gridLayout.addWidget(self.btnDelete, 0, 1, 1, 1)
        self.btnDuplicate = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnDuplicate.sizePolicy().hasHeightForWidth())
        self.btnDuplicate.setSizePolicy(sizePolicy)
        self.btnDuplicate.setObjectName("btnDuplicate")
        self.gridLayout.addWidget(self.btnDuplicate, 1, 1, 1, 1)
        self.verticalRight.addLayout(self.gridLayout)
        self.line_3 = QtWidgets.QFrame(self.centralwidget)
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.verticalRight.addWidget(self.line_3)
        self.lblFileName = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblFileName.sizePolicy().hasHeightForWidth())
        self.lblFileName.setSizePolicy(sizePolicy)
        self.lblFileName.setObjectName("lblFileName")
        self.verticalRight.addWidget(self.lblFileName)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.txtFileName = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(150)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.txtFileName.sizePolicy().hasHeightForWidth())
        self.txtFileName.setSizePolicy(sizePolicy)
        self.txtFileName.setMinimumSize(QtCore.QSize(0, 0))
        self.txtFileName.setMaximumSize(QtCore.QSize(160, 16777215))
        self.txtFileName.setBaseSize(QtCore.QSize(0, 0))
        self.txtFileName.setObjectName("txtFileName")
        self.horizontalLayout_2.addWidget(self.txtFileName)
        self.lblPDF = QtWidgets.QLabel(self.centralwidget)
        self.lblPDF.setObjectName("lblPDF")
        self.horizontalLayout_2.addWidget(self.lblPDF)
        self.verticalRight.addLayout(self.horizontalLayout_2)
        self.line_4 = QtWidgets.QFrame(self.centralwidget)
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.verticalRight.addWidget(self.line_4)
        self.btnPDF = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnPDF.sizePolicy().hasHeightForWidth())
        self.btnPDF.setSizePolicy(sizePolicy)
        self.btnPDF.setObjectName("btnPDF")
        self.verticalRight.addWidget(self.btnPDF)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalRight.addItem(spacerItem)
        self.label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(6)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.verticalRight.addWidget(self.label)
        self.horizontalLayout.addLayout(self.verticalRight)
        self.horizontalLayout_3.addLayout(self.horizontalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 513, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        # My links
        self.btnPDF.clicked.connect(self.click_pdf)
        self.btnBrowse.clicked.connect(self.click_browse)
        self.btnDuplicate.clicked.connect(self.click_duplicate)
        self.btnDelete.clicked.connect(self.click_delete)
        self.btnMoveDown.clicked.connect(self.click_move_down)
        self.btnMoveUp.clicked.connect(self.click_move_up)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    # noinspection PyPep8Naming,PyShadowingNames
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.lblFiles.setText(_translate("MainWindow", "Files:"))
        self.listFiles.setToolTip(_translate("MainWindow", "Drag and drop files here"))
        self.lblSelFiles_2.setText(_translate("MainWindow", "Input files:"))
        self.btnBrowse.setText(_translate("MainWindow", "Browse files"))
        self.lblSelFiles.setText(_translate("MainWindow", "Selected file:"))
        self.btnMoveUp.setText(_translate("MainWindow", "Move up"))
        self.btnMoveDown.setText(_translate("MainWindow", "Move down"))
        self.btnDelete.setText(_translate("MainWindow", "Delete"))
        self.btnDuplicate.setText(_translate("MainWindow", "Duplicate"))
        self.lblFileName.setText(_translate("MainWindow", "File name:"))
        self.lblPDF.setText(_translate("MainWindow", ".PDF"))
        self.btnPDF.setText(_translate("MainWindow", "Make PDF"))
        self.label.setText(_translate("MainWindow", "@Mrivem, 2020"))

    def click_pdf(self):
        # todo: comment code

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

    # TODO: Remove this button
    def click_move_down(self):
        # Get selected items
        selected_items = self.listFiles.selectedItems()
        # No selection ? do nothing
        if not selected_items:
            return
        # Number of items on the list
        list_count = self.listFiles.count()
        #
        for item in selected_items:
            # Get item's current row
            row = self.listFiles.row(item)
            # Remove the item from the list
            self.listFiles.takeItem(self.listFiles.row(item))
            # Update the row value
            row = row + 1
            # If it's the last item, cap the number
            if row == list_count:
                row = list_count - 1
            # Insert the item one row down the list and set it as selected
            self.listFiles.insertItem(row, item.text())
            self.listFiles.item(row).setSelected(True)

    # TODO: Remove this button
    def click_move_up(self):
        # Get selected items
        selected_items = self.listFiles.selectedItems()
        # No selection ? do nothing
        if not selected_items:
            return
        #
        for item in selected_items:
            # Get item's current row
            row = self.listFiles.row(item)
            # Remove the item from the list
            self.listFiles.takeItem(self.listFiles.row(item))
            # Update the row value
            row = row - 1
            # If it's the first item, cap the number
            if row < 0:
                row = 0
            # Insert the item one row up the list and set it as selected
            self.listFiles.insertItem(row, item.text())
            self.listFiles.item(row).setSelected(True)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
