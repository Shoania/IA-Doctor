"""
IA-Doctor
Version: 0.10.1

plugin_scanner.py

Analysiert den plugins-Ordner eines Minecraft-Servers.
"""

from pathlib import Path


class PluginScanner:
    """
    Sucht alle Plugin-JAR-Dateien.
    """

    def __init__(self, server_path: str):
        self.server = Path(server_path)

    def scan(self) -> dict:

        plugins_ordner = self.server / "plugins"

        plugin_liste = []

        if plugins_ordner.exists():

            for datei in plugins_ordner.iterdir():

                if not datei.is_file():
                    continue

                if datei.suffix.lower() != ".jar":
                    continue

                plugin = {
                    "file": datei.name,
                    "path": str(datei)
                }

                plugin_liste.append(plugin)

        plugin_liste.sort(key=lambda p: p["file"].lower())

        return {
            "plugin_count": len(plugin_liste),
            "plugin_list": plugin_liste
        }