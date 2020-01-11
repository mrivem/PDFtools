"""
TODO intro and info here

Todo:
    Document code
    Add a range instructions label to the GUI
"""
import os
import re
from datetime import datetime

from PyPDF2 import PdfFileReader, PdfFileWriter
from PyQt5 import QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi


class Thread_Split(QThread):
    # Signals
    signal_progress = pyqtSignal(int)
    signal_message = pyqtSignal([str], [str, int])
    signal_toggle_ui = pyqtSignal(bool)

    def __init__(self, save_path, input_file, output_prefix, ranges):
        QThread.__init__(self)

        self.save_path = save_path
        self.input_path = input_file
        self.output_prefix = output_prefix
        self.ranges = ranges

    def __del__(self):
        self.wait()

    def run(self):
        progress = 0
        self.signal_progress.emit(progress)
        self.signal_message.emit(f"Now splitting {self.input_path} into {len(self.ranges)} files")

        for counter in range(len(self.ranges)):
            first, last = self.ranges[counter]

            progress = int(counter / len(self.ranges) * 100)
            self.signal_progress.emit(progress)
            self.signal_message.emit(f"[{counter + 1} of {len(self.ranges)}] Working on range {first} to {last}")

            if first == last:
                out_path = os.path.join(self.save_path, f"{self.output_prefix}_{first}.PDF")
                reader = PdfFileReader(self.input_path)
                writer = PdfFileWriter()
                writer.addPage(reader.getPage(first - 1))

                with open(out_path, "wb") as out_file:
                    writer.write(out_file)
                del reader, writer
            else:
                out_path = os.path.join(self.save_path, f"{self.output_prefix}_{first}-{last}.PDF")
                reader = PdfFileReader(self.input_path)
                writer = PdfFileWriter()

                for i in range(first - 1, last):
                    this_progress = progress + int((i / (last - first)) / len(self.ranges))
                    self.signal_progress.emit(this_progress)

                    writer.addPage(reader.getPage(i))

                with open(out_path, "wb") as out_file:
                    writer.write(out_file)
                del reader, writer

        progress = 100
        self.signal_progress.emit(progress)
        self.signal_message[str, int].emit(f"{self.input_path} split operation successful", 2000)
        self.signal_toggle_ui.emit(True)


