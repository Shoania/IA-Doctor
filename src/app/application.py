import sys

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

from src.ui.mainwindow import MainWindow


def run():

    app = QApplication(sys.argv)

    # ----------------------------------
    # Programm-Icon
    # ----------------------------------

    app.setWindowIcon(
        QIcon("assets/logo.png")
    )

    window = MainWindow()

    window.setWindowIcon(
        QIcon("assets/logo.png")
    )

    window.show()

    sys.exit(app.exec())