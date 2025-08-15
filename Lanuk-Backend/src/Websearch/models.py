from pydantic import BaseModel, Field
from typing import List

""" Pydantic Base Models für die Websuche """

class RelatedSubjects(BaseModel):
    topics: List[str] = Field(
        description= "Umfassende Liste relevanter such Queries für Tavily Search über Wetterereignisse in NRW in der gegeben Zeiteinheit, Jahr und Bundesland"
    )

class structuredSum(BaseModel):
    summarization: str = Field(
        description="Zusammenfassung mit nummerierten Fußnoten in eckigen Klammern (z.B. [1], [2]) direkt im Text, sobald du die Quelle verwendest"
    )
    citations: List[str] = Field(
        description= "Liste der Quellen (Url) der passenden Fußnoten im Text, vemeide Duplikate in den Fußnoten"
    )
