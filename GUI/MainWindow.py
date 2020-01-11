from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QStackedWidget, QAction, QMessageBox

from Screen_ToolSelection import Screen_ToolSelection


class Ui_MainWindow(QMainWindow):
    WIN_WIDTH = 800
    WIN_HEIGHT = 600

    CUR_VER = "v0.2.5"
    screen_toolselection: Screen_ToolSelection

    def setupUi(self, MainWindow):
        # main window attributes
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(self.WIN_WIDTH, self.WIN_HEIGHT)
        # set up the central widget
        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)
        MainWindow.setCentralWidget(self.central_widget)
        # set up the menu bar
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, self.WIN_WIDTH, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        # add actions to the menu bar
        self.actionAbout = QAction("About", self)
        self.actionAbout.triggered.connect(self.click_menubar_about)
        self.menubar.addAction(self.actionAbout)

        # set up the status bar
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        # note: no se que hace esta wea
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # init other screens
        self.screen_toolselection = Screen_ToolSelection(self)
        # append screens to the central widget
        self.central_widget.addWidget(self.screen_toolselection)
        # set the starting screen
        self.central_widget.setCurrentWidget(self.screen_toolselection)

        self.screen_toolselection.post_load()

    def click_menubar_about(self):
        dialog = QMessageBox()
        dialog.setWindowTitle("About")
        dialog.setText(f"PDFtools {self.CUR_VER}\nCreated by Mrivem, 2020")
        dialog.setIcon(QMessageBox.Information)
        dialog.exec_()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
