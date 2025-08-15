"""weather_station_downloader.py

Lädt temperatur‑bezogene Kennzahlen (Frosttage, Tropennächte, Höchst-/Tiefst‑
temperatur u. a.) von LUQOS‑Wetterstationen, bereitet sie auf und liefert einen
zusammengeführten DataFrame, der anschließend in der ETL‑Pipeline
persistiert wird.

Nomenklatur
===========
* **Frosttag**   – Tmin < 0 °C
* **Eistag**     – Tmax ≤ 0 °C
* **Sommertag**  – Tmax ≥ 25 °C
* **Heißer Tag** – Tmax ≥ 30 °C
* **Tropennacht**– Tmin ≥ 20 °C (19 h–07 h)

Beispiel
--------
>>> settings = StationSettings()
>>> weather_DWD() = WeatherStationDownloader(settings)
>>> df = weather_DWD()                     # Aufruf via __call__
>>> df.head()

Der resultierende DataFrame besitzt Spalten:
```
['Jahr', 'Zeiteinheit',
 'VKTU_frost', 'WAST_frost', 'VKTU_eis', 'WAST_eis', (...)
```
"""

import requests
import pandas as pd
from src.config.logger_config import logger
from src.utils.utils import custom_round
from functools import reduce



class WeatherStationDownloader:
    """Lädt und bereitet Kennzahlen mehrerer Wetterstationen auf.

    Parameters
    ----------
    settings : StationSettings
        Konfigurationsobjekt, das API-Keys, URL, dtypes u. Ä. enthält.
    """


    def __init__(self, settings):

        logger.info("Initializing WeatherDWDDownloader")

        self.setting = settings

        self.temp_key = self.setting.temp_key
        self.mst_key_W = self.setting.mst_key_W
        self.mst_key_V = self.setting.mst_key_V
        self.params = self.setting.params
        self.dtype = self.setting.dtype 
        self.url = self.setting.url
        self.month_names = self.setting.month_names
        self.season_mapping = self.setting.season_mapping

    def __call__(self):

        """Lädt alle konfigurierten Parameter und gibt einen DataFrame zurück.

        Ablauf
        ------
        1. API‑Aufrufe pro *param* sammeln.
        2. Ein DataFrame pro Kennzahl erzeugen.
        3. DataFrames inner joinen auf (Jahr, Monat).
        4. Datentypen anpassen, Monatsnamen & Saison ergänzen.

        Returns
        -------
        pandas.DataFrame
            Zusammengeführter Datensatz über alle Kennzahlen.
        """
        
        stations = [self.fetch_weather_data(param).reset_index(drop=True) for param in self.params]

        stations = [df.drop(columns=['index']) for df in stations]

        stations = reduce(lambda left, right: pd.merge(left, right, how='inner', on=['Jahr', 'Monat']), stations)

        stations = self._change_d_type(stations)

        stations["Monat"] = stations["Monat"].map(self.month_names)

        stations = self.Jahreszeiten(stations)

        logger.info("Stationswetterdaten erfolgreich verarbeitet")


        return stations
  

         
    def fetch_page_content(self, param):

        """Ruft eine JSON‑Seite der Station‑API ab.

            Returns
            -------
            dict
                Das JSON‑Objekt der API‑Antwort.

            Raises
            ------
            requests.exceptions.RequestException
                Wenn der HTTP‑Request fehl schlägt.
        """
        try:

            response = requests.get(self.url, params = param)
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error("Fehler beim abrufen der Links der Stationswetterdaten")
        
    
    def fetch_weather_data(self, param):
        
        """Setzt den kompletten ETL‑Schritt für eine Wetterstation um."""
        
        response = self.fetch_page_content(param)
        df = self.preprocess_response(response)

        Frosttage = self.Frosttage(df)
        Eistage = self.Eistage(df)
        Sommertage = self.Sommertage(df)
        Heiße_Tage = self.Heiße_tage(df)
        Höchsttemperatur = self.Höchstemperatur(df)
        Tiefsttemperatur = self.Tiefsttemperatur(df)
        Tropennächte = self.Tropennacht(df)



        comb = pd.concat([Frosttage, Eistage, Sommertage, Heiße_Tage, Höchsttemperatur, Tiefsttemperatur, Tropennächte], axis= 1)
        
        station_result = comb.loc[:,~comb.columns.duplicated()]

        return station_result


    def preprocess_response(self, response):

        """Wandelt rohe JSON‑Antwort in einen normalisierten DataFrame um."""
        
        logger.info("Start Preprocessing Stationsdaten...")

        df = pd.DataFrame(response)

        df["mw_beginn"] = pd.to_datetime(df["mw_beginn"])
        df["mw_ende"] = pd.to_datetime(df["mw_ende"])

        df["Monat"] = df["mw_beginn"].dt.month
        df["day"] = df["mw_beginn"].dt.day
        df["Jahr"] = df["mw_beginn"].dt.year
        df["hour"] = df["mw_beginn"].dt.hour

        df["date"] = df["mw_beginn"].dt.date
        df["date"] = pd.to_datetime(df["date"])

        df.drop(columns=["matname", "metname", "freigabe","nwg", "einname", "kmpname"], inplace = True)

        logger.info("Preprocessing der Stationsdaten abgeschlossen")

        return df
      
    def Frosttage(self, df):

        """ Frosttage Berechnung """

        logger.info("Berechnung der Frosttage...")
      
        frost = df.groupby(["mstkrz", "Jahr", "Monat", "day"])["messwert"].apply(lambda x: ~(x.apply(lambda v: custom_round(v, precision=1) >= 0)).all()).reset_index()
        
        frost_df = self._calculate_df_res(frost)
        frost_df = self._rename(frost_df, "_frost")

        return frost_df

    
    def Eistage(self, df):

        """ Eistage Berechnung """

        logger.info("Berechnung der Eistage...")

        eis = df.groupby(["mstkrz", "Jahr", "Monat", "day"])["messwert"].apply(lambda x: (x <= 0).all()).reset_index()

        eis_df = self._calculate_df_res(eis)
        eis_df = self._rename(eis_df, "_eis")

        return eis_df
    
    def Sommertage(self, df): 

        """ Sommertage Berechnung """

        logger.info("Berechnung der Sommertage...")
      
        sommer = df.groupby(["mstkrz","Jahr", "Monat", "day"])["messwert"].apply(lambda x: ~(x.apply(lambda v: custom_round(value= v, precision=1)) < 25).all()).reset_index()

        sommer_df = self._calculate_df_res(sommer)
        sommer_df = self._rename(sommer_df, "_sommertage")

        return sommer_df

    def Heiße_tage(self, df):

        """ Heiße Tage Berechnung """

        logger.info("Berechnung der Heißentage...")
       
        heiße = df.groupby(["mstkrz","Jahr", "Monat", "day"])["messwert"].apply(lambda x: ~(x < 30).all()).reset_index()

        heiße_df = self._calculate_df_res(heiße)
        heiße_df = self._rename(heiße_df, "_heißetage")

        return heiße_df


    def Höchstemperatur(self, df):

        """ Höchtstemperatur Berechnung """

        logger.info("Berechnung der Höchsttemperatur...")
       
        höchst_df = df.groupby(["mstkrz", "Jahr", "Monat"])["messwert"].max().reset_index()

        höchst_df["messwert"] = höchst_df["messwert"].apply(lambda x: custom_round(value  = x, precision = 1))
        höchst_df = self._rename(höchst_df, "_höchsttemperatur")

        return höchst_df
    
    def Tiefsttemperatur(self, df):

        """ Tiefsttemperatur Berechnung """

        logger.info("Berechnung der Tiefsttemperatur...")
        
        tiefst_df = df.groupby(["mstkrz", "Jahr", "Monat"])["messwert"].min().reset_index()

        tiefst_df["messwert"] = tiefst_df["messwert"].apply(lambda x: custom_round(value = x, precision = 1))

        tiefst_df = self._rename(tiefst_df, "_tiefsttemperatur")

        return tiefst_df
    
    def Tropennacht(self, df):

        """ Tropennacht Berechnung """

        logger.info("Berechnung der Tropennacht..")

        part1 = df[df['hour'] >= 19]
        part2 = df[df['hour'] < 7] 
        part2['date'] = part2['date'] - pd.Timedelta(days=1)
        
        combined = pd.concat([part1, part2])
        
        tropen = combined.groupby(["mstkrz", "date"])["messwert"].apply(lambda x: (x.apply(lambda v: custom_round(value= v, precision = 1)) >= 20).all()).reset_index()
        tropen["Monat"] = tropen["date"].dt.month
        tropen["Jahr"] = tropen["date"].dt.year

        tropen_df = self._calculate_df_res(tropen)
        tropen_df = self._rename(tropen_df, "_tropennächte")

        tropen_df = tropen_df[1:].reset_index()

        return tropen_df
    
    def Jahreszeiten(self, df):

        """ Hilfsfunktion für Quartalsberichte """

        df["Saison"] = df["Monat"].map(self.season_mapping)

        return df

    
    def _calculate_df_res(self, df):

        "Hilsfunktion zum Berechnen der Temperatur Kenntage"

        res = df.groupby(["mstkrz", "Jahr", "Monat"])["messwert"].sum().reset_index()

        return res
    
    
    def _rename(self, df, kpi):

        """ Hilsfunktion zum umbenennen der Stationskürzel"""
      
        df.rename(columns = {"messwert": df.loc[0, "mstkrz"] + kpi}, inplace= True)
        df.drop(columns = "mstkrz", inplace= True)
        
        return df 
        
    def _change_d_type(self, df):
       
        """ Hilsfunktion zum Wechseln der Datentypen """
        df = df.astype(self.dtype)

        return df
        
