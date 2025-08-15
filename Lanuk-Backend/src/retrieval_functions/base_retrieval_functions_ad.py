from .base_retrieval_functions import get_rain, get_temp, get_sun, append_current_month, append_current_year
from src.db import read_sql_query
from sqlalchemy import text
from src.settings import get_settings, get_model_settings
from src.templates import temp_prompt_adv, rain_prompt_adv, sun_prompt_adv, summarize_prompt_wetter
from src.utils import extract_metadata, time_unit_mapping
from langgraph.prebuilt import create_react_agent
from typing import Annotated
from langchain_experimental.utilities import PythonREPL
from pyairtable import Api
import pandas as pd
from langchain_openai import ChatOpenAI

"""
base_retrieval_functions_ad.py
===============================

Erweiterte Retrieval-Funktionen für die Textgenerierung von Wetterberichten im Adanved Modus.

Aufbau
---------
- `get_adv_month`: Holt Basiswerte (temp/rain/sun), ergänzt eine explorative
  Analyse (ReAct-Agent mit Python-REPL) und baut einen strukturierten Promptkontext.

- `get_adv_quarter` / `get_adv_year`: Wiederverwenden der Monatslogik + Anhängen
  der aktuellen Abschnitte (Saison bzw. Jahr).

- `get_weather_intro_adv`: Holt aktuelle DWD Wetterberichte aus dem Airtable, bereitet sie
  je Zeitintervall auf, sodass diese als zusätzlichen Kontext für die Einleitung dienen (Wetterereignisse).

"""

settings = get_settings()
model_settings = get_model_settings()



async def get_adv_month(year:int, time_unit:str, absatz:str):

    """Kontexterweiterung des Adnvanced Modus um Zeitreihenanalyse der jeweiligen Zeiteinheit
    
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
    dict : Daten für den jeweiligen Berichtabschnitt mit Zeitreihenanalyse Kontext
    
    """
    
    #relevante Werte der Zeiteinheit
    match absatz:
        case "temp":
            data = get_temp(year, time_unit)
            task_v = "°C"
            prompt = temp_prompt_adv
        
        case "rain":
            data = get_rain(year, time_unit)
            task_v = "l/m²"
            prompt = rain_prompt_adv
        
        case "sun":
            data = get_sun(year, time_unit)
            task_v = "h"
            prompt = sun_prompt_adv
    

    query_ref = text(f"""SELECT "{time_unit}_{absatz}_avg" FROM dwd_{absatz}_ref 
                     WHERE index = '1961-1990' """)
    
    df_ref = read_sql_query(query_ref)
    
    ref_value = float(df_ref[f"{time_unit}_{absatz}_avg"].values[0])

    # Aufgabenset für den ReAct-Agent
    Aufgabenset = """Aufgabenstellung

                Führe eine detaillierte Analyse der Witterungsdaten durch, mit besonderem Fokus auf die letzten Jahrzehnte der Zeitreihe.
                
                Terminologie
                Positive Abweichung: Werte über dem Referenzmittelwert (1961-1990)
                Negative Abweichung: Werte unter dem Referenzmittelwert (1961-1990)
                Referenzmittelwert: {ref_value} {task_v} (Periode 1961-1990)

                Analyseaufgaben
                1. Abweichungsanalyse
                Identifiziere markante positive und negative Abweichungen vom Referenzmittelwert in den letzten Jahrzehnten. Quantifiziere die Stärke dieser Abweichungen.
                2. Extremwertanalyse
                Lokalisiere auffällige Extremwerte und charakterisiere starke Ausreißer in den jüngeren Jahrzehnten. Bewerte deren Häufigkeit und Intensität.
                3. Periodisches Verhalten
                Idenztifiziere Perioden mit negativen sowie positiven Abweichungen der letzten Jahrzehnte. Benenne diese und bewerte deren Häufigkeit und Intensität.
                4. Aktuelle Einordnung
                Ordne die aktuelle Zeiteinheit {year} {time_unit} in den Kontext der gesamten Zeitreihe ein. Bewerte dessen Position relativ zu deinen gefundenen Ergebnissen.
                5. Syntheseanalyse
                Fasse die Erkenntnisse zusammen und beschreibe den Witterungsverlauf in Absatzform basierend auf den gefunden Ergebnissen aus der Aufgabenanalyse

                Ausgabeformat

                Strukturierte Darstellung nach den fünf Analysepunkten
                Präzise, datenbasierte Aussagen
                Fokus auf {year} und {time_unit}
                Kompakte, aussagekräftige Zusammenfassung in Absatzform""".format(ref_value = ref_value, year = year, time_unit = time_unit, task_v = task_v)

    query_anal = text(f""" SELECT "Jahr", "{time_unit}" from dwd_table_{absatz}""")

    df_anal = read_sql_query(query_anal)

    if time_unit == "Winter":
        df_anal = df_anal[1:]

    df_anal = df_anal[df_anal["Jahr"]<= year]

    df_metadata = extract_metadata(df_anal)

    repl = PythonREPL()
    repl.globals["df"] = df_anal

    # Python REPL Tool
    def python_repl(code: Annotated[str, " Der Python Programmcode zum ausführen deiner Analysis Aufgaben."]):
    
        """Nutze dieses Tool um Python Code auszuführen. Nutze den print(...) command 
        um deine Ergebnisse der Berechnungen auszugeben. Alles was du durch print(...) ausgibst ist sichtbar"""
        
        try:
            result = repl.run(code)
        except BaseException as e:
            return f"Failed to execute. Error: {repr(e)}"
        result_str = f"Successfully executed:\n```python\n{code}\n```\nStdout: {result}"
        return (
            result_str 
        )
    tools = [python_repl]

    # Intialisierung des Agenten   
    agent = create_react_agent(
    model=model_settings.gpt_4_1,  
    tools=tools,  
    prompt=prompt)

    res_anal = await agent.ainvoke(
    {"messages": [{"role": "user", "content": "Erledige deine Aufgabe"}]},
    config={"configurable": {"Schema": df_metadata["Schema"], 
                             "Number_of_columns": df_metadata["Number_of_columns"], 
                             "Number_of_rows": df_metadata["Number_of_rows"], 
                             "Sample": df_metadata["Sample"], 
                             "Data_Types":df_metadata["Data_Types"],
                             "table_head": df_metadata["table_head"],
                             "table_tail": df_metadata["table_tail"],
                             "Input_m": Aufgabenset,
                             "time_unit": time_unit,
                             "recursion_limit": 8}})



    data["anal_time_unit"] = res_anal["messages"][-1].content

    print(data["anal_time_unit"])

    return data
    

    

