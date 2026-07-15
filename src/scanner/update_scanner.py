"""
IA-Doctor
Version: 0.18.0

update_scanner.py
"""

class UpdateScanner:

    def __init__(self, plugin_list):

        self.plugins = plugin_list

    def scan(self):

        updates = []

        for plugin in self.plugins:

            updates.append({
                "name": plugin["name"],
                "installed": plugin["version"],
                "latest": "Unbekannt",
                "status": "Nicht geprüft"
            })

        return {
            "updates": updates
        }