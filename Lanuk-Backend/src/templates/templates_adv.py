from src.settings import get_settings
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from .template_data import *
from .template_struktur import *
from .template_important import *


"""
"Advanced"-Modus

Modul: LLM-Reporter-Prompts für Einleitung, Temperatur, Niederschlag, Sonnenscheindauer, Wetterstationsvergleich

Dieses Modul definiert:
- Rollen-, Ziel-, Richtlinien-, Hinweis- und Kontextbausteine für Wetterberichte.
- Kombinierte PromptTemplates für Monats-, Saison- und Jahresabsätze.
- Einen Handler (`template_handler_adv`), der abhängig von Variable (`absatz`)
  und Zeitbezug (`time_unit`) das richtige PromptTemplate zurückliefert.

Zweck:
Diese Prompts werden an ein LLM gegeben, um aus strukturierten Wetterdaten
und Kontexttexten fertige, stilistisch konsistente Berichtabsätze zu generieren.

Wichtige Konventionen:
- Platzhalter in geschweiften Klammern ({...}) müssen zur Laufzeit mit passenden
  Werten gefüllt werden.
- Die Tags in spitzen Klammern (<...> ... </...>) dienen nur der Strukturierung
  innerhalb des Prompt-Textes für das LLM.
"""

settings = get_settings()

#-----------------------------------------------------------------------------------------------------------------#
### LLM Reporter prompts ###

#-----------------------------------------------------------------------------------------------------------------#
### Role ###
template_role = """<role>Du bist ein Meteorologe für Nordrhein Westfalen.</role>"""

#-----------------------------------------------------------------------------------------------------------------#
### Guidelines ###

# Guidelines aller Prompts
template_guidelines = """
<guidelines>                                   
Achte dabei auf folgende Richtlinien:
- Verfasse einen Absatz, der detailliert, gründlich, tiefgehend und komplex ist, dabei jedoch Klarheit und Prägnanz wahrt.
- Integriere Hauptgedanken und wesentliche Informationen, entferne überflüssige Formulierungen und konzentriere dich auf die entscheidenden Aspekte.
- Stütze dich ausschließlich auf die bereitgestellten Informationen, Texte und Daten ohne externe Informationen einzubeziehen.
- Halte dabei eine strukturierte Absatzform bei, um ein leicht verständliches Leseerlebnis zu ermöglichen.
- Verwende einen sachlichen, informativen Schreibstil und halte die Länge bei etwa 100–150 Wörtern. 
- Schreibe nicht "die Zeitreihen Analyse zeigt" sondern z.B. mit einem Blick in die Zeitreihe (...) 
- Gib bei allen Vergleichen, Abweichungen und relativen Angaben den vollständigen Kontext an. Nenne immer explizit die Referenzperioden, Basisdaten oder Vergleichswerte. Vermeide vage Begriffe ohne klare zeitliche oder quantitative Bezugspunkte.
- Schreibe nur den Absatz, ohne Überschrift.
</guidelines>"""

#-----------------------------------------------------------------------------------------------------------------#
### Goal ### 

# Goal Temperatur
template_goal_temp = """
<goal>
Ziel: Erstelle einen informativen Absatz für einen Bericht, der die Entwicklung des Witterungsverlaufsparameter Temperatur über verschiedene Zeiträume hinweg aus den gegebenen Daten(<data>) und Informationen(<context>) für die gegebene Zeiteinheit beschreibt.
</goal>"""

# Goal Niederschlag 
template_goal_rain = """
<goal>
Ziel: Erstelle einen informativen Absatz für einen Bericht, der die Entwicklung des Witterungsverlaufsparameter Niederschlag über verschiedene Zeiträume hinweg aus den gegebenen Daten(<data>) und Informationen(<context>) für die gegebene Zeiteinheit beschreibt.
</goal>"""

# Goal Sonnenscheindauer 
template_goal_sun = """
<goal>
Ziel: Erstelle einen informativen Absatz für einen Bericht, der die Entwicklung des Witterungsverlaufsparameter Sonnenscheindauer über verschiedene Zeiträume hinweg aus den gegebenen Daten(<data>) und Informationen(<context>) für die gegebene Zeiteinheit beschreibt.
</goal>"""

