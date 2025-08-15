from pydantic import BaseModel, Field
from typing import List
from langchain_openai import ChatOpenAI
from src.settings import get_model_settings
from .template import heading_temp


"""
heading.py
====================

Erzeugt Abschnitts-Überschriften für Wetterberichte mithilfe eines LLM

Hauptbestandteile
-----------------
- `Heading_struc` (Pydantic-Modell): Strukturierte, typsichere Rückgabe der
  generierten Überschriften.
- `generate_heading(...)`: Baut aus einem Berichtsdiktat einen geordneten
  Prompt und ruft die LLM-Kette `heading_temp | ChatOpenAI` mit strukturiertem
  Output auf.

"""


settings = get_model_settings()

llm_sum = ChatOpenAI(model = settings.gpt_4_1_mini, openai_api_base = settings.OPENROUTER_BASE_URL, openai_api_key = settings.OPENROUTER_API_KEY)

# Überschriftenstruktur
class Heading_struc(BaseModel):
    headings: List[str] = Field(
        description= "Liste der verschiedenen Überschriften"
    )
    


def generate_heading(report:dict, year:int, time_unit:str):

    """ Strukturierte Rückgabe für Überschriftenergebnisse 
    
    Args
    ---------------
    report : dict
            Berichtsabschnitte
    year : int
            Jahr
    time_unit : str        
            Zeiteinheit
    Returns
    -------
    Heading_struc : Liste der verschiedenen Überschriften
    
    """


    Items_string = """
    {Absatz}:
    {content}
    """ 


    items_list = []
    for index, content in report.items():
        
        if index == "4":
            value = Items_string.format(Absatz = "Einleitung", content = content)

        elif index == "0":
            value = Items_string.format(Absatz = "Temperatur", content = content)

        elif index == "1": 
            value = Items_string.format(Absatz = "Niederschlag", content = content)

        elif index == "2": 
            value = Items_string.format(Absatz = "Sonnenscheindauer", content = content)
        
        elif index == "3":
            value = Items_string.format(Absatz = "Kenntageauswertung", content = content)
            
        items_list.append(value)


    Bericht = "\n".join(items_list[i] for i in [4,0,1,2,3])

    
    heading_chain = heading_temp | llm_sum.with_structured_output(Heading_struc)

    res = heading_chain.invoke({"year": year, "time_unit": time_unit, "Bericht": Bericht})

    return res 







