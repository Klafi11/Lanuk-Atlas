from pyairtable import Api
from config import Settings
import requests
from bs4 import BeautifulSoup
from headers import example_scraping
from datetime import datetime
import os
import time

"""Airtable Web-Scraper
======================

Robuster Web-Scraper mit Requests + BeautifulSoup, der Inhalte von einer
konfigurierten URL lädt, strukturiert extrahiert und in Airtable speichert.

"""

Settings = Settings()

AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")
APP_ID_AIR = os.getenv("APP_ID_AIR")
TABLE_ID_AIR = os.getenv("TABLE_ID_AIR")

api = Api(AIRTABLE_API_KEY)
table = api.table(APP_ID_AIR, TABLE_ID_AIR)


def fetch_page_content(max_retries: int = 3, backoff_seconds: float = 2.0): 


    """Lädt den HTML-Inhalt der konfigurierten Seite mit begrenzten Re‑tries.

    Args:
        max_retries: Maximale Anzahl Wiederholversuche bei Netzwerkfehlern.
        backoff_seconds: Basiswartezeit zwischen Versuchen (exponentiell).

    Returns:
        HTML-Inhalt als String.

    Raises:
        requests.RequestException: Wenn alle Versuche scheitern.
    """

    url = Settings.BASE_URL
    headers = example_scraping()

    attempt = 0
    while True:
        try:
            attempt += 1
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            return response.text
        except (requests.RequestException, TypeError) as exc:
            if attempt >= max_retries:
                raise
            sleep_for = backoff_seconds * (2 ** (attempt - 1))
            time.sleep(sleep_for)


def scrape_website(): 
    """Parst die Website und extrahiert Textblöcke.

    Args:
        html: HTML-String der Zielseite.

    Returns:
        `ScrapeResult` mit `wetterlage` und `vorhersage`.

    """

    response = fetch_page_content()
    soup = BeautifulSoup(response, "html.parser")
    data = soup.find("div", {"class": "body-text"})


    headers = [value.get_text() for value in data.find_all("h2")][:2]

    text_cap = [value.get_text() for value in data.find_all("strong")][:2] if len(data.find_all("strong")) >= 2 else ["", ""]

    text = [value.get_text() for value in data.find_all("pre")][:2]

    zip_data = zip(headers, text_cap, text)

    result = []
    for v in zip_data:
        result.append(" ".join(i for i in v))
    
    return result

def upload_to_airtable(): 
    """Erstellt einen neuen Datensatz in Airtable.

    Args:
        result: `ScrapeResult` mit zwei Textfeldern.
    """
    now = datetime.now()

    formatted_str = now.isoformat()

    result = scrape_website()
    
    table.create({"time_unit": formatted_str, "Wetterlage":result[0], "Vorhersage": result[1]})


# ----------------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------------


if __name__ == "__main__":

    upload_to_airtable()
