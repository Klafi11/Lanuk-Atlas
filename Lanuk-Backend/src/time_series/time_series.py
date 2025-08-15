from sqlalchemy import text
from src.db import read_sql_query
import json
from src.retrieval_functions import TimeSeriesData, TimeSeriesEntry, TimeSeriesDeviation


def get_time_series_data(year: int, time_unit: str):

    """Lädt und verarbeitet DWD-Zeitreihen für Temperatur, Niederschlag und Sonnenscheindauer für API Endpunkt
    
    Args
    ---------------
    year : int
            Jahr
    time_unit : str        
            Zeiteinheit
    Returns
    -------
    TimeSeriesData : Rückgabe der Zeitreihendaten
    
    """

    data_res = TimeSeriesData(root={})
    
    for metric_id, metric_type in enumerate(["temp", "rain", "sun"]):
        try:

            query = text(f"""SELECT "Jahr", "{time_unit}" FROM dwd_table_{metric_type}""")
            data = read_sql_query(query)

            data = data[data["Jahr"] <= year]
            
            if data.empty:
                raise ValueError(f"No data returned for {metric_type}")
            

            if metric_type in ["rain", "temp"]:
                query_ref = text(f"""
                SELECT index, "{time_unit}_{metric_type}_avg" 
                FROM dwd_{metric_type}_ref 
                WHERE index IN ('1881-1910', '1961-1990', '1991-2020')
                """)
            else:
                query_ref = text(f"""
                SELECT index, "{time_unit}_{metric_type}_avg" 
                FROM dwd_{metric_type}_ref 
                WHERE index IN ('1951-1980', '1961-1990', '1991-2020')
                """)

            ref = read_sql_query(query_ref)
            
            ref_dict = {row['index']: row[f'{time_unit}_{metric_type}_avg'] for row in ref.to_dict('records')}
            ref_value = ref_dict.get("1961-1990")
            
            data["Abweichung"] = data[time_unit] - ref_value
            data["Temperatur"] = data[time_unit]
            data = data.drop(columns=[time_unit])

            if time_unit == "Winter":
                data = data.iloc[1:]
            
        
            data_dicts = json.loads(data.to_json(orient="records"))


            entry = TimeSeriesEntry(
                values=[TimeSeriesDeviation(**item) for item in data_dicts],
                ref=ref_dict
            )
            
            data_res.root[metric_id] = entry
            
   
        except Exception as e:
            return f"Error processing {metric_type}: {str(e)}"
            
    return data_res