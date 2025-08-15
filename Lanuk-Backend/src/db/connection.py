from sqlalchemy import create_engine, MetaData, Table, and_, update
import pandas as pd
from src.settings import get_model_settings
import logging

"""
connection.py
=====================

Persistiert generierte Berichtstexte in der PostgreSQL-Datenbank (Upsert)
und bietet eine Hilfsfunktion zum Ausführen beliebiger SQL-SELECTs zum Abrufen der Daten aus der Datenbank.


Funktionen
----------
- read_sql_query(query): Führt eine SELECT-Abfrage aus und gibt ein DataFrame zurück.
- upsert_report_data(year, time_unit, data_text): Führt ein Upsert der generierten Berichte aus.
"""



settings = get_model_settings()
logger = logging.getLogger(__name__)


DATABASE_URL = DATABASE_URL = f"postgresql+psycopg2://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"

engine = create_engine(DATABASE_URL)


def read_sql_query(query:str):
  
  """Lesen der SQL-Query für Datenbankenabfrage"""

  try:
    with engine.connect() as connection: 
      return pd.read_sql_query(query, connection)
  except Exception as e:
    logger.info("Error with Database, pls check DB connection")


def upsert_report_data(year:int, time_unit:str, data_text:dict):

    """Persistieren des aktuellen Klimaatlas Berichts in die Alt Berichtstabelle"""

    column_map = {
    "0": "temp_text",
    "1": "rain_text",
    "2": "sun_text",
    "3": "Wetterstation_text",
    "4": "Einleitung"}
    
    metadata = MetaData()
    metadata.reflect(bind=engine)

    report_table = metadata.tables["report_table"]

    values_to_save = {}
    for key, value in data_text.items():
        col = column_map.get(str(key))
        if col:
            values_to_save[col] = value

    values_to_save["Jahr"] = year
    values_to_save["Monat"] = time_unit

    try:
        with engine.begin() as conn:
            # Prüfen ob Eintrag existiert
            existing = conn.execute(
                report_table.select().where(
                    and_(report_table.c.Jahr == year, report_table.c.Monat == time_unit)
                )
            ).fetchone()

            if existing:
                # Update ausführen
                stmt = (
                    update(report_table)
                    .where(and_(report_table.c.Jahr == year, report_table.c.Monat == time_unit))
                    .values(**values_to_save)
                )
                conn.execute(stmt)
            else:
                # Insert ausführen
                conn.execute(report_table.insert().values(**values_to_save))

        logger.info("Succesfully updated Reports")
    except Exception as e:
      logger.info("Error with updating Reports in Database", e)
