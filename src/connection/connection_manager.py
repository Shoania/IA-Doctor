"""
IA-Doctor
Version: 0.15.1

Speichert die aktuelle Serververbindung.
"""


class ConnectionManager:

    client = None
    connected = False

    @classmethod
    def set_client(cls, client):
        cls.client = client
        cls.connected = True

    @classmethod
    def disconnect(cls):

        if cls.client:
            cls.client.disconnect()

        cls.client = None
        cls.connected = False

    @classmethod
    def is_connected(cls):
        return cls.connected

    @classmethod
    def get_client(cls):
        return cls.client