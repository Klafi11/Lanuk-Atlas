# 🌍 Lanuk-Atlas — Automatisierte Klimaatlas-Berichte

**Ein End-to-End-Prototyp zur (teil)automatisierten Erstellung von Klimaatlas-Berichten für LANUK**  
**Mit ETL-Pipelines, RAG-ähnlichem Retrieval, LLM-gestützter Textgenerierung, Self-Correction, ReAct-Zeitreihen-Agent und React-Frontend.**  

Repository: [Klafi11/Lanuk-Atlas](https://github.com/Klafi11/Lanuk-Atlas)

---

## 🎯 Überblick & Ziel
Der **Lanuk-Atlas** beschleunigt die Erstellung von Monats-, Quartals- und Jahresberichten für den Klimaatlas.

**Kernprinzipien**
- **Mixed-Methods**: Experimentelle Analyse + iterativ-entwicklungsorientierte Prototypisierung  

**Betriebsmodi**
- **Standard**: Robuste, kerndatenbasierte Pipeline  
- **Advanced**: Plus automatisierte Integration des ReAct Zeitreihennalyse Agenten & DWD Wetterbericht 

---

## 📂 Repository-Übersicht
- [🗄️ Lanuk-DB](Lanuk-DB/README.md) – Datenbank-ETL, Scraper, Datenaufbereitung 
- [📦 Lanuk-Backend](Lanuk-Backend/README.md) – Backend-Logik, API-Endpoints, Retrieval-Funktionen, Evaluierung  
- [💻 Lanuk-Frontend](Lanuk-Frontend/README.md) – Weboberfläche, Assistenzsystem, Visualisierung

---

## 🏗️ Architektur
**3-Schicht-Architektur**

1. **Datenschicht — Lanuk-DB**  
   - Containerisierte PostgreSQL  
   - ETL-Jobs

2. **Verarbeitungsschicht — Lanuk-Backend (Flask)**  
   - API-Endpoints zur Berichtserstellung
   - RAG-ähnliches Retrieval → ICL-Prompting (Few-Shot)  
   - Self-Correction 
   - ReAct-Zeitreihen-Agent 
   - Tools: Websuche, DWD-Wetterberichte, Überschriftengenerator, Stationsabfrage, Grafik-Download  

3. **Präsentationsschicht — Lanuk-Frontend (React/TypeScript)**  
   - Navigationsbar: Steuerung  
   - Variationsdisplay: Modell-Vergleich & Abschnitts-Editor  
   - Informationsdisplay: Daten-Tab, PDF-Vorschau-Tab, Info-Tab  

---

## 📁 Vereinfachte Verzeichnisstruktur
```
Lanuk-Atlas/
├─ README.md
├─ .env                                 # Konfigurationsdatei
├─ docker-compose.yml                   # Multi-Container Setup
├─ deploy.sh                            # Deploy Skript
├─ fill-database.sh                     # Befüllung der Datenbank (initial)

├─ Lanuk-DB/                            # ETL-Pipeline (DWD/LUQS → PostgreSQL)
│  ├─ README.md
│  ├─ main.py                           # Startpunkt des ETL-Prozesses
│  └─ src/
│     ├─ WeatherSpider/                 # DWD-Wetterbericht-Scraper
│     └─ services/
│        ├─ dwd.py                      # DWD ETL-Job
│        └─ station.py                  # LUQS-Wetterstationen ETL-Job

├─ Lanuk-Backend/                       # Flask-Backend (API + Berichtserstellung)
│  ├─ README.md
│  ├─ main_api.py                       # Einstiegspunkt des Backends (Orchestrierung der Endpunkte)
│  └─ src/
│     ├─ db/                            # Datenbankabfragen (PostgreSQL)
│     ├─ download/                      # Generierung von Download-Grafiken
│     ├─ pdf_generator/                 # PDF-Erstellung (UI)
│     ├─ llm_reporters/                  # LLM-Module zur Berichtserstellung
│     ├─ templates/                      # Prompt-Templates für LLM-Generierung
│     │  ├─ templates_first_it.py        # P1: Zero/Few/CoT-Templates
│     │  ├─ templates_std.py             # P2/P3: Few-Shot Standard
│     │  ├─ templates_adv.py             # P2/P3: Few-Shot Advanced
│     │  ├─ template_struktur.py         # P3: Struktur der Berichte
│     │  ├─ template_agents_adv.py       # P2/P3: ReAct Zeitreihen-Agent
│     │  ├─ template_val_tasks.py        # P2/P3: Self-Correction
│     ├─ retrieval_functions/            # Datenabruf + Berichtspipelines
│     │  ├─ base_retrieval_functions_adv.py # Advanced DB-Retrieval + ReAct-Agent Aufgabenbeschreibung
│     │  ├─ base_retrieval_functions.py     # Standard DB-Retrieval
│     │  ├─ models.py                       # Interfaces / Datamodelle
│     │  ├─ retrieval_functions.py          # Haupt-Berichtspipelines
│     │  └─ valuation.py                    # Self-Correction-Pipeline
│     ├─ Websearch/                      # Websuche-Tool
│     ├─ heading/                        # Überschriftengenerator
│     └─ evaluation/                     # Evaluationsdaten & -berichte
│        ├─ Evaluation_G_Eval/           # P1: G-Eval
│        └─ Reports_eval/                 # Projektphasen-Evaluierungen
│           ├─ reports_first_it           # P1: Erste Projektphase
│           ├─ reports_second_it          # P2: Zweite Projektphase
│           └─ reports_third_it           # P3: Dritte Projektphase

├─ Lanuk-Frontend/                       # React/TypeScript-Frontend
│  ├─ App.tsx                             # Hauptkomponente (Orchestrierung)
│  ├─ Navigationsbar.tsx                  # Navigationsleiste
│  ├─ Variationdisplay.tsx                # Ansicht: Variationsanzeige
│  └─ Informationdisplay.tsx              # Ansicht: Informationsanzeige

```

---

## 🔄 Projektphasen
**Phase 1 — Initialer Prototyp**
- ETL & DB: Monats-Cronjob füllt PostgreSQL mit DWD/LUQS-Daten  
- Modellauswahl: LLM-Kriterien; Start mit GPT-4o  
- Pipeline: Lanuk-DB / Lanuk-Backend 
- Produktionsreife 3.7


**Phase 2 — End-to-End-System & Optimierung**
- Backend: Flask-API, Self-Correction, ReAct-Zeitreihen-Agent  
- Frontend: React/TS mit Standard/Advanced-Toggle  
- Tools: Websuche, DWD-Wetterberichte, Überschriftengenerator, Stationsabfrage
- Modellauswahl: OpenAI-Gpt 4.1(nano, mini, 4.1), Anthropic-Sonnet(3.7, 4.0), DeepSeekV3 
- Produktionsreife 4.6

**Phase 3 — Feinschliff & Finalisierung**
- Prompt-Struktur überarbeitet  
- Filtermenü im Daten-Tab  
- Produktionsreife  5.0  

---

## Relevante Skripte ausgewählter Kapitel der Masterarbeit

Dieser Abschnitt listet die relevanten Code-Dateien und Ordner auf, die in den jeweiligen Kapiteln der Masterarbeit erwähnt werden.


## 📍 Kapitel 5 – Projektphase 1

### 5.2 Datenaufbereitung
- [DWD-ETL-Skript](Lanuk-DB/src/services/dwd.py)  
- [LUQS-Messstationen-ETL-Skript](Lanuk-DB/src/services/station.py)  
- [Orchestrierung](Lanuk-DB/main.py)  
- [RAG-ähnlicher Daten-Retriever](Lanuk-Backend/src/retrieval_functions/models.py#L34)  

### 5.5 Angewendete ICL-Methoden
- [ICL-Templates – Phase 1](Lanuk-Backend/src/templates/templates_first_it.py)  

---

## 📍 Kapitel 6 – Experimente (Phase 1)
- [Evaluierung G-Eval](Lanuk-Backend/src/evaluation/Evaluation_G_Eval/)  
- [Evaluierung Mensch](Lanuk-Backend/src/evaluation/Reports_eval/reports_first_it/)  

---

## 📍 Kapitel 7 – Projektphase 2

### 7.3.1 Optimierung – Präsentationsschicht (Assistenzsystem)
- [Navigationsbar](Lanuk-Frontend/src/Navigationsbar.tsx)  
- [Variationdisplay](Lanuk-Frontend/src/Variationsdisplay.tsx)  
- [Informationsdisplay](Lanuk-Frontend/src/Informationdisplay.tsx)  
- [Orchestrierung](Lanuk-Frontend/src/App.tsx)  

### 7.3.2 Optimierung – Information-Tools

#### 🌐 Websuche
- [API-Endpoint](Lanuk-Backend/main_api.py#L190)  
- [Websuche-Skripte](Lanuk-Backend/src/Websearch/)  
- [Websuche-Prompts](Lanuk-Backend/src/Websearch/templates_s.py)  

#### ☁ DWD-Wetterbericht
- [API-Endpoint](Lanuk-Backend/main_api.py#L345)  
- [Scraper](Lanuk-DB/src/WeatherSpider/)  
- [Prompt](Lanuk-Backend/src/templates/templates_adv.py#L340)  
- [Orchestrierung](Lanuk-Backend/src/retrieval_functions/base_retrieval_functions_ad.py#L223)  

### 7.3.3 Optimierung - zwei Modi
- [Zwei-Modi](Lanuk-Backend/src/retrieval_functions/retrieval_functions.py)

### 7.3.4 Optimierung – Zeitreihenanalyse-Agent
- [Agent](Lanuk-Backend/src/retrieval_functions/base_retrieval_functions_ad.py#L38)  
- [Agent-Aufgaben](Lanuk-Backend/src/retrieval_functions/base_retrieval_functions_ad.py#L84)  
- [Agent-Instruktionen](Lanuk-Backend/src/templates/template_agents_adv.py)  

### 7.3.5 Optimierung – Self-Correction
- [Self-Correction-Logik](Lanuk-Backend/src/retrieval_functions/valuation.py)
- [Self-Correction-Aufgaben](Lanuk-Backend/src/templates/template_val_tasks.py)  
- [Prompt Standard](Lanuk-Backend/src/templates/template_val_std.py)  
- [Prompt Advanced](Lanuk-Backend/src/templates/template_val_adv.py)  

### 7.3.6 Optimierung – Few-Shot-Prompting
- [Few-Shot Standard](Lanuk-Backend/src/templates/templates_std.py)  
- [Few-Shot Advanced](Lanuk-Backend/src/templates/templates_adv.py)  

---

## 📍 Kapitel 7.4 – Sonstige Prototyp-Erweiterungen

### 📰 Überschriftengenerator
- [Überschriftengenerator](Lanuk-Backend/src/heading/)
- [API-Endpoint](Lanuk-Backend/main_api.py#L273)  

### 📡 Stationsabfrage
- [Stations-Grid](Lanuk-Frontend/src/ButtonGrid.tsx)  
- [API-Endpoint](Lanuk-Backend/main_api.py#L378)  

### 📊 Grafik- & Berichtsdownload
- [Grafiken](Lanuk-Backend/src/download/)  
- [Download-Endpoint](Lanuk-Backend/main_api.py#L418)  

---

## 📍 Kapitel 7.5 – Systemintegration
- [Docker Compose](docker-compose.yml)  

---

## 📍 Kapitel 8 – Experimente (Phase 2)
- [Evaluierung](Lanuk-Backend/src/evaluation/Reports_eval/reports_second_it/)  

---

## 📍 Kapitel 9 – Projektphase 3

### 9.2 Optimierung – Prompt-Struktur
- [Prompt-Struktur](Lanuk-Backend/src/templates/template_struktur.py)  

### 9.3.1 Optimierung – Filtermenü
- [Filtermenü](Lanuk-Frontend/src/Informationdisplay.tsx#L65)  
- [Zeitreihendaten-Endpoint](Lanuk-Backend/main_api.py#L310)  

---

## 📍 Kapitel 10 – Experimente (Phase 3)
- [Evaluierung](Lanuk-Backend/src/evaluation/Reports_eval/reports_third_it/)  


--- 
## 🌍 Lanuk-Atlas – .env Konfiguration
## Dieser Abschnitt enthält alle benötigten Umgebungsvariablen
## für den Betrieb von Datenbank, Backend, Frontend und APIs.

**Parameterübersicht:**

- **PostgreSQL-Datenbank**
  - `POSTGRES_USER` — Benutzername für die Wetterdatenbank  
  - `POSTGRES_PASSWORD` — Passwort für die Wetterdatenbank  
  - `POSTGRES_DB` — Name der Datenbank  
  - `POSTGRES_HOST` — Hostname oder Service-Name des DB-Containers  
  - `POSTGRES_PORT` — Interner Datenbank-Port  
  - `POSTGRES_PORT_OUT` — Externer Port für lokale Verbindungen  
  - `FILL_DATABASE` — Option zur initialen Befüllung (1 = Ja, 0 = Nein)  
  - `TEXT_DATA_PATH` — Pfad zu den Textabschnitt-Daten (JSON)  
  - `TEXT_DATA_PATH_STATION` — Pfad zu den Stationsdaten (JSON)  

- **API-Integrationen**
  - `OPENROUTER_BASE_URL` — Basis-URL des OpenRouter-LLM-Dienstes  
  - `OPENROUTER_API_KEY` — API-Key für OpenRouter  
  - `TVLY_API_KEY` — API-Key für Tavily Websuche  
  - `AIRTABLE_API_KEY` — API-Key für Airtable  
  - `APP_ID_AIR` — Airtable App-ID  
  - `TABLE_ID_AIR` — Airtable Tabellen-ID  

- **Server- und Proxy-Einstellungen**
  - `SERVER_NAME` — Servername oder Domain für Nginx  
  - `PROXY_PORT` — Port des Reverse-Proxy  
  - `PROXY_TIMEOUT` — Timeout-Einstellung des Proxys  
  - `BACKEND_HOST` — Hostname des Backends  
  - `BACKEND_PORT` — Port des Backend-Servers  
  - `FRONTEND_PORT` — Port des Frontend-Servers  

---
## 🚀 Initiales Setup des Prototyps

Zur Erstinstallation und Einrichtung des Prototyps stehen zwei Shell-Skripte bereit:

- **`deploy.sh`** – Führt die notwendigen Schritte zum Aufbau der Umgebung aus (z. B. Container starten, Abhängigkeiten installieren, Konfigurationen setzen).
- **`fill-database.sh`** – Füllt die Datenbank mit initialen Daten aus dem Lanuk-DB/main.py Skript.

### Verwendung
```bash
# Schritt 1: Deploy-Skript ausführen
./deploy.sh

# Schritt 2: Datenbank mit Beispieldaten befüllen
./fill-database.sh
