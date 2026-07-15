"""
IA-Doctor
Version: 0.18.0

analyse_worker.py

Führt die Serveranalyse in einem Hintergrund-Thread aus.
"""

from PySide6.QtCore import QObject, Signal, Slot

from src.engine.doctor_engine import DoctorEngine


class AnalyseWorker(QObject):

    finished = Signal(dict)
    error = Signal(str)

    @Slot(str)
    def analyse(self, server_path: str):

        try:

            engine = DoctorEngine()

            daten = engine.analyse_server(server_path)

            self.finished.emit(daten)

        except Exception as e:

            self.error.emit(str(e))