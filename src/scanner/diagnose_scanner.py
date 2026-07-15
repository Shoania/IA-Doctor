"""
IA-Doctor
Version: 0.16.2

diagnose_scanner.py
"""

from collections import Counter
from pathlib import Path
import re


class DiagnoseScanner:

    def __init__(self, server_daten):
        self.daten = server_daten

    def normalisiere(self, name: str) -> str:

        name = name.lower()

        name = Path(name).stem

        # Versionsnummern entfernen
        name = re.sub(r"[-_ ]?\d+(\.\d+)*.*$", "", name)

        return name

    def scan(self):

        infos = []
        warnungen = []
        fehler = []

        plugins = self.daten.get("plugin_list", [])

        if not plugins:
            fehler.append("Keine Plugins gefunden.")

        plugin_namen = []

        for plugin in plugins:

            name = plugin.get("name")

            if not name:
                name = plugin.get("file", "")

            plugin_namen.append(
                self.normalisiere(name)
            )

        # -----------------------
        # Doppelte Plugins
        # -----------------------

        counter = Counter(plugin_namen)

        for plugin, anzahl in counter.items():

            if anzahl > 1:

                if plugin == "itemsadder":

                    fehler.append(
                        f"{anzahl} ItemsAdder-Versionen gefunden."
                    )

                else:

                    warnungen.append(
                        f"Mehrere Versionen von '{plugin}' gefunden."
                    )

        # -----------------------
        # Essentials
        # -----------------------

        if "essentials" in plugin_namen:

            infos.append("Essentials erkannt.")

            if "vault" not in plugin_namen:

                warnungen.append(
                    "Vault fehlt."
                )

        # -----------------------
        # LuckPerms
        # -----------------------

        if "luckperms" in plugin_namen:

            infos.append("LuckPerms erkannt.")

        # -----------------------
        # ItemsAdder
        # -----------------------

        if "itemsadder" in plugin_namen:

            infos.append("ItemsAdder erkannt.")

            if not self.daten.get("itemsadder", False):

                warnungen.append(
                    "ItemsAdder-Datenordner fehlt."
                )

        return {
            "infos": infos,
            "warnungen": warnungen,
            "fehler": fehler
        }