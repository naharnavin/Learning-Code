import sys
from PyQt5.QtWidgets import QApplication, QDialog, QFileDialog
from designer_file import Ui_Dialog# Import the generated class


class MyDialog(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super(MyDialog, self).__init__(parent)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.open_file_dialog)

    def open_file_dialog(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File", "", "All Files (*);;Text Files (*.txt)", options=options)
        if file_path:
            self.lineEdit.setText(file_path)

def main():
    app = QApplication(sys.argv)
    dialog = MyDialog()
    dialog.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()