#-----------------------------------------------------------------------------------------------------------------#

### Kontext der Berichte ###

#Template Kontext Temperatur
template_context_temp_month = """
<context>
Dir stehen im Abschnitt <reference_materials> folgende ergänzende Informationen zur Verfügung:

1. (<previous_months>) Stilistische und inhaltliche Absätze der vergangenen {time_unit}-Monate: 
Diese dienen dir als Vorlage für Stil, Aufbau, Wortwahl und inhaltliche Tiefe. Nutze sie, um deinen neuen Text kohärent, einheitlich und anschlussfähig zu gestalten. 
Du darfst Formulierungen, Strukturen oder inhaltliche Bezüge übernehmen, wenn sie sinnvoll passen.

2. (<timeseries_analytic>) Analytischer Absatz zu den aktuellen Temperaturdaten vom Referenzzeitraum 1961–1990:
Hier findest du Informationen zu:
- Abweichungen vom Mittelwert
- zusammenhängenden Perioden mit gleichen Abweichungen
- Extremwerten
- langfristiger Entwicklung der {time_unit}-Zeitreihe seit 1881

Nutze diese Informationen, um die aktuellen Daten in einen historischen Kontext einzuordnen. 
</context>
"""

#Template Kontext Niederschlag
template_context_rain_month = """
<context>
Dir stehen im Abschnitt <reference_materials> folgende ergänzende Informationen zur Verfügung:

1. (<previous_months>) Stilistische und inhaltliche Absätze der vergangenen {time_unit}-Monate: 
Diese dienen dir als Vorlage für Stil, Aufbau, Wortwahl und inhaltliche Tiefe. Nutze sie, um deinen neuen Text kohärent, einheitlich und anschlussfähig zu gestalten. 
Du darfst Formulierungen, Strukturen oder inhaltliche Bezüge übernehmen, wenn sie sinnvoll passen.

2. (<timeseries_analytic>) Analytischer Absatz zu den aktuellen Niederschlagsdaten vom Referenzzeitraum 1961–1990:
Hier findest du Informationen zu:
- Abweichungen vom Mittelwert
- zusammenhängenden Perioden mit gleichen Abweichungen
- Extremwerten
- langfristiger Entwicklung der {time_unit}-Zeitreihe seit 1881

Nutze diese Informationen, um die aktuellen Daten in einen historischen Kontext einzuordnen. 
</context>
"""
#Template Kontext Sonnenscheindauer
template_context_sun_month = """
<context>
Dir stehen im Abschnitt <reference_materials> folgende ergänzende Informationen zur Verfügung:

1. (<previous_months>) Stilistische und inhaltliche Absätze der vergangenen {time_unit}-Monate: 
Diese dienen dir als Vorlage für Stil, Aufbau, Wortwahl und inhaltliche Tiefe. Nutze sie, um deinen neuen Text kohärent, einheitlich und anschlussfähig zu gestalten. 
Du darfst Formulierungen, Strukturen oder inhaltliche Bezüge übernehmen, wenn sie sinnvoll passen.

2. (<timeseries_analytic>) Analytischer Absatz zu den aktuellen Sonnenscheindauerdaten vom Referenzzeitraum 1961–1990:
Hier findest du Informationen zu:
- Abweichungen vom Mittelwert
- zusammenhängenden Perioden mit gleichen Abweichungen
- Extremwerten
- langfristiger Entwicklung der {time_unit}-Zeitreihe seit 1881
Nutze diese Informationen, um die aktuellen Daten in einen historischen Kontext einzuordnen. 
</context>
"""

