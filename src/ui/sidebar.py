from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout


class Sidebar(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        self.dashboard = QPushButton("🏠 Dashboard")
        self.analyse = QPushButton("🔍 Analyse")
        self.reparatur = QPushButton("🛠 Reparatur")
        self.ressourcen = QPushButton("📦 Ressourcen")
        self.berichte = QPushButton("📄 Berichte")
        self.einstellungen = QPushButton("⚙ Einstellungen")

        for button in [
            self.dashboard,
            self.analyse,
            self.reparatur,
            self.ressourcen,
            self.berichte,
            self.einstellungen,
        ]:
            button.setMinimumHeight(45)
            layout.addWidget(button)

        layout.addStretch()