import pandas as pd
from src.config.logger_config import logger
from src.config.settings import AccSettings

settings = AccSettings()

""" Aufsetzen der Altberichte """

def json_to_pandas():

    logger.info("Aufsetzen der der Tabelle für Report text Daten")
    
    return pd.read_json(settings.TEXT_DATA_PATH)

def json_to_pandas_station():
    
    logger.info("Aufsetzen der Station Tabelle")

    return pd.read_json(settings.TEXT_DATA_PATH_STATION)