from pydantic import BaseModel, RootModel
from typing import List, Dict, Optional

"""
models.py
========================

Ein asynchroner `DataRetriever`, der die `retrieval_functions`
(LLM-/Datenpipelines) aufruft und die Ergebnisse in ein `Page`-Schema schreibt.

(Pydantic-Modelle zur Strukturierung von Berichtsmetadaten und Zeitreihen)

Hauptbestandteile
-----------------
- Tag / Page: Struktur für die Berichtsabschnitte (Tags) und die Seite.
- DataRetriever: Orchestrator, der je Tag die passende Retrieval-Funktion
  ausführt und die Resultate in `tag.value` (und optional `tag.intro`) schreibt.
"""


class Tag(BaseModel):

    """Ein einzelner Berichtsabschnitt (Tag) mit Ergebnissen."""

    id: str
    value: List[Dict]
    intro: Optional[str] = None

class Page(BaseModel):

    """Container für mehrere 'Tag'- Abschnitte der Klimaatlasberichte"""
    tags: List[Tag]

class DataRetriever(BaseModel): 

    """Asynchroner Orchestrator zum Befüllen der Berichtsabschnitte aus retrieval_functions.

    Dieser Retriever nimmt die Retrieval-Funktionen entgegen
    (`retrieval_functions`) und ruft pro `Tag` die passende Funktion auf.
    Ergebnisse werden in `tag.value / tag.intro (für die Einleitung)` gespeichert.
    """

    year: int
    time_unit: str
    report_schema: Page
    retrieval_functions: dict
    run_id: str
    report_pipe: str

    async def populate_tag(self, tag):

        """Füllt einen einzelnen `Tag` durch Aufruf der passenden Retrieval-Funktion.
        
        Args
        ---------------
        tag : Tag
                enthält Retrieval Funktion die den Berichtsgenerierungsprozess für den jeweiligen Berichtstyp startet.

        Returns
        -------
        Befüllt einen Tag für das `report_schema` mit Berichtabschnitten
        
        
        """
        
        retriever = self.retrieval_functions[tag.id]
        
        if retriever.__name__ == "get_report_introduction":
            result = await retriever(self.year, self.time_unit, self.report_schema, self.run_id, self.report_pipe)

            if isinstance(result, list):
                tag.value.append(result[0])
                tag.intro = result[1]
                return
        
        else:
            result = await retriever(self.year, self.time_unit, self.run_id, self.report_pipe)
                
        tag.value.append(result)
    
    @property
    def get_data(self): 

        """Serialisiert das gefüllte `report_schema (Page)` als dict für API

        Returns
        -------
        dict : Berichtsabschnitte jeweiligen Sprachmodelle in JSON-Format

        """

        
        return self.report_schema.model_dump(by_alias=True)
    

## Pydantic Basemodels für Datenvalidierung
    
class Data_report(BaseModel): 
    data: List[Dict]


class TimeSeriesDeviation(BaseModel):
    Jahr: int
    Abweichung: float
    Temperatur: float

class TimeSeriesEntry(BaseModel):
    values: List[TimeSeriesDeviation]
    ref: Dict[str, float]  

class TimeSeriesData(RootModel):
    root: Dict[int, TimeSeriesEntry]

