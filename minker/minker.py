import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QIcon, QFont
from tablewidget import TableWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Minker")
        self.setWindowIcon(QIcon('list.png'))

        tw = TableWidget(self)
        self.setCentralWidget(tw)


if __name__ == '__main__':
    sCSS = '''
    QTableWidget {
        gridline-color: black;
    }
    QHeaderView::section {
        background-color: black;
        color: white
    }
    '''
    app = QApplication(sys.argv)
    app.setStyleSheet(sCSS)
    app.setFont(QFont("Ubuntu Mono", 16))
    m = MainWindow()
    m.setGeometry(200, 200, 600, 809)
    m.show()
    app.exec_()

