# !/usr/bin/env python
# -*- coding:utf-8 -*-

from PyQt5.QtWidgets import QMessageBox, QLineEdit, QListWidget
from PyQt5.QtGui import QIcon

import sys
import os


class ListFileEdit(QListWidget):
    debug = False
    mainWindow = None

    def __init__(self, mainWindow, parent):
        super(ListFileEdit, self).__init__(parent)
        self.mainWindow = mainWindow
        self.setDragEnabled(True)

    def dragEnterEvent(self, event):
        data = event.mimeData()
        urls = data.urls()

        if not urls:
            super(ListFileEdit, self).dragEnterEvent(event)
            return

        if urls and urls[0].scheme() == 'file':
            event.acceptProposedAction()

    def dragMoveEvent(self, event):
        data = event.mimeData()
        urls = data.urls()

        if not urls:
            super(ListFileEdit, self).dragMoveEvent(event)
            return

        if urls and urls[0].scheme() == 'file':
            event.acceptProposedAction()

    def dropEvent(self, event):
        # Retrieve urls from event data
        data = event.mimeData()
        urls = data.urls()

        # No urls? Do nothing
        if not urls:
            super(ListFileEdit, self).dropEvent(event)
            return

        # Extension list
        allowed_extensions = self.mainWindow.allowed_file_extensions
        # allowed_extensions = [".jpg", ".png", ".tif"]
        blocked_files = ""
        # Loop through every url
        for url in urls:
            # Get the path from url (Removing leading \)
            path = url.path()[1:]

            # If path is a directory, loop through and add allowed items
            if os.path.isdir(path):
                dir_name = os.path.basename(path)

                if self.mainWindow.txtFileName.text() == "":
                    self.mainWindow.txtFileName.setText(dir_name)

                for file in os.listdir(path):
                    file_path = f"{path}/{file}"

                    # Get the file extension fixme
                    file_ext = file_path.split('.')[-1].lower()

                    # Add item to the list if the extension is allowed
                    if file_ext in allowed_extensions:
                        self.addItem(file_path)
                    # Log all disallowed items
                    else:
                        blocked_files += f"{file_path}\n"
            # If path is a file, add if it's allowed
            else:
                file_path = path

                # Get the file extension
                file_ext = file_path.split('.')[-1].lower()

                # Add item to the list if the extension is allowed
                if file_ext in allowed_extensions:
                    self.addItem(file_path)
                # Log all disallowed items
                else:
                    blocked_files += f"{file_path}\n"

        # If any items were blocked, show warning w/ blocked file names
        if blocked_files:
            dialog = QMessageBox()
            dialog.setWindowTitle("Error: Invalid file(s)")
            dialog.setText(
                f"Only {allowed_extensions} are accepted\nThe following files were rejected:\n{blocked_files}")
            dialog.setIcon(QMessageBox.Warning)
            dialog.exec_()
