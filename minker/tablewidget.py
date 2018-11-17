from PyQt5.QtWidgets import QTableWidget, QHeaderView
from delegate import StyledItemDelegate


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
