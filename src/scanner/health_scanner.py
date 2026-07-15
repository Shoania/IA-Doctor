"""
IA-Doctor
Version: 0.21.0

health_scanner.py
"""


class HealthScanner:

    def __init__(self, daten: dict):
        self.daten = daten

    def scan(self):

        score = 0
        gruende = []

        # -------------------------
        # Server
        # -------------------------

        if self.daten.get("server_exists", False):
            score += 20
            gruende.append("✅ Server gefunden")
        else:
            gruende.append("❌ Server nicht gefunden")

        if self.daten.get("server_properties", False):
            score += 10
            gruende.append("✅ server.properties vorhanden")
        else:
            gruende.append("❌ server.properties fehlt")

        if self.daten.get("plugins", False):
            score += 10
            gruende.append("✅ Plugins-Ordner vorhanden")
        else:
            gruende.append("❌ Plugins-Ordner fehlt")

        if self.daten.get("world", False):
            score += 10
            gruende.append("✅ Welt gefunden")
        else:
            gruende.append("⚠ Keine Welt gefunden")

        if self.daten.get("logs", False):
            score += 10
            gruende.append("✅ Logs vorhanden")
        else:
            gruende.append("⚠ Logs fehlen")

        # -------------------------
        # Diagnose
        # -------------------------

        warnungen = len(
            self.daten.get("warnungen", [])
        )

        fehler = len(
            self.daten.get("fehler", [])
        )

        if fehler == 0:
            score += 20
            gruende.append("✅ Keine Fehler erkannt")
        else:
            gruende.append(f"❌ {fehler} Fehler erkannt")

        if warnungen == 0:
            score += 10
            gruende.append("✅ Keine Warnungen")
        else:
            gruende.append(f"⚠ {warnungen} Warnungen gefunden")

        # -------------------------
        # Bonus
        # -------------------------

        if self.daten.get("itemsadder", False):
            score += 10
            gruende.append("✅ ItemsAdder erkannt")

        score = min(score, 100)

        # -------------------------
        # Bewertung
        # -------------------------

        if score >= 90:
            status = "★★★★★ Exzellent"

        elif score >= 75:
            status = "★★★★☆ Sehr gut"

        elif score >= 60:
            status = "★★★☆☆ Gut"

        elif score >= 40:
            status = "★★☆☆☆ Kritisch"

        else:
            status = "★☆☆☆☆ Schlecht"

        return {
            "health_score": score,
            "health_status": status,
            "health_reasons": gruende
        }