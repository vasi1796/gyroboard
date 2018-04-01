import sys
from PyQt5 import QtWidgets, QtCore, QtGui
import datetime
import serial
import re
from threading import Thread
from GazeNN import GazeNN

string_vect = []
eye_position = -1
init_index = 15
form_width = 1500
form_height = 400


def process_gaze(network):
    while True:
        global eye_position
        eye_position = network.process_image()


def process_serial_string(serial_object):
    while True:
        angle_string = serial_object.readline().decode().strip('\t\r\n')
        global string_vect
        string_vect = re.split(r'\t+', angle_string)


class KeyboardScroll(object):
    def __init__(self):
        self.label = QtWidgets.QLabel(Form)
        self.board_labels = []
        self.pred_word_labels = []
        self.letter_list = []
        self.horizontalIndex = init_index
        self.verticalIndex = init_index
        keyboard = "abcdefghijklmnopqrstuvwxyz1234567890"
        for letter in keyboard:
            self.letter_list.append(letter)

    def setup_ui(self, Form):
        Form.setObjectName("Form")
        Form.resize(form_width, form_height)
        # horizontal keyboard
        for index in range(5):
            label = QtWidgets.QLabel(Form)
            label.setGeometry(QtCore.QRect(int(form_width / 2.3 + 50 * index), 80, 40 + 50 * index, 20))
            self.board_labels.append(label)
        # vertical keyboard
        for index in range(5):
            label = QtWidgets.QLabel(Form)
            if index == 2:
                continue
            else:
                label.setGeometry(QtCore.QRect(int(form_width / 2.3 + 50 * 2), 20 + 20 * index, 40, 20 + 20 * index))
            self.board_labels.append(label)
        # predicted words
        for index in range(3):
            label = QtWidgets.QLabel(Form)
            label.setGeometry(QtCore.QRect(int(form_width / 15 + 650 * index), 250, 40 + 50 * index, 20))
            self.pred_word_labels.append(label)
        self.label.setGeometry(QtCore.QRect(int(form_width / 2.3 + 50 * 2), 200, 60, 20))
        self.label.setObjectName("label")

        self.init_ui_labels(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def init_ui_labels(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "init clock"))
        for index in range(0, len(self.board_labels)):
            self.board_labels[index].setText(_translate("Form", self.letter_list[init_index + index]))
        for index in range(0, len(self.pred_word_labels)):
            self.pred_word_labels[index].setText(_translate("Form", "test" + str(index)))

    def process_angles(self, angles_string):
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

    def move_list(self, index, direction):
        if (direction is "up") or (direction is "right"):
            if index is 35:
                index = 0
            localIndex = index
            if direction is "up":
                for label_index in [5, 6, 2, 7, 8]:
                    self.board_labels[label_index].setText(self.letter_list[localIndex])
                    if localIndex is 35:
                        localIndex = -1
                    localIndex += 1
            else:
                for label_index in range(5):
                    self.board_labels[label_index].setText(self.letter_list[localIndex])
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
                    self.board_labels[label_index].setText(self.letter_list[localIndex])
                    if localIndex is 35:
                        localIndex = -1
                    localIndex += 1
            else:
                for label_index in range(5):
                    self.board_labels[label_index].setText(self.letter_list[localIndex])
                    if localIndex is 35:
                        localIndex = -1
                    localIndex += 1
            index -= 1
        return index

    def update_labels(self, angles_string):
        movement = self.process_angles(angles_string)
        if movement is 1:
            self.verticalIndex = self.move_list(self.verticalIndex, "up")
        elif movement is 2:
            self.verticalIndex = self.move_list(self.verticalIndex, "down")
        elif movement is 3:
            self.horizontalIndex = self.move_list(self.horizontalIndex, "right")
        elif movement is 4:
            self.horizontalIndex = self.move_list(self.horizontalIndex, "left")
        self.color_word_label(eye_position)

    def get_center_label(self):
        doc = QtGui.QTextDocument()
        doc.setHtml(self.board_labels[2].text())
        labelText = doc.toPlainText()
        return labelText

    def color_word_label(self, position):
        if position == 0:
            self.pred_word_labels[0].setStyleSheet('color: blue')
            self.pred_word_labels[1].setStyleSheet('color: black')
            self.pred_word_labels[2].setStyleSheet('color: black')
        elif position == 2:
            self.pred_word_labels[0].setStyleSheet('color: black')
            self.pred_word_labels[1].setStyleSheet('color: blue')
            self.pred_word_labels[2].setStyleSheet('color: black')
        elif position == 1:
            self.pred_word_labels[0].setStyleSheet('color: black')
            self.pred_word_labels[1].setStyleSheet('color: black')
            self.pred_word_labels[2].setStyleSheet('color: blue')


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = KeyboardScroll()
    ui.setup_ui(Form)
    Form.show()

    ser = serial.Serial('\\.\COM8', 115200)
    ser.close()
    ser.open()

    gaze_nn = GazeNN('./models/gaze.json', './models/gaze.h5')
    gazeNN_thread = Thread(target=process_gaze, args=(gaze_nn,))
    gazeNN_thread.start()

    arduino_thread = Thread(target=process_serial_string, args=(ser,))
    arduino_thread.start()


    def update_label():
        current_time = str(datetime.datetime.now().time())
        ui.label.setText(current_time)
        global string_vect
        if len(string_vect) is 6:
            temp = string_vect
            ui.update_labels(temp)


    timer = QtCore.QTimer()
    timer.timeout.connect(update_label)
    timer.start(250)  # every 10,000 milliseconds

    # thread.join()
    sys.exit(app.exec_())
