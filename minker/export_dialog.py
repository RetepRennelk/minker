from PyQt5.QtWidgets import QDialog, QHBoxLayout, QTextEdit
from PyQt5.QtCore import Qt


class ExportDialog(QDialog):
    def __init__(self):
        super().__init__()

        flags = self.windowFlags()
        flags &= ~Qt.WindowContextHelpButtonHint
        flags &= Qt.Window
        self.setWindowFlags(flags)

        layout = QHBoxLayout(self)
        self.te_left = QTextEdit(self)
        self.te_right = QTextEdit(self)
        layout.addWidget(self.te_left)
        layout.addWidget(self.te_right)

        self.setGeometry(200, 200, 1309, 809)

    def setLeftText(self, txt):
        self.te_left.setText(txt)

    def setRightText(self, txt):
        self.te_right.setText(txt)
