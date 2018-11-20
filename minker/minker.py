import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QIcon, QFont
from minker.tablewidget import TableWidget
from pathlib import Path
import minker.config as config


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Minker")
        iconfile = Path(__file__).parent / 'list.png'
        self.setWindowIcon(QIcon(str(iconfile)))

        tw = TableWidget(self)
        self.setCentralWidget(tw)


def main():
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
    app.setFont(QFont("Ubuntu Mono", config.fontSize))
    m = MainWindow()
    m.setGeometry(200, 200, 600, 809)
    m.show()
    app.exec_()


if __name__ == '__main__':
    main()
