"""
IA-Doctor
Version: 0.16.1

server_scanner.py
"""

from pathlib import Path


class ServerScanner:

    def __init__(self, server_path: str):

        self.server = Path(server_path)

    def scan(self):

        daten = {}

        daten["server_exists"] = self.server.exists()

        daten["server_properties"] = (
            self.server / "server.properties"
        ).exists()

        daten["plugins"] = (
            self.server / "plugins"
        ).exists()

        daten["world"] = (
            self.server / "world"
        ).exists()

        daten["logs"] = (
            self.server / "logs"
        ).exists()

        daten["itemsadder"] = (
            self.server / "plugins" / "ItemsAdder"
        ).exists()

        return daten