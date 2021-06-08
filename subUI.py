# very basic terminal emulator in pyqt
# https://pythonbasics.org/pyqt/

from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QIcon
import sys
import os
import subprocess
from sub import main
import time



class Subdomain(QtWidgets.QMainWindow):
    def __init__(self):
        super(Subdomain, self).__init__()
        uic.loadUi('subUI.ui', self)
        self.setWindowIcon(QIcon('2435355-200.png'))
        self.setWindowTitle('Subdomain Finder')
        # self.lineEdit.returnPressed.connect(self.doCMD)
        # self.pushButtonInstall.clicked.connect(self.onClick)
        self.startBtn.clicked.connect(self.on_startClick)
        self.backBtn.clicked.connect(self.on_backClick)
        self.resetBtn.clicked.connect(self.on_resetClick)


    @pyqtSlot()
    def on_resetClick(self):

        self.url.setText('')
        self.port.setText('')
        self.outPut.setText('')


    @pyqtSlot()
    def on_backClick(self):
        from startUI import Start
        self.f = Start()
        self.f.show()
        self.hide()

    @pyqtSlot()
    def on_startClick(self):
        url=str(self.url.text())
        self.outPut.append('Searching for domain: '+url)
        ans = main(url)
        for a in range(len(ans)):

            if a==2:
                for i in ans[2]:
                    print(i)
                    self.outPut.append(str(i))
            else:
                self.outPut.append(str(ans[a]))


if __name__ == '__main__':

    app = QtWidgets.QApplication([])
    win = Subdomain()
    win.show()
    sys.exit(app.exec())
