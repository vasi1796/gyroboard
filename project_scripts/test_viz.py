import sys
from PyQt5 import QtWidgets, QtCore, QtGui
import datetime
import numpy as np
import serial
import re
from threading import Thread

string_vect = []


def processSerialString(serial_object):
    while True:
        angle_string = serial_object.readline().decode().strip('\t\r\n')
        global string_vect
        string_vect = re.split(r'\t+', angle_string)


class keyboard_scroll(object):
    def __init__(self):
        self.label = QtWidgets.QLabel(Form)
        self.labels = []
        self.letter_list = []
        self.horizontalIndex = 15
        self.verticalIndex = 15
        keyboard = "abcdefghijklmnopqrstuvwxyz1234567890"
        for letter in keyboard:
            self.letter_list.append(letter)
        print(len(self.letter_list))

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 400)
        for index in range(0, 5):
            label = QtWidgets.QLabel(Form)
            label.setGeometry(QtCore.QRect(80 + 50 * index, 80, 40 + 50 * index, 20))
            self.labels.append(label)
        for index in range(0, 5):
            label = QtWidgets.QLabel(Form)
            if index == 2:
                continue
            else:
                label.setGeometry(QtCore.QRect(180, 20 + 20 * index, 40, 20 + 20 * index))
            self.labels.append(label)

        self.label.setGeometry(QtCore.QRect(180, 200, 60, 20))
        self.label.setObjectName("label")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "init clock"))
        for index in range(0, len(self.labels)):
            self.labels[index].setText(_translate("Form", self.letter_list[index]))

    def processAngles(self, angles_string):
        roll_kalman = float(angles_string[2])
        yaw_kalman = float(angles_string[5])
        if roll_kalman > 20:
            return 1
        elif roll_kalman < -20:
            return 2
        elif yaw_kalman > 20:
            return 3
        elif yaw_kalman < -20:
            return 4
        else:
            return 5

    def moveList(self, index, direction):
        if (direction is "up") or (direction is "right"):
            if index is 35:
                index = 0
            localIndex = index
            if direction is "up":
                for label_index in [5, 6, 2, 7, 8]:
                    self.labels[label_index].setText(self.letter_list[localIndex])
                    if localIndex is 35:
                        localIndex = -1
                    localIndex += 1
            else:
                for label_index in range(5):
                    self.labels[label_index].setText(self.letter_list[localIndex])
                    if localIndex is 35:
                        localIndex = -1
                    localIndex += 1
            index += 1
        else:
            if index is 0:
                index = 35
            localIndex = index
            if direction is "down":
                for label_index in [5, 6, 2, 7, 8]:
                    self.labels[label_index].setText(self.letter_list[localIndex])
                    localIndex -= 1
            else:
                for label_index in range(5):
                    self.labels[label_index].setText(self.letter_list[localIndex])
                    localIndex -= 1
            index -= 1
        return index

    def updateLabels(self, angles_string):
        movement = self.processAngles(angles_string)
        if movement is 1:
            self.verticalIndex = self.moveList(self.verticalIndex, "up")
        elif movement is 2:
            self.verticalIndex = self.moveList(self.verticalIndex, "down")
        elif movement is 3:
            self.horizontalIndex = self.moveList(self.horizontalIndex, "right")
        elif movement is 4:
            self.horizontalIndex = self.moveList(self.horizontalIndex, "left")

    def getCenterLabel(self):
        doc = QtGui.QTextDocument()
        doc.setHtml(self.labels[2].text())
        labelText = doc.toPlainText()
        return labelText


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = keyboard_scroll()
    ui.setupUi(Form)
    Form.show()
    ser = serial.Serial('\\.\COM8', 115200)
    ser.close()
    ser.open()
    thread = Thread(target=processSerialString, args=(ser,))
    thread.start()


    def update_label():
        current_time = str(datetime.datetime.now().time())
        ui.label.setText(current_time)
        global string_vect
        if len(string_vect) is 6:
            temp = string_vect
            ui.updateLabels(temp)


    timer = QtCore.QTimer()
    timer.timeout.connect(update_label)
    timer.start(250)  # every 10,000 milliseconds

    # thread.join()
    sys.exit(app.exec_())
