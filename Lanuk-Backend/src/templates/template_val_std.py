from langchain_core.prompts import PromptTemplate
from .template_data import *
from .template_struktur import *
from .template_val_tasks import *
from src.settings import get_settings

settings = get_settings()

"""
Modul: Prompt-Vorlagen und Auswahl-Handler für qualitätsgesicherte
Selbstkorrektur-Texte für den "Standard"-Modus (Temperatur, Niederschlag, Sonnenschein, Wetterstationen) über
verschiedene Zeitbezüge (Monat, Saison, Jahr).

Dieses Modul definiert:
- Vollständige Prompt-Strings (Aufgabe, Daten, Struktur, Kontext/Referenzen).
- Zusammengesetzte LangChain-PromptTemplates für jede (Variable × Zeitraum)-Kombination.
- Einen Handler (`template_handler_eval_adv`), der abhängig von `absatz` und
  `time_unit` das passende PromptTemplate zurückliefert.

Wichtige Konventionen:
- Platzhalter in geschweiften Klammern ({...}) müssen zur Laufzeit mit passenden
  Werten gefüllt werden.
- Die Tags in spitzen Klammern (<...> ... </...>) dienen nur der Strukturierung
  innerhalb des Prompt-Textes für das LLM.
"""

#-----------------------------------------------------------------------------------------------------------------#
 ### Wichtige Hinsweise ### 

important_temp = """
Wichtig: gebe Temperaturabweichungen immer in Kelvin (K) an 
"""

important_rain = """
Wichtig: gebe den Niederschlag in l/m² an
"""

#-----------------------------------------------------------------------------------------------------------------#
 ### Kontext für die jeweilge Zeiteinheit ### 

context_month =  """
<context>
Dir stehen im Abschnitt <reference_materials> folgende ergänzende Informationen zur Verfügung:

1. (<previous_months>) Stilistische und inhaltliche Absätze der vergangenen {time_unit}-Monate: 
Diese dienen dir als Vorlage für Stil, Aufbau, Wortwahl und inhaltliche Tiefe. Nutze sie, um deinen neuen Text kohärent, einheitlich und anschlussfähig zu gestalten. 
Du darfst Formulierungen, Strukturen oder inhaltliche Bezüge übernehmen, wenn sie sinnvoll passen.

Nutze diese Informationen, um den aktuellen Text anhand deiner Aufgabe zu verbessern.
</context>
"""

context_season = """
<context>
Dir stehen im Abschnitt <reference_materials> folgende ergänzende Informationen zur Verfügung:

1. (<previous_seasons>) Stilistische und inhaltliche Absätze der vergangenen {time_unit}-Saisons: 
Diese dienen dir als Vorlage für Stil, Aufbau, Wortwahl und inhaltliche Tiefe. Nutze sie, um deinen neuen Text kohärent, einheitlich und anschlussfähig zu gestalten. 
Du darfst Formulierungen, Strukturen oder inhaltliche Bezüge übernehmen, wenn sie sinnvoll passen.

2. (<current_months>) Absätze der aktuellen Monate der laufenden Saison:  
Diese enthalten relevante Informationen zu den aktuellen Monaten des {time_unit}. Greife bei Bedarf auf diese Inhalte zurück und integriere sie korrekt und sinnvoll in deinen neuen Absatz, um aktuelle Entwicklungen abzubilden.

Nutze diese Informationen, um den aktuellen Text anhand deiner Aufgabe zu verbessern.
</context>
"""

context_year = """
<context>
Dir stehen im Abschnitt <reference_materials> folgende ergänzende Informationen zur Verfügung:

1. (<previous_seasons>) Stilistische und inhaltliche Absätze der vergangenen {time_unit}-Saisons: 
Diese dienen dir als Vorlage für Stil, Aufbau, Wortwahl und inhaltliche Tiefe. Nutze sie, um deinen neuen Text kohärent, einheitlich und anschlussfähig zu gestalten. 
Du darfst Formulierungen, Strukturen oder inhaltliche Bezüge übernehmen, wenn sie sinnvoll passen.

2. (<current_months>) Absätze der aktuellen Monate des laufenden Jahres:  
Diese enthalten relevante Informationen zu den aktuellen Monaten des {time_unit}. Greife bei Bedarf auf diese Inhalte zurück und integriere sie korrekt und sinnvoll in deinen neuen Absatz, um aktuelle Entwicklungen abzubilden.

Nutze diese Informationen, um den aktuellen Text anhand deiner Aufgabe zu verbessern.
</context>
"""

#-----------------------------------------------------------------------------------------------------------------#
 ### Referenzmaterial für die Zeiteinheit ### 

# Ref month
ref_month = """
Hiermit erhälst du die Daten aus den Referenzberichten, diese dienen dir als stilistische Referenz:
<reference_materials>
<previous_months>
1. Absätze der vorangegangenen {time_unit} Monate:
{vora_time_unit}
</previous_months>
</reference_materials>
"""

