import sys
from PyQt5 import QtWidgets, QtCore
import datetime
import numpy as np
import serial

class keyboard_scroll(object):
    def __init__(self):
        self.label = QtWidgets.QLabel(Form)
        self.labels = []

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 400)
        for index in range(0,5):
            label=QtWidgets.QLabel(Form)
            label.setGeometry(QtCore.QRect(80+50*index, 80, 40+50*index, 20))
            self.labels.append(label)
        for index in range(0,5):
            label=QtWidgets.QLabel(Form)
            if index == 2:
                continue
            else:
                label.setGeometry(QtCore.QRect(180, 20+20*index, 40, 20+20*index))
            self.labels.append(label)

        self.label.setGeometry(QtCore.QRect(180, 200, 60, 20))
        self.label.setObjectName("label")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "init clock"))
        for index in range(0,len(self.labels)):
            self.labels[index].setText(_translate("Form", "hello"+str(index)))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = keyboard_scroll()
    ui.setupUi(Form)
    Form.show()
    ser = serial.Serial('\\.\COM6', 115200)
    ser.close()
    ser.open()

    def update_label():
        current_time = str(datetime.datetime.now().time())
        ui.label.setText(current_time)
        print(ser.readline())

    timer = QtCore.QTimer()
    timer.timeout.connect(update_label)
    timer.start(500)  # every 10,000 milliseconds

    sys.exit(app.exec_())
