"""
IA-Doctor
Version: 0.18.1

plugin_scanner.py

Liest Plugininformationen direkt aus plugin.yml.
"""

from pathlib import Path
import zipfile


class PluginScanner:

    def __init__(self, server_path: str):
        self.server = Path(server_path)

    def scan(self):

        plugins_ordner = self.server / "plugins"

        plugin_liste = []

        if not plugins_ordner.exists():

            return {
                "plugin_count": 0,
                "plugin_list": []
            }

        for datei in plugins_ordner.iterdir():

            if not datei.is_file():
                continue

            if datei.suffix.lower() != ".jar":
                continue

            plugin = {
                "file": datei.name,
                "path": str(datei),
                "name": "",
                "version": "",
                "author": "",
                "website": "",
                "description": ""
            }

            try:

                with zipfile.ZipFile(datei) as jar:

                    try:

                        with jar.open("plugin.yml") as f:

                            text = f.read().decode(
                                "utf-8",
                                errors="ignore"
                            )

                    except KeyError:
                        text = ""

                    for zeile in text.splitlines():

                        zeile = zeile.strip()

                        if zeile.startswith("name:"):
                            plugin["name"] = zeile.split(":", 1)[1].strip()

                        elif zeile.startswith("version:"):
                            plugin["version"] = zeile.split(":", 1)[1].strip()

                        elif zeile.startswith("author:"):
                            plugin["author"] = zeile.split(":", 1)[1].strip()

                        elif zeile.startswith("authors:"):

                            wert = zeile.split(":", 1)[1].strip()

                            wert = wert.replace("[", "")
                            wert = wert.replace("]", "")

                            plugin["author"] = wert

                        elif zeile.startswith("website:"):
                            plugin["website"] = zeile.split(":", 1)[1].strip()

                        elif zeile.startswith("description:"):
                            plugin["description"] = zeile.split(":", 1)[1].strip()

            except Exception:
                pass

            plugin_liste.append(plugin)

        plugin_liste.sort(
            key=lambda p: p["name"].lower() if p["name"] else p["file"].lower()
        )

        return {
            "plugin_count": len(plugin_liste),
            "plugin_list": plugin_liste
        }