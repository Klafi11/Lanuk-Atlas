from src.db import read_sql_query
from sqlalchemy import text
import pandas as pd
from src.settings import get_settings
from src.utils import min_ranking

"""
base_retrieval_functions.py
===========================

Liefert aufbereitete Eingabedaten für die Berichtsgenerierung:
- Monats-/Saison-/Jahreswerte zu Temperatur, Niederschlag und Sonnenscheindauer
  - aktueller Wert
  - Referenzperioden (1881–1910, 1961–1990, 1991–2020 bzw. 1951–1980)  
  - Ranking 
  - Kontext aus Alteberichten

- Stationsauswertungen (WAST, VKTU, …) je Monat/Saison/Jahr.

"""

settings = get_settings()

def get_temp(year: int, time_unit:str):

    """Liest Temperatur-Kerngrößen (Abweichung/Mittel) für Jahr und Zeiteinheit.

    Es werden Referenzperioden (1881–1910, 1961–1990, 1991–2020), der Wert für
    das angefragte Jahr sowie das Ranking geladen. Zusätzlich wird der
    Kontextblock für das Zeitreihenretrieval aus den Altberichten aus der Datenbank abgefragt.
    
    Args
    ---------------
    year : int
            Jahr
    time_unit : str        
            Zeiteinheit
    Returns
    -------
    dict : Daten für den jeweiligen Berichtabschnitt
    
    """

    # Referenzwerte
    query_ref = text(f"""SELECT index, "{time_unit}_temp_avg" FROM dwd_temp_ref 
                        WHERE index IN('1881-1910','1961-1990','1991-2020')""")
    
    # aktueller Wert & Ranking
    query_rank = text(f"""SELECT "{time_unit}", "{time_unit}_ranking" FROM dwd_table_temp
                        WHERE "Jahr" = {year}""")
    
    # Kontext aus Altberichten
    query_fs_ex = text(f"""SELECT * from report_table
                    WHERE "Monat" = '{time_unit}' """)
    
    
    # Retrieval Start
    query_obj = [query_ref, query_rank, query_fs_ex]
    
    temp = [read_sql_query(query) for query in query_obj]

    temp_ex = temp[2].sort_values(["Jahr"], ascending= True)


    item_format = """
    ------------------------------   
    {time_unit} {year}: 
    {content} 
    ------------------------------
    """

    vora_sections = "\n".join(
        item_format.format(time_unit= row["Monat"], year = row["Jahr"], content =  row[f"temp_text"])
            for index, row in temp_ex.iterrows())

    # Datenrückgabe
    temp_dict = {"year": year, 
                    "time_unit": time_unit,
                    "m_temp" : temp[1][time_unit].values[0], 
                    "ranking_temp": int(temp[1][f"{time_unit}_ranking"].values[0].astype(int)),
                    "m_temp_80_10": float(temp[0].loc[temp[0]['index'] == '1881-1910', f'{time_unit}_temp_avg'].values[0]),
                    "m_temp_60_90": float(temp[0].loc[temp[0]['index'] == '1961-1990', f'{time_unit}_temp_avg'].values[0]),
                    "m_temp_90_20": float(temp[0].loc[temp[0]['index'] == '1991-2020', f'{time_unit}_temp_avg'].values[0]),
                    "vora_time_unit": vora_sections
                    }
    
    return temp_dict


