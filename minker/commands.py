from PyQt5.QtWidgets import QUndoCommand, QTableWidgetItem


class UndoCommand(QUndoCommand):
    def __init__(self, tableWidget):
        super().__init__()
        self.tableWidget = tableWidget

    def snapshot(self):
        t = self.tableWidget
        L = []
        for r in range(t.rowCount()):
            l = []
            for c in range(t.columnCount()):
                i = t.item(r, c)
                l.append("" if i is None else i.text())
            L.append(l)
        return L

    def undo(self):
        self.tableWidget.populate(self.oldTableContent)

    def redo(self):
        self.tableWidget.populate(self.newTableContent)


class CopyCellCommand(UndoCommand):
    def __init__(self, tableWidget):
        super().__init__(tableWidget)
        self.hasCopiedCell = False
        if tableWidget.isNeighborCellEmpty():
            self.oldTableContent = self.snapshot()
            tableWidget.copyCell()
            self.newTableContent = self.snapshot()
            self.hasCopiedCell = True


class SplitCellCommand(UndoCommand):
    def __init__(self, tableWidget, txt):
        super().__init__(tableWidget)
        self.oldTableContent = self.snapshot()
        self.newRow = self.insertRowBelow(txt)
        self.newTableContent = self.snapshot()

    def insertRowBelow(self, txt):
        tw = self.tableWidget
        select = tw.selectionModel()
        r = select.currentIndex().row()
        tw.insertRow(r+1)
        newItem = QTableWidgetItem(txt)
        tw.setItem(r+1, 0, newItem)

        d = tw.itemDelegate()
        d.commit_and_close_editor()

        newRow = r+1
        return newRow

