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
# from xss import checkwaf,xss_,banner,xst_,lfi_
from xss import checkwaf,xss_,banner,xst_
import time




class XSS(QtWidgets.QMainWindow):
    def __init__(self):
        super(XSS, self).__init__()
        uic.loadUi('xssUI.ui', self)
        self.setWindowIcon(QIcon('XSS-file-program-512.png'))
        self.setWindowTitle('XSS')
        # self.lineEdit.returnPressed.connect(self.doCMD)
        # self.pushButtonInstall.clicked.connect(self.onClick)
        self.startBtn.clicked.connect(self.on_startClick)
        self.backBtn.clicked.connect(self.on_backClick)
        self.resetBtn.clicked.connect(self.on_resetClick)

    @pyqtSlot()
    def on_resetClick(self):
        self.url.setText('')
        # self.port.setText('')
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
        #---------checkwaf
        ans=checkwaf(url)
        self.outPut.append(ans)
        self.outPut.append('')

        #---------banner
        ans2=banner(url)
        self.outPut.append(ans2)
        self.outPut.append('')

        # ---------xxs_
        ans1 = xss_(url)
        self.outPut.append('[!] Testing XSS')
        self.outPut.append('[!] 10 Payloads.')
        self.outPut.append('')

        for a in range(len(ans1)):
            self.outPut.append(str(ans1[a]))
        self.outPut.append('')

        #------------lfi
        # self.outPut.append('')
        # self.outPut.append('[!] Testing LFI')
        # self.outPut.append('')
        # ans4=lfi_(url)
        # print(ans4)
        # for a in range(len(ans4)):
        #     self.outPut.append(str(ans4[a]))
        self.outPut.append('')

        #------------xst_
        self.outPut.append('')
        self.outPut.append('Testing XST')
        self.outPut.append('')
        ans3=xst_(url)
        self.outPut.append(ans3)








if __name__ == '__main__':

    app = QtWidgets.QApplication([])
    win = XSS()
    win.show()
    sys.exit(app.exec())
