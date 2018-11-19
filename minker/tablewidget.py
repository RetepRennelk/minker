from PyQt5.QtWidgets import QTableWidget, QHeaderView, QShortcut,\
    QTableWidgetItem, QUndoStack, QFileDialog
from PyQt5.QtGui import QKeySequence
from PyQt5.QtCore import QItemSelectionModel
from minker.delegate import StyledItemDelegate
from minker.commands import CopyCellCommand, SplitCellCommand, \
    SwapRowsCommand, DeleteRowCommand, InsertRowAboveCommand, \
    InsertRowBelowCommand
import json
from minker.export_dialog import ExportDialog


class TableWidget(QTableWidget):
    def __init__(self, parent):
        super().__init__(parent)

        header = self.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

        self.setColumnCount(2)
        self.setRowCount(1)

        self.cellChanged.connect(self.resize)

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

        shortcut = QShortcut(QKeySequence("Alt+Down"), self)
        shortcut.activated.connect(self.swapRowDown)
        shortcut = QShortcut(QKeySequence("Alt+Up"), self)
        shortcut.activated.connect(self.swapRowUp)

        shortcut = QShortcut(QKeySequence("Ctrl+D"), self)
        shortcut.activated.connect(self.deleteRow)

        shortcut = QShortcut(QKeySequence("Ctrl+S"), self)
        shortcut.activated.connect(self.save)

        shortcut = QShortcut(QKeySequence("Ctrl+O"), self)
        shortcut.activated.connect(self.open)

        shortcut = QShortcut(QKeySequence("Ctrl+E"), self)
        shortcut.activated.connect(self.export)

        shortcut = QShortcut(QKeySequence("Ctrl+A"), self)
        shortcut.activated.connect(self.insertRowAbove)

        shortcut = QShortcut(QKeySequence("Ctrl+B"), self)
        shortcut.activated.connect(self.insertRowBelow)

        self.setAlternatingRowColors(True)
        css='''alternate-background-color: floralwhite; 
        background-color: white;
        '''
        self.setStyleSheet(css)
        

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

    def swapRowDown(self):
        self.swapRows(+1)

    def swapRowUp(self):
        self.swapRows(-1)

    def swapRows(self, direction):
        swapRowsCommand = SwapRowsCommand(self, direction)
        if swapRowsCommand.hasSwappedCells:
            self.undoStack.push(swapRowsCommand)

            self.clearSelection()
            r = swapRowsCommand.newRow
            c = swapRowsCommand.newColumn
            self.setCurrentCell(r, c, QItemSelectionModel.Select)

    def resize(self, row, column):
        self.resizeRowsToContents()

    def resizeEvent(self, event):
        self.resizeRowsToContents()
        super().resizeEvent(event)

    def deleteRow(self):
        if self.rowCount() > 1:
            select = self.selectionModel()
            row = select.currentIndex().row()
            deleteRowCommand = DeleteRowCommand(self, row)
            self.undoStack.push(deleteRowCommand)
            
    def snapshot(self):
        L = []
        for r in range(self.rowCount()):
            l = []
            for c in range(self.columnCount()):
                i = self.item(r, c)
                l.append("" if i is None else i.text())
            L.append(l)
        return L

    def save(self):
        fd = QFileDialog()
        fd.setNameFilter("Minker files (*.mkon)")
        if (fd.exec()):
            filename = fd.selectedFiles()[0]
            if not filename.endswith(".mkon"):
                filename += ".mkon"
            with open(filename, 'w') as f:
                json.dump(self.snapshot(), f)

    def open(self):
        fd = QFileDialog()
        fd.setNameFilter("Minker files (*.mkon)")
        if (fd.exec()):
            filename = fd.selectedFiles()[0]
            if not filename.endswith(".mkon"):
                filename += ".mkon"
            with open(filename, 'r') as f:
                self.populate(json.load(f))

    def getColumnText(self, column):
        str = ""
        for r in range(self.rowCount()):
            i = self.item(r, column)
            str += "" if i is None else i.text() + "\n\n"
        return str

    def export(self):
        d = ExportDialog()
        d.setLeftText(self.getColumnText(0))
        d.setRightText(self.getColumnText(1))
        d.exec()

    def selectCell(self, row, col):
        self.clearSelection()
        self.setCurrentCell(row, col, QItemSelectionModel.Select)

    def insertRowAbove(self):
        insertRowAboveCommand = InsertRowAboveCommand(self)
        self.undoStack.push(insertRowAboveCommand)
        self.selectCell(insertRowAboveCommand.newRow, insertRowAboveCommand.col)

    def insertRowBelow(self):
        insertRowBelowCommand = InsertRowBelowCommand(self)
        self.undoStack.push(insertRowBelowCommand)
        self.selectCell(insertRowBelowCommand.newRow, insertRowBelowCommand.col)
