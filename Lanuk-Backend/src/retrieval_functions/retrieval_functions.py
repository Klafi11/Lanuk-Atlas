from .base_retrieval_functions import *
from src.llm_reporters import get_all_reports
from src.templates import template_handler, template_handler_adv, chain_intro, template_handler_std
from collections import defaultdict
from src.settings import get_model_settings
from src.llm_reporters import claude_reporter, gpt_reporter, deepseek_reporter
from .base_retrieval_functions_ad import get_adv_month, get_adv_quarter, get_adv_year, get_weather_intro_adv
from .models import Page
import asyncio
import logging
from .valuation import check_reports, check_reports_adv

"""
retrieval_functions.py
========================

Asynchrone Hauptberichtspipeline zur Generierung von Wetterberichts-Abschnitten
(Einleitung, Temperatur, Niederschlag, Sonnenschein, Stationsvergleich) für
**Monat**, **Quartal** und **Jahr**. Die Pipeline kann in zwei Modi laufen:

- **standard**: nutzt Basis-Retrieval-Funktionen und Standard-Prompts.
- **advanced**: nutzt erweiterte Retrieval-Funktionen (inkl. aktueller DWD-Lage, Zeitreihenanalyse Agent).

  _std = Standard
  _adv = Advanced

Ablauf (vereinfacht)
--------------------
1) Datenbeschaffung (Retrieval) – `get_*`-Funktionen -> `base_retrieval_functions`
   bzw. `base_retrieval_functions_ad`.
2) Prompt-Erzeugung – über `template_handler_std`/`template_handler_adv`
   oder `chain_intro` für die Einleitung.
3) Mehrfacher LLM-Aufruf – `get_all_reports(...)` fragt GPT, Claude, DeepSeek
   parallel an.
4) Self-Correction –  valuation.py -> `check_reports` bzw. `check_reports_adv`.

Beispiel: 

1) values = await get_adv_month(year, month, "temp")
2) template_adv = template_handler_adv("temp", month)
3) reports = await get_all_reports(template_adv, values, run_id)
4) val_reports = await check_reports_adv(reports, values, "temp", month)

Erzeugte Abschnitte
-------------------
- Temperatur, Niederschlag, Sonnenscheindauer (Monat/Quartal/Jahr)
- Stationsvergleich (WAST vs. VKTU)
- Einleitung: aus aktuellen/letzten Abschnitten plus (im advanced-Modus) aktueller Wetterlage.
"""

logger = logging.getLogger(__name__)
model_settings = get_model_settings()


# -------------------------------------------------------------------------------------------------
# MONAT
# -------------------------------------------------------------------------------------------------

async def get_temp_report_month(year:int, month:str, run_id:str, report_pipe:str): 

        """Erzeugt den Temperatur-Absatz für einen Monat.
        
        Args
        ---------------
        year : int
                Zieljahr für den Bericht.
        month : str
                Zeitgranularität
        run_id : str
                run_id für Time Tracking
        report_pipe : str        
                Report-Pipeline/Variante ('Standard', 'Adnvanced'); 

        Returns
        -------
        dict: Berichtsabschnitte der jeweiligen Sprachmodelle
        """
        
        logger.info("Start Temp Process")
        
        match report_pipe:
               
                case "advanced":
                      values = await get_adv_month(year, month, "temp")
                      template_adv = template_handler_adv("temp", month)
                      reports = await get_all_reports(template_adv, values, run_id)
                      val_reports = await check_reports_adv(reports, values, "temp", month)
                
                case "standard": 
                        values = get_temp(year, month)
                        template = template_handler_std("temp", month)
                        reports = await get_all_reports(template, values, run_id)
                        val_reports = await check_reports(reports, values, "temp", month)
        
        logger.info("Finish Temp Process")

        return val_reports

