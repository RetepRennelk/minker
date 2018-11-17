import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QIcon
from tablewidget import TableWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Minker")
        self.setWindowIcon(QIcon('list.png'))

        tw = TableWidget(self)
        self.setCentralWidget(tw)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    m = MainWindow()
    m.show()
    app.exec_()
