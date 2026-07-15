"""
IA-Doctor
Version: 0.16.2

SFTP-Verbindung zu ByteBlitz
"""

import paramiko


class SFTPClient:

    def __init__(self, host, port, username, password):

        self.host = host
        self.port = port
        self.username = username
        self.password = password

        self.client = None
        self.sftp = None

    def connect(self):

        try:

            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(
                paramiko.AutoAddPolicy()
            )

            self.client.connect(
                hostname=self.host,
                port=self.port,
                username=self.username,
                password=self.password,
                timeout=10
            )

            self.sftp = self.client.open_sftp()

            return True

        except Exception as e:

            print(e)
            return False

    def disconnect(self):

        if self.sftp:
            self.sftp.close()

        if self.client:
            self.client.close()

    def list_directory(self, path):

        try:
            return self.sftp.listdir(path)

        except Exception:
            return []

    def read_file(self, path):

        try:

            with self.sftp.open(path, "rb") as f:
                return f.read()

        except Exception:
            return None