async def get_rain_report_month(year:int, month:str, run_id:str, report_pipe:str): 

        """Erzeugt den Niederschlag-Absatz für einen Monat.
        
        Args
        ---------------
        year : int
                Zieljahr für den Bericht.
        month : str
                Zeitgranularität (Monat/Jahreszeit/Jahr). 
        run_id : str
                run_id für Time Tracking
        report_pipe : str        
                Report-Pipeline/Variante ('Standard', 'Adnvanced'); 

        Returns
        -------
        dict : Berichtsabschnitte der jeweiligen Sprachmodelle        
        """

        logger.info("Start Rain Process")
        match report_pipe:
               
                case "advanced":
                      values = await get_adv_month(year, month, "rain")
                      template_adv = template_handler_adv("rain", month)
                      reports = await get_all_reports(template_adv, values, run_id)
                      val_reports = await check_reports_adv(reports, values, "rain", month)
                
                case "standard":
                      values = get_rain(year, month)
                      template = template_handler_std("rain", month)
                      reports = await get_all_reports(template, values, run_id)
                      val_reports = await check_reports(reports, values, "rain", month)

        logger.info("Finish Rain Process")
        return val_reports 

async def get_sun_report_month(year:int, month:str, run_id:str, report_pipe:str): 

        """Erzeugt den Sonnenscheindauer-Absatz für einen Monat.

        Args
        ---------------
        year : int
                Zieljahr für den Bericht.
        month : str
                Zeitgranularität
        run_id : str
                run_id für Time Tracking
        report_pipe : str        
                Report-Pipeline/Variante ('Standard', 'Adnvanced'); 

        Returns
        -------
        dict : Berichtsabschnitte der jeweiligen Sprachmodelle      
        
        """

        logger.info("Start Sun Process")

        match report_pipe:
                
                case "advanced":
                      values = await get_adv_month(year, month, "sun")
                      template_adv = template_handler_adv("sun", month)
                      reports = await get_all_reports(template_adv, values, run_id)
                      val_reports = await check_reports_adv(reports, values, "sun", month)
                
                case "standard":
                      values = get_sun(year, month)
                      template = template_handler_std("sun", month)
                      reports = await get_all_reports(template, values, run_id)
                      val_reports = await check_reports(reports, values, "sun", month)

        logger.info("Finish Sun Process")

        return val_reports


async def get_station_report_month(year:int, month:str, run_id:str, report_pipe:str): 

        """Erzeugt den Wetterstations-Absatz für einen Monat.
        
        Args
        ---------------
        year : int
                Zieljahr für den Bericht.
        month : str
                Zeitgranularität
        run_id : str
                run_id für Time Tracking
        report_pipe : str        
                Report-Pipeline/Variante ('Standard', 'Adnvanced'); 

        Returns
        -------
        dict : Berichtsabschnitte der jeweiligen Sprachmodelle
        
        """
        
        logger.info("Start Station Process")

        res_station = get_station_month(year, month) 
        
        template = template_handler("_station", month) 
        
        reports = await get_all_reports(template, res_station, run_id)

        res_station_eval = station_ref(month, year, res_station)

        val_reports = await check_reports(reports, res_station_eval, "station", month)

        logger.info("Finish Station Process")
        
        
        return val_reports

# -------------------------------------------------------------------------------------------------
# QUARTAL
# -------------------------------------------------------------------------------------------------

async def get_temp_report_quarter(year:int, quarter:str, run_id:str, report_pipe:str):

        """Erzeugt den Temperatur-Absatz für ein Quartal.
        
        
        Args
        ---------------
        year : int
                Zieljahr für den Bericht.
        quarter : str
                Zeitgranularität
        run_id : str
                run_id für Time Tracking
        report_pipe : str        
                Report-Pipeline/Variante ('Standard', 'Adnvanced'); 

        Returns
        -------
        dict : Berichtsabschnitte der jeweiligen Sprachmodelle
        """
        
        logger.info("Start Temp Process")
        
        match report_pipe:
                case "advanced": 
                        values =  await get_adv_quarter(year, quarter, "temp")
                        template_adv = template_handler_adv("temp", quarter)
                        reports = await get_all_reports(template_adv, values, run_id)
                        val_reports = await check_reports_adv(reports, values, "temp", quarter)


                case "standard": 
                        values = get_temp(year, quarter)
                        values = append_current_month("temp", quarter, year, values)
                        template = template_handler_std("temp", quarter)
                        reports = await get_all_reports(template, values, run_id)
                        val_reports = await check_reports(reports, values, "temp", quarter)

        logger.info("Finish Temp Process")
                        
        return val_reports


