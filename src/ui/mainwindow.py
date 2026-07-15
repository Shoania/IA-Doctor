from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QStackedWidget,
    QLabel,
)
from PySide6.QtCore import Qt

from src.ui.sidebar import Sidebar
from src.ui.dashboard import Dashboard
from src.ui.settings import Settings
from src.config.config_manager import ConfigManager
from src.connection.connection_manager import ConnectionManager


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("IA-Doctor 0.4.0")
        self.resize(1300, 800)

        self.build_ui()

    def build_ui(self):

        central = QWidget()
        self.setCentralWidget(central)

        layout = QHBoxLayout(central)

        self.sidebar = Sidebar()
        self.sidebar.setFixedWidth(220)

        self.stack = QStackedWidget()

        self.dashboard = Dashboard()

        self.analyse = QLabel("🔍 Analyse")
        self.analyse.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.reparatur = QLabel("🛠 Reparatur")
        self.reparatur.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.ressourcen = QLabel("📦 Ressourcen")
        self.ressourcen.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.berichte = QLabel("📄 Berichte")
        self.berichte.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.einstellungen = Settings()

        self.stack.addWidget(self.dashboard)
        self.stack.addWidget(self.analyse)
        self.stack.addWidget(self.reparatur)
        self.stack.addWidget(self.ressourcen)
        self.stack.addWidget(self.berichte)
        self.stack.addWidget(self.einstellungen)

        layout.addWidget(self.sidebar)
        layout.addWidget(self.stack)

        self.sidebar.dashboard.clicked.connect(
            lambda: self.stack.setCurrentIndex(0)
        )

        self.sidebar.analyse.clicked.connect(
            lambda: self.stack.setCurrentIndex(1)
        )

        self.sidebar.reparatur.clicked.connect(
            lambda: self.stack.setCurrentIndex(2)
        )

        self.sidebar.ressourcen.clicked.connect(
            lambda: self.stack.setCurrentIndex(3)
        )

        self.sidebar.berichte.clicked.connect(
            lambda: self.stack.setCurrentIndex(4)
        )

        self.sidebar.einstellungen.clicked.connect(
            lambda: self.stack.setCurrentIndex(5)
        )

        # ----------------------------------
        # Auto-Connect
        # ----------------------------------

        config = ConfigManager.load()

        if config.get("auto_connect", False):

            self.statusBar().showMessage(
                "🟡 Verbinde mit Server..."
            )

            self.einstellungen.verbinden()

        # ----------------------------------
        # Statusleiste
        # ----------------------------------

        if ConnectionManager.is_connected():

            self.statusBar().showMessage(
                f"🟢 Verbunden | {config['host']}"
            )

        else:

            self.statusBar().showMessage(
                "🔴 Nicht verbunden"
            )