#Quartal
#---------------------------------------------------------------#
template_context_temp_quarter = """
<context>
Dir stehen im Abschnitt <reference_materials> folgende ergänzende Informationen zur Verfügung:

1. (<previous_seasons>) Stilistische und inhaltliche Absätze der vergangenen {time_unit}-Saisons: 
Diese dienen dir als Vorlage für Stil, Aufbau, Wortwahl und inhaltliche Tiefe. Nutze sie, um deinen neuen Text kohärent, einheitlich und anschlussfähig zu gestalten. 
Du darfst Formulierungen, Strukturen oder inhaltliche Bezüge übernehmen, wenn sie sinnvoll passen.

2. (<current_months>) Absätze der aktuellen Monate der laufenden {time_unit}-Saison:  
Diese enthalten relevante Informationen zu den aktuellen Monaten des {time_unit}. Greife bei Bedarf auf diese Inhalte zurück und integriere sie korrekt und sinnvoll in deinen neuen Absatz, um aktuelle Entwicklungen abzubilden.

3. (<timeseries_analytic>) Analytischer Absatz zu den aktuellen Temperaturdaten vom Referenzzeitraum 1961–1990:
Hier findest du Informationen zu:
- Abweichungen vom Mittelwert
- zusammenhängenden Perioden mit gleichen Abweichungen
- Extremwerten
- langfristiger Entwicklung der {time_unit}-Zeitreihe seit 1881

Nutze diese Informationen, um die aktuellen Daten in einen historischen Kontext einzuordnen. 
Verfasse auf Basis dieser Kontexte einen neuen, eigenständigen, klar formulierten Absatz für die aktuelle Saison, der sich stilistisch und inhaltlich nahtlos in die bestehende Reihe einfügt. 
</context>
"""

template_context_rain_quarter = """
<context>
Dir stehen im Abschnitt <reference_materials> folgende ergänzende Informationen zur Verfügung:

1. (<previous_seasons>) Stilistische und inhaltliche Absätze der vergangenen {time_unit}-Saisons: 
Diese dienen dir als Vorlage für Stil, Aufbau, Wortwahl und inhaltliche Tiefe. Nutze sie, um deinen neuen Text kohärent, einheitlich und anschlussfähig zu gestalten. 
Du darfst Formulierungen, Strukturen oder inhaltliche Bezüge übernehmen, wenn sie sinnvoll passen.

2. (<current_months>) Absätze der aktuellen Monate der laufenden {time_unit}-Saison:  
Diese enthalten relevante Informationen zu den aktuellen Monaten des {time_unit}. Greife bei Bedarf auf diese Inhalte zurück und integriere sie korrekt und sinnvoll in deinen neuen Absatz, um aktuelle Entwicklungen abzubilden.

3. (<timeseries_analytic>) Analytischer Absatz zu den aktuellen Niederschlagsdaten vom Referenzzeitraum 1961–1990:
Hier findest du Informationen zu:
- Abweichungen vom Mittelwert
- zusammenhängenden Perioden mit gleichen Abweichungen
- Extremwerten
- langfristiger Entwicklung der {time_unit}-Zeitreihe seit 1881

Nutze diese Informationen, um die aktuellen Daten in einen historischen Kontext einzuordnen. 
</context>
"""

template_context_sun_quarter = """
<context>
Dir stehen im Abschnitt <reference_materials> folgende ergänzende Informationen zur Verfügung:

1. (<previous_seasons>) Stilistische und inhaltliche Absätze der vergangenen {time_unit}-Saisons: 
Diese dienen dir als Vorlage für Stil, Aufbau, Wortwahl und inhaltliche Tiefe. Nutze sie, um deinen neuen Text kohärent, einheitlich und anschlussfähig zu gestalten. 
Du darfst Formulierungen, Strukturen oder inhaltliche Bezüge übernehmen, wenn sie sinnvoll passen.

2. (<current_months>) Absätze der aktuellen Monate der laufenden {time_unit}-Saison:  
Diese enthalten relevante Informationen zu den aktuellen Monaten des {time_unit}. Greife bei Bedarf auf diese Inhalte zurück und integriere sie korrekt und sinnvoll in deinen neuen Absatz, um aktuelle Entwicklungen abzubilden.

3. (<timeseries_analytic>) Analytischer Absatz zu den aktuellen Sonnenscheindauerdaten vom Referenzzeitraum 1961–1990:
Hier findest du Informationen zu:
- Abweichungen vom Mittelwert
- zusammenhängenden Perioden mit gleichen Abweichungen
- Extremwerten
- langfristiger Entwicklung der {time_unit}-Zeitreihe seit 1881

Nutze diese Informationen, um die aktuellen Daten in einen historischen Kontext einzuordnen. 
</context>
"""

#Jahr
#---------------------------------------------------------------#

