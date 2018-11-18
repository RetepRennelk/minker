from PyQt5.QtWidgets import QTableWidget, QHeaderView, QShortcut, \
    QTableWidgetItem, QUndoStack
from PyQt5.QtGui import QKeySequence
from PyQt5.QtCore import QItemSelectionModel
from delegate import StyledItemDelegate
from commands import CopyCellCommand


class TableWidget(QTableWidget):
    def __init__(self, parent):
        super().__init__(parent)

        header = self.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

        self.setColumnCount(2)
        self.setRowCount(1)

        labels = ["Original", "Transmogrified"]
        self.setHorizontalHeaderLabels(labels)

        self.setItemDelegate(StyledItemDelegate(self))

        self.undoStack = QUndoStack(self)
        shortcut = QShortcut(QKeySequence.Undo, self)
        shortcut.activated.connect(self.undoStack.undo)

        shortcut = QShortcut(QKeySequence.Redo, self)
        shortcut.activated.connect(self.undoStack.redo)

        shortcut = QShortcut(QKeySequence("Ctrl+Right"), self)
        shortcut.activated.connect(self.copyCellCmd)

    def isNeighborCellEmpty(self):
        select = self.selectionModel()
        if select.currentIndex().column() != 0:
            return False
        row = select.currentIndex().row()
        item = self.item(row, 1)
        if item is not None:
            if item.text() != "":
                return False
        return True

    def splitCellCmd(self, txt):
        splitCellCommand = SplitCellCommand(self, txt)
        self.undoStack.push(splitCellCommand)
        return splitCellCommand.newRow

    def copyCell(self):
        select = self.selectionModel()
        if select.currentIndex().column() != 0:
            return
        txt = self.currentItem().text()
        newItem = QTableWidgetItem(txt)
        row = select.currentIndex().row()
        self.setItem(row, 1, newItem)

    def copyCellCmd(self):
        select = self.selectionModel()
        row = select.currentIndex().row()

        copyCellCommand = CopyCellCommand(self)
        if copyCellCommand.hasCopiedCell:
            self.undoStack.push(copyCellCommand)

        self.clearSelection()
        self.setCurrentCell(row, 1, QItemSelectionModel.Select)

    def populate(self, L):
        self.clearContents()
        self.setRowCount(0)
        self.setRowCount(len(L))
        for r in range(len(L)):
            for c in range(2):
                newItem = QTableWidgetItem(L[r][c])
                self.setItem(r, c, newItem)
