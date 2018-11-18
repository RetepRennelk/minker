from PyQt5.QtWidgets import QTextEdit, QSizeGrip, QVBoxLayout, \
    QShortcut, QApplication
from PyQt5.QtCore import Qt, QItemSelectionModel
from PyQt5.QtGui import QKeySequence, QTextCursor


class TextEdit(QTextEdit):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowFlag(Qt.SubWindow)
        sizeGrip = QSizeGrip(self)
        layout = QVBoxLayout(self)
        layout.addWidget(sizeGrip, 0, Qt.AlignBottom | Qt.AlignRight)

        shortcut = QShortcut(QKeySequence("Ctrl+Down"), self)
        shortcut.activated.connect(self.splitCell)

    def splitCell(self):
        self.moveCursor(QTextCursor.End, QTextCursor.KeepAnchor)
        self.cut()
        clipboard = QApplication.clipboard()
        tableWidget = self.parent().parent()
        newRow = tableWidget.splitCellCmd(clipboard.text())

        tableWidget.clearSelection()
        tableWidget.setCurrentCell(newRow, 0, QItemSelectionModel.Select)
