from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QIcon
import sys
from sql import checkwaf,header,banner,sql_
import os
import subprocess
from sub import main
import time
 


class SQL(QtWidgets.QMainWindow): # icon/ headers / and button initilize 
    def __init__(self):
        super(SQL, self).__init__()
        uic.loadUi('sqlxssUI.ui', self)
        self.setWindowIcon(QIcon('3358758-200.png'))
        self.setWindowTitle('SQL Injection Vulnerbility')
        # self.lineEdit.returnPressed.connect(self.doCMD)
        # self.pushButtonInstall.clicked.connect(self.onClick)
        self.startBtn.clicked.connect(self.on_startClick)
        self.backBtn.clicked.connect(self.on_backClick)
        self.resetBtn.clicked.connect(self.on_resetClick)

    @pyqtSlot() #all values null
    def on_resetClick(self):
        self.url.setText('')
        # self.port.setText('')
        self.outPut.setText('')

    @pyqtSlot() # main form import 
    def on_backClick(self):
        from startUI import Start
        self.f = Start()
        self.f.show()
        self.hide()


    @pyqtSlot() # outPut.append for printing purpose 
    def on_startClick(self):
        url=str(self.url.text())
        payload=str(self.url_2.text())
        # checkwaf(url)
        # banner(url)
        # header(url)
        # sql_(url)
        self.outPut.append('Executing...')
        self.outPut.append('')
        self.outPut.append('')

        # return from checkwaf is ans and ans is appended to ouput - which is showing the result

        ans=checkwaf(url) 
        self.outPut.append(str(ans))
        self.outPut.append('')

        self.outPut.append('')
        self.outPut.append('')
        self.outPut.append('')
        ans1=banner(url)
        self.outPut.append(str(ans1))
        self.outPut.append('')

        self.outPut.append('')
        self.outPut.append('')
        self.outPut.append('')
        ans2=header(url)

        for aa in ans2:
            self.outPut.append(str(aa))

        self.outPut.append('')

        self.outPut.append('')
        self.outPut.append('[!] Testing SQLi')
        self.outPut.append('')
        ans3=sql_(url,payload)
        for one in ans3[0]:
            self.outPut.append(str(one))
        for two in ans3[1]:
            self.outPut.append(str(two))
        # for i in range(len(ans3[1])):
        #     self.outPut.append(ans3[i])

        self.outPut.append('')
        self.outPut.append('')


if __name__ == '__main__':

    app = QtWidgets.QApplication([])
    win = SQL()
    win.show()
    sys.exit(app.exec())