def get_rain(year: int, time_unit: str):

    """Liest Niederschlags-Kerngrößen (Abweichung/Mittel) für Jahr und Zeiteinheit.

    Es werden Referenzperioden (1881–1910, 1961–1990, 1991–2020), der Wert für
    das angefragte Jahr sowie das Ranking geladen. Zusätzlich wird der
    Kontextblock für das Zeitreihenretrieval aus den Altberichten aus der Datenbank abgefragt.
    
    Args
    ---------------
    year : int
            Jahr
    time_unit : str        
            Zeiteinheit
    Returns
    -------
    dict : Daten für den jeweiligen Berichtabschnitt"""

    # Referenzwerte
    query_ref = text(f"""SELECT index, "{time_unit}_rain_avg" FROM dwd_rain_ref 
                        WHERE index IN('1881-1910','1961-1990','1991-2020')""")
    
    # Aktueller Wert & Ranking
    query_rank = text(f"""SELECT "{time_unit}", "{time_unit}_ranking" FROM dwd_table_rain
                        WHERE "Jahr" = {year}""")
    
    # Kontext als Albterichten
    query_fs_ex = text(f"""SELECT * from report_table
                    WHERE "Monat" = '{time_unit}' """)
    
    # Retrieval Start
    query_obj = [query_ref, query_rank, query_fs_ex]
    
    rain = [read_sql_query(query) for query in query_obj]

    rain_ex = rain[2].sort_values(["Jahr"], ascending= True)

    item_format = """
    ------------------------------
    {time_unit} {year}: 
    {content} 
    ------------------------------
    """

    vora_sections = "\n".join(
        item_format.format(time_unit= row["Monat"], year = row["Jahr"], content =  row[f"rain_text"])
            for index, row in rain_ex.iterrows())


    # Datenrückgabe
    rain_dict = {"year": year, 
                    "time_unit": time_unit,
                    "m_rain" : int(rain[1][time_unit].values[0]), 
                    "ranking_rain": int(rain[1][f"{time_unit}_ranking"].values[0].astype(int)),
                    "ranking_rain_min": int (min_ranking(rain[1][f"{time_unit}_ranking"].values[0].astype(int), year, "_rain")),
                    "m_rain_80_10": int(rain[0].loc[rain[0]['index'] == '1881-1910', f'{time_unit}_rain_avg'].values[0]),
                    "m_rain_60_90": int(rain[0].loc[rain[0]['index'] == '1961-1990', f'{time_unit}_rain_avg'].values[0]),
                    "m_rain_90_20": int(rain[0].loc[rain[0]['index'] == '1991-2020', f'{time_unit}_rain_avg'].values[0]),
                    "vora_time_unit": vora_sections
                    }
    return rain_dict

def get_sun(year:int, time_unit:str):

    """Liest Sonnenscheindauer-Kerngrößen (Abweichung/Mittel) für Jahr und Zeiteinheit.

    Es werden Referenzperioden (1881–1910, 1961–1990, 1991–2020), der Wert für
    das angefragte Jahr sowie das Ranking geladen. Zusätzlich wird der
    Kontextblock für das Zeitreihenretrieval aus den Altberichten aus der Datenbank abgefragt.
    
    Args
    ---------------
    year : int
            Jahr
    time_unit : str        
            Zeiteinheit
    Returns
    -------
    dict : Daten für den jeweiligen Berichtabschnitt"""


    # Referenzwerte
    query_ref = text(f"""SELECT index, "{time_unit}_sun_avg" FROM dwd_sun_ref 
                        WHERE index IN('1951-1980','1961-1990','1991-2020')""")
    
    # Aktueller Wert & Ranking
    query_rank = text(f"""SELECT "{time_unit}", "{time_unit}_ranking" FROM dwd_table_sun
                        WHERE "Jahr" = {year}""")
    
    # Kontext aus Altberichten
    query_fs_ex = text(f"""SELECT * from report_table
                    WHERE "Monat" = '{time_unit}' """)
    
   # Retrieval 
    query_obj = [query_ref, query_rank, query_fs_ex]
    
    sun = [read_sql_query(query) for query in query_obj]

    sun_ex = sun[2].sort_values(["Jahr"], ascending= True)

    item_format = """
    ------------------------------
    {time_unit} {year}: 
    {content} 
    ------------------------------
    """

    vora_sections = "\n".join(
        item_format.format(time_unit= row["Monat"], year = row["Jahr"], content =  row[f"sun_text"])
            for index, row in sun_ex.iterrows())


    # Rückgabe
    sun_dict = {"year": year, 
                "time_unit": time_unit,
                "m_sun" : int(sun[1][time_unit].values[0]), 
                "ranking_sun": int(sun[1][f"{time_unit}_ranking"].values[0].astype(int)),
                "ranking_sun_min": int(min_ranking(sun[1][f"{time_unit}_ranking"].values[0].astype(int), year, "_sun")),
                "m_sun_50_80": int(sun[0].loc[sun[0]['index'] == '1951-1980', f'{time_unit}_sun_avg'].values[0]),
                "m_sun_60_90": int(sun[0].loc[sun[0]['index'] == '1961-1990', f'{time_unit}_sun_avg'].values[0]),
                "m_sun_90_20": int(sun[0].loc[sun[0]['index'] == '1991-2020', f'{time_unit}_sun_avg'].values[0]),
                "vora_time_unit": vora_sections
                }
    return sun_dict

