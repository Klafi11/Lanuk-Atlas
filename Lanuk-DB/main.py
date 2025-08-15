from src.services.dwd import WeatherDWDDownloader
from src.services.station import WeatherStationDownloader
from src.config.settings import StationSettings, DWDSettings, AccSettings
from sqlalchemy import create_engine
from src.utils.utils import dwd_table
from src.config.logger_config import logger
from src.text_data.text_data import json_to_pandas, json_to_pandas_station

import os

settings = AccSettings()
DATABASE_URL = f"postgresql+psycopg2://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@localhost:5431/{settings.POSTGRES_DB}"

def main():
    """
    Startet den ETL‑Prozess für Wetter‑ und Stationsdaten.

    Ablauf
    ------
    1. Datenbank‑Verbindung herstellen.
    2. DWD‑Daten laden, transformieren und persistieren.
    3. Stationsdaten laden und persistieren.
    4. Berichtstexte importieren.
    5. Fortschritt protokollieren.

    """
 
    #Verbidnung mit der Datenbank

    try:
        engine = create_engine(DATABASE_URL, echo = True)
    except:
        logger.error("Keine Connection zur Datenbank")    
    
    # Aufsetzen & Ausführung der Datapipelines
    dwd_settings = DWDSettings()
    station_settings = StationSettings()
    
    weather_DWD = WeatherDWDDownloader(dwd_settings)
    result_DWD = weather_DWD()

    weather_station = WeatherStationDownloader(station_settings)
    result_station = weather_station()

    
    # Aufsetzen der DWD Tabelle
    dwd_table_base = dwd_table(result_DWD)
    dwd_table_base.to_sql("dwd_table_base", engine, if_exists = "replace", index = False)


    # Aufsetzen DWD Tabellen für (Temperatur, Niederschlag, Sonnenscheindauer) & Ranking der Jahre
    dwd_temp_table = result_DWD["df_clear"][0]
    dwd_rain_table = result_DWD["df_clear"][1]
    dwd_sun_table = result_DWD["df_clear"][2]

    dwd_temp_table.to_sql("dwd_table_temp", engine, if_exists = "replace", index = True)
    dwd_rain_table.to_sql("dwd_table_rain", engine, if_exists = "replace", index = True)
    dwd_sun_table.to_sql("dwd_table_sun", engine, if_exists = "replace", index = True)

    logger.info("Aufsetzen der DWD Tabellen für (Temperatur, Niederschlag, Sonnenscheindauer) & Ranking der Jahre abgeschlossen")

    # Aufsetzen der Referenztabellen 
    dwd_temp_ref = result_DWD["df_ref"][0]
    dwd_rain_ref = result_DWD["df_ref"][1]
    dwd_sun_ref = result_DWD["df_ref"][2]

    dwd_temp_ref.to_sql("dwd_temp_ref", engine, if_exists = "replace", index = True)
    dwd_rain_ref.to_sql("dwd_rain_ref", engine, if_exists = "replace", index = True)
    dwd_sun_ref.to_sql("dwd_sun_ref", engine, if_exists = "replace", index = True)

    logger.info("Aufsetzen der Referenztabellen abgeschlossen")

    
    # Aufsetzen der Wetterstation Tabelle VKTU & WAST
    result_station.to_sql("v_wetterstationen", engine, if_exists= "replace", index = False)

    logger.info("Aufsetzen der Wetterstations Tabelle VKTU & WAST abgeschlossen")
    #Aufsetzen der Berichtstexte Tabelle
    reports = json_to_pandas()
    reports.to_sql("report_table", engine, if_exists = "replace", index = False)

    #stations_des = json_to_pandas_station()
    #stations_des.to_sql("station_des_table", engine, if_exists = "replace", index = False)

    logger.info("Aufsetzen der Berichtstexte abgeschlossen")


    #result = pd.merge(left= result_station, right= Weather_DWD_merge , how = "left", left_on=["year", "month"], right_on = ["Jahr", "Monat"])

    #result.drop(columns=["Jahr", "Monat"], inplace = True)

    

    #result.to_sql("table_", engine, if_exists = "replace", index = False)

    logger.info("Finished")


if __name__ == "__main__":

    main()



    
