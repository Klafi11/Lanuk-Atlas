from langchain_core.prompts import ChatPromptTemplate

### Überschriften Template ###


heading_temp = ChatPromptTemplate.from_template(
    """
Als professioneller Überschriften Verfasser erstellt du eine passende Überschrift für einen Bericht der den Witterungsverlauf in NRW beschreibt.
Dabei ist es wichtig das du eine kurze prägnante Überschrift verfasst, welche den Witterungsverlauf im {year} und Zeitraum {time_unit} kurz, prägnant und bünding zusammenfasst.

<examples>
Hier sind einige Beispiele aus vorherigen Berichten: 
- Sehr sonnig und überwiegend trocken – der Mai 2025
- Sehr warm, aber mit unterschiedlichen Gesichtern – der April 2025
- Mild, vergleichsweise trocken und trüb – der Dezember 2024
- Trotz fulminantem Ende eher durchschnittlich – der Oktober 2024 
- Vom Altweibersommer zu herbstlicher Frische – der September 2024
- Eher durchschnittlich und daher gefühlt wenig sommerlich – der Juni 2024
- Von kalt zu warm – der Sommer 2024
- Platz 2 bei der Temperatur, Platz 3 beim Niederschlag – der Winter 2023/24 mischt ganz oben mit
</examples>

<important>
– gehe dabei nicht auf das Klima 
– Nutze nur Wörter wie "Rekord" wenn die Daten unter den Top 3 Ranglistenplätzen sind
– Nutze prägnante Adjektive wie in den Beispielen, die das Witterungsgeschehen wiedergeben
</important>

<task>Überlege dir eine handvoll passender Überschriften, die ähnlich aufgebaut sind wie die Überschriften aus den Beispielen (<examples>) und repräsentativ das Witterungsgeschehen im Bericht zur Zeiteinheit wiedergeben. </task>


Hier der gegebene Bericht für den du eine passende Überschrift generieren sollst:

{Bericht}
""")