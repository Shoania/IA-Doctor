"""
IA-Doctor
Version: 0.18.0

RemoteServerScanner
(Schnellmodus)
"""

from src.connection.connection_manager import ConnectionManager


class RemoteServerScanner:

    def scan(self):

        client = ConnectionManager.get_client()

        if client is None:

            return {
                "server_exists": False,
                "server_properties": False,
                "plugins": False,
                "world": False,
                "logs": False,
                "itemsadder": False,
                "plugin_count": 0,
                "plugin_list": []
            }

        root = client.list_directory(".")

        daten = {
            "server_exists": True,
            "server_properties": "server.properties" in root,
            "plugins": "plugins" in root,
            "world": "world" in root,
            "logs": "logs" in root,
            "itemsadder": False,
            "plugin_count": 0,
            "plugin_list": []
        }

        if not daten["plugins"]:
            return daten

        plugin_liste = []

        try:

            dateien = sorted(
                client.list_directory("plugins")
            )

            for datei in dateien:

                if not datei.lower().endswith(".jar"):
                    continue

                name = datei[:-4]

                if name.lower() == "itemsadder":
                    daten["itemsadder"] = True

                plugin_liste.append({
                    "file": datei,
                    "name": name,
                    "version": "-",
                    "author": "-"
                })

        except Exception:
            pass

        daten["plugin_count"] = len(plugin_liste)
        daten["plugin_list"] = plugin_liste

        return daten