# TEXSIB - 10x Goals Project

## Übersicht

Dies ist ein Flask-basiertes Webprojekt zur Verwaltung von Zielen. Benutzer können Ziele erstellen, aktualisieren und löschen, und die Anwendung bietet auch eine Visualisierung der Ziele in Form von Charts.

## Anforderungen

- Python 3.11.7
- Pipenv

## Installation

1. **Klonen Sie das Repository:**
   ```bash
   git clone https://github.com/Duewiger/Goal-Project.git
   ```

2. **Installieren Sie die Abhängigkeiten:**
   ```bash
   pipenv install
   ```

3. **Datenbank einrichten:**
   Stellen Sie sicher, dass Ihre Datenbank konfiguriert ist und die entsprechenden Tabellen existieren. Sie können das SQL-Schema in `schema.sql` finden.

4. **Umgebung einrichten:**
   Legen Sie Ihre Umgebungsvariablen fest, falls erforderlich und initialisieren sie die Datenbank:
   ```bash
   flask --app src/api/app.py init-db
   ```
   
5. **Die Anwendung starten:**
   ```bash
   pipenv run python -m src.api.app
   ```

## Benutzung

- **Ziele verwalten:** Nach dem Einloggen können Sie Ziele erstellen, aktualisieren und löschen.
- **Charts anzeigen:** Die Anwendung zeigt die Ziele in einer übersichtlichen Darstellung an.

## Hinweise

- Verwenden Sie die Datei `startup.sh`, um die Anwendung in einer Produktionsumgebung mit Gunicorn zu starten:
   ```bash
   ./startup.sh
   ```
- Die Skripte `server.crt` und `server.key` in den `Keys`-Ordnern ermöglichen HTTPS, wenn sie in `startup.sh` aktiviert werden.

## Lizenz
Dieses Projekt ist unter der MIT-Lizenz lizenziert - siehe die [LICENSE](LICENSE) Datei für Details.

### Zusammenfassung

1. **Pipfile:** Überprüfen und gegebenenfalls spezifischere Versionen verwenden.
2. **README.md:** Die bereitgestellte Anleitung ermöglicht es Ihrem Vorgesetzten, das Projekt einfach zu installieren und auszuführen.
3. **Startup-Script:** Überprüfen Sie die Berechtigungen und stellen Sie sicher, dass es korrekt funktioniert.