import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QIcon, QFont
from minker.tablewidget import TableWidget
from pathlib import Path
import minker.config as config


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        iconfile = Path(__file__).parent / 'list.png'
        self.setWindowIcon(QIcon(str(iconfile)))
        self.setWindowTitle()

        tw = TableWidget(self)
        self.setCentralWidget(tw)

    def setWindowTitle(self):
        super().setWindowTitle(config.windowTitle)

    def setExtendedWindowTitle(self, fileName):
        super().setWindowTitle(config.windowTitle + ": " + fileName)

    def setModifiedWindowTitle(self, fileName):
        if fileName != "":
            s = config.windowTitle + ": " + fileName + " (*)"
            super().setWindowTitle(s)


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
