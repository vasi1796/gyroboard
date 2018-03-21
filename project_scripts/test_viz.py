import sys
from PyQt5 import QtWidgets, QtCore
import datetime
import numpy as np
import serial


class keyboard_scroll(object):
    def __init__(self):
        self.label = QtWidgets.QLabel(Form)
        self.labels = []
        self.letter_list = []
        self.horizontalIndex = 0
        self.verticalIndex = 0
        keyboard = "abcdefghijklmnopqrstuvwxyz1234567890"
        for letter in keyboard:
            self.letter_list.append(letter)
        print(self.letter_list)

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
        # process angle string
        return [True, True]

    def moveList(self, index, direction):
        if index is 31:
            index = 0
        if (direction is "up") or (direction is"right"):
            index += 1
            localIndex = index
            if direction is "up":
                for label_index in [5, 6, 2, 7, 8]:
                    self.labels[label_index].setText(self.letter_list[localIndex])
                    localIndex += 1
            else:
                for label_index in range(4,-1,-1):
                    self.labels[label_index].setText(self.letter_list[localIndex])
                    localIndex += 1
                    print(localIndex)
        else:
            index -= 1
            localIndex = index
            if direction is "down":
                for label_index in [8, 7, 2, 6, 5]:
                    self.labels[label_index].setText(self.letter_list[localIndex])
                    localIndex -= 1
            else:
                for label_index in range(5):
                    self.labels[label_index].setText(self.letter_list[localIndex])
                    localIndex -= 1
        return index

    def updateLabels(self, angles_string):
        movements = self.processAngles(angles_string)
        if movements[0] is True:
            print("up")
            self.verticalIndex=self.moveList(self.verticalIndex, "up")
        else:
            print("down")
            #self.verticalIndex=self.moveList(self.verticalIndex, "down")
        if movements[1] is True:
            print("right")
            #self.horizontalIndex=self.moveList(self.horizontalIndex, "right")
        else:
            print("left")
            # self.horizontalIndex=self.moveList(self.horizontalIndex, "left")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = keyboard_scroll()
    ui.setupUi(Form)
    Form.show()
    """ser = serial.Serial('\\.\COM6', 115200)
    ser.close()
    ser.open()"""


    def update_label():
        current_time = str(datetime.datetime.now().time())
        ui.label.setText(current_time)
        ui.updateLabels("12 13 14 15")
        # print(ser.readline())


    timer = QtCore.QTimer()
    timer.timeout.connect(update_label)
    timer.start(500)  # every 10,000 milliseconds

    sys.exit(app.exec_())
