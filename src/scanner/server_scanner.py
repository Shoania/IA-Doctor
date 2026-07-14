"""
IA-Doctor
Version: 0.8.2

server_scanner.py

Analysiert die Grundstruktur eines Minecraft-Servers
und die Installation von ItemsAdder.
"""

from pathlib import Path
import yaml


class ServerScanner:

    def __init__(self, server_path: str):
        self.server = Path(server_path)

    def scan(self) -> dict:

        ergebnis = {}

        # -------------------------
        # Server
        # -------------------------

        plugins_ordner = self.server / "plugins"
        logs_ordner = self.server / "logs"
        world_ordner = self.server / "world"
        server_properties = self.server / "server.properties"

        # -------------------------
        # ItemsAdder
        # -------------------------

        itemsadder_ordner = plugins_ordner / "ItemsAdder"

        contents_ordner = itemsadder_ordner / "contents"
        data_ordner = itemsadder_ordner / "data"
        storage_ordner = itemsadder_ordner / "storage"

        plugin_yml = itemsadder_ordner / "plugin.yml"

        # -------------------------
        # Server prüfen
        # -------------------------

        ergebnis["server_exists"] = self.server.exists()
        ergebnis["server_properties"] = server_properties.exists()
        ergebnis["plugins"] = plugins_ordner.exists()
        ergebnis["logs"] = logs_ordner.exists()
        ergebnis["world"] = world_ordner.exists()

        # -------------------------
        # ItemsAdder prüfen
        # -------------------------

        ergebnis["itemsadder"] = itemsadder_ordner.exists()
        ergebnis["contents"] = contents_ordner.exists()
        ergebnis["data"] = data_ordner.exists()
        ergebnis["storage"] = storage_ordner.exists()

        # -------------------------
        # Plugin-Anzahl
        # -------------------------

        plugin_count = 0

        if plugins_ordner.exists():
            plugin_count = len(
                [datei for datei in plugins_ordner.iterdir() if datei.is_file()]
            )

        ergebnis["plugin_count"] = plugin_count

        # -------------------------
        # Content-Packs
        # -------------------------

        contentpack_count = 0

        if contents_ordner.exists():
            contentpack_count = len(
                [ordner for ordner in contents_ordner.iterdir() if ordner.is_dir()]
            )

        ergebnis["contentpack_count"] = contentpack_count

        # -------------------------
        # ItemsAdder-Version
        # -------------------------

        version = "Unbekannt"

        if plugin_yml.exists():

            try:
                with open(plugin_yml, "r", encoding="utf-8") as datei:
                    daten = yaml.safe_load(datei)

                version = daten.get("version", "Unbekannt")

            except Exception:
                version = "Unbekannt"

        ergebnis["itemsadder_version"] = version

        # -------------------------
        # Gültiger Server
        # -------------------------

        ergebnis["valid_server"] = (
            ergebnis["server_properties"]
            and ergebnis["plugins"]
            and ergebnis["world"]
        )

        return ergebnis