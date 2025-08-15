from pydantic_settings import BaseSettings 
from typing import List, Dict, Type
import datetime as dt
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

class AccSettings(BaseSettings):

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    TEXT_DATA_PATH: str
    TEXT_DATA_PATH_STATION:str
    

    class Config: 
        env_file = BASE_DIR / ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"






class StationSettings(BaseSettings):
    
    """
    Initialisiert das Modul mit der API-BASE_URL des DWD-Wetterdienst.
    Über die angegebenen Links werden die Monatsdaten über den Witterungsverlauf 
    von Nordrhein-Westfalen für die Berichte heruntergeladen. Die Daten umfassen 
    Temperatur, Niederschlag und Sonnenscheindauer.
    """

    temp_key: str = "113"
    mst_key_W: str = "1914"
    mst_key_V: str = "1955"
    today: str =  dt.datetime.today().strftime("%m")
    url: str = "https://luftqualitaet.nrw.de/api/stundenmittelwerte.php"
    
    params: List[Dict[str, str]] = [
        #VKTU
        {
            "station": "1914",
            "komponente": "113",
            "beginn": "2020-01-01T00:00",
            "ende": f"2025-{today}-02T00:00",
            "messwerteliste": "name",
            "index": "obj",
        },
        # WAST
        {
            "station": "1955",
            "komponente": "113",
            "beginn": "2020-01-01T00:00",
            "ende": f"2025-{today}-02T00:00",
            "messwerteliste": "name",
            "index": "obj",
        },
        # SOLI
        {
            "station": "444",
            "komponente": "113",
            "beginn": "2020-01-01T00:00",
            "ende": f"2025-{today}-02T00:00",
            "messwerteliste": "name",
            "index": "obj",
        },
        #EIFE
        {
            "station": "122",
            "komponente": "113",
            "beginn": "2020-01-01T00:00",
            "ende": f"2025-{today}-02T00:00",
            "messwerteliste": "name",
            "index": "obj",
        },

        {
            "station": "1939",
            "komponente": "113",
            "beginn": "2020-01-01T00:00",
            "ende": f"2025-{today}-02T00:00",
            "messwerteliste": "name",
            "index": "obj",
        },

        {
            "station": "413",
            "komponente": "113",
            "beginn": "2020-01-01T00:00",
            "ende": f"2025-{today}-02T00:00",
            "messwerteliste": "name",
            "index": "obj",
        },

        {
            "station": "493",
            "komponente": "113",
            "beginn": "2020-01-01T00:00",
            "ende": f"2025-{today}-02T00:00",
            "messwerteliste": "name",
            "index": "obj",
        },

        {
            "station": "329",
            "komponente": "113",
            "beginn": "2020-01-01T00:00",
            "ende": f"2025-{today}-02T00:00",
            "messwerteliste": "name",
            "index": "obj",
        },

        {
            "station": "416",
            "komponente": "113",
            "beginn": "2020-01-01T00:00",
            "ende": f"2025-{today}-02T00:00",
            "messwerteliste": "name",
            "index": "obj",
        },
        {
            "station": "63",
            "komponente": "113",
            "beginn": "2020-01-01T00:00",
            "ende": f"2025-{today}-02T00:00",
            "messwerteliste": "name",
            "index": "obj",
        },
        {
            "station": "360",
            "komponente": "113",
            "beginn": "2020-01-01T00:00",
            "ende": f"2025-{today}-02T00:00",
            "messwerteliste": "name",
            "index": "obj",
        },
        #{
        #    "station": "54",
        #    "komponente": "113",
        #    "beginn": "2020-01-01T00:00",
        #    "ende": f"2025-{today}-02T00:00",
       #     "messwerteliste": "name",
        #    "index": "obj",
        #}
       
        ]
    
    dtype: Dict[str, Type] = {
        "Jahr": int,
        "Monat": int,
        "VKTU_frost": int,
        "VKTU_eis": int,
        "VKTU_sommertage": int,
        "VKTU_heißetage": int,
        "VKTU_höchsttemperatur": float,
        "VKTU_tiefsttemperatur": float,
        "VKTU_tropennächte": int,
        "WAST_frost": int, 
        "WAST_eis": int,
        "WAST_sommertage": int, 
        "WAST_heißetage": int, 
        "WAST_höchsttemperatur": float, 
        "WAST_tiefsttemperatur": float,
        "WAST_tropennächte": int,
        "SOLI_frost": int,
        "SOLI_eis": int,
        "SOLI_sommertage": int,
        "SOLI_heißetage": int,
        "SOLI_höchsttemperatur": float,
        "SOLI_tiefsttemperatur": float,
        "SOLI_tropennächte": int,
        "EIFE_frost": int,
        "EIFE_eis": int,
        "EIFE_sommertage": int,
        "EIFE_heißetage": int,
        "EIFE_höchsttemperatur": float,
        "EIFE_tiefsttemperatur": float,
        "EIFE_tropennächte": int,
        "VACW_frost": int,
        "VACW_eis": int,
        "VACW_sommertage": int,
        "VACW_heißetage": int,
        "VACW_höchsttemperatur": float,
        "VACW_tiefsttemperatur": float,
        "VACW_tropennächte": int,
        "RODE_frost": int,
        "RODE_eis": int,
        "RODE_sommertage": int,
        "RODE_heißetage": int,
        "RODE_höchsttemperatur": float,
        "RODE_tiefsttemperatur": float,
        "RODE_tropennächte": int,
        "WALS_frost": int,
        "WALS_eis": int,
        "WALS_sommertage": int,
        "WALS_heißetage": int,
        "WALS_höchsttemperatur": float,
        "WALS_tiefsttemperatur": float,
        "WALS_tropennächte": int,
        "MGRH_frost": int,
        "MGRH_eis": int,
        "MGRH_sommertage": int,
        "MGRH_heißetage": int,
        "MGRH_höchsttemperatur": float,
        "MGRH_tiefsttemperatur": float,
        "MGRH_tropennächte": int,
        "ROTH_frost": int,
        "ROTH_eis": int,
        "ROTH_sommertage": int,
        "ROTH_heißetage": int,
        "ROTH_höchsttemperatur": float,
        "ROTH_tiefsttemperatur": float,
        "ROTH_tropennächte": int,
        "BOTT_frost": int,
        "BOTT_eis": int,
        "BOTT_sommertage": int,
        "BOTT_heißetage": int,
        "BOTT_höchsttemperatur": float,
        "BOTT_tiefsttemperatur": float,
        "BOTT_tropennächte": int,
        "NIED_frost": int,
        "NIED_eis": int,
        "NIED_sommertage": int,
        "NIED_heißetage": int,
        "NIED_höchsttemperatur": float,
        "NIED_tiefsttemperatur": float,
        "NIED_tropennächte": int,
        #"BORG_frost": int,
        #"BORG_eis": int,
       # "BORG_sommertage": int,
        #"BORG_heißetage": int,
        #"BORG_höchsttemperatur": float,
        #"BORG_tiefsttemperatur": float,
        #"BORG_tropennächte": int,
    }

    month_names: Dict[int, str] = {
            1: 'Januar',
            2: 'Februar',
            3: 'März',
            4: 'April',
            5: 'Mai',
            6: 'Juni',
            7: 'Juli',
            8: 'August',
            9: 'September',
            10: 'Oktober',
            11: 'November',
            12: 'Dezember'
    }

    season_mapping: Dict[str, str] = {
        "Januar": "Winter",
        "Februar": "Winter",
        "März": "Frühling", 
        "April": "Frühling", 
        "Mai": "Frühling", 
        "Juni": "Sommer", 
        "Juli": "Sommer", 
        "August": "Sommer", 
        "September": "Herbst",
        "Oktober": "Herbst", 
        "November": "Herbst", 
        "Dezember": "Winter", 

    }