async def get_rain_report_quarter(year:int, quarter:str, run_id:str, report_pipe:str):

        """Erzeugt den Niederschlag-Absatz für ein Quartal.
        
        Args
        ---------------
        year : int
                Zieljahr für den Bericht.
        quarter : str
                Zeitgranularität
        run_id : str
                run_id für Time Tracking
        report_pipe : str        
                Report-Pipeline/Variante ('Standard', 'Adnvanced'); 

        Returns
        -------
        dict : Berichtsabschnitte der jeweiligen Sprachmodelle
        
        """
        
        logger.info("Start Rain Process")
        
        match report_pipe:
                case "advanced": 
                        values =  await get_adv_quarter(year, quarter, "rain")
                        template_adv = template_handler_adv("rain", quarter)
                        reports = await get_all_reports(template_adv, values, run_id)
                        val_reports = await check_reports_adv(reports, values, "rain", quarter)


                case "standard": 
                        values = get_rain(year, quarter)
                        values = append_current_month("rain", quarter, year, values)
                        template = template_handler_std("rain", quarter)
                        reports = await get_all_reports(template, values, run_id)
                        val_reports = await check_reports(reports, values, "rain", quarter)
        
        logger.info("Finish Rain Process")
                        
        return val_reports
    
async def get_sun_report_quarter(year:int, quarter:str, run_id:str, report_pipe:str):

        """Erzeugt den Sonnenscheindauer-Absatz für ein Quartal.
        
        Args
        ---------------
        year : int
                Zieljahr für den Bericht.
        quarter : str
                Zeitgranularität
        run_id : str
                run_id für Time Tracking
        report_pipe : str        
                Report-Pipeline/Variante ('Standard', 'Adnvanced'); 

        Returns
        -------
        dict : Berichtsabschnitte der jeweiligen Sprachmodelle
        
        """
        
        logger.info("Start Sun Process")
        match report_pipe:
                case "advanced": 
                        values =  await get_adv_quarter(year, quarter, "sun")
                        template_adv = template_handler_adv("sun", quarter)
                        reports = await get_all_reports(template_adv, values, run_id)
                        val_reports = await check_reports_adv(reports, values, "sun", quarter)


                case "standard": 
                        values = get_sun(year, quarter)
                        values = append_current_month("sun", quarter, year, values)
                        template = template_handler_std("sun", quarter)
                        reports = await get_all_reports(template, values, run_id)
                        val_reports = await check_reports(reports, values, "sun", quarter)
        
        logger.info("Finish Sun Process")
                        
        return val_reports

async def get_station_report_quarter(year:int, quarter:str, run_id:str, report_pipe:str):

        """Erzeugt den Wetterstations-Absatz für ein Quartal.
        
        Args
        ---------------
        year : int
                Zieljahr für den Bericht.
        quarter : str
                Zeitgranularität
        run_id : str
                run_id für Time Tracking
        report_pipe : str        
                Report-Pipeline/Variante ('Standard', 'Adnvanced'); 

        Returns
        -------
        dict : Berichtsabschnitte der jeweiligen Sprachmodelle
        
        """

        logger.info("Start Station Process")

        res_station = get_station_quarter(year, quarter)

        template = template_handler("_station", quarter)

        reports = await get_all_reports(template, res_station, run_id)

        res_station_eval = station_ref(quarter, year, res_station)
        
        val_reports = await check_reports(reports, res_station_eval, "station", quarter)

        logger.info("Finish Station Process")

        return val_reports

# -------------------------------------------------------------------------------------------------
# JAHR
# -------------------------------------------------------------------------------------------------

