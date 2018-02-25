import sys
from PyQt5.QtWidgets import (QWidget, QGridLayout,
                             QPushButton, QApplication)
from PyQt5.QtGui import QKeyEvent


class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        grid = QGridLayout()
        self.setLayout(grid)

        keyboard = "abcdefghijklmnopqrstuvwxyz1234567890"
        letter_list = []
        for letter in keyboard:
            letter_list.append(letter)
        print(len(letter_list))

        positions_a = [(2, j) for j in range(5)]
        positions_b = [(i, 2) for i in range(5)]
        positions = positions_a + positions_b
        for index in range(0,len(positions)):
            button = QPushButton(keyboard[index])
            grid.addWidget(button, *positions[index])

        self.move(300, 150)
        self.setWindowTitle('Keyboard')
        self.show()

    def keyPressEvent(self, event):
        if type(event) == QKeyEvent:
            # here accept the event and do something
            print(event.key())
            event.accept()
        else:
            event.ignore()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
