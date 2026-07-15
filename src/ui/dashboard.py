"""
IA-Doctor
Version: 0.16.0

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
from src.connection.connection_manager import ConnectionManager


class Dashboard(QWidget):
    """
    Represents the main dashboard UI for the IA-Doctor application.
    Allows users to select a Minecraft server, analyze it, and view diagnostic information.
    """

    def __init__(self):
        """
        Initializes the Dashboard widget.
        Sets up the DoctorEngine and builds the user interface.
        """
        super().__init__()

        # Initialize the core analysis engine
        self.engine = DoctorEngine()

        # Build the visual components of the dashboard
        self.build_ui()

    def build_ui(self):
        """
        Constructs the user interface elements for the dashboard.
        Includes a title, server selection input, analysis button, and status display.
        """
        # Main vertical layout for the entire widget
        layout = QVBoxLayout(self)

        # Title label with styling
        titel = QLabel("🏠 Dashboard")
        titel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titel.setStyleSheet("""
            font-size:24px;
            font-weight:bold;
        """)
        layout.addWidget(titel)

        # Add spacing for visual separation
        layout.addSpacing(20)

        # Horizontal layout for server selection input and browse button
        server_layout = QHBoxLayout()

        # Line edit for displaying and entering the server path
        self.server = QLineEdit()
        self.server.setPlaceholderText(
            "Minecraft-Server auswählen..."
        )

        # Button to open a file dialog for server selection
        self.button = QPushButton("📂 Durchsuchen")
        self.button.clicked.connect(self.server_waehlen)

        # Add input field and button to the server layout
        server_layout.addWidget(self.server)
        server_layout.addWidget(self.button)

        # Add the server selection layout to the main layout
        layout.addLayout(server_layout)

        # Add spacing
        layout.addSpacing(15)

        # Button to trigger server analysis
        self.analyse = QPushButton("🔍 Server analysieren")
        self.analyse.setMinimumHeight(45)  # Ensure a consistent button height
        self.analyse.clicked.connect(self.server_analysieren)
        layout.addWidget(self.analyse)

        # Add spacing
        layout.addSpacing(15)

        # Text edit to display analysis results, set to read-only
        self.status = QTextEdit()
        self.status.setReadOnly(True)
        self.status.setText("Noch keine Analyse durchgeführt.")
        layout.addWidget(self.status)

    def server_waehlen(self):
        """
        Opens a file dialog to allow the user to select a Minecraft server directory.
        Updates the server input field with the selected directory path.
        """
        # Open a directory selection dialog
        ordner = QFileDialog.getExistingDirectory(
            self,
            "Minecraft-Server auswählen"
        )

        # If a directory was selected, update the server input field
        if ordner:
            self.server.setText(ordner)

    def server_analysieren(self):
        """
        Initiates the server analysis process.
        Disables the analyze button and updates its text to indicate processing.
        Determines whether to use a connected server or a locally specified path.
        Calls the DoctorEngine to perform the analysis and updates the status text edit.
        Re-enables the analyze button and resets its text upon completion.
        """
        # Disable the analyze button and change its text to show it's processing
        self.analyse.setEnabled(False)
        self.analyse.setText("⏳ Analysiere...")

        # --- Connection Handling ---
        # Check if a connection to a remote server (ByteBlitz) is already established
        if ConnectionManager.is_connected():
            # If connected, analyze the server remotely
            daten = self.engine.analyse_server()
        else:
            # If not connected, check if a local server path has been provided
            if not self.server.text():
                # If no server path is provided, inform the user and stop
                self.status.setText(
                    "Bitte zuerst einen Server auswählen oder eine Serververbindung herstellen."
                )
                # Re-enable button before returning
                self.analyse.setEnabled(True)
                self.analyse.setText("🔍 Server analysieren")
                return

            # If a local path is provided, analyze that server
            daten = self.engine.analyse_server(
                self.server.text()
            )

        # --- Output Formatting ---
        # Initialize a list to hold the lines of the status message
        text = []

        # Add header information
        text.append("🩺 IA-Doctor Diagnose")
        text.append("")
        text.append("=" * 60)
        text.append("")
        text.append("📂 SERVER")
        text.append("-" * 60)

        # Append server status checks with visual indicators
        text.append(
            f"Server gefunden       : {'✅' if daten.get('server_exists', False) else '❌'}"
        )
        text.append(
            f"server.properties     : {'✅' if daten.get('server_properties', False) else '❌'}"
        )
        text.append(
            f"Plugins-Ordner        : {'✅' if daten.get('plugins', False) else '❌'}"
        )
        text.append(
            f"Welt                  : {'✅' if daten.get('world', False) else '❌'}"
        )
        text.append(
            f"Logs                  : {'✅' if daten.get('logs', False) else '❌'}"
        )

        # Check for specific server components like ItemsAdder
        if "itemsadder" in daten:
            text.append(
                f"ItemsAdder            : {'✅' if daten['itemsadder'] else '❌'}"
            )

        text.append("")
        text.append("=" * 60)
        text.append("")
        text.append("📦 PLUGINS")
        text.append("-" * 60)

        # Handle plugin information based on whether it's from a local or remote scan
        if "plugin_list" in daten:  # Local Scanner results
            text.append(
                f"Installierte Plugins : {daten['plugin_count']}"
            )
            text.append("")
            # Iterate through each plugin and display its details
            for plugin in daten["plugin_list"]:
                name = plugin.get("name") or plugin.get("file", "Unbekanntes Plugin")
                version = plugin.get("version", "-")
                author = plugin.get("author", "-")
                text.append(f"📦 {name}")
                text.append(f"   Version : {version}")
                text.append(f"   Autor   : {author}")
                text.append("")
        elif "plugin_files" in daten:  # Remote Scanner results
            text.append(
                f"Installierte Plugins : {len(daten['plugin_files'])}"
            )
            text.append("")
            # List plugin file names
            for plugin in daten["plugin_files"]:
                text.append(f"📦 {plugin}")
            text.append("")

        # --- Plugin Updates Section ---
        if daten.get("updates"):
            text.append("=" * 60)
            text.append("")
            text.append("🔄 PLUGIN-UPDATES")
            text.append("-" * 60)
            # Display details for each plugin update
            for update in daten["updates"]:
                text.append(f"📦 {update.get('name', 'Unbekanntes Plugin')}")
                text.append(f"   Installiert : {update.get('installed', '-')}")
                text.append(f"   Neueste     : {update.get('latest', '-')}")
                text.append(f"   Status      : {update.get('status', 'Unbekannt')}")
                text.append("")

        # --- Server Health Section ---
        if "health_score" in daten:
            text.append("=" * 60)
            text.append("")
            text.append("💚 SERVER HEALTH")
            text.append("-" * 60)

            score = daten.get("health_score", 0)
            # Create a visual health bar
            balken = "█" * (score // 10)
            balken += "░" * (10 - (score // 10))

            text.append("")
            text.append(f"{balken}  {score}%")
            text.append("")
            text.append(daten.get("health_status", "Kein Status verfügbar."))
            text.append("")

            # Display reasons for the health score if available
            if "health_reasons" in daten:
                text.append("Warum dieser Score?")
                text.append("")
                for grund in daten["health_reasons"]:
                    text.append(grund)
                text.append("")

        # --- General Diagnosis Section ---
        # Check if there are any diagnostic messages (info, warnings, errors)
        if "infos" in daten or "warnungen" in daten or "fehler" in daten:
            text.append("")
            text.append("=" * 60)
            text.append("")
            text.append("🧠 DIAGNOSE")
            text.append("-" * 60)

            # Append informational messages
            for info in daten.get("infos", []):
                text.append(f"• {info}")

            # Append warning messages with a warning icon
            for warnung in daten.get("warnungen", []):
                text.append(f"⚠ {warnung}")

            # Append error messages with an error icon
            for fehler in daten.get("fehler", []):
                text.append(f"❌ {fehler}")

        # --- Finalization ---
        text.append("")
        text.append("=" * 60)
        text.append("")
        text.append("🟢 Analyse erfolgreich abgeschlossen.")

        # Set the formatted text to the status display
        self.status.setText("\n".join(text))

        # Re-enable the analyze button and reset its text
        self.analyse.setEnabled(True)
        self.analyse.setText("🔍 Server analysieren")
