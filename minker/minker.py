import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget,\
    QHeaderView
from PyQt5.QtGui import QIcon


class TableWidget(QTableWidget):
    def __init__(self, parent):
        super().__init__(parent)

        header = self.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

        self.setColumnCount(2)
        self.setRowCount(1)

        labels = ["Original", "Transmogrified"]
        self.setHorizontalHeaderLabels(labels)




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
