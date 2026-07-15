"""
IA-Doctor
Version: 0.20.0

doctor_engine.py
"""

from src.connection.connection_manager import ConnectionManager

from src.scanner.server_scanner import ServerScanner
from src.scanner.plugin_scanner import PluginScanner
from src.scanner.remote_server_scanner import RemoteServerScanner
from src.scanner.diagnose_scanner import DiagnoseScanner
from src.scanner.health_scanner import HealthScanner


class DoctorEngine:

    def analyse_server(self, server_path: str = "") -> dict:

        # -------------------------
        # Remote-Server
        # -------------------------

        if ConnectionManager.is_connected():

            scanner = RemoteServerScanner()

            ergebnis = scanner.scan()

            diagnose = DiagnoseScanner(ergebnis)

            ergebnis.update(diagnose.scan())

            health = HealthScanner(ergebnis)

            ergebnis.update(health.scan())

            return ergebnis

        # -------------------------
        # Lokaler Server
        # -------------------------

        server_scanner = ServerScanner(server_path)
        server_daten = server_scanner.scan()

        plugin_scanner = PluginScanner(server_path)
        plugin_daten = plugin_scanner.scan()

        ergebnis = {}

        ergebnis.update(server_daten)
        ergebnis.update(plugin_daten)

        diagnose = DiagnoseScanner(ergebnis)

        ergebnis.update(diagnose.scan())

        health = HealthScanner(ergebnis)

        ergebnis.update(health.scan())

        return ergebnis