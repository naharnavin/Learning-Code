import sys
import random
import pandas as pd
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QProgressBar, QFileDialog, QStackedWidget
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor, QPalette
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class LoginWindow(QWidget):
    def __init__(self, parent=None):
        super(LoginWindow, self).__init__(parent)
        self.setWindowTitle("Login")
        self.setGeometry(100, 50 ,300, 150)
        layout = QVBoxLayout()

        self.username_label = QLabel("Username:")
        self.username_input = QLineEdit()
        self.password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.check_login)

        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)

        self.setLayout(layout)

    def check_login(self):
        # Simple login check
        if self.username_input.text() == "admin" and self.password_input.text() == "password":
            self.parent().setCurrentIndex(1)
        else:
            self.username_input.clear()
            self.password_input.clear()

class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(PlotCanvas, self).__init__(fig)
        self.setParent(parent)
        self.plot()

    def plot(self):
        data = [random.randint(0, 10) for _ in range(10)]
        self.axes.clear()
        self.axes.plot(data, 'r-')
        self.axes.set_title('Random Data Plot')
        self.draw()

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Main Window")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.drag_drop_label = QLabel("Drag and Drop Excel Files Here")
        self.drag_drop_label.setAlignment(Qt.AlignCenter)
        self.drag_drop_label.setStyleSheet("border: 2px dashed #aaa; padding: 20px;")
        self.drag_drop_label.setFont(QFont("Arial", 14))
        self.drag_drop_label.setAcceptDrops(True)

        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)

        self.file_name_label = QLabel("No file loaded")
        self.file_name_label.setFont(QFont("Arial", 12))

        self.load_button = QPushButton("Load File")
        self.load_button.clicked.connect(self.load_file)

        self.plot_canvas = PlotCanvas(self, width=5, height=4)

        self.layout.addWidget(self.drag_drop_label)
        self.layout.addWidget(self.file_name_label)
        self.layout.addWidget(self.progress_bar)
        self.layout.addWidget(self.load_button)
        self.layout.addWidget(self.plot_canvas)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        if urls:
            file_path = urls[0].toLocalFile()
            self.load_excel(file_path)

    def load_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Excel File", "", "Excel Files (*.xlsx *.xls)")
        if file_path:
            self.load_excel(file_path)

    def load_excel(self, file_path):
        self.file_name_label.setText(f"Loading: {file_path}")
        self.progress_bar.setValue(0)
        QApplication.processEvents()

        # Simulate loading process
        try:
            df = pd.read_excel(file_path)
            self.progress_bar.setValue(100)
            self.file_name_label.setText(f"Loaded: {file_path}")
        except Exception as e:
            self.file_name_label.setText(f"Failed to load: {file_path}")
            self.progress_bar.setValue(0)

class App(QStackedWidget):
    def __init__(self):
        super(App, self).__init__()
        self.setWindowTitle("PyQt5 Application")
        self.setGeometry(100, 100, 800, 600)

        self.login_window = LoginWindow(self)
        self.main_window = MainWindow()

        self.addWidget(self.login_window)
        self.addWidget(self.main_window)

        self.setCurrentIndex(0)

def main():
    app = QApplication(sys.argv)

    # Set a modern style
    app.setStyle("Fusion")
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, Qt.white)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, Qt.black)
    app.setPalette(palette)

    main_app = App()
    main_app.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()