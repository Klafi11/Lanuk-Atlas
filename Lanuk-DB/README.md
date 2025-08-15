# Lanuk-DB

Das **Lanuk-DB** bildet über `main.py` die zentrale Datenaufbereitung. Die gesamte Funktionalität ist modular im `src/`-Verzeichnis strukturiert und über das `main.py` abrufbar.


## 📁 Projektstruktur (`src/`)

| Ordner                | Beschreibung |
|-----------------------|--------------|
| `config/`             | Zentrale Konfiguration und Umgebungsparameter |
| `services/`           |Ruft die API Endpunkte des DWD und des Luqualitätsnetz NRW ab|
| `text_data/`          | Hinzufügen der Klimaatlas Alt-Berichte |
| `utils/`              | Hilfsfunktionen|
| `WeatherSpider/`      | DWD Wetterberichtstool Webscrapper |

Über das main.py Skript wird die zentrale Datenaufbereitung gesteuert.