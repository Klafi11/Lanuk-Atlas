from langchain_openai import ChatOpenAI
from src.settings import get_model_settings
from src.templates import template_handler_eval, template_handler_eval_adv
from langchain_anthropic import ChatAnthropic
import asyncio
import logging
from pydantic import BaseModel, Field
from typing import Optional

"""
valuation.py
============
Self-Correction Mechanismus

---

Validiert und verfeinert generierte Berichtstexte:

- `check_reports(...)`: Bewertet/vereinheitlicht mehrere Rohtexte (z. B. von
  GPT/Claude/DeepSeek) anhand einer standardisierten Instruktions-Prompt in templates/template_val_tasks und /template_val_std(_adv)
  und liefert die korrigierten Berichtstexte zurück.
- `check_reports_adv(...)`: Wie oben, aber mit erweitertem Bewertungs-Prompt
  (Advanced-Pfad).

"""


settings = get_model_settings()
openai_llm_val = ChatOpenAI(model_name = settings.gpt_o3, openai_api_base = settings.OPENROUTER_BASE_URL, openai_api_key = settings.OPENROUTER_API_KEY)
logger = logging.getLogger(__name__)

async def check_reports(reports:dict, values:dict, absatz:str, time_unit:str):

    """Self-Correction: Validiert/vereinheitlicht die Berichtsabschnitte für den Standard-Modus
    
    Args
    ---------------
    reports : dict
            Berichtsabschnitte
    values : dict
            Werte für die Validierung der Berichte
    absatz : str
            Absatz des jeweiligen Berichtsabschnitt für Self-Correction
    time_unit : str        
            Zeiteinheit

    Returns
    -------
    dict : Berichtsabschnitte der jeweiligen Sprachmodelle

    """

    async def process_report(key:int, report:str):
        # Template handler
        val_prompt = template_handler_eval(absatz, time_unit)

        # Validierungspipeline
        corrected_report_pipe = val_prompt | openai_llm_val

        try:
            corrected_report = await corrected_report_pipe.ainvoke({**values, "report": report})
            return key, corrected_report.content
        except Exception as e:
            logger.warning("Failed to Process Valuation")

    
    tasks = [process_report(key, report) for key, report in reports.items()]
    # Rückgabe
    results = await asyncio.gather(*tasks)

    return {key: content for key, content in results}

async def check_reports_adv(reports:dict, values:dict, absatz:str, time_unit:str):

    """Self-Correction: Validiert/vereinheitlicht die Berichtsabschnitte für den Advanced-Modus
    
    Args
    ---------------
    reports : dict
            Berichtsabschnitte
    values : dict
            Werte für die Validierung der Berichte
    absatz : str
            Absatz des jeweiligen Berichtsabschnitt für Self-Correction
    time_unit : str        
            Zeiteinheit

    Returns
    -------
    dict : Berichtsabschnitte der jeweiligen Sprachmodelle
    
    """

    async def process_report(key:int, report:str):
        # Template handler
        val_prompt = template_handler_eval_adv(absatz, time_unit)
        
        #Validierungspipeline
        corrected_report_pipe = val_prompt | openai_llm_val

        try:
            corrected_report = await corrected_report_pipe.ainvoke({**values, "report": report})
            return key, corrected_report.content
        except Exception as e:
            logger.warning(f"Failed to Process Valuation {e}")

    tasks = [process_report(key, report) for key, report in reports.items()]
    # Rückgabe 
    results = await asyncio.gather(*tasks)

    return {key: content for key, content in results}