#ref season 
ref_season = """
<reference_materials>
<previous_seasons>
Hiermit erhälst du die Daten aus den Referenzberichten, diese dienen als stilistische Referenz:
1. Absätze der vorangegangenen {time_unit}-Saison:                                   
{vora_time_unit}
</previous_season>

<current_months>
Hiermit erhälst du die Daten für die laufenden Monate, diese sind auch im Absatz der Saison enthalten:
2. Aktuelle Monate der laufenden {time_unit}-Saison:                                        
{aktuelle_time_unit}
</current_months>
</reference_materials>
"""

#ref year 

ref_year = """
<reference_materials>
<previous_years>
Hiermit erhälst du die Daten aus den Referenzberichten, diese dienen als stilistische Referenz:
1. Absätze der vorangegangenen Jahre:                                 
{vora_time_unit}
</previous_years>

<current_months>
Hiermit erhälst du die Daten für die laufenden Monate, diese sind auch im Absatz der Saison enthalten:
2. Aktuelle Monate des laufenden Jahres:                                      
{aktuelle_time_unit}
</current_months>
</reference_materials>
"""

ref_station = """
<reference_materials>
<previous_years>
Hiermit erhälst du die Daten aus den Referenzberichten, diese dienen als stilistische Referenz:
1. Absätze der vorangegangenen Zeiteinheit {Monat} {Jahr}:                                 
{station_ref}
</previous_years>
"""


#-----------------------------------------------------------------------------------------------------------------#
 ### Zusammenführt der Promptabschnitte für die jeweilige Berichtsausprägung ### 



# Month prompt
val_prompt_temp = PromptTemplate.from_template(f"""
{task_prompt_temp_sun}
{data_temp_month}
{important_temp}
{template_aufbau_temp}
{context_month}
{ref_month}
""")

val_prompt_rain = PromptTemplate.from_template(f"""
{task_prompt_rain}
{data_rain_month}
{important_rain}
{template_aufbau_rain}
{context_month}
{ref_month}
""")

val_prompt_sun = PromptTemplate.from_template(f"""
{task_prompt_temp_sun}
{data_sun_month}
{template_aufbau_sun}
{context_month}
{ref_month}
""")

#season_prompt
val_prompt_temp_season = PromptTemplate.from_template(f"""
{task_prompt_temp_sun}
{data_temp_season}
{important_temp}
{template_aufbau_temp_season}
{context_season}
{ref_season}
""")

val_prompt_rain_season = PromptTemplate.from_template(f"""
{task_prompt_rain}
{data_rain_season}
{important_rain}
{template_aufbau_rain_season}
{context_season}
{ref_season}
""")

val_prompt_sun_season = PromptTemplate.from_template(f"""
{task_prompt_temp_sun}
{data_sun_season}
{template_aufbau_sun_season}
{context_season}
{ref_season}
""")

val_prompt_temp_year = PromptTemplate.from_template(f"""
{task_prompt_temp_sun}
{data_temp_year}
{important_temp}
{template_aufbau_temp_year}
{context_year}
{ref_year}
""")

val_prompt_rain_year = PromptTemplate.from_template(f"""
{task_prompt_rain}
{data_rain_year}
{important_rain}
{template_aufbau_rain_year}
{context_year}
{ref_year}
""")

val_prompt_sun_year = PromptTemplate.from_template(f"""
{task_prompt_temp_sun}
{data_sun_year}
{template_aufbau_sun_year}
{context_year}
{ref_year}
""")

val_prompt_station_winter = PromptTemplate.from_template(f"""
{task_prompt_station}
{data_station_winter}
{ref_station}
""")

val_prompt_station_sommer = PromptTemplate.from_template(f"""
{task_prompt_station}
{data_station_sommer}
{ref_station}
""")

val_prompt_station_trans = PromptTemplate.from_template(f"""
{task_prompt_station}
{data_station_trans}
{ref_station}
""")

val_prompt_station_year = PromptTemplate.from_template(f"""
{task_prompt_station}
{data_station_year}
{ref_station}
""")

#-----------------------------------------------------------------------------------------------------------------#
 ### Template Handler ### 


def template_handler_eval(absatz, time_unit):

    if time_unit in settings.months:
        match absatz:
            case "temp":
                return val_prompt_temp
            case "rain": 
                return  val_prompt_rain
            case "sun": 
                return val_prompt_sun
            
    if time_unit in settings.seasons:
        match absatz:
            case "temp":
                return val_prompt_temp_season
            case "rain": 
                return val_prompt_rain_season
            case "sun":
                return val_prompt_sun_season
            
    if time_unit in settings.year:
        match absatz:
            case "temp":
                return val_prompt_temp_year
            case "rain":
                return val_prompt_rain_year
            case "sun":
                return val_prompt_sun_year
    
    if time_unit in settings.trans_season_set and absatz == "station":
        return val_prompt_station_trans

    if time_unit in settings.sommer_template_set and absatz == "station":
        return val_prompt_station_sommer

    if time_unit in settings.winter_template_set and absatz == "station":
        return val_prompt_station_winter

    if time_unit in settings.Jahr_template_set and absatz == "station":
        return val_prompt_station_year

