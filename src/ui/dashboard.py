"""
IA-Doctor
Version: 0.10.1

Dashboard
"""

from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QLineEdit,
    QTextEdit,
    QVBoxLayout,
    QHBoxLayout,
    QFileDialog,
)

from PySide6.QtCore import Qt

from src.engine.doctor_engine import DoctorEngine


class Dashboard(QWidget):

    def __init__(self):
        super().__init__()

        self.engine = DoctorEngine()

        self.build_ui()

    def build_ui(self):

        layout = QVBoxLayout(self)

        titel = QLabel("🏠 Dashboard")
        titel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titel.setStyleSheet("""
            font-size:24px;
            font-weight:bold;
        """)

        layout.addWidget(titel)

        layout.addSpacing(20)

        server_layout = QHBoxLayout()

        self.server = QLineEdit()
        self.server.setPlaceholderText(
            "Minecraft-Server auswählen..."
        )

        button = QPushButton("📂 Durchsuchen")
        button.clicked.connect(self.server_waehlen)

        server_layout.addWidget(self.server)
        server_layout.addWidget(button)

        layout.addLayout(server_layout)

        layout.addSpacing(15)

        analyse = QPushButton("🔍 Server analysieren")
        analyse.setMinimumHeight(45)
        analyse.clicked.connect(self.server_analysieren)

        layout.addWidget(analyse)

        layout.addSpacing(15)

        self.status = QTextEdit()
        self.status.setReadOnly(True)
        self.status.setText("Noch keine Analyse durchgeführt.")

        layout.addWidget(self.status)

    def server_waehlen(self):

        ordner = QFileDialog.getExistingDirectory(
            self,
            "Minecraft-Server auswählen"
        )

        if ordner:
            self.server.setText(ordner)

    def server_analysieren(self):

        if not self.server.text():

            self.status.setText(
                "Bitte zuerst einen Server auswählen."
            )

            return

        daten = self.engine.analyse_server(
            self.server.text()
        )

        text = []

        text.append("🩺 IA-Doctor Diagnose")
        text.append("")
        text.append("=" * 50)
        text.append("")

        text.append(
            f"📂 Server gefunden: {'✅' if daten['server_exists'] else '❌'}"
        )

        text.append(
            f"⚙️ server.properties: {'✅' if daten['server_properties'] else '❌'}"
        )

        text.append(
            f"📦 Plugins-Ordner: {'✅' if daten['plugins'] else '❌'}"
        )

        text.append(
            f"🌍 Welt: {'✅' if daten['world'] else '❌'}"
        )

        text.append(
            f"📄 Logs: {'✅' if daten['logs'] else '❌'}"
        )

        text.append(
            f"🧩 ItemsAdder: {'✅' if daten['itemsadder'] else '❌'}"
        )

        text.append("")
        text.append(f"📊 Installierte Plugins: {daten['plugin_count']}")
        text.append("")
        text.append("Plugin-Liste")
        text.append("-" * 50)

        if daten["plugin_list"]:

            for plugin in daten["plugin_list"]:
                text.append(f"• {plugin['file']}")

        else:

            text.append("Keine Plugins gefunden.")

        self.status.setText("\n".join(text))