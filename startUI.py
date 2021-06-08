

from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QIcon
import sys
import os
from subUI import Subdomain
from xssUI import XSS
from dosUI import Dos
from sqlUI import SQL
import time


class Start(QtWidgets.QMainWindow):
    def __init__(self):
        super(Start, self).__init__()
        uic.loadUi('startUI.ui', self)
        self.setWindowIcon(QIcon('1464646-200.png'))
        self.setWindowTitle('Pententing')
        self.sqlBtn.clicked.connect(self.on_sqlClick)
        self.subBtn.clicked.connect(self.on_subClick)
        self.dosBtn.clicked.connect(self.on_dosClick)
        self.xssBtn.clicked.connect(self.on_xssClick)

    @pyqtSlot()
    def on_dosClick(self):
        self.d = Dos()
        self.d.show()
        self.hide()

    @pyqtSlot()
    def on_xssClick(self):
        self.f = XSS()
        self.f.show()
        self.hide()

    @pyqtSlot()
    def on_subClick(self):
        self.s=Subdomain()
        self.s.show()
        self.hide()

    @pyqtSlot()
    def on_sqlClick(self):
        self.q = SQL()
        self.q.show()
        self.hide()

if __name__ == '__main__':

    app = QtWidgets.QApplication([])
    win = Start()
    win.show()
    sys.exit(app.exec())
