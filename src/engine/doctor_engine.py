"""
IA-Doctor
Version: 0.10.1

doctor_engine.py

Steuert alle Scanner von IA-Doctor.
"""

from src.scanner.server_scanner import ServerScanner
from src.scanner.plugin_scanner import PluginScanner


class DoctorEngine:
    """
    Startet alle Scanner und sammelt deren Ergebnisse.
    """

    def analyse_server(self, server_path: str) -> dict:

        server_scanner = ServerScanner(server_path)
        server_daten = server_scanner.scan()

        plugin_scanner = PluginScanner(server_path)
        plugin_daten = plugin_scanner.scan()

        ergebnis = {}

        ergebnis.update(server_daten)
        ergebnis.update(plugin_daten)

        return ergebnis