from PyQt5.QtWidgets import QTextEdit, QSizeGrip, QVBoxLayout, \
    QShortcut, QApplication
from PyQt5.QtCore import Qt, QItemSelectionModel
from PyQt5.QtGui import QKeySequence, QTextCursor
import minker.config as config


class TextEdit(QTextEdit):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowFlag(Qt.SubWindow)
        sizeGrip = QSizeGrip(self)
        layout = QVBoxLayout(self)
        layout.addWidget(sizeGrip, 0, Qt.AlignBottom | Qt.AlignRight)

        shortcut = QShortcut(QKeySequence("Ctrl+Down"), self)
        shortcut.activated.connect(self.splitCell)

        font = self.font()
        font.setPointSize(config.fontSize)
        self.setFont(font)

        self.document().contentsChanged.connect(self.sizeChange)

    def splitCell(self):
        self.moveCursor(QTextCursor.End, QTextCursor.KeepAnchor)
        tc = self.textCursor()
        txt = tc.selectedText()

        self.moveCursor(QTextCursor.End, QTextCursor.KeepAnchor)
        tc.removeSelectedText()

        tableWidget = self.parent().parent()
        newRow = tableWidget.splitCellCmd(txt)

        tableWidget.clearSelection()
        tableWidget.setCurrentCell(newRow, 0, QItemSelectionModel.Select)

    def sizeChange(self):
        h = self.document().size().height()
        if h < self.parent().geometry().height():
            self.setMinimumHeight(h)