async def get_temp_report_year(year, year_agg, run_id, report_pipe):

        """Erzeugt den Temperatur-Absatz für ein Jahr.
        
        Args
        ---------------
        year : int
                Zieljahr für den Bericht.
        year_agg : str
                Zeitgranularität
        run_id : str
                run_id für Time Tracking
        report_pipe : str        
                Report-Pipeline/Variante ('Standard', 'Adnvanced'); 

        Returns
        -------
        dict : Berichtsabschnitte der jeweiligen Sprachmodelle
        
        """
        
        logger.info("Start Temp Process")
        match report_pipe:
                case "advanced": 
                        values =  await get_adv_year(year, year_agg, "temp")
                        template_adv = template_handler_adv("temp", year_agg)
                        reports = await get_all_reports(template_adv, values, run_id)
                        val_reports = await check_reports_adv(reports, values, "temp", year_agg)


                case "standard": 
                        values = get_temp(year, year_agg)
                        values = append_current_year("temp", year_agg, year, values)
                        template = template_handler_std("temp", year_agg)
                        reports = await get_all_reports(template, values, run_id)
                        val_reports = await check_reports(reports, values, "temp", year_agg)
        
        logger.info("Finish Temp Process")                
        return val_reports

async def get_rain_report_year(year:int, year_agg:str, run_id:str, report_pipe:str): 

        """Erzeugt den Niederschlag-Absatz für ein Jahr.
        
        Args
        ---------------
        year : int
                Zieljahr für den Bericht.
        year_agg : str
                Zeitgranularität
        run_id : str
                run_id für Time Tracking
        report_pipe : str        
                Report-Pipeline/Variante ('Standard', 'Adnvanced'); 

        Returns
        -------
        dict : Berichtsabschnitte der jeweiligen Sprachmodelle
        
        """
    
        logger.info("Start Rain Process")
        match report_pipe:
                
                case "advanced": 
                        values =  await get_adv_year(year, year_agg, "rain")
                        template_adv = template_handler_adv("rain", year_agg)
                        reports = await get_all_reports(template_adv, values, run_id)
                        val_reports = await check_reports(reports, values, "rain", year_agg)


                case "standard": 
                        values = get_rain(year, year_agg)
                        values = append_current_year("rain", year_agg, year, values)
                        template = template_handler_std("rain", year_agg)
                        reports = await get_all_reports(template, values, run_id)
                        val_reports = await check_reports(reports, values, "rain", year_agg)

        logger.info("Finish Rain Process")                
        return val_reports

async def get_sun_report_year(year:int, year_agg:str, run_id:str, report_pipe:str):

        """Erzeugt den Sonnenscheindauer-Absatz für ein Jahr.
        
        Args
        ---------------
        year : int
                Zieljahr für den Bericht.
        year_agg : str
                Zeitgranularität
        run_id : str
                run_id für Time Tracking
        report_pipe : str        
                Report-Pipeline/Variante ('Standard', 'Adnvanced'); 

        Returns
        -------
        dict : Berichtsabschnitte der jeweiligen Sprachmodelle
        
        """
    
        logger.info("Start Sun Process")
        
        match report_pipe:
                case "advanced": 
                        values =  await get_adv_year(year, year_agg, "sun")
                        template_adv = template_handler_adv("sun", year_agg)
                        reports = await get_all_reports(template_adv, values, run_id)
                        val_reports = await check_reports(reports, values, "sun", year_agg)


                case "standard": 
                        values = get_sun(year, year_agg)
                        values = append_current_year("sun", year_agg, year, values)
                        template = template_handler_std("sun", year_agg)
                        reports = await get_all_reports(template, values, run_id)
                        val_reports = await check_reports(reports, values, "sun", year_agg)
        
        logger.info("Finish Sun Process")
                        
        return val_reports

async def get_station_report_year(year:int, year_agg:str, run_id:str, report_pipe:str):

        """Erzeugt den Wetterstations-Absatz für ein Jahr.
        
        Args
        ---------------
        year : int
                Zieljahr für den Bericht.
        year_agg : str
                Zeitgranularität
        run_id : str
                run_id für Time Tracking
        report_pipe : str        
                Report-Pipeline/Variante ('Standard', 'Adnvanced'); 

        Returns
        -------
        dict : Berichtsabschnitte der jeweiligen Sprachmodelle
        
        """

        
        logger.info("Start Station Process")

        res_station = get_station_year(year, year_agg)

        template = template_handler("_station", year_agg)

        reports = await get_all_reports(template, res_station, run_id)
        
        res_station_eval = station_ref(year_agg, year, res_station)

        res_station_eval["Monat"] = "Jahr"

        val_reports = await check_reports(reports, res_station_eval, "station", year_agg)

        logger.info("Finish Station Process")


        return val_reports