class DWDSettings(BaseSettings):
    """
    Initialisiert das Modul mit der API-BASE_URL des DWD-Wetterdienst.
    Über die angegebenen Links werden die Monatsdaten über den Witterungsverlauf 
    von Nordrhein-Westfalen für die Berichte heruntergeladen. Die Daten umfassen 
    Temperatur, Niederschlag und Sonnenscheindauer.
    """
    
    url: str = "https://opendata.dwd.de/climate_environment/CDC/regional_averages_DE/monthly/"
    
    links: List[str] = [
        "air_temperature_mean/regional_averages_tm_", 
        "precipitation/regional_averages_rr_", 
        "sunshine_duration/regional_averages_sd_"
    ]
    
    dtype_clear_temp: Dict[str, Type] = {
        "Januar": float, 
        "Februar": float, 
        "März": float, 
        "April": float, 
        "Mai": float, 
        "Juni": float, 
        "Juli": float, 
        "August": float,
        "September": float,
        "Oktober": float,
        "November": float,
        "Dezember": float
    }
    
    dtype_clear_rain_sun: Dict[str, str] = {

        "Januar": "Int64", 
        "Februar": "Int64", 
        "März": "Int64", 
        "April": "Int64", 
        "Mai": "Int64", 
        "Juni": "Int64", 
        "Juli": "Int64", 
        "August": "Int64",
        "September": "Int64",
        "Oktober": "Int64",
        "November": "Int64",
        "Dezember": "Int64"
    }       
    
    dtype_raw_temp: Dict[str, Type] = {
        "Monat": int,
        "Jahr": int, 
        "temperatur_Nrw": float
    }
    
    dtype_raw_rain: Dict[str, Type] = {
        "Monat": int, 
        "Jahr": int, 
        "niederschlag_Nrw": int
    }
    
    dtype_raw_sun: Dict[str, Type] = {
        "Monat": int, 
        "Jahr": int, 
        "sonnenscheindauer_Nrw": int
    }   

    dtype_ref_temp: Dict[str, Type] = {
        "Januar_temp_avg": float,
        "Februar_temp_avg": float, 
        "März_temp_avg": float, 
        "April_temp_avg": float, 
        "Mai_temp_avg": float,
        "Juni_temp_avg": float, 
        "Juli_temp_avg": float, 
        "August_temp_avg": float, 
        "September_temp_avg": float, 
        "Oktober_temp_avg": float, 
        "November_temp_avg": float,
        "Dezember_temp_avg": float,
        "Winter_temp_avg": float, 
        "Frühling_temp_avg": float,
        "Sommer_temp_avg": float,
        "Winter_temp_avg": float, 
        "Herbst_temp_avg": float, 
        "Jahr_agg_temp_avg": float

    }

    dtype_ref_rain: Dict[str, Type] = {
        "Januar_rain_avg": int,
        "Februar_rain_avg": int, 
        "März_rain_avg": int, 
        "April_rain_avg": int, 
        "Mai_rain_avg": int,
        "Juni_rain_avg": int, 
        "Juli_rain_avg": int, 
        "August_rain_avg": int, 
        "September_rain_avg": int, 
        "Oktober_rain_avg": int, 
        "November_rain_avg": int,
        "Dezember_rain_avg": int,
        "Winter_rain_avg": int, 
        "Frühling_rain_avg": int,
        "Sommer_rain_avg": int,
        "Winter_rain_avg": int, 
        "Herbst_rain_avg": int,
        "Jahr_agg_rain_avg": int
    }

    dtype_ref_sun: Dict[str, Type] = {
        "Januar_sun_avg": int,
        "Februar_sun_avg": int, 
        "März_sun_avg": int, 
        "April_sun_avg": int, 
        "Mai_sun_avg": int,
        "Juni_sun_avg": int, 
        "Juli_sun_avg": int, 
        "August_sun_avg": int, 
        "September_sun_avg": int, 
        "Oktober_sun_avg": int, 
        "November_sun_avg": int,
        "Dezember_sun_avg": int,
        "Winter_sun_avg": int, 
        "Frühling_sun_avg": int,
        "Sommer_sun_avg": int,
        "Winter_sun_avg": int, 
        "Herbst_sun_avg": int,
        "Jahr_agg_sun_avg": int
    }