template_context_temp_year = """
<context>
Dir stehen im Abschnitt <reference_materials> folgende ergänzende Informationen zur Verfügung:

1. (<previous_years>) Stilistische und inhaltliche Absätze der vergangenen Jahre: 
Diese dienen dir als Vorlage für Stil, Aufbau, Wortwahl und inhaltliche Tiefe. Nutze sie, um deinen neuen Text kohärent, einheitlich und anschlussfähig zu gestalten. 
Du darfst Formulierungen, Strukturen oder inhaltliche Bezüge übernehmen, wenn sie sinnvoll passen.

2. (<current_months>) Absätze der aktuellen Monate des laufenden Jahres:  
Diese enthalten relevante Informationen zu den aktuellen Monaten des Jahres. Greife bei Bedarf auf diese Inhalte zurück und integriere sie korrekt und sinnvoll in deinen neuen Absatz, um aktuelle Entwicklungen abzubilden.

3. (<timeseries_analytic>) Analytischer Absatz zu den aktuellen Temperaturdaten vom Referenzzeitraum 1961–1990:
Hier findest du Informationen zu:
- Abweichungen vom Mittelwert
- zusammenhängenden Perioden mit gleichen Abweichungen
- Extremwerten
- langfristiger Entwicklung der {time_unit}-Zeitreihe seit 1881

Nutze diese Informationen, um die aktuellen Daten in einen historischen Kontext einzuordnen. 
</context>
"""

template_context_rain_year = """
<context>
Dir stehen im Abschnitt <reference_materials> folgende ergänzende Informationen zur Verfügung:

1. (<previous_years>) Stilistische und inhaltliche Absätze der vergangenen Jahre: 
Diese dienen dir als Vorlage für Stil, Aufbau, Wortwahl und inhaltliche Tiefe. Nutze sie, um deinen neuen Text kohärent, einheitlich und anschlussfähig zu gestalten. 
Du darfst Formulierungen, Strukturen oder inhaltliche Bezüge übernehmen, wenn sie sinnvoll passen.

2. (<current_months>) Absätze der aktuellen Monate des laufenden Jahres:  
Diese enthalten relevante Informationen zu den aktuellen Monaten des Jahres. Greife bei Bedarf auf diese Inhalte zurück und integriere sie korrekt und sinnvoll in deinen neuen Absatz, um aktuelle Entwicklungen abzubilden.

3. (<timeseries_analytic>) Analytischer Absatz zu den aktuellen Niederschlagsdaten vom Referenzzeitraum 1961–1990:
Hier findest du Informationen zu:
- Abweichungen vom Mittelwert
- zusammenhängenden Perioden mit gleichen Abweichungen
- Extremwerten
- langfristiger Entwicklung der {time_unit}-Zeitreihe seit 1881

Nutze diese Informationen, um die aktuellen Daten in einen historischen Kontext einzuordnen. 
</context>
"""

template_context_sun_year = """
<context>
Dir stehen im Abschnitt <reference_materials> folgende ergänzende Informationen zur Verfügung:

1. (<previous_years>) Stilistische und inhaltliche Absätze der vergangenen Jahre: 
Diese dienen dir als Vorlage für Stil, Aufbau, Wortwahl und inhaltliche Tiefe. Nutze sie, um deinen neuen Text kohärent, einheitlich und anschlussfähig zu gestalten. 
Du darfst Formulierungen, Strukturen oder inhaltliche Bezüge übernehmen, wenn sie sinnvoll passen.

2. (<current_months>) Absätze der aktuellen Monate des laufenden Jahres:  
Diese enthalten relevante Informationen zu den aktuellen Monaten des Jahres. Greife bei Bedarf auf diese Inhalte zurück und integriere sie korrekt und sinnvoll in deinen neuen Absatz, um aktuelle Entwicklungen abzubilden.

3. (<timeseries_analytic>) Analytischer Absatz zu den aktuellen Sonnenscheindauerdaten vom Referenzzeitraum 1961–1990:
Hier findest du Informationen zu:
- Abweichungen vom Mittelwert
- zusammenhängenden Perioden mit gleichen Abweichungen
- Extremwerten
- langfristiger Entwicklung der {time_unit}-Zeitreihe seit 1881

Nutze diese Informationen, um die aktuellen Daten in einen historischen Kontext einzuordnen. 
</context>"""
#-----------------------------------------------------------------------------------------------------------------#
### Referenz Material ###