# -------------------------------------------------------------------------------------------------
# ÜBERSCHRIFT
# -------------------------------------------------------------------------------------------------

async def get_report_introduction(year:int, time_unit:str, report_schema: Page, run_id, report_pipe: str):
    
    """Erzeugt die Einleitung aus den Berichtsabschnitten.
    
        Args
        ---------------
        year : int
                Zieljahr für den Bericht.
        time_unit : str
                Zeitgranularität
        report_schema: Page
                Report Schema mit den jeweilig generierten Berichtsabschnitten
        run_id : str
                run_id für Time Tracking
        report_pipe : str        
                Report-Pipeline/Variante ('Standard', 'Adnvanced'); 

        Returns
        -------
        dict : Berichtsabschnitte der jeweiligen Sprachmodelle

    """
                         
    logger.info("Start Introduction Process")
    report = defaultdict(list)
    reports = {}


    for tag in report_schema.tags:
        for v in tag.value:
            report["gpt"].append(v[0])
            report["claude"].append(v[1])
            report["deepseek"].append(v[2])


    llm_reporters = [
        (gpt_reporter, model_settings.gpt_4_1),
        (claude_reporter, model_settings.an_son_4),
        (deepseek_reporter, model_settings.v3_se),
    ]

    query = text(f"""SELECT * from report_table
                    WHERE "Monat" = '{time_unit}' """)
    df = read_sql_query(query)
    
    df = df.sort_values(["Jahr"], ascending= True)
    
    item_format = """
        {time_unit} {year}: \n
        {content}
        ------------------------------
        """
    vora_sections = "\n".join(
        item_format.format(time_unit= row["Monat"], year = row["Jahr"], content =  row[f"Einleitung"])
        for index, row in df.iterrows())

    
    def pipe():
        return report_pipe == "advanced" and year >= 2025 and time_unit in ["April", "Mai", "Juni", "Juli", "August", "September", "November", "Dezember"]
    
    if pipe():
    
        wetter_data = await get_weather_intro_adv(year, time_unit)
            

    else:
    
        template = template_handler_std("intro", time_unit)


    loop = asyncio.get_event_loop()
    tasks = []


    for index, key in enumerate(report.keys()):
        data = {"report": " ".join(report[key])}
        data["time_unit"] = time_unit
        data["year"] = year
        data["vora_time_unit"] = vora_sections
        reporter_func, model = llm_reporters[index]
        
        if pipe():

            data["aktuelle_wetterlage"] = wetter_data

        task = loop.run_in_executor(
            None,
            lambda func=reporter_func, tmpl=template if not pipe() else chain_intro, d=data, m=model, rid=run_id:
                func(tmpl, d, m, rid)
        )
        tasks.append(task)


    results = await asyncio.gather(*tasks)

    for index, result in enumerate(results):
        reports[index] = result

    logger.info("Finish Introduction Process")
    if pipe():
        return [reports, wetter_data]
    
    return reports


# -------------------------------------------------------------------------------------------------
# RETRIEVAL FUNKTIONEN für den DataRetriever (llm_reporters/models.py)
# -------------------------------------------------------------------------------------------------

retrieval_functions = {"get_temp_report_month" : get_temp_report_month,
                       "get_rain_report_month" : get_rain_report_month,
                       "get_sun_report_month" : get_sun_report_month,
                       "get_station_report_month" : get_station_report_month,
                       "get_temp_report_quarter" : get_temp_report_quarter,
                       "get_rain_report_quarter" : get_rain_report_quarter,
                       "get_sun_report_quarter" : get_sun_report_quarter,
                       "get_station_report_quarter" : get_station_report_quarter,
                       "get_temp_report_year" : get_temp_report_year,
                       "get_rain_report_year" : get_rain_report_year,
                       "get_sun_report_year" : get_sun_report_year,
                       "get_station_report_year" : get_station_report_year,
                       "get_report_introduction": get_report_introduction
                       }