In diesem File können alle wichtigen Hinweise zum Projekt gesammelt werden.
Es wird bei github automatisch auf der Projektseite mit angezeigt.

Starten der virtuellen Umgebung:
pipenv install

Anpassen der Konfig für die Datenbank
src/api/app.ini

Starten des Servers:
pipenv run python -m src.api.app


Für die Teamarbeit sind einige Konventionen gut:
- das Projekt immer innerhalb eine virtuellen Umgebung wie pipenv ausführen
    - alle Projektanhängigkeiten über pipenv install installieren
- in Python nutzt man Snakecase also alles klein mit Unterstrichen getrennt
- Funktions-/ Variablen-/ Routennamen sollten Aufschluss über den Nutzen haben
    - z.B. /view/ für alle Endpunkte mit einer Ansicht
    oder /data/ für Datenverarbeitung
- Datenbank Tabllen im Plural Spalten im Singular
- Kommentare nutzen um Aktionen zu erklären (EN / DE)


Um ein Projekt als Service anzumelden und so bei jedem start der VM mitstarten oder neu Änderung neustarten   
  
cd /etc/systemd/system
sudo nano project_name.service
[Unit]
Description=project_name
After=network.target
StartLimitIntervalSec=0

[Service]
Type=exec
Restart=always
RestartSec=1
User=service
ExecStart=sh /home/service/project_name/startup.sh

[Install]
WantedBy=multi-user.target


sudo systemctl enable project_name.service
sudo systemctl start project_name.service

sudo systemctl restart project_name.service

Immer an das Anlegen der Datenbank denken!
