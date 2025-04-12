import os

class FileHandler:
    def __init__(self):
        pass

    def list_files(self, path="."):
        """Listet Dateien und Ordner im angegebenen Verzeichnis auf."""
        try:
            return os.listdir(path)
        except FileNotFoundError:
            return f"Pfad nicht gefunden: {path}"
        except Exception as e:
            return f"Fehler: {str(e)}"

    def open_file(self, path):
        """Liest den Inhalt einer Datei."""
        if not os.path.exists(path):
            return f"Datei nicht gefunden: {path}"
        try:
            with open(path, 'r') as file:
                return file.read()
        except Exception as e:
            return f"Fehler beim Öffnen der Datei: {str(e)}"

    def save_file(self, path, content):
        """Speichert Inhalt in einer Datei."""
        try:
            with open(path, 'w') as file:
                file.write(content)
            return f"Datei erfolgreich gespeichert: {path}"
        except Exception as e:
            return f"Fehler beim Speichern der Datei: {str(e)}"

    def delete_file(self, path):
        """Löscht eine Datei."""
        if not os.path.exists(path):
            return f"Datei nicht gefunden: {path}"
        try:
            os.remove(path)
            return f"Datei erfolgreich gelöscht: {path}"
        except Exception as e:
            return f"Fehler beim Löschen der Datei: {str(e)}"
