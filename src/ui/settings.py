"""
IA-Doctor
Version: 0.17.0

Serververbindung
"""

from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QFormLayout,
    QCheckBox,
)

from src.connection.sftp_client import SFTPClient
from src.connection.connection_manager import ConnectionManager
from src.config.config_manager import ConfigManager


class Settings(QWidget):

    def __init__(self):
        super().__init__()

        self.client = None
        self.config = ConfigManager.load()

        layout = QVBoxLayout(self)

        titel = QLabel("🌐 Serververbindung")
        titel.setStyleSheet("""
            font-size:22px;
            font-weight:bold;
        """)

        layout.addWidget(titel)

        form = QFormLayout()

        self.host = QLineEdit()
        self.host.setText(self.config["host"])

        self.port = QLineEdit()
        self.port.setText(str(self.config["port"]))

        self.user = QLineEdit()
        self.user.setText(self.config["username"])

        self.password = QLineEdit()
        self.password.setText(self.config["password"])
        self.password.setEchoMode(QLineEdit.Password)

        form.addRow("Host", self.host)
        form.addRow("Port", self.port)
        form.addRow("Benutzer", self.user)
        form.addRow("Passwort", self.password)

        self.auto_connect = QCheckBox(
            "Beim Start automatisch verbinden"
        )

        self.auto_connect.setChecked(
            self.config.get("auto_connect", False)
        )

        form.addRow("", self.auto_connect)

        layout.addLayout(form)

        self.button = QPushButton("🌐 Verbinden")
        self.button.clicked.connect(self.verbinden)

        layout.addWidget(self.button)

        self.status = QLabel("🔴 Nicht verbunden")
        layout.addWidget(self.status)

        layout.addStretch()

    def verbinden(self):

        self.button.setEnabled(False)
        self.button.setText("⏳ Verbinde...")

        self.status.setText(
            f"🟡 Verbinde mit {self.host.text()}..."
        )

        self.client = SFTPClient(
            self.host.text(),
            int(self.port.text()),
            self.user.text(),
            self.password.text()
        )

        if self.client.connect():

            ConfigManager.save({
                "host": self.host.text(),
                "port": int(self.port.text()),
                "username": self.user.text(),
                "password": self.password.text(),
                "auto_connect": self.auto_connect.isChecked()
            })

            ConnectionManager.set_client(self.client)

            self.status.setText(
                f"🟢 Verbunden mit {self.host.text()}"
            )

            self.button.setText("✅ Verbunden")

        else:

            self.status.setText(
                "🔴 Verbindung fehlgeschlagen"
            )

            self.button.setEnabled(True)
            self.button.setText("🌐 Verbinden")