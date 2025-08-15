import time
from datetime import datetime
import os
import csv
from src.settings import get_model_settings, get_settings

model_settings = get_model_settings()

settings = get_settings()


def cost_latency(func):
    
    """ Hilfsfunktion für Kost und Zeittracking der Sprachmodelle """

    def wrapper(prompt, input, model, run_id):
        
        # Time Tracking
        start_time = time.time()
        report = func(prompt, input, model, run_id)
        end_time = time.time()
        current_timestamp = datetime.now()
        
        latency = round(end_time - start_time, 2)
        
        #Csv Header
        fieldnames = model_settings.csv_header
        
        #Match über func name und Model
        match func.__name__:
            
            case "gpt_reporter":

                output_tokens = report.usage.completion_tokens
                input_tokens = report.usage.prompt_tokens
                total_tokens = output_tokens + input_tokens
                
                match model:
                    
                    case "gpt-4o":
                        
                        Pricing = (input_tokens / 1000000)*2.5 + (output_tokens / 1000000)*10
                    
                    case "o3-mini":

                        Pricing = (input_tokens / 1000000)*1.1 + (output_tokens / 1000000)*4.4
                    
                    case "gpt-4.1-2025-04-14":
                        
                        Pricing = (input_tokens / 1000000)*2 + (output_tokens / 1000000)*8
                
                report = report.choices[0].message.content
            
            case "claude_reporter":
                
                input_tokens = report.usage.input_tokens
                output_tokens = report.usage.output_tokens
                total_tokens = input_tokens + output_tokens

                match model:
                    case "claude-3-5-sonnet-latest":
                        
                        Pricing = (input_tokens / 1000000)*3 + (output_tokens / 1000000)*15
                    
                    case "claude-3-5-haiku-latest":
                        
                        Pricing = (input_tokens / 1000000)*0.8 + (output_tokens / 1000000)*4
                    
                    case "claude-3-7-sonnet-latest":

                        Pricing = (input_tokens / 1000000)*3 + (output_tokens / 1000000)*15
                    
                    case "claude-sonnet-4-20250514":
                        
                        Pricing = (input_tokens / 1000000)*3 + (output_tokens / 1000000)*15

                
                report = report.content[0].text

            case "deepseek_reporter":

                output_tokens = report.usage.completion_tokens
                input_tokens = report.usage.prompt_tokens
                total_tokens = output_tokens + input_tokens
                
                match model: 
                    case "deepseek-chat":
                        
                        Pricing = (input_tokens / 1000000)*0.27 + (output_tokens / 1000000)*1.1
                    
                    case "deepseek-reasoner":
                        
                        Pricing = (input_tokens / 1000000)*0.55 + (output_tokens / 1000000)*2.19
                
                report = report.choices[0].message.content

        if settings.CoT: 
            incontext = "CoT"
        elif settings.few_shot: 
            incontext = "few_shot"
        elif settings.zero_shot: 
            incontext = "zero_shot"

        # Check ob file existiert
        file_exists = os.path.exists("cost_latency.csv")
        # Schreiben in csv
        with open("cost_latency.csv", mode = "a", newline ="") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            
            if not file_exists: 
                writer.writeheader()
            
            writer.writerow({
                "Model": model,
                "Durchlaufs_id": run_id,
                "InContext_method": incontext, 
                "Timestamp": current_timestamp,
                "Latenz": latency,
                "Input_tokens": input_tokens,
                "Output_tokens": output_tokens,
                "Gesamt_tokens": total_tokens,
                "Kosten_in_USD": Pricing

            })

        
        return report
    return wrapper
    
def min_ranking(rank, year, param):

    """ Hilsfunktion zur Berechnung des Rankings """

    if param == "_rain":
    
        start_year = 1880
    
    if param == "_sun": 
        start_year = 1951

    year_count = year - start_year + 1


   
    min_rank = abs(rank - year_count)
  

    return min_rank

def extract_metadata(df):

    """ Hilfsfunktion für den Zeitreihenanalyse Agenten """
    metadata = {}

    metadata["Number_of_columns"] = df.shape[1]

    metadata["Schema"] = df.columns.tolist()

    metadata["Number_of_rows"] = df.shape[0]

    metadata["Data_Types"] = str(df.dtypes)

    metadata["Sample"] = df.head(1).to_dict(orient ="records")

    metadata["table_head"] = df.head(5).to_string()

    metadata["table_tail"] = df.tail(5).to_string()

    return metadata 


def time_unit_mapping(time_unit): 

    """ Hilfsfunktion zum Zeiteinheit Mapping """
    unit_dict = {
        "Januar": [1],
        "Februar": [2],
        "März": [3],
        "April": [4],
        "Mai": [5],
        "Juni": [6],
        "Juli": [7],
        "August": [8],
        "September": [9],
        "Oktober": [10],
        "November": [11],
        "Dezember": [12],
        "Winter": [12, 1, 2],
        "Frühling": [3,4,5],
        "Sommer": [6,7,8],
        "Herbst": [9,10,11],
        "Jahr_agg": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    }

    return unit_dict[time_unit]