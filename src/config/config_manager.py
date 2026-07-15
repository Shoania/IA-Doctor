"""
IA-Doctor
Version: 0.19.0

config_manager.py
"""

import json
from pathlib import Path


class ConfigManager:

    CONFIG = Path("config.json")

    @classmethod
    def load(cls):

        if not cls.CONFIG.exists():

            return {
                "host": "",
                "port": 22,
                "username": "",
                "password": "",
                "auto_connect": False
            }

        with open(cls.CONFIG, "r", encoding="utf-8") as f:
            return json.load(f)

    @classmethod
    def save(cls, data):

        with open(cls.CONFIG, "w", encoding="utf-8") as f:
            json.dump(
                data,
                f,
                indent=4,
                ensure_ascii=False
            )