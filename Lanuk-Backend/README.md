# Lanuk-Backend

Das **Lanuk-Backend** stellt über `main_api.py` die zentrale API-Schnittstelle bereit.  
Die Funktionalität ist modular im `src/`-Verzeichnis organisiert und wird über definierte API-Endpunkte abgerufen.

---

## 📁 Projektstruktur (`src/`)

| Ordner                | Beschreibung |
|-----------------------|--------------|
| `settings/`           | Zentrale Konfiguration und Umgebungsparameter |
| `db/`                 | Datenbankverbindungen und Abfragen |
| `heading/`            | Generierung von Berichtüberschriften |
| `llm_reporters/`      | LLM-Endpunkte zur automatischen Berichtserstellung |
| `pdf_generator/`      | PDF-Erzeugung aus generierten Inhalten |
| `retrieval_functions/`| Berichtspipeline-Logik|
| `templates/`          | Berichtsvorlagen |
| `time_series/`        | Aufbereitung der Zeitreihendaten |
| `utils/`              | Helfer- und Utility-Funktionen |
| `Websearch/`          | Tool zur Websuche aus der Anwendung |

---

## 🌐 API-Endpunkte

| Methode & Route                  | Beschreibung |
|----------------------------------|--------------|
| **`GET /api/retrieveReports`**   | Startet die Berichtspipeline und liefert generierte Berichtsabschnitte. |
| **`POST /api/pdfreports`**       | Erzeugt einen PDF-Report aus bereitgestellten Berichtsdaten. |
| **`POST /api/websearch`**        | Führt Websuche zu Berichtsthemen durch und liefert Zusammenfassung mit Quellen. |
| **`GET /api/tabellendaten`**     | Liefert Basis-Tabellendaten zu Temperatur, Niederschlag, Sonne & Stationen. |
| **`POST /api/heading`**          | Generiert passende Berichtüberschriften. |
| **`GET /api/timeseries`**        | Liefert Zeitreihendaten für Diagramme. |
| **`GET /api/dwdwetter`**         | Ruft Wetterbericht vom DWD (Deutscher Wetterdienst) ab. |
| **`POST /api/stationdata`**      | Liefert Messwerte ausgewählter Stationen. |
| **`POST /api/downloadfiles`**    | Speichert Berichts-Daten, erstellt PDF + SVG-Grafiken und gibt ZIP zurück. |

---

## 🔄 Betrieb & Workflows
1. **ETL-Pipeline**: Monatliche Datenübernahme von DWD/LUQS  
2. **Standard-Modus**: DB-Retrieval → Few-Shot → Self-Correction  
3. **Advanced-Modus**: Standard-Modus + automatisierte Integration (ReAct-Agent + DWD-Wetterbericht)  
4. **Tools**: Websuche, Wetterbericht, Überschriften, Stationen, Grafiken, PDF-Generierung

---

## Ablauf einer Berichtsgenerierung

```mermaid
flowchart TD
    A[Start] --> B["Jahr, Zeiteinheit"]
    B --> C["API-Aufruf (/api/retrieveReports)"]
    C --> D["DataRetriever mit Berichtstyp Schema (retrieval_functions/models.py)"]
    D --> E["Retrieval-Funktionen generieren Berichtsabschnitte (retrieval_functions/retrieval_functions.py)"]
    E --> F["Ausgabe der Berichtsabschnitte in der Oberfläche der Anwendung"]