def get_station_month(year:int, month:str):

    """Stationsdaten (WAST/VKTU …) für einen Monat.

    Aggregiert keine Zeit – liefert Einzelwerte je Station und Metrik.
    Fügt parallel dieselben Spalten mit Suffix `_l_y` (last year) hinzu.
    
    Args
    ---------------
    year : int
            Jahr
    month : str        
            Zeiteinheit
    Returns
    -------
    dict : Daten für den jeweiligen Berichtabschnitt
    """
        
    query_station = text(f"""SELECT * FROM v_Wetterstationen
                            WHERE "Jahr" = {year} AND
                            "Monat" = '{month}' """)
    

    query_station_past_year = text(f"""SELECT * FROM v_Wetterstationen
                                    WHERE "Jahr" = {year - 1 } AND
                                    "Monat" = '{month}' """)
    

    station = read_sql_query(query_station)

    
    station_past = read_sql_query(query_station_past_year)

    station_past.columns = station_past.columns + "_l_y"

    
    res_station = station.to_dict(orient="list")

    res_station_past = station_past.to_dict(orient = "list")

    res_station = {**res_station, **res_station_past}

    return res_station

def get_station_quarter(year:int, quarter:str):

    """Stationsdaten (WAST/VKTU …) für ein Quartal.

    Aggregiert keine Zeit – liefert Einzelwerte je Station und Metrik.
    Fügt parallel dieselben Spalten mit Suffix `_l_y` (last year) hinzu.
    
    Args
    ---------------
    year : int
            Jahr
    quarter : str        
            Zeiteinheit
    Returns
    -------
    dict : Daten für den jeweiligen Berichtabschnitt
    
    """
        
    match quarter:
            
        # Winter muss für Dezember ein Jahr zurück datiert werden
        case "Winter":
            query_station = text(f"""SELECT * FROM v_Wetterstationen 
                                    WHERE ("Jahr" = {year} AND "Monat" IN ('Januar', 'Februar') AND "Saison" = 'Winter')
                                    OR ("Jahr" = {year-1} AND "Monat" = 'Dezember' AND "Saison" = 'Winter')""")
        
        case "Frühling" | "Sommer" | "Herbst":
                
            query_station = text(f"""SELECT * FROM v_Wetterstationen
                                WHERE "Jahr" = {year} AND
                                "Saison" = '{quarter}' """)

    
    station = read_sql_query(query_station)

    station = station.groupby("Saison").agg(settings.Season_agg)

    res_station = station.to_dict(orient="list")   

    res_station["Jahr"] = year

    res_station ["Monat"] = quarter 

    match quarter:
            
        case "Winter":
            query_station_past = text(f"""SELECT * FROM v_Wetterstationen 
                                    WHERE ("Jahr" = {year-1} AND "Monat" IN ('Januar', 'Februar') AND "Saison" = 'Winter')
                                    OR ("Jahr" = {year-2} AND "Monat" = 'Dezember' AND "Saison" = 'Winter')""")
        
        case "Frühling" | "Sommer" | "Herbst":
                
            query_station_past = text(f"""SELECT * FROM v_Wetterstationen
                                WHERE "Jahr" = {year-1} AND
                                "Saison" = '{quarter}' """)

    station_past = read_sql_query(query_station_past)

    station_past = station_past.groupby("Saison").agg(settings.Season_agg)

    station_past.columns = station_past.columns + "_l_y"

    res_station_past = station_past.to_dict(orient="list")   

    res_station_past["Jahr_l_y"] = year - 1

    res_station_past["Monat_l_y"] = quarter 
    
    res_station = {**res_station, **res_station_past}
    
    return res_station

