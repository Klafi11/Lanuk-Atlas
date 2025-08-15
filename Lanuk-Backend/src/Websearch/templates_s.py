from langchain_core.prompts import ChatPromptTemplate

### Template für die Suchqueries ### 
related_topics_prompt = ChatPromptTemplate.from_template(
"""

<task> Generiere hervorragende Suchqueries für TavilySearch die nach markanten Wetterereignissen suchen sollen, die zu diesem gegegeben Bericht <bericht> passen: </task>

<bericht>
Hier der gegebene Bericht: 
{bericht}
</bericht>

<rahmenbedingungen>
Dabei erstellt du die Suchqueries unter diesen gegebenen Rahmenbediungen:  Zeiteinheit: {time_unit},  Jahr: {year} und Bundesland: Nordrhein-Westfalen
</rahmenbedingungen>

<wichtig>
Suche nicht nach Klimatologischen Folgen, sondern bleibe nur bei Wetterereignissen in der gegeben Zeiteinheit, Jahr und Bundesland. Suche dabei nicht nach gleichen oder ähnlichen Suchanfragen, halte die Suchanfragen heterogen.
</wichtig>

<beispiele>
Beispiele für Wettereignisse könnten sein:

- Überflutungen / Überschwemmungen
- Starkregenerignisse 
- Stürme 
- Orkane
- Waldbrände
- Bodenfeuchte
- Dürre / Trockenheit
-Wasserstände
- (...)
</beispiele>

"""
)

### Template Finale Zusammenfassung ###

summarize_prompt_f = ChatPromptTemplate.from_template(""" 
<role> Als professioneller Zusammenfasser erstelle eine prägnante und zugleich umfassende Zusammenfassung des bereitgestellten Informationen – sei es ein Artikel, ein Beitrag, ein Gespräch oder ein Textausschnitt. </role>

Dabei ist es wichtig das du die Informationen kurz und prägnant bündelst, welche mit dem gegeben {year} und Zeitraum {time_unit} eng in Verbindung stehen. 

<ziel> Dein Hauptziel ist markante Informationen zu Wettereignissen wie Schneefall, Überflutungen, Brände, Stürme, Dürren, Bodenfeuchte, Wasserstände und Pflanzenvegetationen etc. aus dem <reference_materials> zusammenzufassen, die den Witterungsverlaufs in Nordrhein-Westfalen beschreiben. </ziel>

<guidelines>
Dies soll unter Einhaltung der folgenden Richtlinien geschehen:                                            

- Verfasse eine Zusammenfassung, die detailliert, gründlich, tiefgehend und komplex ist, dabei jedoch Klarheit und Prägnanz wahrt.
- Integriere Hauptgedanken und wesentliche Informationen, entferne überflüssige Formulierungen und konzentriere dich auf die entscheidenden Aspekte.
- Stütze dich ausschließlich auf den bereitgestellten Text, ohne externe Informationen einzubeziehen.
- Formatiere die Zusammenfassung in Absatzform, um ein leicht verständliches Leseerlebnis zu ermöglichen.                                       
- Halte die Zusammenfassung bei einer Länge von 50-100 Wörter                             
</guidelines> 

Durch die Befolgung dieser optimierten Prompt entsteht so eine wirkungsvolle Zusammenfassung für dein verfolgtes <ziel>, die das Wesentliche des dir zu Verfügung gestellten Inhalts klar, prägnant und leserfreundlich wiedergibt.
       
<reference_materials>
Hiermit erählst du den zu zusammenfassenden Inhalt:                                                   
{inhalt}
</reference_materials>
""")

### Template für den ersten Filter ### 
summarize_prompt = ChatPromptTemplate.from_template(""" 
                                                    
<role> Als professioneller Zusammenfasser erstelle eine prägnante und zugleich umfassende Zusammenfassung des bereitgestellten Informationen – sei es ein Artikel, ein Beitrag, ein Gespräch oder ein Textausschnitt. </role>

Dabei ist es wichtig das du die Informationen kurz und prägnant bündelst, welche mit dem gegeben {year} und Zeitraum {time_unit} eng in Verbindung stehen. 

<ziel> Dein Ziel ist markante Informationen zu Wettereignissen wie zum Beispiel: 
- Schneefall, 
- Starkniederschlag, 
- Überflutungen, 
- Brände, Stürme, 
- Dürren, etc. oder 
- Bodenfeuchte,
- Wasserstände 
- Pflanzenvegetationen
- (...)                                                    

aus den Inhalt von <reference_materials> zusammenzutragen, um daraus eine detaillierte Zusammenfassung zu erstellen, die den Witterungsverlaufs in Nordrhein-Westfalen zur gegebenen Zeiteinheit und Jahr beschreibt. 
</ziel>

<guidelines>
Dies soll unter Einhaltung der folgenden Richtlinien geschehen:
- Verfasse eine Zusammenfassung, die detailliert, gründlich, tiefgehend und komplex ist, dabei jedoch Klarheit und Prägnanz wahrt.
- Integriere Hauptgedanken und wesentliche Informationen, entferne überflüssige Formulierungen und konzentriere dich auf die entscheidenden Aspekte.
- Stütze dich ausschließlich auf den bereitgestellten Text, ohne externe Informationen einzubeziehen.
- Formatiere die Zusammenfassung in Absatzform, um ein leicht verständliches Leseerlebnis zu ermöglichen.   
- Halte dich bei der Zusammenfassung bei einer Länge von 150-200 Wörter                             
</guidelines>
                                        
<wichtig>
 - Wichtig: Du musst jede Quelle die du im Text nennst und ausführst mit einer Fußnote an der gegeben Stelle im Text versehen. Gebe dabei die Fußnoten im Text an mit [Nummer der Fußnote] bsp. [1] die auf die Quelle hinweist.   
</wichtig>                                                                                                    

Durch die Befolgung dieser optimierten Prompt entsteht eine wirkungsvolle Zusammenfassung, die das Wesentliche des zu Verfügung gestellten Inhalts bezogen auf das <Ziel> klar, prägnant und leserfreundlich wiedergibt.

<reference_materials>
Hiermit erählst du den zu zusammenfassenden Inhalt: 
{inhalt}

</reference_materials>                                        
""")