class Screen_SplitPDF(QWidget):
    # Class global variables
    parent = None
    default_save_path = f"{os.sep.join((os.path.expanduser('~'), 'Desktop'))}"
    split_thread = None

    reg_range_complete = re.compile(r"\d+-\d+")
    reg_range_to_end = re.compile(r"\d+-")
    reg_range_to_start = re.compile(r"-\d+")
    reg_range_single = re.compile(r"\d+")

    page_count = 0
    valid_ranges = []

    # Explicit all variable types for items inherited from the .ui file
    central_widget: QStackedWidget
    statusbar: QStatusBar

    progressBar: QProgressBar
    btnBack: QPushButton
    btnBrowse: QPushButton
    btnSplit: QPushButton
    txtRange: QLineEdit
    txtOutput: QLineEdit
    txtInput: QLineEdit
    txtPreview: QPlainTextEdit
    spacerBottom: QSpacerItem

    def __init__(self, parent=None):
        # noinspection PyArgumentList
        super(Screen_SplitPDF, self).__init__()

        self.parent = parent
        self.statusbar = parent.statusbar
        self.central_widget = parent.central_widget

        loadUi("ui/screen_splitpdf.ui", self)

        self.btnSplit.clicked.connect(self.click_split)
        self.btnBrowse.clicked.connect(self.click_browse)
        self.btnBack.clicked.connect(self.click_back)

        self.txtRange.textChanged.connect(self.update_preview)
        self.txtOutput.textChanged.connect(self.update_preview)

        self.progressBar.setVisible(False)

    def click_split(self):
        if self.txtInput.text() == "":
            return

        if not self.valid_ranges:
            return

        input_file = self.txtInput.text()

        output_prefix = self.txtOutput.text()
        if output_prefix == "":
            output_prefix = datetime.now().strftime("%Y%m%d_%H-%M-%S")

        # Lock UI elements
        self.toggle_ui(False)

        # Define and start the split thread
        self.split_thread = Thread_Split(save_path=self.default_save_path, input_file=input_file, output_prefix=output_prefix, ranges=self.valid_ranges)
        self.split_thread.start()
        # Link thread's signals
        self.split_thread.signal_progress.connect(self.progressBar.setValue)
        self.split_thread.signal_message[str].connect(self.statusbar.showMessage)
        self.split_thread.signal_message[str, int].connect(self.statusbar.showMessage)
        self.split_thread.signal_toggle_ui.connect(self.toggle_ui)

    def toggle_ui(self, is_activated):
        # Disable these buttons
        self.btnSplit.setDisabled(not is_activated)
        self.btnBack.setDisabled(not is_activated)
        # Show progress bar
        self.progressBar.setVisible(not is_activated)

    def update_preview(self):
        txt_input = self.txtInput.text()
        txt_range = self.txtRange.text()
        txt_output_prefix = self.txtOutput.text()

        if txt_range != "":
            self.valid_ranges = self.parse_ranges(txt_range)
        else:
            self.valid_ranges = []

        sim_output = ""
        for vr in self.valid_ranges:
            first, last = vr
            if first != last:
                sim_output += f"{self.default_save_path}\\{txt_output_prefix}_{first}-{last}.PDF\n"
            else:
                sim_output += f"{self.default_save_path}\\{txt_output_prefix}_{first}.PDF\n"

        txt = f"INPUT FILE\n" \
              f"path:\t{txt_input if txt_input != '' else 'Not selected'}\n" \
              f"pages:\t{self.page_count}\n" \
              f"\nOPTIONS\n" \
              f"Range(s):\t{self.valid_ranges if self.valid_ranges else 'No range'}\n" \
              f"Output prefix:\t{txt_output_prefix if txt_output_prefix != '' else 'No prefix'}\n" \
              f"\nOUTPUT\n" \
              f"{sim_output if sim_output != '' else 'None'}"

        self.txtPreview.setPlainText(txt)

    def parse_ranges(self, txt_ranges):
        ranges = txt_ranges.replace(" ", "").split(",")
        valid_ranges = []

        for r in ranges:
            # Check for a complete range
            mo = self.reg_range_complete.search(r)
            if mo:
                try:
                    first, last = r.split("-")
                except ValueError:
                    continue

                first, last = int(first), int(last)
                if first >= last \
                        or (first > self.page_count or last > self.page_count) \
                        or (first == 0 or last == 0):
                    # Not valid, skip it
                    continue
                # Add to valid list and go to the next one
                valid_ranges.append((first, last))
                continue

            # Check for incomplete from Num to End
            mo = self.reg_range_to_end.search(r)
            if mo:
                first = int(r.replace("-", ""))
                if first > self.page_count or first == 0:
                    # Not valid, skip it
                    continue
                # Add to valid list and go to the next one
                valid_ranges.append((first, self.page_count))
                continue

            # Check for incomplete from Start to Num
            mo = self.reg_range_to_start.search(r)
            if mo:
                last = int(r.replace("-", ""))
                if last > self.page_count or last == 0:
                    # Not valid, skip it
                    continue
                # Add to valid list
                valid_ranges.append((1, last))
                continue

            # Check for single pages
            mo = self.reg_range_single.search(r)
            if mo:
                single = int(r)
                if single == 0 or single > self.page_count:
                    continue
                valid_ranges.append((single, single))
                continue
        return valid_ranges

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

        # Get the number of pages
        pdf = PdfFileReader(file_name)
        self.page_count = pdf.getNumPages()
        del pdf

        # Set the path to the input path box
        self.txtInput.setText(file_name)
        # Delete whatever is on the range box
        self.txtRange.setText("")

        # Modify the prefix box if no prefix was stated
        if self.txtOutput.text() == "":
            new_text = f"{os.path.splitext(os.path.split(file_name)[1])[0]}_split"
            self.txtOutput.setText(new_text)

        self.update_preview()

    def click_back(self):
        self.central_widget.removeWidget(self)
        del self
