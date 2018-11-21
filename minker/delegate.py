from PyQt5.QtWidgets import QStyledItemDelegate
from PyQt5.QtCore import Qt, QEvent
from minker.textedit import TextEdit
from minker.commands import ChangeCellCommand


class StyledItemDelegate(QStyledItemDelegate):
    def __init__(self, parent):
        super().__init__(parent)
        self.installEventFilter(self)

    def createEditor(self, parent, option, index):
        self.changeCellCommand = ChangeCellCommand(self.parent())
        self.t = TextEdit(parent)
        return self.t

    def setEditorData(self, editor, index):
        value = index.model().data(index, Qt.EditRole)
        editor.setPlainText(value)

    def setModelData(self, editor, model, index):
        str = editor.toPlainText()
        model.setData(index, str, Qt.EditRole)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)

    def eventFilter(self, editor, event):
        if event.type() == QEvent.KeyPress:
            sw1 = event.modifiers() == Qt.ControlModifier
            sw2 = event.key() == Qt.Key_Return
            if sw1 and sw2:
                self.commit_and_close_editor()
                return False
        elif event.type() == QEvent.FocusOut:
            self.commit_and_close_editor()
            return False
        return super().eventFilter(editor, event)

    def commit_and_close_editor(self):
        print(type(self.parent()))
        self.commitData.emit(self.t)
        self.closeEditor.emit(self.t)

        self.changeCellCommand.commit()
        self.parent().undoStack.push(self.changeCellCommand)
