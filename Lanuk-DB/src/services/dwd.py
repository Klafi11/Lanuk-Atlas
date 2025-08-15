import requests
import pandas as pd
from io import StringIO
import time
from collections import defaultdict
import datetime as dt
from src.config.logger_config import logger
from src.utils.utils import custom_round

"""weather_dwd_downloader.py

Lädt Temperatur‑, Niederschlags‑ und Sonnenscheindauer‑Daten des Deutschen
Wetterdienstes (DWD) für Nordrhein‑Westfalen, bereitet sie auf und liefert:

* **df_raw**   – Monatswerte in *Long‑Form* (Jahr, Monat, Wert)
* **df_clear** – Breite Pivot‑Tabelle (Jahr × Monat + Saisons + Jahr_agg)
* **df_ref**   – Klimareferenzwerte je 30 Jahres‑Intervall

Beispiel
--------
>>> settings = DWDSettings()
>>> dwd = WeatherDWDDownloader(settings)
>>> result = dwd()                # __call__

```"""

class WeatherDWDDownloader:


    def __init__(self, settings):

        logger.info("Initializing WeatherDWDDownloader")
        self.setting = settings

        self.url = self.setting.url
        self.links = self.setting.links
        self.dtype_clear_temp = self.setting.dtype_clear_temp
        self.dtype_clear_rain_sun = self.setting.dtype_clear_rain_sun
        self.dtype_raw_temp = self.setting.dtype_raw_temp
        self.dtype_raw_rain = self.setting.dtype_raw_rain
        self.dtype_raw_sun = self.setting.dtype_raw_sun
        self.dtype_ref_temp = self.setting.dtype_ref_temp
        self.dtype_ref_rain = self.setting.dtype_ref_rain
        self.dtype_ref_sun  = self.setting.dtype_ref_sun
        
        self.months = ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember","Winter", "Frühling", "Sommer", "Herbst", "Jahr_agg"]
    
    def __call__(self):

        """Lädt und verarbeitet alle verlinkten DWD‑Datensätze.

        Returns
        -------
        dict
            ``{"df_clear": [...], "df_raw": [...], "df_ref": [...]}``, jeweils
            eine Liste mit 3 DataFrames (Temp, Niederschlag, Sonne).
        df_raw = []
        df_clear = []
        df_ref = []
        """

        for index, link in enumerate(self.links):
            df = self._fetch_weather_DWD(link)
            df_raw.append(self._transform_df_raw(df, index))
            df_clear.append(self._transform_df_clear(df, index))
            df_ref.append(self._transform_df_ref(df_clear[index], index))
        
        logger.info("Daten Verarbeitung der DWD Daten abgeschlossen")


        return {"df_clear": df_clear, "df_raw": df_raw, "df_ref": df_ref}
        
    def _transform_df_raw(self, df, index):
        """Normalisiert Rohdaten und wendet Typen + Runden an."""
      

        logger.info("Transformierung der Basisdaten des DWD...")



        df = df[["Jahr", "Monat", "Nordrhein-Westfalen"]].copy()

        match index: 
            #case temp
            case 0:
                
                df.rename(columns = {"Nordrhein-Westfalen": "temperatur_Nrw"}, inplace = True)
                df["temperatur_Nrw"] = df["temperatur_Nrw"].apply(lambda x: custom_round(value=x, precision=1))
                df = df.astype(self.dtype_raw_temp)
            
            case 1 | 2:  
            #case rain or sun
                if index == 1:
                    df.rename(columns = {"Nordrhein-Westfalen": "niederschlag_Nrw"}, inplace = True)
                    df["niederschlag_Nrw"] = df["niederschlag_Nrw"].apply(lambda x: custom_round(value=x, precision=0))
                    df = df.astype(self.dtype_raw_rain)
                else:
                    df.rename(columns = {"Nordrhein-Westfalen": "sonnenscheindauer_Nrw"}, inplace = True)
                    df["sonnenscheindauer_Nrw"] = df["sonnenscheindauer_Nrw"].apply(lambda x: custom_round(value=x, precision=0))
                    df = df.astype(self.dtype_raw_sun)
        return df
    
    
    def _transform_df_ref(self, df, index):
        """Berechnet 30 jährige Klimareferenzen."""

        logger.info("Berechnung der Referenzperioden...")

        ref_month = defaultdict(list)
        periods = self.generate_time_intervals(index)
       
        
        for month in self.months:
           
            for period in periods:   
                
                match index:
                    case 0:
                        ref_month[f"{month}_temp_avg"].append(custom_round(df[month].loc[period[0]:period[1]].mean(), precision=1))
                    case 1: 
                        ref_month[f"{month}_rain_avg"].append(custom_round(df[month].loc[period[0]:period[1]].mean(), precision=0))
                    case 2:
                        ref_month[f"{month}_sun_avg"].append(custom_round(df[month].loc[period[0]:period[1]].mean(), precision=0))
        
        result = pd.DataFrame(ref_month).set_index(pd.Index([str(period[0]) +"-"+ str(period[1]) for period in periods]))
        
        match index: 
            case 0: 
                result = result.astype(self.dtype_ref_temp)
            case 1: 
               result = result.astype(self.dtype_ref_rain)
            case 2:
                result = result.astype(self.dtype_ref_sun)
                
        
        return result


    def _transform_df_clear(self, df, index):
        """Erstellt Pivot‑Tabelle + Saisons + Gesamtjahr + Rankings."""

        result  = df.pivot(index = "Jahr", columns = "Monat", values = "Nordrhein-Westfalen")
        result.columns = ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"]
        result.index = result.index.astype(int)
    
  
        match index:
        # case Temp
            case 0:
                
                #result_1 = result.copy()
                result = result.map(lambda x: custom_round(value=x, precision=1))
                #result_1 = result_1.map(lambda x: custom_round(value=x, precision=2))
                
                result = result.astype(self.dtype_clear_temp)
    
                
                result = self._add_year(result, index)
                
                result = self._add_seasons(result, index)
            
                result = self._add_rank(result)

                #result_1 = self._add_rank(result_1)            
                
        # case Rain or Sun   --> convert to int
            case 1 | 2:
                result = result.map(lambda x: custom_round(value=x, precision=0))
                result = result.astype(self.dtype_clear_rain_sun)
                        
                
                result = self._add_year(result, index)
                
                result = self._add_seasons(result, index)
            
                result = self._add_rank(result)

        return result
    
    # Helperfunctions
    def _add_seasons(self, df, index):
    # add Seasons to table 

        # Convert to DataFrame
        match index:
            case 0:
                df["Winter"] = ((df["Dezember"].shift(1) + df["Januar"] + df["Februar"]) / 3).apply(lambda x: custom_round(value=x, precision=1)).astype(float)
                df["Frühling"] = ((df["März"] + df["April"] + df["Mai"]) / 3).apply(lambda x: custom_round(value=x, precision=1)).astype(float)
                df["Sommer"] = ((df["Juni"] + df["Juli"] + df["August"]) / 3).apply(lambda x: custom_round(value=x, precision=1)).astype(float)
                df["Herbst"] = ((df["September"] + df["Oktober"] + df["November"]) / 3).apply(lambda x: custom_round(value=x, precision=1)).astype(float)



            case 1 | 2:
                df["Winter"] = (df["Dezember"].shift(1) + df["Januar"] + df["Februar"])   
                df["Frühling"] = df["März"] + df["April"] + df["Mai"]
                df["Sommer"] = df["Juni"] + df["Juli"] + df["August"]
                df["Herbst"] = df["September"] + df["Oktober"] + df["November"]
        
        return df
    
    
    def _add_year(self, df, index): 

        """Hilfsfunktion für Jahreswerte"""
        
        match index: 
            case 0: df["Jahr_agg"] = (df.sum(axis = 1) / 12).apply(lambda x: custom_round(value=x, precision=1)).astype(float)
            case 1 | 2 : df["Jahr_agg"] = df.sum(axis = 1)
        
        return df 
     
    
    def _add_rank(self, df):

        "Hilfsfunktion zum Aufsetzen der Rakings"

        def _rank_by_first(series):
            
            ranks = series.rank(method="first", ascending = False)
            return ranks.iloc[-1]



        for month in df.columns:
        
           df[f"{month}_ranking"] = df[month].expanding(1).apply(_rank_by_first)

           df[f"{month}_ranking"] = round(df[f"{month}_ranking"])
        
        return df
    
    
    @staticmethod
    def generate_time_intervals(index):

        """ Hilfsfuktion für Referenzwerte Berechnung der Zeitintervalle (1881-1910, ... )"""
        current_year = dt.datetime.today().year  
        end = (current_year // 10) *10  
        start = end - 29 
        intervals = []

        match index: 

            case 0 | 1:

                while start >= 1881:  # Stop wenn  1881-1910 erreicht wurde
                    intervals.append((start, end))
                    start -= 10  # Start wieder 10 Jahre zurücksetzen
                    end -= 10  
            case 2: 
                while start >= 1951: # Sonnenscheindauer
                    intervals.append((start, end))
                    start -= 10
                    end -= 10

    
        return intervals
        

    def fetch_page_content(self, link, month):

        """ Fetch der DWD-Daten
            
            Args: link --> link der einzelnen Daten [Temperatur, Niederschlag, Sonnenscheindauer]
                    month --> angegebener Monat "01" etc. 
        
        """
        
        try:
            full_url = self.url + link + month + ".txt"
            response = requests.get(full_url)

            response.raise_for_status()
            csv_data = StringIO(response.text)
            
            return csv_data
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Fehler beim Abrufen der Wetterdaten von {full_url}: {e}")
              

    def _fetch_weather_DWD(self, link):
        """ Ruft Wetterdaten für ein bestimmtes Jahr & Monat ab.
        
            params: link der einzelnen Daten [Temperatur, Niederschlag, Sonnenscheindauer]
        
        """
        months = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
        result = pd.DataFrame()
        
        for month in months:

                
                csv_data = self.fetch_page_content(link, month)
                logger.info(f"Processing {link} & {month}")
                if csv_data is None:
                    logger.warning(f"Fehler beim abrufen der Monatsdaten -> fetch_page_content is None")
                

                df = pd.read_csv(csv_data, delimiter = ";")
                df.reset_index(inplace = True)
                df.columns = df.iloc[0]
                df_clear = df.iloc[1:]

                result = pd.concat([result, df_clear], ignore_index=True)

                time.sleep(2)

        logger.info("Erfolgreiches abrufen der Wetterdaten des DWD")
            
        return result
  

  