def get_station_year(year:int, year_agg:str):

    """Stationsdaten (WAST/VKTU …) für ein Jahr.

    Aggregiert keine Zeit – liefert Einzelwerte je Station und Metrik.
    Fügt parallel dieselben Spalten mit Suffix `_l_y` (last year) hinzu.
    
    Args
    ---------------
    year : int
            Jahr
    year_agg : str        
            Zeiteinheit
    Returns
    -------
    dict : Daten für den jeweiligen Berichtabschnitt
    """

    query_station = text(f"""SELECT * FROM v_Wetterstationen
                                    WHERE "Jahr" = {year} """)
    
            
    station = read_sql_query(query_station)

    station = station.groupby("Jahr").agg(settings.Season_agg)

    res_station = station.to_dict(orient="list")  


    res_station["Monat"] = year_agg

    res_station["Jahr"] = year
    
    query_station_past = text(f"""SELECT * FROM v_Wetterstationen
                                    WHERE "Jahr" = {year-1} """)
    
            
    station_past = read_sql_query(query_station_past)

    station_past = station_past.groupby("Jahr").agg(settings.Season_agg)

    station_past.columns = station_past.columns + "_l_y"

    res_station_past = station_past.to_dict(orient="list")  

    res_station_past["Jahr_l_y"] = year - 1

    res_station_past["Monat_l_y"] = year_agg


    res_station = {**res_station, **res_station_past}


    return res_station


def get_station(year:int, time_unit:str, stations:list[str]):
   
    """Stationsdaten (WAST/VKTU …) Hilfsfunktion für Stationsabfrage API Endpunkte.
    
    Args
    ---------------
    year : int
            Jahr
    time_unit : str        
            Zeiteinheit
    stations : list
            Liste der Stationsnamen

    Returns
    -------
    dict : Daten für den jeweiligen Berichtabschnitt
    
    """

    columns = [f'"{station}_frost", "{station}_eis", "{station}_sommertage", "{station}_heißetage", "{station}_tropennächte", "{station}_höchsttemperatur", "{station}_tiefsttemperatur"' for station in stations]

    sql_stations = ", ".join(columns)
    
    
    def build_season_agg_dict(stations: list[str]):

        metrics_config = {
            "frost": "sum",
            "eis": "sum", 
            "sommertage": "sum",
            "heißetage": "sum",
            "höchsttemperatur": "max",
            "tiefsttemperatur": "min",
            "tropennächte": "sum"
        }
        
        season_agg = {}
        for station in stations:
            for metric, agg_method in metrics_config.items():
                key = f"{station}_{metric}"
                season_agg[key] = agg_method
        
        return season_agg
    
    season_agg = build_season_agg_dict(stations)
    
    
    if time_unit in settings.months:
    
        query_station = text(f"""SELECT {sql_stations}, "Saison" FROM v_Wetterstationen
                            WHERE "Jahr" = {year} AND
                            "Monat" = '{time_unit}' """) 
        
        station = read_sql_query(query_station)

    elif time_unit in settings.seasons:

        match time_unit:
            
            case "Winter":
                query_station = text(f"""SELECT {sql_stations}, "Saison" FROM v_Wetterstationen 
                                        WHERE ("Jahr" = {year} AND "Monat" IN ('Januar', 'Februar') AND "Saison" = 'Winter')
                                        OR ("Jahr" = {year-1} AND "Monat" = 'Dezember' AND "Saison" = 'Winter')""")
            
            case "Frühling" | "Sommer" | "Herbst":
                    
                query_station = text(f"""SELECT {sql_stations}, "Saison" FROM v_Wetterstationen
                                    WHERE "Jahr" = {year} AND
                                    "Saison" = '{time_unit}' """)
            
        station = read_sql_query(query_station)
            
        station = station.groupby("Saison").agg(season_agg)
    
    
    elif time_unit in settings.year:

            query_station = text(f"""SELECT {sql_stations}, "Jahr", "Saison" FROM v_Wetterstationen
                                    WHERE "Jahr" = {year} """)
            
            station = read_sql_query(query_station)

            station = station.groupby("Jahr").agg(season_agg)
 

    res_station = station.to_dict(orient="list")

    return res_station