# Referenzmaterial Monat
template_reference_materials_month = """
<reference_materials>
<previous_months>
1. Absätze der vorangegangenen {time_unit} Monate:
{vora_time_unit}
</previous_months>

<timeseries_analytic>                        
2. Hiermit erhälst du weitere Informationen über die Zeitreihe:                                      
{anal_time_unit}
</timeseries_analytic>
</reference_materials>"""

# Referenzmaterial Quartal
template_reference_materials_quarter = """
<reference_materials>
<previous_seasons>
1. Absätze der vorangegangenen {time_unit}-Saison:                                   
{vora_time_unit}
</previous_seasons>

<current_months>
2. Aktuelle Monate der laufenden {time_unit}-Saison:                                        
{aktuelle_time_unit}
</current_months>

<timeseries_analytic>
3. Hiermit erhälst du weitere Informationen über die Zeitreihe:                             
{anal_time_unit}
</timeseries_analytic>
</reference_materials>
"""

# Referenzmaterial Jahr 

template_reference_materials_year = """
<reference_materials>
<previous_years>
1. Absätze der vorangegangenen Jahre:                                 
{vora_time_unit}
</previous_years>

<current_months>
2. Aktuelle Monate des laufenden Jahres:                                      
{aktuelle_time_unit}
</current_months>

<timeseries_analytic>
3. Hiermit erhälst du weitere Informationen über die Zeitreihe:   
{anal_time_unit}
</timeseries_analytic>
</reference_materials>
"""

#-----------------------------------------------------------------------------------------------------------------#
### Output Task ###

template_output_task= """<output_task>Verfasse auf Basis aller gegebenen Informationen, Daten und Kontexte einen neuen, eigenständigen, klar formulierten Absatz für die aktuell gegebene Zeiteinheit {time_unit} {year}, der sich stilistisch und inhaltlich nahtlos in die bestehende Reihe der Witterungsverlaufsberichte einfügt: </output_task> """

#-----------------------------------------------------------------------------------------------------------------#

### DWD-Wetterbericht ###

summarize_prompt_wetter = ChatPromptTemplate.from_template(""" 
<role>Als professioneller Zusammenfasser erstelle eine prägnante und zugleich umfassende Zusammenfassung des bereitgestellten Informationen aus den Tages Wetterberichten des DWD.</role>

<goal>Dein Hauptziel ist: Den Witterungsverlauf in dem gegeben {year} und Zeitraum {time_unit} aus dem gegebenen Inhalt im <context> Abschnitt wiederzugeben. 
Achte dabei verstärkt auf extreme Wetterereignisse: wie Gewitter, Stürme, Überlflutungen, Dürre, Brände, Starkniederschlag, Schneefall, Glätte usw. und benne die Zeiträume sowie Orte exakt.</goal>
                                                           
<important>
– Dabei ist es wichtig das du die Informationen kurz und prägnant bündelst, welche mit dem gegeben {year} und Zeitraum {time_unit} eng in Verbindung stehen.
– Wichtig dabei ist, dass die Zusammenfassung den Wetterverlauf von Anfang der Zeiteinheit bis Ende der Zeiteinheit strukturiert, klar und logisch wiedergibt.
</important>

<guidelines>                                                         
Dies soll unter Einhaltung der folgenden Richtlinien geschehen:
- Verfasse eine Zusammenfassung, die detailliert, gründlich, tiefgehend und komplex ist, dabei jedoch Klarheit und Prägnanz wahrt.
- Integriere Hauptgedanken und wesentliche Informationen, entferne überflüssige Formulierungen und konzentriere dich auf die entscheidenden Aspekte.
- Stütze dich ausschließlich auf den bereitgestellten Text, ohne externe Informationen einzubeziehen.                                                      
- Formatiere die Zusammenfassung in Absatzform, um ein leicht verständliches Leseerlebnis zu ermöglichen.                                         
- Halte dich bei der Zusammenfassung bei einer Länge von 150-200 Wörter  
- Sollten bestimmte Wettererignisse nicht im <context> enthalten sein, nenne diese nicht.     
- Durch die Befolgung dieses optimierten Prompts entsteht eine wirkungsvolle Zusammenfassung, die das Wesentliche der gegebenen Texte in <context> klar, prägnant und leserfreundlich wiedergibt.                                                                               
</guidelines>


<context>
Hiermit erählst du den zu zusammenfassenden Inhalt: 
{inhalt}
</context>                                                        

""")

