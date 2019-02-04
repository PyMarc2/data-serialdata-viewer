from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from mainWindow import MainWindow
import sys


def main():
    app = QApplication(sys.argv)
    app.setAttribute(Qt.AA_EnableHighDpiScaling)
    app.setStyle("Fusion")
    form = MainWindow()
    form.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