def append_current_month(absatz:str, time_unit:str, year:int, values:dict): 

    """ Hilfsfunktion für Quartalsberichte, um die aktuellen Monate als Kontext mit in die Werte anzuhängen die in die Prompt eingesetzt werden.

    Args
    ---------------
    absatz : str
            Absatz(Temperatur, Niederschlag, Sonnenscheindauer)
    year : int
            Jahr
    time_unit : str        
            Zeiteinheit
    values : dict
            relevante Daten
    Returns
    -------
    dict : Daten für den jeweiligen Berichtabschnitt
    

    """

    match time_unit:
        case "Winter":
    
            s_query = text(f"""SELECT * FROM report_table
                                WHERE ("Jahr" = {year} AND "Monat" IN ('Januar', 'Februar'))
                                OR ("Jahr" = {year-1} AND "Monat" = 'Dezember') """)
        case "Sommer":

            s_query = text(f"""SELECT * FROM report_table
                                WHERE "Jahr" = {year} AND "Monat" IN ('Juni', 'Juli', 'August') """)
            
        case "Herbst":

            s_query = text(f"""SELECT * FROM report_table
                                WHERE "Jahr" = {year} AND "Monat" IN ('September', 'Oktober', 'November') """)
        case "Frühling": 

            s_query = text(f"""SELECT * FROM report_table
                                WHERE "Jahr" = {year} AND "Monat" IN ('März', 'April', 'Mai') """)

    item_format = """
    ------------------------------
    {time_unit} {year}:
    {content}
    ------------------------------
    """
     
    
    df_s = read_sql_query(s_query)
    df_s = df_s.sort_values(["Jahr"], ascending= True)

    sections_s = "\n".join(
        item_format.format(time_unit= row["Monat"], year = row["Jahr"], content =  row[f"{absatz}_text"])
        for index, row in df_s.iterrows())


    values["aktuelle_time_unit"] = sections_s

    return values

def append_current_year(absatz:str, time_unit:str, year:int, values:dict): 

    """Hilfsfunktion für Jahresberichte, um die aktuellen Monate als Kontext mit in die Werte anzuhängen die in die Prompt eingesetzt werden.
    
    Args
    ---------------
    absatz : str
            Absatz(Temperatur, Niederschlag, Sonnenscheindauer)
    year : int
            Jahr
    time_unit : str        
            Zeiteinheit
    values : dict
            relevante Daten
    Returns
    -------
    dict : Daten für den jeweiligen Berichtabschnitt

    """

    query = text(f"""SELECT * FROM report_table
                WHERE "Monat" IN ('Januar', 'Februar', 'März', 'April', 'Mai','Juni','Juli','August','September', 'Oktober', 'November', 'Dezember') AND
                "Jahr" = {year} """)

    item_format = """
    ------------------------------    
    {time_unit} {year}: 
    {content}
    ------------------------------
    """
    
    
    df_s = read_sql_query(query)
    df_s = df_s.sort_values(["Jahr"], ascending= True)

    sections_s = "\n".join(
        item_format.format(time_unit= row["Monat"], year = row["Jahr"], content =  row[f"{absatz}_text"])
        for index, row in df_s.iterrows())


    values["aktuelle_time_unit"] = sections_s
    values["time_unit"] = "Jahr"

    
    return values

def station_ref(time_unit:str, year:int, values:dict):
    
    """Hilfunktion für Self-Correction Stationsdaten, um die aktuellen Monate als Kontext mit in die Werte anzuhängen, die in die Prompt eingesetzt werden.
    
    Args
    ---------------
    year : int
            Jahr
    time_unit : str        
            Zeiteinheit
    values : dict
            relevante Daten
    Returns
    -------
    dict : Daten für den jeweiligen Berichtabschnitt

    """

    query = text(f""" SELECT * FROM report_table 
                 WHERE "Monat" = '{time_unit}' """)
    
    df = read_sql_query(query)
    df = df.sort_values(["Jahr"], ascending= True)

    item_format = """
    ------------------------------   
    {time_unit} {year}: 
    {content} 
    ------------------------------
    """

    vora_sections = "\n".join(
        item_format.format(time_unit= row["Monat"], year = row["Jahr"], content =  row[f"Wetterstation_text"])
            for index, row in df.iterrows())
    
    
    if time_unit in settings.months:
    
        values["Jahr"] = values["Jahr"][0]
        values["Monat"] = values["Monat"][0]
        
    values["station_ref"] = vora_sections
    
    return values