#-----------------------------------------------------------------------------------------------------------------#

### Einleitungsabsatz ###


chain_intro = ChatPromptTemplate.from_template(""" <role>Du bist Meteorologe für den Witterungsverlauf in Nordrhein Westfalen. </role>

<goal> Ziel: Erstelle Einleitungsabsatz, die den Witterungsverlauf in Nordrhein-Westfalen im Ganzen beschreiben, fasse dabei alle wichtigen Erkenntnisse der bereitgestellten Informationen kurz und markant für die Einleitung zusammen. </goal>

<guidelines>
Dies soll unter Einhaltung der folgenden Richtlinien geschehen:
- Verfasse eine Einleitung, die detailliert, gründlich, tiefgehend und komplex ist, dabei jedoch Klarheit und Prägnanz wahrt.
- Integriere Hauptgedanken und wesentliche Informationen, entferne überflüssige Formulierungen und konzentriere dich auf die entscheidenden Aspekte.
- Stütze dich ausschließlich auf die bereitgestellten Informationen in <reference_materials>, ohne externe Informationen einzubeziehen.                                                    
- Formatiere die Einleitung in Absatzform, um ein leicht verständliches Leseerlebnis zu ermöglichen.                                       
- Halte dich bei der Einleitung bei einer Länge von 150-200 Wörter
- Spreche nicht von Trend sondern von Abweichungen 
- Füge keine Überschrift der Einleitung hinzu, schreibe nur den Absatz
- Durch die Befolgung dieses optimierten Prompts entsteht eine wirkungsvolle Einleitung, die das Wesentliche der gegeben Informationen klar, prägnant und leserfreundlich wiedergibt.                               
</guidelines>   
                                                 
<important>
- Gebe Keine Interpretationen über das Klima oder Klimageschehen ab 
- Implementiere keine Interpretationen des Stationsvergleich von WAST und VKTU in Einleitung                                                    
</important>
                                               
<context>
Dir stehen weitere folgende Informationen im <reference_materials> Abschnitt zur Verfügung:
1.(<previous_intro>) Einleitungsabsätze der vorangegangenen Zeiteinheiten: Diese dienen dir als Vorlage für Stil, Aufbau, Wortwahl und inhaltliche Tiefe. Nutze sie, um deinen neuen Einleitungsabsatz kohärent und einheitlich zu gestalten. 
2.(<currrent_report>) Die Absätze des Berichts für den du die Einleitung schreiben sollst: Die Absätze unterteilen sich in Temperatur, Niederschlag, Sonnenscheindauer und ein Wetterstationsvergleich.
3.(<current_weather>) Ein kurzer Absatz zur aktuellen Wetterlage in NRW zum aktuellen Monat {time_unit}: Dieser dient dir als zusätzliche Informationsquelle über die Wetterlage in der gebenen Zeiteinheit für Nordrhein Westfalen. Beziehe diese Information bei Bedarf in deinen Absatz mit ein und benenne Wetterereginisszeiträume exakt.
</context>
                                               
<rerference_materials>
Hiermit erhälst du folgende Informationen:
<previous_intro>                                    
1. Einleitungsabsätze der vorangegangenen Zeiteinheiten:
{vora_time_unit}
</previous_intro>                                               

<current_report>                                               
2. Die Absätze des Berichts für den du die Einleitung schreiben sollst:                                              
{report}
</current_report>

<current_weather>
3. Absatz zur aktuellen Wetterlage in der gegeben Zeiteinheit: {time_unit} {year}:                                      
{aktuelle_wetterlage}
</current_weather>
</reference_material>
                                               
<output_task>Verfasse nun auf dieser Grundlage einen neuen, stilistisch passenden Einleitungsabsatz für {time_unit} {year}:</output_task> 
""")

#-----------------------------------------------------------------------------------------------------------------#
### Template Monat ###

