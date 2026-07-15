from src.connection.sftp_client import SFTPClient

HOST = "omar.n.u0.eu"
PORT = 2022
USER = "lhz8q5rlo20uw9iq.e302c7b8"
PASSWORD = input("Passwort: ")

client = SFTPClient(
    HOST,
    PORT,
    USER,
    PASSWORD
)

if client.connect():

    print("\nVerbindung erfolgreich!\n")

    plugins = client.list_directory("plugins")

    print(f"Plugins gefunden: {len(plugins)}\n")

    for plugin in sorted(plugins):
        print(plugin)

    client.disconnect()

else:

    print("Verbindung fehlgeschlagen.")