async def get_adv_quarter(year:int, time_unit:str, absatz:str):

    """ Erweiterung der Pipeline für Quartalberichte 
    
    Args
    ---------------
    absatz : str
            Absatz(Temperatur, Niederschlag, Sonnenscheindauer)
    year : int
            Jahr
    time_unit : str        
            Zeiteinheit
    Returns
    -------
    dict : Daten für den jeweiligen Berichtabschnitt
    
    """
    data = await get_adv_month(year, time_unit, absatz)

    data = append_current_month(absatz = absatz, time_unit = time_unit, year = year, values = data)

    return data



    
async def get_adv_year(year:int, time_unit:str, absatz:str):

    """ Erweiterung der Pipeline für Jahresberichte
    
    Args
    ---------------
    absatz : str
            Absatz(Temperatur, Niederschlag, Sonnenscheindauer)
    year : int
            Jahr
    time_unit : str        
            Zeiteinheit
    Returns
    -------
    dict : Daten für den jeweiligen Berichtabschnitt
    """
        
    data = await get_adv_month(year, time_unit, absatz)

    data = append_current_year(absatz = absatz, time_unit = time_unit, year = year, values = data)

    
    return data


async def get_weather_intro_adv(year:int, time_unit:str):

    """ Erweiterung des Kontextes der Einleitung durch die DWD Wetterberichte.
    
    Args
    ---------------
    year : int
            Jahr
    time_unit : str        
            Zeiteinheit
    Returns
    -------
    str : DWD Wetterbericht für die jeweilige Zeiteinheit
    """


    llm_sum = ChatOpenAI(model = model_settings.gpt_4_1_mini, openai_api_base = settings.OPENROUTER_BASE_URL, openai_api_key = settings.OPENROUTER_API_KEY)
    api = Api(model_settings.AIRTABLE_API_KEY)
    table = api.table(model_settings.APP_ID_AIR, model_settings.TABLE_ID_AIR)

    airtable_data = table.all()

    df = pd.json_normalize(
    airtable_data,
    record_path=None,
    meta=[
        'id',
        'createdTime',
        ['fields', 'time_unit'],
        ['fields', 'Wetterlage'],
        ['fields', 'Vorhersage']
    ],
)

    df.columns = df.columns.str.replace('fields.', '')


    df['createdTime'] = pd.to_datetime(df['createdTime'])
    df['time_unit'] = pd.to_datetime(df['time_unit'])

    time_unit_mapping_val = time_unit_mapping(time_unit)

    if time_unit != "Winter":
        time_unit_data = df[
            (df['time_unit'].dt.month.isin(time_unit_mapping_val)) & 
            (df["time_unit"].dt.year == year)]
    else:
        dez_winter = df[
            (df["time_unit"].dt.month == 12) & 
            (df["time_unit"].dt.year == year - 1)]
        
        jan_feb_winter = df[
            (df["time_unit"].dt.month.isin(time_unit_mapping_val[1:])) & 
            (df["time_unit"].dt.year == year)]
        
        time_unit_data = pd.concat([dez_winter, jan_feb_winter])


        time_unit_data = time_unit_data.assign(
            day=time_unit_data['time_unit'].dt.day,
            hour=time_unit_data['time_unit'].dt.hour,
            month=time_unit_data['time_unit'].dt.month).sort_values(["month", "day", "hour"])


    time_unit_data_list = [
        time_unit_data[time_unit_data["time_unit"].dt.month == month] 
        for month in time_unit_mapping_val]

    if time_unit in settings.months:
        time_unit_data = time_unit_data_list[0].drop_duplicates(
            subset=['Wetterlage'], 
            keep='first')
    else: 
        
        processed_dfs = [
            df.drop_duplicates(subset=['Wetterlage'], keep='first')
            for df in time_unit_data_list
        ]
        
    
        time_unit_data = pd.concat(processed_dfs, ignore_index=True)
            
    time_unit_data_str = time_unit_data[["time_unit", "Wetterlage"]].to_string()
    
    chain_wetter_sum = summarize_prompt_wetter | llm_sum 
    res_wetter_sum = await chain_wetter_sum.ainvoke({
        "time_unit": time_unit,
        "year": year, 
        "inhalt": time_unit_data_str
    })
    
    return res_wetter_sum.content
        
