#Template Temperatur Monat
template_adv_temp_month =f"""
    {template_role}
    {template_goal_temp}
    {data_temp_month}
    {template_guidelines}
    {template_important_temp}
    {template_aufbau_temp}
    {template_context_temp_month}
    {template_reference_materials_month}
    {template_output_task}
    """
#Template Niederschlag Monat
template_adv_rain_month = f"""
    {template_role}
    {template_goal_rain}
    {data_rain_month}
    {template_guidelines}
    {template_important_rain}
    {template_aufbau_rain}
    {template_context_rain_month}
    {template_reference_materials_month}
    {template_output_task}
    """
# Template Sonnenscheindauer Monat
template_adv_sun_month = f"""
    {template_role}
    {template_goal_sun}
    {data_sun_month}
    {template_guidelines}
    {template_important_sun}
    {template_aufbau_sun}
    {template_context_sun_month}
    {template_reference_materials_month}
    {template_output_task}
"""

template_adv_temp = PromptTemplate.from_template(template_adv_temp_month)
template_adv_rain = PromptTemplate.from_template(template_adv_rain_month)
template_adv_sun = PromptTemplate.from_template(template_adv_sun_month)

#-----------------------------------------------------------------------------------------------------------------#
### Template Quartal ###

# Template Temperatur Quartal
template_adv_temp_saison = f"""
{template_role}
{template_goal_temp}
{data_temp_season}
{template_guidelines}
{template_important_temp}
{template_aufbau_temp_season}
{template_context_temp_quarter}
{template_reference_materials_quarter}
{template_output_task}
"""

# Template Niederschlag Quartal
template_adv_rain_saison = f"""
{template_role}
{template_goal_rain}
{data_rain_season}
{template_guidelines}
{template_important_rain}
{template_aufbau_rain_season}
{template_context_rain_quarter}
{template_reference_materials_quarter}
{template_output_task}
"""

# Template Sonnenscheindauer Quartal

template_adv_sun_saison = f"""
{template_role}
{template_goal_sun}
{data_sun_season}
{template_guidelines}
{template_important_sun}
{template_aufbau_sun_season}
{template_context_sun_quarter}
{template_reference_materials_quarter}
{template_output_task}
"""

template_adv_temp_quarter = PromptTemplate.from_template(template_adv_temp_saison)
template_adv_rain_quarter = PromptTemplate.from_template(template_adv_rain_saison)
template_adv_sun_quarter = PromptTemplate.from_template(template_adv_sun_saison)

#-----------------------------------------------------------------------------------------------------------------#
### Template Jahr ###

_template_adv_temp_year = f"""
{template_role}
{template_goal_temp}
{data_temp_year}
{template_guidelines}
{template_important_temp}
{template_aufbau_temp_year}
{template_context_temp_year}
{template_reference_materials_year}
{template_output_task}
"""

_template_adv_rain_year = f"""
{template_role}
{template_goal_rain}
{data_rain_year}
{template_guidelines}
{template_important_rain}
{template_aufbau_rain_year}
{template_context_rain_year}
{template_reference_materials_year}
{template_output_task}
"""

_template_adv_sun_year = f"""
{template_role}
{template_goal_sun}
{data_sun_year}
{template_guidelines}
{template_important_sun}
{template_aufbau_sun_year}
{template_context_sun_year}
{template_reference_materials_year}
{template_output_task}
"""

template_adv_temp_year = PromptTemplate.from_template(_template_adv_temp_year)
template_adv_rain_year = PromptTemplate.from_template(_template_adv_rain_year)
template_adv_sun_year = PromptTemplate.from_template(_template_adv_sun_year)

#-----------------------------------------------------------------------------------------------------------------#
### Template handler ###

def template_handler_adv(absatz, time_unit):

    if time_unit in settings.months:

        match absatz:
            case "temp":
               return template_adv_temp
            case "rain":
               return template_adv_rain
            case "sun":
               return template_adv_sun
    
    if time_unit in settings.seasons:

        match absatz: 

            case "temp": 
                return template_adv_temp_quarter

            case "rain":
                return template_adv_rain_quarter

            case "sun": 
                return template_adv_sun_quarter
    
    if time_unit in settings.year:

        match absatz:

            case "temp":
                return template_adv_temp_year
            case "rain": 
                return template_adv_rain_year
            case "sun": 
                return template_adv_sun_year

