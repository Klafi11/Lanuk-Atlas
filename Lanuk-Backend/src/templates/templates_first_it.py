
from src.settings import get_settings

"""
Templates erste Projektphase 

Modul: LLM-Reporter-Prompts für Einleitung, Temperatur, Niederschlag, Sonnenscheindauer, Wetterstationsvergleich

Dieses Modul definiert:
- Verschiedene PromptTemplates für die jeweilig definierten ICL-Methoden.
- PromptTemplates für Monats-, Saison- und Jahresabsätze.

Zweck:
Diese Prompts werden an ein LLM gegeben, um aus strukturierten Wetterdaten
und Kontexttexten fertige, stilistisch konsistente Berichtabsätze zu generieren.

Wichtige Konventionen:
- Platzhalter in geschweiften Klammern ({...}) müssen zur Laufzeit mit passenden
  Werten gefüllt werden.
"""

settings = get_settings()

# Template Temperaturen ----------------------------------------------------------------------------------------------------------------------------------

template_temp = """ 
Du bist ein Meteorologe für Nordrhein Westfalen.
Erstelle einen informativen Absatz für einen Bericht, der die Entwicklung des Klimaparameters Temperatur, über verschiedene Zeiträume hinweg beschreibt. Beginne mit der aktuellen Situation und vergleiche sie mit früheren Referenzperioden. 
Erwähne, wie sich der aktuelle Wert im Vergleich zu historischen Daten verhält und ob er über oder unter dem Durchschnitt liegt. 
Gib an, wie sich der Parameter im Laufe der Zeit verändert hat und füge eine Tabelle ein, die diese Entwicklung veranschaulicht. Achte darauf, die relevanten Zeiträume und die entsprechenden Werte sowie das Ranking klar und präzise darzustellen.

Hier die gegebenen Daten: 

- Berichtszeitraum aktuelles Jahr: {year} 
- Berichtszeitraum aktuelle Zeiteinheit: {time_unit} (Sofern Jahr_agg gebe nur das entsprechende Jahr wieder)
- Einordnung des Berichtszeitraums in das Ranking: {ranking_temp}
- Durchschnittliche Temperatur des Berichtszeitraums der aktuellen Zeiteinheit: {m_temp} °C
- Durchschnittliche Temperatur der Klimanormalperiode in den Jahren 1881-1910: {m_temp_80_10} °C
- Durchschnittliche Temperatur der Klimanormalperiode in den Jahren 1961-1990: {m_temp_60_90} °C
- Durchschnittliche Temperatur der Klimanormalperiode in den jahren 1991-2020: {m_temp_90_20} °C """

template_temp_zero_shot = """Du bist ein Meteorologe für Nordrhein Westfalen.
Erstelle einen informativen Absatz für einen Bericht, der die Entwicklung des Klimaparameters Temperatur über verschiedene Zeiträume hinweg aus den gegebenen Daten beschreibt.
Hier die gegebenen Daten: 

- Berichtszeitraum aktuelles Jahr: {year}
- Berichtszeitraum aktuelle Zeiteinheit: {time_unit} (Sofern Jahr_agg gebe nur das entsprechende Jahr wieder)
- Einordnung des Berichtszeitraums in das Ranking: {ranking_temp}
- Durchschnittliche Temperatur des Berichtszeitraums der aktuellen Zeiteinheit: {m_temp} °C
- Durchschnittliche Temperatur der Klimanormalperiode in den Jahren 1881-1910: {m_temp_80_10} °C
- Durchschnittliche Temperatur der Klimanormalperiode in den Jahren 1961-1990: {m_temp_60_90} °C
- Durchschnittliche Temperatur der Klimanormalperiode in den jahren 1991-2020: {m_temp_90_20} °C

Verwende einen sachlichen, informativen Schreibstil und halte die Länge bei etwa 100–150 Wörtern. Achte darauf, dass der Text flüssig und gut strukturiert ist. Schreibe nur den Absatz, ohne Überschrift.
 """

template_temp_CoT = """Du bist ein Meteorologe für Nordrhein Westfalen.
Erstelle einen informativen Absatz für einen Bericht, der die Entwicklung des Klimaparameters Temperatur, über verschiedene Zeiträume hinweg beschreibt.
Denke Schritt für Schritt und gehe dabei auf folgende Punkte ein:

Schritt 1: Analysiere die aktuellen Daten:

- Nenne das Berichtsjahr ({year}) und die Zeiteinheit ({time_unit}, Sofern Jahr_agg gebe nur das entsprechende Jahr wieder).

- Gib die aktuelle Durchschnittstemperatur ({m_temp} °C) an.

- Vergleiche diesen Wert mit den drei Klimanormalperioden (1881–1910, 1961–1990, 1991–2020) und berechne die Abweichung.
    - Daten:
    - Durchschnittliche Temperatur der Klimanormalperiode in den Jahren 1881-1910: {m_temp_80_10} °C
    - Durchschnittliche Temperatur der Klimanormalperiode in den Jahren 1961-1990: {m_temp_60_90} °C
    - Durchschnittliche Temperatur der Klimanormalperiode in den jahren 1991-2020: {m_temp_90_20} °C


Schritt 2: Kontextualisiere die Daten:

- Erkläre, dass der aktuelle Zeitraum den {ranking_temp}. Platz im historischen Ranking einnimmt.

- Beschreibe, ob die Temperatur über/unter dem langjährigen Durchschnitt liegt.


Schritt 3: Zeige den Langzeittrend:

- Analysiere und beschreibe die Temperaturveränderungen zwischen den Perioden und dem aktuellen Wert.

Schritt 4: Fasse die Erkenntnisse zusammen

Schritt 5: Umschreibe und verbessere den Berichtabsatz kontinuierlich

Verwende einen sachlichen, informativen Schreibstil und halte die Länge bei etwa 100–150 Wörtern. Achte darauf, dass der Text flüssig und gut strukturiert ist. Schreibe nur den Absatz, ohne Überschrift.
    
"""

template_temp_few_shot = """Du bist ein Meteorologe für Nordrhein Westfalen.
Erstelle einen informativen Absatz für einen Bericht, der die Entwicklung des Witterungsverlaufsparameter Temperatur über verschiedene Zeiträume hinweg aus den gegebenen Daten beschreibt.
Hier die gegebenen Daten: 

- Berichtszeitraum aktuelles Jahr: {year}
- Berichtszeitraum aktuelle Zeiteinheit: {time_unit} (Sofern Jahr_agg gebe nur das entsprechende Jahr wieder)
- Aktueller Ranglistenplatz für die höchste durchschnittliche Temperatur der Zeiteinheit, des Witterungsverlaufsparameter (Aufzeichnungszeitraum: 1881 bis heute): {ranking_temp}
- Durchschnittliche Temperatur des Berichtszeitraums der aktuellen Zeiteinheit: {m_temp} °C
- Durchschnittliche Temperatur der Klimanormalperiode in den Jahren 1881-1910: {m_temp_80_10} °C
- Durchschnittliche Temperatur der Klimanormalperiode in den Jahren 1961-1990: {m_temp_60_90} °C
- Durchschnittliche Temperatur der Klimanormalperiode in den jahren 1991-2020: {m_temp_90_20} °C


Verwende einen sachlichen, informativen Schreibstil und halte die Länge bei etwa 100–150 Wörtern. Achte darauf, dass der Text flüssig und gut strukturiert ist. 
Gebe dabei keine Prognose über das Klima ab, sondern bleibe bei den Daten die Du hast, du gibst nur beschreibend den Witterungsverlauf der gegebenen Zeiteinheit wieder.
Schreibe nur den Absatz, ohne Überschrift.

Hier einige gegebene Beispiele:

Der Februar 2025 fiel mit einer durchschnittlichen Temperatur von 3,0 °C zwar deutlich kühler aus als im Vorjahr, lag aber bereits zum siebten Jahr in Folge über dem Mittelwert der Referenzperiode 1961-1990 (Abweichung: +1,2 K) sowie, 
wenn auch nur knapp, über dem der aktuellen Klimanormalperiode 1991-2020 (Abweichung: +0,2 K). Somit landete der diesjährige Februar lediglich im oberen Mittelfeld der beobachteten Zeitreihe seit Messbeginn 1881.

---

Mit einer Durchschnittstemperatur von 6,1 °C lag der diesjährige November, wenn auch nur minimal, bereits im achten Jahr in Folge über dem Durchschnitt der aktuellen Klimanormalperiode 1991-2020 (Abweichung: 0,1 Kelvin) und daher auch entsprechend deutlicher über dem Durchschnitt der Referenzperiode 1961-1990 (Abweichung: 1,0 Kelvin). 
Dieser November belegt somit Rang 37 der wärmsten Novembermonate seit Aufzeichnungsbeginn. In der folgenden Tabelle sind die Temperaturwerte der Klimanormalperioden 1881-1910, 1961-1990 und 1991-2020 gegenübergestellt. 
Es ist deutlich zu erkennen, dass die langjährige Mitteltemperatur für November merklich angestiegen ist, nämlich um insgesamt 1,5 Kelvin im Vergleich der Zeiträume 1881-1910 und 1991-2020.

---


Der Sommer 2024 lieferte in NRW ein Mittelwert von 18,1 °C ab. Gegenüber dem Wert der Referenzperiode 1961-1990 von 16,3 °C ergibt sich eine positive Abweichung von +1,8 Kelvin. 
Gegenüber dem Durchschnitt der aktuellen, durch den Klimawandel bereits stark beeinflussten Klimanormalperiode (1991-2020: 17,5 °C) liegt die Abweichung noch bei +0,6 Kelvin. 
Der Sommer belegt damit immerhin noch Rang 13 der wärmsten Sommermonate seit Beginn der Aufzeichnungen im Jahr 1881. 
Ein Vergleich der Mitteltemperaturen der Klimanormalperioden 1881-1910, 1961-1990 und 1991-2020 (s. nachfolgende Tabelle) zeigt deutlich einen zunehmenden Anstieg der Lufttemperatur zum Ende der Zeitreihe hin: Fiel die Differenz zwischen den Klimanormalperioden 1881-1910 und 1961-1990 mit 0,3 K noch recht gering aus, so hat sich der Temperaturanstieg zwischen den KNP 1881-1910 und 1991-2020 mit 0,6 Kelvin verdoppelt.

---

Die durchschnittliche Temperatur im Winter 2022 lag in NRW bei 4,5°C und damit im vierten Jahr in Folge deutlich über dem Durchschnitt der aktuellen Referenzperiode (1991-2020: 2,7 °C; Abweichung: 1,8 Kelvin). 
Damit belegt dieser Winter Rang 7 der wärmsten Winterperioden seit Beginn der Aufzeichnungen. 
Seit der ersten Klimanormalperiode (1881-1910) zeigt sich ein kontinuierlich ansteigender Trend der Lufttemperatur um insgesamt 1,7 Kelvin.

---

Die verzeichneten Werte für Temperatur, Niederschlag und Sonnschein fielen in Bezug auf die Referenzperiode 1961-1990 im Wesentlichen durchschnittlich aus, in Bezug auf die aktuelle Klimanormalperiode 1991-2020 gab es dagegen jedoch deutliche Abweichungen.

Die Durchschnittstemperatur im April 2023 lag mit 8,2 °C im zweiten Jahr in Folge wieder über dem Mittelwert der Referenzperiode 1961-1990, allerdings mit einer positiven Abweichung von 0,3 K nur knapp. 
Dagegen fiel die Abweichung gegenüber der aktuellen Klimanormalperiode 1991-2020 jedoch negativ aus (Abweichung: -1,3 K). 
Dieser April belegt damit Rang 76 der wärmsten Aprilmonate seit Beginn der Aufzeichnungen und liegt somit im Mittelfeld der Gesamtzeitreihe. 
Im Vergleich der Mitteltemperaturen der Klimanormalperioden 1881-1910, 1961-1990 und 1991-2020, wird neben dem generellen Anstieg der Lufttemperatur von insgesamt 1,9 K deutlich, dass diese Zunahme vor allem zum Ende der Messreihe hin sehr viel stärker voranschreitet als zum Beginn, was unter dem Aspekt des fortschreitenden Klimawandels nachvollziehbar ist.
 
"""

# Template Niederschlag ----------------------------------------------------------------------------------------------------------------------------------

template_rain = """Du bist ein Meteorologe für Nordrhein Westfalen.
Erstelle einen informativen Absatz für einen Bericht, der die Entwicklung des Klimaparameters Niederschlag, über verschiedene Zeiträume hinweg beschreibt. Beginne mit der aktuellen Situation und vergleiche sie mit früheren Referenzperioden. 
Erwähne, wie sich der aktuelle Wert im Vergleich zu historischen Daten verhält und ob er über oder unter dem Durchschnitt liegt. 
Gib an, wie sich der Parameter im Laufe der Zeit verändert hat und füge eine Tabelle ein, die diese Entwicklung veranschaulicht. Achte darauf, die relevanten Zeiträume und die entsprechenden Werte sowie das Ranking klar und präzise darzustellen. 

Hier die gegeben Daten:
- Berichtszeitraum aktuelles Jahr: {year} (Sofern Jahr_agg gebe nur das entsprechende Jahr wieder)
- Berichtszeitraum aktuelle Zeiteinheit: {time_unit}
- Einordnung des Berichtszeitraum in das Ranking: {ranking_rain}
- Durchschnittlicher Niederschlag des Berichtszeitraums der aktuellen Zeiteinheit: {m_rain} l/m²
- Durchschnittlicher Niederschlag der Klimanormalperiode in den Jahren 1881-1910: {m_rain_80_10} l/m²
- Durchschnittlicher Niederschlag der Klimanormalperiode in den Jahren 1961-1990: {m_rain_60_90} l/m²
- Durchschnittlicher Niederschlag der Klimanormalperiode in den jahren 1991-2020: {m_rain_90_20} l/m²
"""

template_rain_zero_shot = """Du bist ein Meteorologe für Nordrhein Westfalen.
Erstelle einen informativen Absatz für einen Bericht, der die Entwicklung des Klimaparameters Niederschlag über verschiedene Zeiträume hinweg aus den gegebenen Daten beschreibt.

Hier die gegebenen Daten: 
- Berichtszeitraum aktuelles Jahr: {year} (Sofern Jahr_agg gebe nur das entsprechende Jahr wieder)
- Berichtszeitraum aktuelle Zeiteinheit: {time_unit}
- Einordnung des Berichtszeitraum in das Ranking: {ranking_rain}
- Durchschnittlicher Niederschlag des Berichtszeitraums der aktuellen Zeiteinheit: {m_rain} l/m²
- Durchschnittlicher Niederschlag der Klimanormalperiode in den Jahren 1881-1910: {m_rain_80_10} l/m²
- Durchschnittlicher Niederschlag der Klimanormalperiode in den Jahren 1961-1990: {m_rain_60_90} l/m²
- Durchschnittlicher Niederschlag der Klimanormalperiode in den jahren 1991-2020: {m_rain_90_20} l/m²

Verwende einen sachlichen, informativen Schreibstil und halte die Länge bei etwa 100–150 Wörtern. Achte darauf, dass der Text flüssig und gut strukturiert ist. Schreibe nur den Absatz, ohne Überschrift.
 """

template_rain_CoT = """Du bist ein Meteorologe für Nordrhein Westfalen.
Erstelle einen informativen Absatz für einen Bericht, der die Entwicklung des Klimaparameters Niederschlag, über verschiedene Zeiträume hinweg beschreibt.

Denke Schritt für Schritt und gehe dabei auf folgende Punkte ein:

Schritt 1: Analysiere die aktuellen Daten:

- Nenne das Berichtsjahr ({year}) und die Zeiteinheit ({time_unit}, Sofern Jahr_agg gebe nur das entsprechende Jahr wieder).

- Gib die aktuelle Durchschnittstemperatur ({m_rain} l/m²) an.

- Vergleiche diesen Wert mit den drei Klimanormalperioden (1881–1910, 1961–1990, 1991–2020) und berechne die Abweichung.
    
    Hier die gegebenen Daten:
    - Durchschnittlicher Niederschlag der Klimanormalperiode in den Jahren 1881-1910: {m_rain_80_10} l/m²
    - Durchschnittlicher Niederschlag der Klimanormalperiode in den Jahren 1961-1990: {m_rain_60_90} l/m²
    - Durchschnittlicher Niederschlag der Klimanormalperiode in den jahren 1991-2020: {m_rain_90_20} l/m²

    

Schritt 2: Kontextualisiere die Daten:

- Erkläre, dass der aktuelle Zeitraum den {ranking_rain}. Platz im historischen Ranking einnimmt.

- Beschreibe, ob der Niederschlag über/unter dem langjährigen Durchschnitt liegt.

Schritt 3: Zeige den Langzeittrend:

- Analysiere und beschreibe Niederschlagsveränderungen zwischen den Perioden und dem aktuellen Wert.


Schritt 4: Fasse die Erkenntnisse zusammen

Schritt 5: Umschreibe und verbessere den Berichtabsatz kontinuierlich

Verwende einen sachlichen, informativen Schreibstil und halte die Länge bei etwa 100–150 Wörtern. Achte darauf, dass der Text flüssig und gut strukturiert ist. Schreibe nur den Absatz, ohne Überschrift.
    
"""


template_rain_few_shot = """Du bist ein Meteorologe für Nordrhein Westfalen.
Erstelle einen informativen Absatz für einen Bericht, der die Entwicklung des Witterungsverlaufsparameters Niederschlag über verschiedene Zeiträume hinweg aus den gegebenen Daten beschreibt.

Hier die gegebenen Daten: 
- Berichtszeitraum aktuelles Jahr: {year} (Sofern Jahr_agg gebe nur das entsprechende Jahr wieder)
- Berichtszeitraum aktuelle Zeiteinheit: {time_unit}
- Ranglistenplatz für die niederschlagreichste aktuelle Zeiteinheit des Parameters Niederschlag (Aufzeichnungszeitraum: 1881 bis heute): {ranking_rain}
- Ranglistenplatz für die niederschlagärmste aktuelle Zeiteinheit des Parameters Niederschlag (Aufzeichnungszeitraum: 1881 bis heute): {ranking_rain_min}
- Durchschnittlicher Niederschlag des Berichtszeitraums der aktuellen Zeiteinheit: {m_rain} l/m²
- Durchschnittlicher Niederschlag der Klimanormalperiode in den Jahren 1881-1910: {m_rain_80_10} l/m²
- Durchschnittlicher Niederschlag der Klimanormalperiode in den Jahren 1961-1990: {m_rain_60_90} l/m²
- Durchschnittlicher Niederschlag der Klimanormalperiode in den jahren 1991-2020: {m_rain_90_20} l/m²

Verwende einen sachlichen, informativen Schreibstil und halte die Länge bei etwa 100–150 Wörtern. Achte darauf, dass der Text flüssig und gut strukturiert ist. 
Gebe dabei keine Prognose über das Klima ab, sondern bleibe bei den Daten die Du hast, du gibst nur beschreibend den Witterungsverlauf der gegebenen Zeiteinheit wieder.
Wähle für die Beschreibung des Ranglistenplatzes entweder den Ranglistenplatz für den niederschlagärmsten oder niederschlagreichsten Platz der Zeiteinheit aus, orientiere dich dabei am Mittel aller Ranglistenplätze.
Schreibe nur den Absatz, ohne Überschrift.

Hier einige gegebene Beispiele: 

Nach 13 „zu trockenen“ Aprilmonaten zwischen 2009 und 2021 lag der Niederschlag im April 2023, genauso wie schon im vergangenen Jahr, wieder minimal über dem Durchschnitt des langjährigen Mittels (April 2022 und 2023: 63 l/m²; 1961-1990: 62 l/m²) und dabei auch deutlich über dem Wert der aktuellen Klimanormalperiode 1991-2020 (48 l/m²). 
Damit teilen sich 2022 und 2023 Platz 89 der niederschlagsärmsten Aprilmonate seit Aufzeichnungsbeginn und liegen damit im unteren Mittelfeld der Messreihe. 
Im Vergleich der Klimanormalperioden 1881-1910, 1961-1990 und 1991-2020 ergibt sich seit 1961-1990 insgesamt eine Abnahme der monatlichen Niederschlagssummen für den April (s. nachfolgende Tabelle). 
Wie sich diese Entwicklung mit den bislang wieder höheren Messwerten ab 2021 fortsetzen wird, bleibt abzuwarten.

--- 

Entgegen dem allgemeinen Trend des Vorjahres fiel der Februar in diesem Jahr deutlich zu trocken aus. Mit einer Niederschlagssumme von lediglich 20 l/m² im Landesdurchschnitt wurden sowohl die Referenzperiode 1961-1990 als auch die aktuelle Klimanormalperiode 1991-2020 um jeweils ungefähr zwei Drittel unterboten. 
Dabei fiel in einigen Landesteilen gut die Hälfte des Monatsniederschlags an einem einzigen Tag, nämlich dem 26. Februar. 
Der Februar 2025 belegt damit in der Rangliste immerhin Platz 16 der niederschlagsärmsten Februarmonate seit Beginn der Aufzeichnungen.

---

Der Sommer 2024 lieferte mit 253 l/m² eine Niederschlagssumme ab, die leicht über dem Durchschnitt der vorangegangenen Referenzperiode 1961-1990 (241 l/m²) und etwas deutlicher über dem Wert der aktuellen Klimanormalperiode 1991-2020 (238 l/m²) liegt. 
Mit diesem eher durchschnittlichen Mittelwert, der nichts über die zum Teil heftigen Starkregenereignisse verrät, landet der Sommer 2024 auf einem eher unspektakulären Rang 60 der niederschlagsreichsten Sommer seit 1881. 
Vergleicht man die Monatsniederschläge für die Klimanormalperioden 1881-1910, 1961-1990 und 1991-2020 (s. nachfolgende Tabelle), ist eine ganz leicht abfallende Entwicklung der Sommerniederschläge erkennbar.

---

Neben den überdurchschnittlichen Temperaturen lag auch die Niederschlagssumme in diesem Winter mit 249 l/ m² über dem Mittelwert der Referenzperiode (1991-2020: 237 l/m²). 
Er liegt damit auf Platz 34 niederschlagsreichsten Winter seit Aufzeichnungsbeginn. 
Im Vergleich der Klimanormalperioden 1881-1910, 1961-1990 und 1991-2020 zeigt sich ein Anstieg der winterlichen Niederschlagssummen (s. nachfolgende Tabelle).

--- 

Fiel der November des Vorjahres noch deutlich zu nass aus, so lag die Niederschlagssumme des diesjährigen Novembers mit 80 l/m² nur knapp über den Mittelwerten von 1961-1990 (79 l/m²) und 1991-2020 (75 l/m²). 
Damit reiht sich der November 2024 wenig überraschend im Mittelfeld der Zeitreihe ein. 
Die Gesamtbetrachtung der Klimanormalperioden 1881-1910, 1961-1990 und 1991-2020 zeigt trotz einzelner Jahre mit deutlichen Abweichungen insgesamt nur eine leichte Zunahme der monatlichen Niederschlagssummen in den letzten Klimanormalperioden (s. nachfolgende Tabelle)

 """

# Template Sonnenscheindauer ----------------------------------------------------------------------------------------------------------------------------------

template_sun = """Du bist ein Meteorologe für Nordrhein Westfalen.
Erstelle einen informativen Absatz für einen Bericht, der die Entwicklung des Klimaparameters Sonnenscheindauer, über verschiedene Zeiträume hinweg beschreibt. Beginne mit der aktuellen Situation und vergleiche sie mit früheren Referenzperioden. 
Erwähne, wie sich der aktuelle Wert im Vergleich zu historischen Daten verhält und ob er über oder unter dem Durchschnitt liegt. 
Gib an, wie sich der Parameter im Laufe der Zeit verändert hat und füge eine Tabelle ein, die diese Entwicklung veranschaulicht. Achte darauf, die relevanten Zeiträume und die entsprechenden Werte sowie das Ranking klar und präzise darzustellen.

Hier die gegeben Daten:
- Berichtszeitraum aktuelles Jahr: {year} (Sofern Jahr_agg gebe nur das entsprechende Jahr wieder)
- Berichtszeitraum aktuelle Zeiteinheit: {time_unit}
- Einordnung des Berichtszeitraum in das Ranking: {ranking_sun}
- Durchschnittliche Sonnenscheindauer des Berichtszeitraums der aktuellen Zeiteinheit: {m_sun} h
- Durchschnittliche Sonnenscheindauer der Klimanormalperiode in den Jahren 1951-1980: {m_sun_50_80} h
- Durchschnittliche Sonnenscheindauer der Klimanormalperiode in den Jahren 1961-1990: {m_sun_60_90} h
- Durchschnittliche Sonnenscheindauer der Klimanormalperiode in den jahren 1991-2020: {m_sun_90_20} h
 """

template_sun_zero_shot = """Du bist ein Meteorologe für Nordrhein Westfalen.
Erstelle einen informativen Absatz für einen Bericht, der die Entwicklung des Klimaparameters Sonnenscheindauer über verschiedene Zeiträume hinweg aus den gegebenen Daten beschreibt.

Hier die gegebenen Daten: 
- Berichtszeitraum aktuelles Jahr: {year} (Sofern Jahr_agg gebe nur das entsprechende Jahr wieder)
- Berichtszeitraum aktuelle Zeiteinheit: {time_unit}
- Einordnung des Berichtszeitraum in das Ranking: {ranking_sun}
- Durchschnittliche Sonnenscheindauer des Berichtszeitraums der aktuellen Zeiteinheit: {m_sun} h
- Durchschnittliche Sonnenscheindauer der Klimanormalperiode in den Jahren 1951-1980: {m_sun_50_80} h
- Durchschnittliche Sonnenscheindauer der Klimanormalperiode in den Jahren 1961-1990: {m_sun_60_90} h
- Durchschnittliche Sonnenscheindauer der Klimanormalperiode in den jahren 1991-2020: {m_sun_90_20} h

Verwende einen sachlichen, informativen Schreibstil und halte die Länge bei etwa 100–150 Wörtern. Achte darauf, dass der Text flüssig und gut strukturiert ist.

"""

template_sun_CoT = """ Du bist ein Meteorologe für Nordrhein Westfalen.
Erstelle einen informativen Absatz für einen Bericht, der die Entwicklung des Klimaparameters Sonnenscheindauer, über verschiedene Zeiträume hinweg beschreibt.

Denke Schritt für Schritt und gehe dabei auf folgende Punkte ein:

Schritt 1: Analysiere die aktuellen Daten:

- Nenne das Berichtsjahr ({year}) und die Zeiteinheit ({time_unit}, Sofern Jahr_agg gebe nur das entsprechende Jahr wieder).

- Gib die aktuelle Sonnenscheindauer ({m_sun} h) an.

- Vergleiche diesen Wert mit den drei Klimanormalperioden (1951–1980, 1961–1990, 1991–2020) und berechne die Abweichung.
    
    Hier die gegebenen Daten:
    - Durchschnittlicher Sonnenscheindauer der Klimanormalperiode in den Jahren 1951-1980: {m_sun_50_80} h
    - Durchschnittlicher Sonnenscheindauer der Klimanormalperiode in den Jahren 1961-1990: {m_sun_60_90} h
    - Durchschnittlicher Sonnenscheindauer der Klimanormalperiode in den jahren 1991-2020: {m_sun_90_20} h


Schritt 2: Kontextualisiere die Daten:

- Erkläre, dass der aktuelle Zeitraum den {ranking_sun}. Platz im historischen Ranking einnimmt.

- Beschreibe, ob die Sonnenscheindauer über/unter dem langjährigen Durchschnitt liegt.

Schritt 3: Zeige den Langzeittrend:

- Analysiere und beschreibe die Sonnenscheindauerveränderungen zwischen den Perioden und dem aktullen Wert.


Schritt 4: Fasse die Erkenntnisse zusammen

Schritt 5: Umschreibe und verbessere den Berichtabsatz kontinuierlich

Verwende einen sachlichen, informativen Schreibstil und halte die Länge bei etwa 100–150 Wörtern. Achte darauf, dass der Text flüssig und gut strukturiert ist. Schreibe nur den Absatz, ohne Überschrift."""


template_sun_few_shot = """

Du bist ein Meteorologe für Nordrhein Westfalen.
Erstelle einen informativen Absatz für einen Bericht, der die Entwicklung des Witterungsverlaufsparameters Sonnenscheindauer über verschiedene Zeiträume hinweg aus den gegebenen Daten beschreibt.

Hier die gegebenen Daten: 
- Berichtszeitraum aktuelles Jahr: {year} (Sofern Jahr_agg gebe nur das entsprechende Jahr wieder)
- Berichtszeitraum aktuelle Zeiteinheit: {time_unit}
- Ranglistenplatz für die sonnenscheinreichste aktuelle Zeiteinheit des Parameters Sonnenscheindauer (Aufzeichnungszeitraum: 1881 bis heute): {ranking_sun}
- Ranglistenplatz für die sonnenscheinärmste aktuelle Zeiteinheit des Parameters Sonnenscheindauer (Aufzeichnungszeitraum: 1881 bis heute): {ranking_sun_min}
- Durchschnittliche Sonnenscheindauer des Berichtszeitraums der aktuellen Zeiteinheit: {m_sun} h
- Durchschnittliche Sonnenscheindauer der Klimanormalperiode in den Jahren 1951-1980: {m_sun_50_80} h
- Durchschnittliche Sonnenscheindauer der Klimanormalperiode in den Jahren 1961-1990: {m_sun_60_90} h
- Durchschnittliche Sonnenscheindauer der Klimanormalperiode in den jahren 1991-2020: {m_sun_90_20} h

Verwende einen sachlichen, informativen Schreibstil und halte die Länge bei etwa 100–150 Wörtern. Achte darauf, dass der Text flüssig und gut strukturiert ist. 
Gebe dabei keine Prognose über das Klima ab, sondern bleibe bei den Daten die Du hast, du gibst nur beschreibend den Witterungsverlauf der gegebenen Zeiteinheit wieder. 
Wähle für die Beschreibung des Ranglistenplatzes entweder den Rang für den Sonnenscheinärmsten oder Sonnenscheinreichsten Platz der Zeiteinheit aus, orientiere dich dabei am Mittel aller Ranglistenplätze.
Schreibe nur den Absatz, ohne Überschrift.

Hier einige gegebene Beispiele: 

Insgesamt wurden im Winter 2021/2022 mit 142 Sonnenscheinstunden bereits zum dritten Mal in Folge unterdurchschnittlich wenige Sonnenscheinstunden verzeichnet (1991-2020: 165 h), 
sogar noch weniger als während der ersten gemessenen Klimanormalperiode (1951-1980: 146 h). Damit belegt dieser Winter Rang 30 der sonnenscheinärmsten Winter seit Aufzeichnungsbeginn. 
Vergleicht man die Winterwerte der drei letzten Klimanormalperioden miteinander, so ist trotz der geringen Sonnenscheinstunden im Winter 2021/2022 dennoch insgesamt ein leichter Anstieg der Sonnenscheindauer festzustellen.

--- 

Wie im November nicht unüblich fiel die Sonnenscheindauer in diesem Jahr mit 49 h erneut unterdurchschnittlich aus (1991-2020: 55 h; 1961-1990: 53 h). Damit ordnet sich der November 2024 abermals im Mittelfeld der Zeitreihe ein. 
Im direkten Vergleich der mittleren Sonnenscheindauern der drei letzten Klimanormalperioden für November zeigt sich lediglich ein schwacher Anstieg der Sonnenscheinstundensumme seit Aufzeichnungsbeginn.

--- 

Für den Sommer 2024 wurde in NRW eine Sonnenscheindauer von insgesamt 650 h registriert. Damit wurde der Durchschnittswert der Referenzperiode 1961-1990 (554 h) wie auch der der aktuellen Klimanormalperiode 1991-2020 (605 h) sehr deutlich übertroffen. Trotz deutlich überdurchschnittlicher Sonnenscheindauer landet der Sommer 2024 nur auf Rang 15 der sonnigsten Sommer seit Beginn der Aufzeichnungen 1951. 
Im Vergleich der Sonnenstunden der drei letzten Klimanormalperioden (s. untenstehende Tabelle) ergibt sich ein deutlicher Anstieg der mittleren Anzahl der Sonnenstunden im Sommer seit dem Beginn der Messreihe. 

---

Die überwiegende Hochdruckprägung brachte auch zahlreiche Sonnenscheinstunden in NRW: mit einer Summe von 88 Sonnenstunden schien in diesem Februar länger die Sonne als im 30-jährigen Mittel der Referenzperiode 1961-1990 sowie der aktuellen Klimanormalperiode 1991-2020 mit jeweils 72 Sonnenscheinstunden. 
Dieser Februar belegt ebenfalls Platz 16 der sonnenscheinreichsten Februare seit Aufzeichnungsbeginn im Jahr 1951.

--- 

Ähnlich wie bei Temperatur und Niederschlag fiel auch die Sonnenscheindauer im April 2023 mit 154 Stunden eher durchschnittlich aus: sie lag zwar im sechsten Jahr in Folge über dem Durchschnitt der Referenzperiode 1961-1990 (148 h), jedoch im dritten Jahr in Folge unter dem deutlich höheren Wert der aktuellen Klimanormalperiode 1991-2020 (174 h). Dieser April belegt Rang 42 der sonnenscheinreichsten Aprilmonate seit Beginn der Aufzeichnungen 1951. 
Im Vergleich der Sonnenstunden der drei letzten Klimanormalperioden ergibt sich für April eine allgemeine Zunahme der Sonnenscheinstunden zum Ende der Messreihe hin.

"""
# Template Wetterstationen ----------------------------------------------------------------------------------------------------------------------------------


# template Winter

template_wetterstation_winter_zero_shot = """ Du bist ein Meteorologe für Nordrhein Westfalen.

Erstelle einen informativen Absatz für einen Bericht über die Auswertung der Temperatur-Kenntage im {Monat} anhand der zwei Stationen des LANUV-Luftqualitätsmessnetzes - Station Köln – Turiner Straße (WKTU) und Station Warstein (WAST)). 

Erwähne den Kontrast zwischen Großstadt und Höhenlage, Vergleich der gegeben Temperatur-Kenntage der Wetterstationen sowie markante Unterschiede zum Vorjahr. 
Ordne die Daten in den Kontext des Monats- und Jahresverlaufs ein.

Hier die gegebenen Daten des aktuellen Jahres: 
    Berichtszeitraum:  
    - Berichtszeitraum aktuelles Jahr: {Jahr} (Sofern Jahr_agg gebe nur das entsprechende Jahr wieder)
    - Berichtszeitraum aktuelle Zeiteinheit: {Monat}

    Temperatur-Kenntage für VKTU aktuelles Jahr:
    - Frosttage: {VKTU_frost} 
    - Eistage: {VKTU_eis} 
    - Tiefsttemperatur: {VKTU_tiefsttemperatur} °C
    - Höchstemperatur: {VKTU_höchsttemperatur} °C

    Temperatur-Kenntage für WAST aktuelles Jahr: 
    - Frosttage: {WAST_frost} 
    - Eistage: {WAST_eis} 
    - Tiefsttemperatur: {WAST_tiefsttemperatur} °C
    - Höchstemperatur: {WAST_höchsttemperatur} °C

Hier die gegebenen Daten des Vorjahres: 
    
    Berichtszeitraum:  
    - Berichtszeitraum vorherigen Jahres: {Jahr_l_y}
    - Berichtszeitraum vorherigen Zeiteinheit: {Monat_l_y}

    Temperatur-Kenntage für VKTU letzten Jahres:
    - Frosttage: {VKTU_frost_l_y} 
    - Eistage: {VKTU_eis_l_y} 
    - Tiefsttemperatur: {VKTU_tiefsttemperatur_l_y} °C
    - Höchstemperatur: {VKTU_höchsttemperatur_l_y} °C

    Temperatur-Kenntage für WAST letzten Jahres: 
    - Frosttage: {WAST_frost_l_y} 
    - Eistage: {WAST_eis_l_y}
    - Tiefsttemperatur: {WAST_tiefsttemperatur_l_y} °C
    - Höchstemperatur: {WAST_höchsttemperatur_l_y} °C

Verwende einen sachlichen, informativen Schreibstil und halte die Länge bei etwa 150–200 Wörtern. Achte darauf, dass der Text flüssig und gut strukturiert ist. Schreibe nur den Absatz, ohne Überschrift.
"""

template_wetterstation_winter_CoT = """Du bist ein Meteorologe für Nordrhein Westfalen.

Erstelle einen informativen Absatz für einen Bericht über die Auswertung Temperatur-Kenntage im {Monat} anhand der zwei Stationen des LANUV-Luftqualitätsmessnetzes - Station Köln – Turiner Straße (WKTU) und Station Warstein (WAST)). 

Denke Schritt für Schritt und gehe dabei auf folgende Punkte ein:

Schritt 1: Allgemeine Wetterlage im Januar und eine kurze Einordnung, warum diese beiden Stationen ausgewählt wurden (Großstadt vs. Höhenlage).
    Folge dabei diesem Aufbau: 
        "Um einen Einblick zu geben, wie das Temperaturgeschehen im {Monat} war, werden an zwei Stationen des LANUV-Luftqualitätsmessnetzes Temperatur-Kenntage ausgewertet. 
        Dafür wird zum einen die Station Köln – Turiner Straße (VKTU), als eine innerstädtische Station einer Großstadt in der wärmebegünstigten Niederrheinischen Bucht, 
        und zum anderen die Station Warstein (WAST) in Warstein als ein Beispiel für eine Stadtrandlage in einer Mittelstadt am Nordrand des Sauerlands, dargestellt."

Schritt 2: Vergleich der beiden Stationen hinsichtlich der gegebenen Temperatur-Kenntage.
        Berichtszeitraum:  
        - Berichtszeitraum aktuelles Jahr: {Jahr}
        - Berichtszeitraum aktuelle Zeiteinheit: {Monat}

        Temperatur-Kenntage für VKTU aktuelles Jahr:
        - Frosttage: {VKTU_frost} 
        - Eistage: {VKTU_eis} 
        - Tiefsttemperatur: {VKTU_tiefsttemperatur} °C
        - Höchstemperatur: {VKTU_höchsttemperatur} °C

        Temperatur-Kenntage für WAST aktuelles Jahr: 

        - Frosttage: {WAST_frost} 
        - Eistage: {WAST_eis} 
        - Tiefsttemperatur: {WAST_tiefsttemperatur} °C
        - Höchstemperatur: {WAST_höchsttemperatur} °C

    
Schritt 3: Erläuterung nur von markanten Unterschieden zwischen den Temperatur-Kenntagen dieses Jahres und dem Vorjahr.
        Berichtszeitraum:  
        - Berichtszeitraum vorherigen Jahres: {Jahr_l_y}
        - Berichtszeitraum vorherigen Zeiteinheit: {Monat_l_y}

        Temperatur-Kenntage für VKTU letzten Jahres:
        - Frosttage: {VKTU_frost_l_y} 
        - Eistage: {VKTU_eis_l_y} 
        - Tiefsttemperatur: {VKTU_tiefsttemperatur_l_y} °C
        - Höchstemperatur: {VKTU_höchsttemperatur_l_y} °C

        Temperatur-Kenntage für WAST letzten Jahres:
        - Frosttage: {WAST_frost_l_y} 
        - Eistage: {WAST_eis_l_y}
        - Tiefsttemperatur: {WAST_tiefsttemperatur_l_y} °C
        - Höchstemperatur: {WAST_höchsttemperatur_l_y} °C


Schritt 4: Einordnung der Daten in den Kontext des Monats- und Jahresverlaufs.

Schritt 5: Umschreibe und verbessere den Bericht kontinuierlich

Verwende einen sachlichen, informativen Schreibstil und halte die Länge bei etwa 150–200 Wörtern. Achte darauf, dass der Text flüssig und gut strukturiert ist. Schreibe nur den Absatz, ohne Überschrift."""


template_wetterstation_winter_few_shots = """ Du bist ein Meteorologe für Nordrhein Westfalen.

Erstelle einen informativen Absatz für einen Bericht über die Auswertung der Temperatur-Kenntage im {Monat} anhand der zwei Stationen des LANUV-Luftqualitätsmessnetzes - Station Köln – Turiner Straße (WKTU) und Station Warstein (WAST)). 

Erwähne den Kontrast zwischen Großstadt und Höhenlage, Vergleich der gegeben Temperatur-Kenntage der Wetterstationen sowie markante Unterschiede zum Vorjahr. 
Ordne die Daten in den Kontext des Monats- und Jahresverlaufs ein.

Hier die gegebenen Daten des aktuellen Jahres: 
    Berichtszeitraum:  
    - Berichtszeitraum aktuelles Jahr: {Jahr} (Sofern Jahr_agg gebe nur das entsprechende Jahr wieder)
    - Berichtszeitraum aktuelle Zeiteinheit: {Monat}

    Temperatur-Kenntage für VKTU aktuelles Jahr:
    - Frosttage: {VKTU_frost} 
    - Eistage: {VKTU_eis} 
    - Tiefsttemperatur: {VKTU_tiefsttemperatur} °C
    - Höchstemperatur: {VKTU_höchsttemperatur} °C

    Temperatur-Kenntage für WAST aktuelles Jahr: 
    - Frosttage: {WAST_frost} 
    - Eistage: {WAST_eis} 
    - Tiefsttemperatur: {WAST_tiefsttemperatur} °C
    - Höchstemperatur: {WAST_höchsttemperatur} °C

Hier die gegebenen Daten des Vorjahres: 
    
    Berichtszeitraum:  
    - Berichtszeitraum vorherigen Jahres: {Jahr_l_y}
    - Berichtszeitraum vorherigen Zeiteinheit: {Monat_l_y}

    Temperatur-Kenntage für VKTU letzten Jahres:
    - Frosttage: {VKTU_frost_l_y} 
    - Eistage: {VKTU_eis_l_y} 
    - Tiefsttemperatur: {VKTU_tiefsttemperatur_l_y} °C
    - Höchstemperatur: {VKTU_höchsttemperatur_l_y} °C

    Temperatur-Kenntage für WAST letzten Jahres: 
    - Frosttage: {WAST_frost_l_y} 
    - Eistage: {WAST_eis_l_y}
    - Tiefsttemperatur: {WAST_tiefsttemperatur_l_y} °C
    - Höchstemperatur: {WAST_höchsttemperatur_l_y} °C


Verwende einen sachlichen, informativen Schreibstil und halte die Länge bei etwa 150–200 Wörtern. Achte darauf, dass der Text flüssig und gut strukturiert ist. 
Gebe dabei keine Prognose über das Klima, oder politische Statements ab, sondern bleibe bei den Daten die Du hast. Du gibst nur beschreibend die Temperatur-Kenntage der gegebenen Zeiteinheit wieder.
Schreibe nur den Absatz, ohne Überschrift.

Hier einige gegebene Beispiele: 

Um einen Einblick zu geben, wie das Temperaturgeschehen im April war, werden an zwei Stationen des LANUV-Luftqualitätsmessnetzes Temperatur-Kenntage ausgewertet. 
Dafür wird zum einen die Station Köln –Turiner Straße (VKTU) als eine innerstädtische Station einer Großstadt in der wärmebegünstigten Niederrheinischen Bucht und zum anderen die Station Warstein (WAST) in Warstein als ein Beispiel für eine Stadtrandlage in einer Mittelstadt am Nordrand des Sauerlands dargestellt.

Sowohl an der Kölner Station als auch in Warstein wurden in diesem April kaum temperaturbedingte Kenntage erfasst; lediglich in Warstein konnten vier Frosttage verzeichnet werden. Damit fiel die Bilanz ähnlich aus wie im Vorjahr (April 2022: 3 Frosttage an der Station WAST). 
Sommertage gab es im Gegensatz zu manch vorherigem Jahr noch nicht. Die Tiefsttemperaturen waren an beiden Stationen höher als im Vorjahr, wobei die Tiefsttemperatur an der Station in Warstein dieses Jahr etwa doppelt so hoch ausfiel wie im letzten (Differenz VKTU: 0,9 °C; WAST: 3,4 °C). 
Die Tageshöchsttemperaturen lagen in Warstein annähernd auf und in Köln sichtlich unter dem Vorjahresniveau (Differenz: ca. -3 °C).

---

Um einen Einblick zu geben, wie das Temperaturgeschehen im Februar war, werden an zwei Stationen des LANUV-Luftqualitätsmessnetzes Temperatur-Kenntage ausgewertet. 
Dafür wird zum einen die Station Köln –Turiner Straße (VKTU) als eine innerstädtische Station einer Großstadt in der wärmebegünstigten Niederrheinischen Bucht und zum anderen die Station Warstein (WAST) in Warstein als ein Beispiel für eine Stadtrandlage in einer Mittelstadt am Nordrand des Sauerlands dargestellt.

Weder in Köln (VKTU) noch in Warstein (WAST) konnte in diesem Jahr ein Eistag verzeichnet werden. Allerdings wurden, im Gegensatz zum Vorjahr, in Köln fünf Frosttage gemessen und in Warstein sogar mehr als doppelt so viele (elf). 
In Köln lag die Tiefsttemperatur mit -2,3 °C ca. 6 °C über und die Höchsttemperatur mit 16,2 °C in etwa auf dem Niveau des Wertes vom Februar 2024. In Warstein war die Tiefsttemperatur mit -4,8 °C fast drei Grad Celsius niedriger als letztes Jahr, die Höchsttemperatur mit 16,0 °C dagegen fast zwei Grad Celsius höher als im Februar 2024.

---

Um einen Einblick zu geben, wie das Temperaturgeschehen im Frühling war, werden an zwei Stationen des LANUV-Luftqualitätsmessnetzes Temperatur-Kenntage ausgewertet. Dafür wird zum einen die Station Köln –Turiner Straße (VKTU) als eine innerstädtische Station einer Großstadt in der wärmebegünstigten Niederrheinischen Bucht und zum anderen die Station Warstein (WAST) in Warstein als ein Beispiel für eine Stadtrandlage in einer Mittelstadt am Nordrand des Sauerlands dargestellt.
Der Sommer 2024 machte sich auch im Messnetz des LANUV bemerkbar, wie im Folgenden erläutert wird. In der Kölner Innenstadt (VKTU) wurden insgesamt 47 Sommertage verzeichnet, was exakt der Vorjahreszahl entspricht. 
Im höher gelegenen Warstein wurden insgesamt 31 Sommertage aufgezeichnet, womit die Anzahl von 25 Sommertagen vom Sommer 2023 übertroffen wurde. In der Kölner Innenstadt wurden im Sommer 2024 12 Heiße Tage registriert, in ländlichen Warstein 6 Heiße Tage. Auch hier zieht Köln mit dem Wert vom letzten Jahr gleich und Warstein hatte doppelt so viele Heiße Tage als im Sommer 2023. Bei der Anzahl der Tropennächte zeigt sich auch im Sommer 2024 klar die urbane Überwärmung gegenüber der Station Warstein. 
Mit 20 Tropennächten in Köln (2023: 21) und nur 4 Tropennächten in Warstein (2023: 2) wird abermals ein starker Kontrast deutlich. Die Tageshöchsttemperaturen konnten mit jeweils rund 35 °C in Köln und 32,9 °C in Warstein jene des Vorjahres nicht ganz übertreffen, worüber gerade die Kölnerinnen und Kölner glücklich gewesen sein dürften. Die Tiefstwerte lagen mit rund 11,0 °C (VKTU) bzw. 7,4 °C (WAST) in Köln unter und in Warstein über den Vorjahreswerten. 

---

Um einen Einblick zu geben, wie das Temperaturgeschehen im November war, werden an zwei Stationen des LANUV-Luftqualitätsmessnetzes Temperatur-Kenntage ausgewertet. 
Dafür wird zum einen die Station Köln –Turiner Straße (VKTU) als eine innerstädtische Station einer Großstadt in der wärmebegünstigten Niederrheinischen Bucht und zum anderen die Station Warstein (WAST) in Warstein als ein Beispiel für eine Stadtrandlage in einer Mittelstadt am Nordrand des Sauerlands dargestellt.

Während an der Kölner Messstation keinerlei Temperaturkenntage erfasst wurden, konnten an der Station Warstein zwei Frosttage verzeichnet werden. 
Verglichen mit den Vorjahreswerten fielen die Tiefsttemperaturen des Novembers 2024 in Köln und Warstein um jeweils rund 1 °C bzw. 5 °C niedriger aus, die Höchsttemperaturen lagen an beiden Stationen in diesem Jahr um jeweils rund 3 °C höher als im November 2023.

---

Um einen Einblick zu geben, wie das Temperaturgeschehen im Winter war, werden an zwei Stationen des LANUV-Luftqualitätsmessnetzes Temperatur-Kenntage ausgewertet. 
Dafür wird zum einen die Station Köln –Turiner Straße (VKTU) als eine innerstädtische Station einer Großstadt in der wärmebegünstigten Niederrheinischen Bucht und zum anderen die Station Warstein (WAST) in Warstein als ein Beispiel für eine Stadtrandlage in einer Mittelstadt am Nordrand des Sauerlands dargestellt.
Lediglich zwei Frosttage wurden im Winter 2021/2022 an der Station Köln – Turiner Straße gemessen, an der Station Warstein waren es 21 Frosttage. 
Das sind jeweils fünf Frosttage weniger als noch im Vorjahr. Eistage wurden in diesem Winter an keiner der beiden Stationen erfasst; auch hier zeigt sich eine deutliche Abnahme gegenüber dem Winter 2020/2021. 
Zwar lagen die Tageshöchsttemperaturen in diesem Winter an den Stationen VKTU und WAST jeweils rund 4 °C und 5 °C unter den Werten des Vorjahres, doch die Tagestiefsttemperaturen waren an beiden Messstationen dafür signifikant höher, in Köln um gut 7 °C und in Warstein sogar um 11 °C.

"""

# template Sommer

template_wetterstation_Sommer_zero_shot = """ Du bist ein Meteorologe für Nordrhein Westfalen.

Erstelle einen informativen Absatz für einen Bericht über die Auswertung der Temperatur-Kenntage im {Monat} anhand der zwei Stationen des LANUV-Luftqualitätsmessnetzes - Station Köln – Turiner Straße (WKTU) und Station Warstein (WAST)). 

Erwähne den Kontrast zwischen Großstadt und Höhenlage, Vergleich der gegeben Temperatur-Kenntage der Wetterstationen sowie markante Unterschiede zum Vorjahr. 
Ordne die Daten in den Kontext des Monats- und Jahresverlaufs ein. 

Hier die gegebenen Temperatur-Kenntage des aktuellen Jahres: 

    Berichtszeitraum:  
    - Berichtszeitraum aktuelles Jahr: {Jahr}
    - Berichtszeitraum aktuelle Zeiteinheit: {Monat}

    Temperatur-Kenntage für VKTU aktuelles Jahr:
    - Sommertage: {VKTU_sommertage}
    - heiße Tage: {VKTU_heißetage}
    - Tropennächte: {VKTU_tropennächte} 
    - Tiefsttemperatur: {VKTU_tiefsttemperatur} °C
    - Höchstemperatur: {VKTU_höchsttemperatur} °C

    Temperatur-Kenntage für WAST aktuelles Jahr: 
    - Sommertage: {WAST_sommertage}
    - heiße Tage: {WAST_heißetage}
    - Tropennächte: {WAST_tropennächte} 
    - Tiefsttemperatur: {WAST_tiefsttemperatur} °C
    - Höchstemperatur: {WAST_höchsttemperatur} °C

Hier die gegebenen Temperatur-Kenntage des Vorjahres: 
    
    Berichtszeitraum:  
    - Berichtszeitraum vorherigen Jahres: {Jahr_l_y}
    - Berichtszeitraum vorherigen Zeiteinheit: {Monat_l_y}

    Temperatur-Kenntage für VKTU letzten Jahres:
    - Sommertage: {VKTU_sommertage_l_y}
    - heiße Tage: {VKTU_heißetage_l_y}
    - Tropennächte: {VKTU_tropennächte_l_y} 
    - Tiefsttemperatur: {VKTU_tiefsttemperatur_l_y} °C
    - Höchstemperatur: {VKTU_höchsttemperatur_l_y} °C

    Temperatur-Kenntage für WAST letzten Jahres: 
    - Sommertage: {WAST_sommertage_l_y}
    - heiße Tage: {WAST_heißetage_l_y}
    - Tropennächte: {WAST_tropennächte_l_y} 
    - Tiefsttemperatur: {WAST_tiefsttemperatur_l_y} °C
    - Höchstemperatur: {WAST_höchsttemperatur_l_y} °C

Verwende einen sachlichen, informativen Schreibstil und halte die Länge bei etwa 150–200 Wörtern. Achte darauf, dass der Text flüssig und gut strukturiert ist. Schreibe nur den Absatz, ohne Überschrift.
"""


template_wetterstation_Sommer_CoT = """ Du bist ein Meteorologe für Nordrhein Westfalen.

Erstelle einen informativen Absatz für einen Bericht über die Auswertung der Temperatur-Kenntage im {Monat} anhand der zwei Stationen des LANUV-Luftqualitätsmessnetzes - Station Köln – Turiner Straße (WKTU) und Station Warstein (WAST)). 

Denke Schritt für Schritt und gehe dabei auf folgende Punkte ein:

Schritt 1: Allgemeine Wetterlage im {Monat} und eine kurze Einordnung, warum diese beiden Stationen ausgewählt wurden (Großstadt vs. Höhenlage).
    Folge dabei diesem Aufbau: 
        "Um einen Einblick zu geben, wie das Temperaturgeschehen im {Monat} war, werden an zwei Stationen des LANUV-Luftqualitätsmessnetzes Temperatur-Kenntage ausgewertet. 
        Dafür wird zum einen die Station Köln – Turiner Straße (VKTU), als eine innerstädtische Station einer Großstadt in der wärmebegünstigten Niederrheinischen Bucht, 
        und zum anderen die Station Warstein (WAST) in Warstein als ein Beispiel für eine Stadtrandlage in einer Mittelstadt am Nordrand des Sauerlands, dargestellt."

Schritt 2: Vergleich der beiden Stationen hinsichtlich der gegebenen Temperatur-Kenntage:
        Berichtszeitraum:  
        - Berichtszeitraum aktuelles Jahr: {Jahr}
        - Berichtszeitraum aktuelle Zeiteinheit: {Monat}

        Temperatur-Kenntage für VKTU aktuelles Jahr:
        - Sommertage: {VKTU_sommertage}
        - heiße Tage: {VKTU_heißetage}
        - Tropennächte: {VKTU_tropennächte} 
        - Tiefsttemperatur: {VKTU_tiefsttemperatur} °C
        - Höchstemperatur: {VKTU_höchsttemperatur} °C

        Temperatur-Kenntage für WAST aktuelles Jahr: 
        - Sommertage: {WAST_sommertage}
        - heiße Tage: {WAST_heißetage}
        - Tropennächte: {WAST_tropennächte} 
        - Tiefsttemperatur: {WAST_tiefsttemperatur} °C
        - Höchstemperatur: {WAST_höchsttemperatur} °C

    
Schritt 3: Erläuterung nur von markanten Unterschieden zwischen den Temperatur-Kenntagen dieses Jahres und dem Vorjahr.
        Berichtszeitraum:  
        - Berichtszeitraum vorherigen Jahres: {Jahr_l_y}
        - Berichtszeitraum vorherigen Zeiteinheit: {Monat_l_y}

        Temperatur-Kenntage für VKTU letzten Jahres:
        - Sommertage: {VKTU_sommertage_l_y}
        - heiße Tage: {VKTU_heißetage_l_y}
        - Tropennächte: {VKTU_tropennächte_l_y} 
        - Monat's Tiefsttemperatur: {VKTU_tiefsttemperatur_l_y} °C
        - Monat's Höchstemperatur: {VKTU_höchsttemperatur_l_y} °C

        Temperatur-Kenntage für WAST letzten Jahres: 
        - Sommertage: {WAST_sommertage_l_y}
        - heiße Tage: {WAST_heißetage_l_y}
        - Tropennächte: {WAST_tropennächte_l_y} 
        - Tiefsttemperatur: {WAST_tiefsttemperatur_l_y} °C
        - Höchstemperatur: {WAST_höchsttemperatur_l_y} °C


Schritt 4: Einordnung der Daten in den Kontext des Monats- und Jahresverlaufs.

Schritt 5: Umschreibe und verbessere den Bericht kontinuierlich

Verwende einen sachlichen, informativen Schreibstil und halte die Länge bei etwa 150–200 Wörtern. Achte darauf, dass der Text flüssig und gut strukturiert ist. Schreibe nur den Absatz, ohne Überschrift. """


template_wetterstation_sommer_few_shots = """Du bist ein Meteorologe für Nordrhein Westfalen.

Erstelle einen informativen Absatz für einen Bericht über die Auswertung der Temperatur-Kenntage im {Monat} anhand der zwei Stationen des LANUV-Luftqualitätsmessnetzes - Station Köln – Turiner Straße (WKTU) und Station Warstein (WAST)). 

Erwähne den Kontrast zwischen Großstadt und Höhenlage, Vergleich der gegeben Temperatur-Kenntage der Wetterstationen sowie markante Unterschiede zum Vorjahr. 
Ordne die Daten in den Kontext des Monats- und Jahresverlaufs ein. 

Hier die gegebenen Temperatur-Kenntage des aktuellen Jahres: 

    Berichtszeitraum:  
    - Berichtszeitraum aktuelles Jahr: {Jahr}
    - Berichtszeitraum aktuelle Zeiteinheit: {Monat}

    Temperatur-Kenntage für VKTU aktuelles Jahr:
    - Sommertage: {VKTU_sommertage}
    - heiße Tage: {VKTU_heißetage}
    - Tropennächte: {VKTU_tropennächte} 
    - Tiefsttemperatur: {VKTU_tiefsttemperatur} °C
    - Höchstemperatur: {VKTU_höchsttemperatur} °C

    Temperatur-Kenntage für WAST aktuelles Jahr: 
    - Sommertage: {WAST_sommertage}
    - heiße Tage: {WAST_heißetage}
    - Tropennächte: {WAST_tropennächte} 
    - Tiefsttemperatur: {WAST_tiefsttemperatur} °C
    - Höchstemperatur: {WAST_höchsttemperatur} °C

Hier die gegebenen Temperatur-Kenntage des Vorjahres: 
    
    Berichtszeitraum:  
    - Berichtszeitraum vorherigen Jahres: {Jahr_l_y}
    - Berichtszeitraum vorherigen Zeiteinheit: {Monat_l_y}

    Temperatur-Kenntage für VKTU letzten Jahres:
    - Sommertage: {VKTU_sommertage_l_y}
    - heiße Tage: {VKTU_heißetage_l_y}
    - Tropennächte: {VKTU_tropennächte_l_y} 
    - Tiefsttemperatur: {VKTU_tiefsttemperatur_l_y} °C
    - Höchstemperatur: {VKTU_höchsttemperatur_l_y} °C

    Temperatur-Kenntage für WAST letzten Jahres: 
    - Sommertage: {WAST_sommertage_l_y}
    - heiße Tage: {WAST_heißetage_l_y}
    - Tropennächte: {WAST_tropennächte_l_y} 
    - Tiefsttemperatur: {WAST_tiefsttemperatur_l_y} °C
    - Höchstemperatur: {WAST_höchsttemperatur_l_y} °C

Verwende einen sachlichen, informativen Schreibstil und halte die Länge bei etwa 150–200 Wörtern. Achte darauf, dass der Text flüssig und gut strukturiert ist. 
Gebe dabei keine Prognose über das Klima, oder politische Statements ab, sondern bleibe bei den Daten die Du hast. Du gibst nur beschreibend die Temperatur-Kenntage der gegebenen Zeiteinheit wieder.
Schreibe nur den Absatz, ohne Überschrift.

Hier einige gegebene Beispiele: 

Um einen Einblick zu geben, wie das Temperaturgeschehen im April war, werden an zwei Stationen des LANUV-Luftqualitätsmessnetzes Temperatur-Kenntage ausgewertet. 
Dafür wird zum einen die Station Köln –Turiner Straße (VKTU) als eine innerstädtische Station einer Großstadt in der wärmebegünstigten Niederrheinischen Bucht und zum anderen die Station Warstein (WAST) in Warstein als ein Beispiel für eine Stadtrandlage in einer Mittelstadt am Nordrand des Sauerlands dargestellt.

Sowohl an der Kölner Station als auch in Warstein wurden in diesem April kaum temperaturbedingte Kenntage erfasst; lediglich in Warstein konnten vier Frosttage verzeichnet werden. Damit fiel die Bilanz ähnlich aus wie im Vorjahr (April 2022: 3 Frosttage an der Station WAST). 
Sommertage gab es im Gegensatz zu manch vorherigem Jahr noch nicht. Die Tiefsttemperaturen waren an beiden Stationen höher als im Vorjahr, wobei die Tiefsttemperatur an der Station in Warstein dieses Jahr etwa doppelt so hoch ausfiel wie im letzten (Differenz VKTU: 0,9 °C; WAST: 3,4 °C). 
Die Tageshöchsttemperaturen lagen in Warstein annähernd auf und in Köln sichtlich unter dem Vorjahresniveau (Differenz: ca. -3 °C).

---

Um einen Einblick zu geben, wie das Temperaturgeschehen im Februar war, werden an zwei Stationen des LANUV-Luftqualitätsmessnetzes Temperatur-Kenntage ausgewertet. 
Dafür wird zum einen die Station Köln –Turiner Straße (VKTU) als eine innerstädtische Station einer Großstadt in der wärmebegünstigten Niederrheinischen Bucht und zum anderen die Station Warstein (WAST) in Warstein als ein Beispiel für eine Stadtrandlage in einer Mittelstadt am Nordrand des Sauerlands dargestellt.

Weder in Köln (VKTU) noch in Warstein (WAST) konnte in diesem Jahr ein Eistag verzeichnet werden. Allerdings wurden, im Gegensatz zum Vorjahr, in Köln fünf Frosttage gemessen und in Warstein sogar mehr als doppelt so viele (elf). 
In Köln lag die Tiefsttemperatur mit -2,3 °C ca. 6 °C über und die Höchsttemperatur mit 16,2 °C in etwa auf dem Niveau des Wertes vom Februar 2024. In Warstein war die Tiefsttemperatur mit -4,8 °C fast drei Grad Celsius niedriger als letztes Jahr, die Höchsttemperatur mit 16,0 °C dagegen fast zwei Grad Celsius höher als im Februar 2024.

---

Um einen Einblick zu geben, wie das Temperaturgeschehen im Frühling war, werden an zwei Stationen des LANUV-Luftqualitätsmessnetzes Temperatur-Kenntage ausgewertet. Dafür wird zum einen die Station Köln –Turiner Straße (VKTU) als eine innerstädtische Station einer Großstadt in der wärmebegünstigten Niederrheinischen Bucht und zum anderen die Station Warstein (WAST) in Warstein als ein Beispiel für eine Stadtrandlage in einer Mittelstadt am Nordrand des Sauerlands dargestellt.
Der Sommer 2024 machte sich auch im Messnetz des LANUV bemerkbar, wie im Folgenden erläutert wird. In der Kölner Innenstadt (VKTU) wurden insgesamt 47 Sommertage verzeichnet, was exakt der Vorjahreszahl entspricht. 
Im höher gelegenen Warstein wurden insgesamt 31 Sommertage aufgezeichnet, womit die Anzahl von 25 Sommertagen vom Sommer 2023 übertroffen wurde. In der Kölner Innenstadt wurden im Sommer 2024 12 Heiße Tage registriert, in ländlichen Warstein 6 Heiße Tage. Auch hier zieht Köln mit dem Wert vom letzten Jahr gleich und Warstein hatte doppelt so viele Heiße Tage als im Sommer 2023. Bei der Anzahl der Tropennächte zeigt sich auch im Sommer 2024 klar die urbane Überwärmung gegenüber der Station Warstein. 
Mit 20 Tropennächten in Köln (2023: 21) und nur 4 Tropennächten in Warstein (2023: 2) wird abermals ein starker Kontrast deutlich. Die Tageshöchsttemperaturen konnten mit jeweils rund 35 °C in Köln und 32,9 °C in Warstein jene des Vorjahres nicht ganz übertreffen, worüber gerade die Kölnerinnen und Kölner glücklich gewesen sein dürften. Die Tiefstwerte lagen mit rund 11,0 °C (VKTU) bzw. 7,4 °C (WAST) in Köln unter und in Warstein über den Vorjahreswerten. 

---

Um einen Einblick zu geben, wie das Temperaturgeschehen im November war, werden an zwei Stationen des LANUV-Luftqualitätsmessnetzes Temperatur-Kenntage ausgewertet. 
Dafür wird zum einen die Station Köln –Turiner Straße (VKTU) als eine innerstädtische Station einer Großstadt in der wärmebegünstigten Niederrheinischen Bucht und zum anderen die Station Warstein (WAST) in Warstein als ein Beispiel für eine Stadtrandlage in einer Mittelstadt am Nordrand des Sauerlands dargestellt.

Während an der Kölner Messstation keinerlei Temperaturkenntage erfasst wurden, konnten an der Station Warstein zwei Frosttage verzeichnet werden. 
Verglichen mit den Vorjahreswerten fielen die Tiefsttemperaturen des Novembers 2024 in Köln und Warstein um jeweils rund 1 °C bzw. 5 °C niedriger aus, die Höchsttemperaturen lagen an beiden Stationen in diesem Jahr um jeweils rund 3 °C höher als im November 2023.

---

Um einen Einblick zu geben, wie das Temperaturgeschehen im Winter war, werden an zwei Stationen des LANUV-Luftqualitätsmessnetzes Temperatur-Kenntage ausgewertet. 
Dafür wird zum einen die Station Köln –Turiner Straße (VKTU) als eine innerstädtische Station einer Großstadt in der wärmebegünstigten Niederrheinischen Bucht und zum anderen die Station Warstein (WAST) in Warstein als ein Beispiel für eine Stadtrandlage in einer Mittelstadt am Nordrand des Sauerlands dargestellt.
Lediglich zwei Frosttage wurden im Winter 2021/2022 an der Station Köln – Turiner Straße gemessen, an der Station Warstein waren es 21 Frosttage. 
Das sind jeweils fünf Frosttage weniger als noch im Vorjahr. Eistage wurden in diesem Winter an keiner der beiden Stationen erfasst; auch hier zeigt sich eine deutliche Abnahme gegenüber dem Winter 2020/2021. 
Zwar lagen die Tageshöchsttemperaturen in diesem Winter an den Stationen VKTU und WAST jeweils rund 4 °C und 5 °C unter den Werten des Vorjahres, doch die Tagestiefsttemperaturen waren an beiden Messstationen dafür signifikant höher, in Köln um gut 7 °C und in Warstein sogar um 11 °C.

"""

# template Wetterstation Übergangsmonate

template_wetterstation_trans_zero_shot = """ Du bist ein Meteorologe für Nordrhein Westfalen.

Erstelle einen informativen Absatz für einen Bericht über die Auswertung der Temperatur-Kenntage im {Monat} anhand der zwei Stationen des LANUV-Luftqualitätsmessnetzes - Station Köln – Turiner Straße (WKTU) und Station Warstein (WAST)). 

Erwähne den Kontrast zwischen Großstadt und Höhenlage, Vergleich der gegeben Temperatur-Kenntage der Wetterstationen sowie markante Unterschiede zum Vorjahr. 
Ordne die Daten in den Kontext des Monats- und Jahresverlaufs ein.

Hier die gegebenen Temperatur-Kenntage des aktuellen Jahres: 

    Berichtszeitraum:  
    - Berichtszeitraum aktuelles Jahr: {Jahr}
    - Berichtszeitraum aktuelle Zeiteinheit: {Monat}

    Temperatur-Kenntage für VKTU aktuelles Jahr:
    - Sommertage: {VKTU_sommertage}
    - heiße Tage: {VKTU_heißetage}
    - Tropennächte: {VKTU_tropennächte}
    - Frosttage: {VKTU_frost} 
    - Eistage: {VKTU_eis}
    - Tiefsttemperatur: {VKTU_tiefsttemperatur} °C
    - Höchstemperatur: {VKTU_höchsttemperatur} °C


    Temperatur-Kenntage für WAST aktuelles Jahr: 
    - Sommertage: {WAST_sommertage}
    - heiße Tage: {WAST_heißetage}
    - Tropennächte: {WAST_tropennächte}
    - Frosttage: {WAST_frost} 
    - Eistage: {WAST_eis}
    - Tiefsttemperatur: {WAST_tiefsttemperatur} °C
    - Höchstemperatur: {WAST_höchsttemperatur} °C


Hier die gegebenen Temperatur-Kenntage des Vorjahres: 
    
    Berichtszeitraum:  
    - Berichtszeitraum vorherigen Jahres: {Jahr_l_y}
    - Berichtszeitraum vorherigen Zeiteinheit: {Monat_l_y}

    Temperatur-Kenntage für VKTU letzten Jahres:
    - Sommertage: {VKTU_sommertage_l_y}
    - heiße Tage: {VKTU_heißetage_l_y}
    - Tropennächte: {VKTU_tropennächte_l_y}
    - Frosttage: {VKTU_frost_l_y} 
    - Eistage: {VKTU_eis_l_y}
    - Tiefsttemperatur: {VKTU_tiefsttemperatur_l_y} °C
    - Höchstemperatur: {VKTU_höchsttemperatur_l_y} °C

    Temperatur-Kenntage für WAST letzten Jahres: 
    - Sommertage: {WAST_sommertage_l_y}
    - heiße Tage: {WAST_heißetage}
    - Tropennächte: {WAST_tropennächte}
    - Frosttage: {WAST_frost_l_y} 
    - Eistage: {WAST_eis_l_y}
    - Tiefsttemperatur: {WAST_tiefsttemperatur_l_y} °C
    - Höchstemperatur: {WAST_höchsttemperatur_l_y} °C

Verwende einen sachlichen, informativen Schreibstil und halte die Länge bei etwa 150–200 Wörtern. Achte darauf, dass der Text flüssig und gut strukturiert ist. Schreibe nur den Absatz, ohne Überschrift.
"""


template_wetterstation_trans_CoT = """ Du bist ein Meteorologe für Nordrhein Westfalen.

Erstelle einen informativen Absatz für einen Bericht über die Auswertung der Temperatur-Kenntage im {Monat} anhand der zwei Stationen des LANUV-Luftqualitätsmessnetzes - Station Köln – Turiner Straße (WKTU) und Station Warstein (WAST)). 

Denke Schritt für Schritt und gehe dabei auf folgende Punkte ein:

Schritt 1: Allgemeine Wetterlage im {Monat} und eine kurze Einordnung, warum diese beiden Stationen ausgewählt wurden (Großstadt vs. Höhenlage).
    Folge dabei diesem Aufbau: 
        "Um einen Einblick zu geben, wie das Temperaturgeschehen im {Monat} war, werden an zwei Stationen des LANUV-Luftqualitätsmessnetzes Temperatur-Kenntage ausgewertet. 
        Dafür wird zum einen die Station Köln – Turiner Straße (VKTU), als eine innerstädtische Station einer Großstadt in der wärmebegünstigten Niederrheinischen Bucht, 
        und zum anderen die Station Warstein (WAST) in Warstein als ein Beispiel für eine Stadtrandlage in einer Mittelstadt am Nordrand des Sauerlands, dargestellt."

Schritt 2: Vergleich der beiden Stationen hinsichtlich der gegebenen Temperatur-Kenntage:
    Berichtszeitraum:  
    - Berichtszeitraum aktuelles Jahr: {Jahr}
    - Berichtszeitraum aktuelle Zeiteinheit: {Monat}

    Temperatur-Kenntage für VKTU aktuelles Jahr:
    - Sommertage: {VKTU_sommertage}
    - heiße Tage: {VKTU_heißetage}
    - Tropennächte: {VKTU_tropennächte}
    - Frosttage: {VKTU_frost} 
    - Eistage: {VKTU_eis}
    - Tiefsttemperatur: {VKTU_tiefsttemperatur} °C
    - Höchstemperatur: {VKTU_höchsttemperatur} °C


    Temperatur-Kenntage für WAST aktuelles Jahr: 
    - Sommertage: {WAST_sommertage}
    - heiße Tage: {WAST_heißetage}
    - Tropennächte: {WAST_tropennächte}
    - Frosttage: {WAST_frost} 
    - Eistage: {WAST_eis}
    - Tiefsttemperatur: {WAST_tiefsttemperatur} °C
    - Höchstemperatur: {WAST_höchsttemperatur} °C

    
Schritt 3: Erläuterung nur von markanten Unterschieden zwischen den Temperatur-Kenntagen dieses Jahres und dem Vorjahr.
    Berichtszeitraum:  
    - Berichtszeitraum vorherigen Jahres: {Jahr_l_y}
    - Berichtszeitraum vorherigen Zeiteinheit: {Monat_l_y}

    Temperatur-Kenntage für VKTU letzten Jahres:
    - Sommertage: {VKTU_sommertage_l_y}
    - heiße Tage: {VKTU_heißetage_l_y}
    - Tropennächte: {VKTU_tropennächte_l_y}
    - Frosttage: {VKTU_frost_l_y} 
    - Eistage: {VKTU_eis_l_y}
    - Tiefsttemperatur: {VKTU_tiefsttemperatur_l_y} °C
    - Höchstemperatur: {VKTU_höchsttemperatur_l_y} °C

    Temperatur-Kenntage für WAST letzten Jahres: 
    - Sommertage: {WAST_sommertage_l_y}
    - heiße Tage: {WAST_heißetage}
    - Tropennächte: {WAST_tropennächte}
    - Frosttage: {WAST_frost_l_y} 
    - Eistage: {WAST_eis_l_y}
    - Tiefsttemperatur: {WAST_tiefsttemperatur_l_y} °C
    - Höchstemperatur: {WAST_höchsttemperatur_l_y} °C


Schritt 4: Einordnung der Daten in den Kontext des Monats- und Jahresverlaufs.

Schritt 5: Umschreibe und verbessere den Bericht kontinuierlich

Verwende einen sachlichen, informativen Schreibstil und halte die Länge bei etwa 150–200 Wörtern. Achte darauf, dass der Text flüssig und gut strukturiert ist. Schreibe nur den Absatz, ohne Überschrift. """

template_wetterstation_trans_few_shots = """ Du bist ein Meteorologe für Nordrhein Westfalen.

Erstelle einen informativen Absatz für einen Bericht über die Auswertung der Temperatur-Kenntage im {Monat} anhand der zwei Stationen des LANUV-Luftqualitätsmessnetzes - Station Köln – Turiner Straße (WKTU) und Station Warstein (WAST)). 

Erwähne den Kontrast zwischen Großstadt und Höhenlage, Vergleich der gegeben Temperatur-Kenntage der Wetterstationen sowie markante Unterschiede zum Vorjahr. 
Ordne die Daten in den Kontext des Monats- und Jahresverlaufs ein.

Hier die gegebenen Temperatur-Kenntage des aktuellen Jahres: 

    Berichtszeitraum:  
    - Berichtszeitraum aktuelles Jahr: {Jahr}
    - Berichtszeitraum aktuelle Zeiteinheit: {Monat}

    Temperatur-Kenntage für VKTU aktuelles Jahr:
    - Sommertage: {VKTU_sommertage}
    - heiße Tage: {VKTU_heißetage}
    - Tropennächte: {VKTU_tropennächte}
    - Frosttage: {VKTU_frost} 
    - Eistage: {VKTU_eis}
    - Tiefsttemperatur: {VKTU_tiefsttemperatur} °C
    - Höchstemperatur: {VKTU_höchsttemperatur} °C


    Temperatur-Kenntage für WAST aktuelles Jahr: 
    - Sommertage: {WAST_sommertage}
    - heiße Tage: {WAST_heißetage}
    - Tropennächte: {WAST_tropennächte}
    - Frosttage: {WAST_frost} 
    - Eistage: {WAST_eis}
    - Tiefsttemperatur: {WAST_tiefsttemperatur} °C
    - Höchstemperatur: {WAST_höchsttemperatur} °C


Hier die gegebenen Temperatur-Kenntage des Vorjahres: 
    
    Berichtszeitraum:  
    - Berichtszeitraum vorherigen Jahres: {Jahr_l_y}
    - Berichtszeitraum vorherigen Zeiteinheit: {Monat_l_y}

    Temperatur-Kenntage für VKTU letzten Jahres:
    - Sommertage: {VKTU_sommertage_l_y}
    - heiße Tage: {VKTU_heißetage_l_y}
    - Tropennächte: {VKTU_tropennächte_l_y}
    - Frosttage: {VKTU_frost_l_y} 
    - Eistage: {VKTU_eis_l_y}
    - Tiefsttemperatur: {VKTU_tiefsttemperatur_l_y} °C
    - Höchstemperatur: {VKTU_höchsttemperatur_l_y} °C

    Temperatur-Kenntage für WAST letzten Jahres: 
    - Sommertage: {WAST_sommertage_l_y}
    - heiße Tage: {WAST_heißetage}
    - Tropennächte: {WAST_tropennächte}
    - Frosttage: {WAST_frost_l_y} 
    - Eistage: {WAST_eis_l_y}
    - Tiefsttemperatur: {WAST_tiefsttemperatur_l_y} °C
    - Höchstemperatur: {WAST_höchsttemperatur_l_y} °C

Verwende einen sachlichen, informativen Schreibstil und halte die Länge bei etwa 150–200 Wörtern. Achte darauf, dass der Text flüssig und gut strukturiert ist. 
Gebe dabei keine Prognose über das Klima, oder politische Statements ab, sondern bleibe bei den Daten die Du hast. Du gibst nur beschreibend die Temperatur-Kenntage der gegebenen Zeiteinheit wieder.
Schreibe nur den Absatz, ohne Überschrift.

Hier einige gegebene Beispiele: 

Um einen Einblick zu geben, wie das Temperaturgeschehen im April war, werden an zwei Stationen des LANUV-Luftqualitätsmessnetzes Temperatur-Kenntage ausgewertet. 
Dafür wird zum einen die Station Köln –Turiner Straße (VKTU) als eine innerstädtische Station einer Großstadt in der wärmebegünstigten Niederrheinischen Bucht und zum anderen die Station Warstein (WAST) in Warstein als ein Beispiel für eine Stadtrandlage in einer Mittelstadt am Nordrand des Sauerlands dargestellt.

Sowohl an der Kölner Station als auch in Warstein wurden in diesem April kaum temperaturbedingte Kenntage erfasst; lediglich in Warstein konnten vier Frosttage verzeichnet werden. Damit fiel die Bilanz ähnlich aus wie im Vorjahr (April 2022: 3 Frosttage an der Station WAST). 
Sommertage gab es im Gegensatz zu manch vorherigem Jahr noch nicht. Die Tiefsttemperaturen waren an beiden Stationen höher als im Vorjahr, wobei die Tiefsttemperatur an der Station in Warstein dieses Jahr etwa doppelt so hoch ausfiel wie im letzten (Differenz VKTU: 0,9 °C; WAST: 3,4 °C). 
Die Tageshöchsttemperaturen lagen in Warstein annähernd auf und in Köln sichtlich unter dem Vorjahresniveau (Differenz: ca. -3 °C).

---

Um einen Einblick zu geben, wie das Temperaturgeschehen im Februar war, werden an zwei Stationen des LANUV-Luftqualitätsmessnetzes Temperatur-Kenntage ausgewertet. 
Dafür wird zum einen die Station Köln –Turiner Straße (VKTU) als eine innerstädtische Station einer Großstadt in der wärmebegünstigten Niederrheinischen Bucht und zum anderen die Station Warstein (WAST) in Warstein als ein Beispiel für eine Stadtrandlage in einer Mittelstadt am Nordrand des Sauerlands dargestellt.

Weder in Köln (VKTU) noch in Warstein (WAST) konnte in diesem Jahr ein Eistag verzeichnet werden. Allerdings wurden, im Gegensatz zum Vorjahr, in Köln fünf Frosttage gemessen und in Warstein sogar mehr als doppelt so viele (elf). 
In Köln lag die Tiefsttemperatur mit -2,3 °C ca. 6 °C über und die Höchsttemperatur mit 16,2 °C in etwa auf dem Niveau des Wertes vom Februar 2024. In Warstein war die Tiefsttemperatur mit -4,8 °C fast drei Grad Celsius niedriger als letztes Jahr, die Höchsttemperatur mit 16,0 °C dagegen fast zwei Grad Celsius höher als im Februar 2024.

---

Um einen Einblick zu geben, wie das Temperaturgeschehen im Frühling war, werden an zwei Stationen des LANUV-Luftqualitätsmessnetzes Temperatur-Kenntage ausgewertet. Dafür wird zum einen die Station Köln –Turiner Straße (VKTU) als eine innerstädtische Station einer Großstadt in der wärmebegünstigten Niederrheinischen Bucht und zum anderen die Station Warstein (WAST) in Warstein als ein Beispiel für eine Stadtrandlage in einer Mittelstadt am Nordrand des Sauerlands dargestellt.
Der Sommer 2024 machte sich auch im Messnetz des LANUV bemerkbar, wie im Folgenden erläutert wird. In der Kölner Innenstadt (VKTU) wurden insgesamt 47 Sommertage verzeichnet, was exakt der Vorjahreszahl entspricht. 
Im höher gelegenen Warstein wurden insgesamt 31 Sommertage aufgezeichnet, womit die Anzahl von 25 Sommertagen vom Sommer 2023 übertroffen wurde. In der Kölner Innenstadt wurden im Sommer 2024 12 Heiße Tage registriert, in ländlichen Warstein 6 Heiße Tage. Auch hier zieht Köln mit dem Wert vom letzten Jahr gleich und Warstein hatte doppelt so viele Heiße Tage als im Sommer 2023. Bei der Anzahl der Tropennächte zeigt sich auch im Sommer 2024 klar die urbane Überwärmung gegenüber der Station Warstein. 
Mit 20 Tropennächten in Köln (2023: 21) und nur 4 Tropennächten in Warstein (2023: 2) wird abermals ein starker Kontrast deutlich. Die Tageshöchsttemperaturen konnten mit jeweils rund 35 °C in Köln und 32,9 °C in Warstein jene des Vorjahres nicht ganz übertreffen, worüber gerade die Kölnerinnen und Kölner glücklich gewesen sein dürften. Die Tiefstwerte lagen mit rund 11,0 °C (VKTU) bzw. 7,4 °C (WAST) in Köln unter und in Warstein über den Vorjahreswerten. 

---

Um einen Einblick zu geben, wie das Temperaturgeschehen im November war, werden an zwei Stationen des LANUV-Luftqualitätsmessnetzes Temperatur-Kenntage ausgewertet. 
Dafür wird zum einen die Station Köln –Turiner Straße (VKTU) als eine innerstädtische Station einer Großstadt in der wärmebegünstigten Niederrheinischen Bucht und zum anderen die Station Warstein (WAST) in Warstein als ein Beispiel für eine Stadtrandlage in einer Mittelstadt am Nordrand des Sauerlands dargestellt.

Während an der Kölner Messstation keinerlei Temperaturkenntage erfasst wurden, konnten an der Station Warstein zwei Frosttage verzeichnet werden. 
Verglichen mit den Vorjahreswerten fielen die Tiefsttemperaturen des Novembers 2024 in Köln und Warstein um jeweils rund 1 °C bzw. 5 °C niedriger aus, die Höchsttemperaturen lagen an beiden Stationen in diesem Jahr um jeweils rund 3 °C höher als im November 2023.

---

Um einen Einblick zu geben, wie das Temperaturgeschehen im Winter war, werden an zwei Stationen des LANUV-Luftqualitätsmessnetzes Temperatur-Kenntage ausgewertet. 
Dafür wird zum einen die Station Köln –Turiner Straße (VKTU) als eine innerstädtische Station einer Großstadt in der wärmebegünstigten Niederrheinischen Bucht und zum anderen die Station Warstein (WAST) in Warstein als ein Beispiel für eine Stadtrandlage in einer Mittelstadt am Nordrand des Sauerlands dargestellt.
Lediglich zwei Frosttage wurden im Winter 2021/2022 an der Station Köln – Turiner Straße gemessen, an der Station Warstein waren es 21 Frosttage. 
Das sind jeweils fünf Frosttage weniger als noch im Vorjahr. Eistage wurden in diesem Winter an keiner der beiden Stationen erfasst; auch hier zeigt sich eine deutliche Abnahme gegenüber dem Winter 2020/2021. 
Zwar lagen die Tageshöchsttemperaturen in diesem Winter an den Stationen VKTU und WAST jeweils rund 4 °C und 5 °C unter den Werten des Vorjahres, doch die Tagestiefsttemperaturen waren an beiden Messstationen dafür signifikant höher, in Köln um gut 7 °C und in Warstein sogar um 11 °C.


"""

# Template Jahresvergleich ----------------------------------------------------------------------------------------------------------------------------------


template_wetterstation_jahr_zero_shot = """ Du bist ein Meteorologe für Nordrhein Westfalen.

Erstelle einen informativen Absatz für einen Bericht über die Auswertung der Temperatur-Kenntage des aktuellen Jahres anhand der zwei Stationen des LANUV-Luftqualitätsmessnetzes - Station Köln – Turiner Straße (WKTU) und Station Warstein (WAST)). 

Erwähne den Kontrast zwischen Großstadt und Höhenlage, Vergleich der gegeben Temperatur-Kenntage der Wetterstationen sowie markante Unterschiede zum Vorjahr. 
Ordne die Daten in den Kontext des Monats- und Jahresverlaufs ein. Der Text sollte sachlich, informativ und etwa 150-200 Wörter lang sein.

Hier die gegebenen Temperatur-Kenntage des aktuellen Jahres: 

    Berichtszeitraum:  
    - Berichtszeitraum aktuelles Jahr: {Jahr}

    Temperatur-Kenntage für VKTU aktuelles Jahr:
    - Sommertage: {VKTU_sommertage}
    - heiße Tage: {VKTU_heißetage}
    - Tropennächte: {VKTU_tropennächte}
    - Frosttage: {VKTU_frost} 
    - Eistage: {VKTU_eis}
    - Tiefsttemperatur: {VKTU_tiefsttemperatur} °C
    - Höchstemperatur: {VKTU_höchsttemperatur} °C

    Temperatur-Kenntage für WAST aktuelles Jahr: 
    - Sommertage: {WAST_sommertage}
    - heiße Tage: {WAST_heißetage}
    - Tropennächte: {WAST_tropennächte}
    - Frosttage: {WAST_frost} 
    - Eistage: {WAST_eis}
    - Tiefsttemperatur: {WAST_tiefsttemperatur} °C
    - Höchstemperatur: {WAST_höchsttemperatur} °C


Hier die gegebenen Temperatur-Kenntage des Vorjahres: 
    
    Berichtszeitraum: 
    - Berichtszeitraum vorherigen Jahres: {Jahr_l_y}

    Temperatur Kenntage für VKTU letzten Jahres:
    - Sommertage: {VKTU_sommertage_l_y}
    - heiße Tage: {VKTU_heißetage_l_y}
    - Tropennächte: {VKTU_tropennächte_l_y}
    - Frosttage: {VKTU_frost_l_y} 
    - Eistage: {VKTU_eis_l_y}
    - Tiefsttemperatur: {VKTU_tiefsttemperatur_l_y} °C
    - Höchstemperatur: {VKTU_höchsttemperatur_l_y} °C

    Temperatur-Kenntage für WAST letzten Jahres: 
    - Sommertage: {WAST_sommertage_l_y}
    - heiße Tage: {WAST_heißetage_l_y}
    - Tropennächte: {WAST_tropennächte_l_y}
    - Frosttage: {WAST_frost_l_y} 
    - Eistage: {WAST_eis_l_y}
    - Tiefsttemperatur: {WAST_tiefsttemperatur_l_y} °C
    - Höchstemperatur: {WAST_höchsttemperatur_l_y} °C

Verwende einen sachlichen, informativen Schreibstil und halte die Länge bei etwa 150–200 Wörtern. Achte darauf, dass der Text flüssig und gut strukturiert ist. Schreibe nur den Absatz, ohne Überschrift.

"""



template_wetterstation_jahr_CoT = """ Du bist ein Meteorologe für Nordrhein Westfalen.

Erstelle einen informativen Absatz für einen Bericht über die Auswertung der Temperatur-Kenntage im Jahr anhand der zwei Stationen des LANUV-Luftqualitätsmessnetzes - Station Köln – Turiner Straße (WKTU) und Station Warstein (WAST)). 

Denke Schritt für Schritt und gehe dabei auf folgende Punkte ein:

Schritt 1: Allgemeine Wetterlage im Jahr {Jahr} und eine kurze Einordnung, warum diese beiden Stationen ausgewählt wurden (Großstadt vs. Höhenlage).
    Folge dabei diesem Aufbau: 
        "Um einen Einblick zu geben, wie das Temperaturgeschehen im Jahr {Jahr} war, werden an zwei Stationen des LANUV-Luftqualitätsmessnetzes Temperatur-Kenntage ausgewertet. 
        Dafür wird zum einen die Station Köln – Turiner Straße (VKTU), als eine innerstädtische Station einer Großstadt in der wärmebegünstigten Niederrheinischen Bucht, 
        und zum anderen die Station Warstein (WAST) in Warstein als ein Beispiel für eine Stadtrandlage in einer Mittelstadt am Nordrand des Sauerlands, dargestellt."

Schritt 2: Vergleich der beiden Stationen hinsichtlich der gegebenen Temperatur-Kenntage:
        Berichtszeitraum:  
        - Berichtszeitraum aktuelles Jahr: {Jahr}
    
        Temperatur-Kenntage für VKTU aktuelles Jahr:
        - Sommertage: {VKTU_sommertage}
        - heiße Tage: {VKTU_heißetage}
        - Tropennächte: {VKTU_tropennächte}
        - Frosttage: {VKTU_frost} 
        - Eistage: {VKTU_eis}
        - Tiefsttemperatur: {VKTU_tiefsttemperatur} °C
        - Höchstemperatur: {VKTU_höchsttemperatur} °C

        Temperatur-Kenntage für WAST aktuelles Jahr: 
        - Sommertage: {WAST_sommertage}
        - heiße Tage: {WAST_heißetage}
        - Tropennächte: {WAST_tropennächte}
        - Frosttage: {WAST_frost} 
        - Eistage: {WAST_eis}
        - Tiefsttemperatur: {WAST_tiefsttemperatur} °C
        - Höchstemperatur: {WAST_höchsttemperatur} °C

    
Schritt 3: Erläuterung nur von markanten Unterschieden zwischen den Temperatur-Kenntagen dieses Jahres und dem Vorjahr.
        Berichtszeitraum:  
        - Berichtszeitraum vorherigen Jahres: {Jahr_l_y}

        Temperatur Kenntage für VKTU letzten Jahres:
        - Sommertage: {VKTU_sommertage_l_y}
        - heiße Tage: {VKTU_heißetage_l_y}
        - Tropennächte: {VKTU_tropennächte_l_y}
        - Frosttage: {VKTU_frost_l_y} 
        - Eistage: {VKTU_eis_l_y}
        - Tiefsttemperatur: {VKTU_tiefsttemperatur_l_y} °C
        - Höchstemperatur: {VKTU_höchsttemperatur_l_y} °C

        Temperatur-Kenntage für WAST letzten Jahres: 
        - Sommertage: {WAST_sommertage_l_y}
        - heiße Tage: {WAST_heißetage_l_y}
        - Tropennächte: {WAST_tropennächte_l_y}
        - Frosttage: {WAST_frost_l_y} 
        - Eistage: {WAST_eis_l_y}
        - Tiefsttemperatur: {WAST_tiefsttemperatur} °C
        - Höchstemperatur: {WAST_höchsttemperatur} °C

Schritt 4: Einordnung der Daten in den Kontext des Monats- und Jahresverlaufs.

Schritt 5: Umschreibe und verbessere den Bericht kontinuierlich

Verwende einen sachlichen, informativen Schreibstil und halte die Länge bei etwa 150–200 Wörtern. Achte darauf, dass der Text flüssig und gut strukturiert ist. Schreibe nur die Einleitung, ohne Überschrift. """

template_wetterstation_jahr_few_shot = """Du bist ein Meteorologe für Nordrhein Westfalen.

Erstelle einen informativen Absatz für einen Bericht über die Auswertung der Temperatur-Kenntage des aktuellen Jahres anhand der zwei Stationen des LANUV-Luftqualitätsmessnetzes - Station Köln – Turiner Straße (WKTU) und Station Warstein (WAST)). 

Erwähne den Kontrast zwischen Großstadt und Höhenlage, Vergleich der gegeben Temperatur-Kenntage der Wetterstationen sowie markante Unterschiede zum Vorjahr. 
Ordne die Daten in den Kontext des Monats- und Jahresverlaufs ein. Der Text sollte sachlich, informativ und etwa 150-200 Wörter lang sein.

Hier die gegebenen Temperatur-Kenntage des aktuellen Jahres: 

    Berichtszeitraum:  
    - Berichtszeitraum aktuelles Jahr: {Jahr}

    Temperatur-Kenntage für VKTU aktuelles Jahr:
    - Sommertage: {VKTU_sommertage}
    - heiße Tage: {VKTU_heißetage}
    - Tropennächte: {VKTU_tropennächte}
    - Frosttage: {VKTU_frost} 
    - Eistage: {VKTU_eis}
    - Tiefsttemperatur: {VKTU_tiefsttemperatur} °C
    - Höchstemperatur: {VKTU_höchsttemperatur} °C

    Temperatur-Kenntage für WAST aktuelles Jahr: 
    - Sommertage: {WAST_sommertage}
    - heiße Tage: {WAST_heißetage}
    - Tropennächte: {WAST_tropennächte}
    - Frosttage: {WAST_frost} 
    - Eistage: {WAST_eis}
    - Tiefsttemperatur: {WAST_tiefsttemperatur} °C
    - Höchstemperatur: {WAST_höchsttemperatur} °C


Hier die gegebenen Temperatur-Kenntage des Vorjahres: 
    
    Berichtszeitraum: 
    - Berichtszeitraum vorherigen Jahres: {Jahr_l_y}

    Temperatur Kenntage für VKTU letzten Jahres:
    - Sommertage: {VKTU_sommertage_l_y}
    - heiße Tage: {VKTU_heißetage_l_y}
    - Tropennächte: {VKTU_tropennächte_l_y}
    - Frosttage: {VKTU_frost_l_y} 
    - Eistage: {VKTU_eis_l_y}
    - Tiefsttemperatur: {VKTU_tiefsttemperatur_l_y} °C
    - Höchstemperatur: {VKTU_höchsttemperatur_l_y} °C

    Temperatur-Kenntage für WAST letzten Jahres: 
    - Sommertage: {WAST_sommertage_l_y}
    - heiße Tage: {WAST_heißetage_l_y}
    - Tropennächte: {WAST_tropennächte_l_y}
    - Frosttage: {WAST_frost_l_y} 
    - Eistage: {WAST_eis_l_y}
    - Tiefsttemperatur: {WAST_tiefsttemperatur_l_y} °C
    - Höchstemperatur: {WAST_höchsttemperatur_l_y} °C

Verwende einen sachlichen, informativen Schreibstil und halte die Länge bei etwa 150–200 Wörtern. Achte darauf, dass der Text flüssig und gut strukturiert ist. 
Gebe dabei keine Prognose über das Klima, oder politische Statements ab, sondern bleibe bei den Daten die Du hast. Du gibst nur beschreibend die Temperatur-Kenntage der gegebenen Zeiteinheit wieder.
Schreibe nur den Absatz, ohne Überschrift.

hier einige gegebene Beispiele: 

Um einen Einblick zu geben, wie das Temperaturgeschehen im April war, werden an zwei Stationen des LANUV-Luftqualitätsmessnetzes Temperatur-Kenntage ausgewertet. 
Dafür wird zum einen die Station Köln –Turiner Straße (VKTU) als eine innerstädtische Station einer Großstadt in der wärmebegünstigten Niederrheinischen Bucht und zum anderen die Station Warstein (WAST) in Warstein als ein Beispiel für eine Stadtrandlage in einer Mittelstadt am Nordrand des Sauerlands dargestellt.

Sowohl an der Kölner Station als auch in Warstein wurden in diesem April kaum temperaturbedingte Kenntage erfasst; lediglich in Warstein konnten vier Frosttage verzeichnet werden. Damit fiel die Bilanz ähnlich aus wie im Vorjahr (April 2022: 3 Frosttage an der Station WAST). 
Sommertage gab es im Gegensatz zu manch vorherigem Jahr noch nicht. Die Tiefsttemperaturen waren an beiden Stationen höher als im Vorjahr, wobei die Tiefsttemperatur an der Station in Warstein dieses Jahr etwa doppelt so hoch ausfiel wie im letzten (Differenz VKTU: 0,9 °C; WAST: 3,4 °C). 
Die Tageshöchsttemperaturen lagen in Warstein annähernd auf und in Köln sichtlich unter dem Vorjahresniveau (Differenz: ca. -3 °C).

---

Um einen Einblick zu geben, wie das Temperaturgeschehen im Februar war, werden an zwei Stationen des LANUV-Luftqualitätsmessnetzes Temperatur-Kenntage ausgewertet. 
Dafür wird zum einen die Station Köln –Turiner Straße (VKTU) als eine innerstädtische Station einer Großstadt in der wärmebegünstigten Niederrheinischen Bucht und zum anderen die Station Warstein (WAST) in Warstein als ein Beispiel für eine Stadtrandlage in einer Mittelstadt am Nordrand des Sauerlands dargestellt.

Weder in Köln (VKTU) noch in Warstein (WAST) konnte in diesem Jahr ein Eistag verzeichnet werden. Allerdings wurden, im Gegensatz zum Vorjahr, in Köln fünf Frosttage gemessen und in Warstein sogar mehr als doppelt so viele (elf). 
In Köln lag die Tiefsttemperatur mit -2,3 °C ca. 6 °C über und die Höchsttemperatur mit 16,2 °C in etwa auf dem Niveau des Wertes vom Februar 2024. In Warstein war die Tiefsttemperatur mit -4,8 °C fast drei Grad Celsius niedriger als letztes Jahr, die Höchsttemperatur mit 16,0 °C dagegen fast zwei Grad Celsius höher als im Februar 2024.

---

Um einen Einblick zu geben, wie das Temperaturgeschehen im Frühling war, werden an zwei Stationen des LANUV-Luftqualitätsmessnetzes Temperatur-Kenntage ausgewertet. Dafür wird zum einen die Station Köln –Turiner Straße (VKTU) als eine innerstädtische Station einer Großstadt in der wärmebegünstigten Niederrheinischen Bucht und zum anderen die Station Warstein (WAST) in Warstein als ein Beispiel für eine Stadtrandlage in einer Mittelstadt am Nordrand des Sauerlands dargestellt.
Der Sommer 2024 machte sich auch im Messnetz des LANUV bemerkbar, wie im Folgenden erläutert wird. In der Kölner Innenstadt (VKTU) wurden insgesamt 47 Sommertage verzeichnet, was exakt der Vorjahreszahl entspricht. 
Im höher gelegenen Warstein wurden insgesamt 31 Sommertage aufgezeichnet, womit die Anzahl von 25 Sommertagen vom Sommer 2023 übertroffen wurde. In der Kölner Innenstadt wurden im Sommer 2024 12 Heiße Tage registriert, in ländlichen Warstein 6 Heiße Tage. Auch hier zieht Köln mit dem Wert vom letzten Jahr gleich und Warstein hatte doppelt so viele Heiße Tage als im Sommer 2023. Bei der Anzahl der Tropennächte zeigt sich auch im Sommer 2024 klar die urbane Überwärmung gegenüber der Station Warstein. 
Mit 20 Tropennächten in Köln (2023: 21) und nur 4 Tropennächten in Warstein (2023: 2) wird abermals ein starker Kontrast deutlich. Die Tageshöchsttemperaturen konnten mit jeweils rund 35 °C in Köln und 32,9 °C in Warstein jene des Vorjahres nicht ganz übertreffen, worüber gerade die Kölnerinnen und Kölner glücklich gewesen sein dürften. Die Tiefstwerte lagen mit rund 11,0 °C (VKTU) bzw. 7,4 °C (WAST) in Köln unter und in Warstein über den Vorjahreswerten. 

---

Um einen Einblick zu geben, wie das Temperaturgeschehen im November war, werden an zwei Stationen des LANUV-Luftqualitätsmessnetzes Temperatur-Kenntage ausgewertet. 
Dafür wird zum einen die Station Köln –Turiner Straße (VKTU) als eine innerstädtische Station einer Großstadt in der wärmebegünstigten Niederrheinischen Bucht und zum anderen die Station Warstein (WAST) in Warstein als ein Beispiel für eine Stadtrandlage in einer Mittelstadt am Nordrand des Sauerlands dargestellt.

Während an der Kölner Messstation keinerlei Temperaturkenntage erfasst wurden, konnten an der Station Warstein zwei Frosttage verzeichnet werden. 
Verglichen mit den Vorjahreswerten fielen die Tiefsttemperaturen des Novembers 2024 in Köln und Warstein um jeweils rund 1 °C bzw. 5 °C niedriger aus, die Höchsttemperaturen lagen an beiden Stationen in diesem Jahr um jeweils rund 3 °C höher als im November 2023.

---

Um einen Einblick zu geben, wie das Temperaturgeschehen im Winter war, werden an zwei Stationen des LANUV-Luftqualitätsmessnetzes Temperatur-Kenntage ausgewertet. 
Dafür wird zum einen die Station Köln –Turiner Straße (VKTU) als eine innerstädtische Station einer Großstadt in der wärmebegünstigten Niederrheinischen Bucht und zum anderen die Station Warstein (WAST) in Warstein als ein Beispiel für eine Stadtrandlage in einer Mittelstadt am Nordrand des Sauerlands dargestellt.
Lediglich zwei Frosttage wurden im Winter 2021/2022 an der Station Köln – Turiner Straße gemessen, an der Station Warstein waren es 21 Frosttage. 
Das sind jeweils fünf Frosttage weniger als noch im Vorjahr. Eistage wurden in diesem Winter an keiner der beiden Stationen erfasst; auch hier zeigt sich eine deutliche Abnahme gegenüber dem Winter 2020/2021. 
Zwar lagen die Tageshöchsttemperaturen in diesem Winter an den Stationen VKTU und WAST jeweils rund 4 °C und 5 °C unter den Werten des Vorjahres, doch die Tagestiefsttemperaturen waren an beiden Messstationen dafür signifikant höher, in Köln um gut 7 °C und in Warstein sogar um 11 °C.
"""

# Template Einleitung ----------------------------------------------------------------------------------------------------------------------------------


template_introduction_zero_shot = """Du bist Meteorologe für das Klima in Nordrhein Westfalen.
Erstelle einen Einleitungsabsatz für einen Bericht, der alle wichtigen Erkenntnisse und Informationen des Berichts kurz und markant für die Einleitung zusammenfasst. 

Bericht:
{report} 

Verwende einen sachlichen, informativen Schreibstil und halte die Länge bei etwa 150–200 Wörtern. Achte darauf, dass der Text flüssig und gut strukturiert ist. Schreibe nur die Einleitung, ohne Überschrift.

"""
template_introduction_CoT = """Du bist Meteorologe für das Klima in Nordrhein Westfalen.
Erstelle einen Einleitungsabsatz für einen Bericht, der alle wichtigen Erkenntnisse und Informationen des Berichts kurz und markant für die Einleitung zusammenfasst. 

Denke Schritt für Schritt:

Schritt 1: Hauptaussagen identifizieren: Welche zentralen Ergebnisse liefert der Bericht? Gibt es Trends, Auffälligkeiten oder extreme Wetterereignisse?
Schritt 2: Relevante Daten und Entwicklungen zusammenfassen: Sind klimatische Besonderheiten bemerkenswert?
Schritt 3: Einordnung der Ergebnisse: Welche Bedeutung haben diese Veränderungen für die Region? 
Schritt 4: Flüssige Einleitung formulieren: Verknüpfe die gewonnenen Erkenntnisse zu einem prägnanten Absatz. Vermeide Aufzählungen – stattdessen soll der Text eine zusammenhängende Einleitung mit klarer Struktur sein.
Schritt 5: Umschreibe und verbessere den Bericht kontinuierlich

Bericht:
{report}

Verwende einen sachlichen, informativen Schreibstil und halte die Länge bei etwa 150–200 Wörtern. Achte darauf, dass der Text flüssig und gut strukturiert ist. Schreibe nur die Einleitung, ohne Überschrift.
"""

template_introduction_few_shot = """Du bist Meteorologe für das Klima in Nordrhein Westfalen.
Erstelle einen Einleitungsabsatz für einen Bericht, der alle wichtigen Erkenntnisse und Informationen des Berichts kurz und markant für die Einleitung zusammenfasst. 

Bericht:
{report} 

Verwende einen sachlichen, informativen Schreibstil und halte die Länge bei etwa 150–200 Wörtern. Achte darauf, dass der Text flüssig und gut strukturiert ist. Schreibe nur die Einleitung, ohne Überschrift.

Hier einige gegebene Beispiele: 

Insgesamt verhielt sich der April in diesem Jahr so wie man es von einem April erwartet - typisch wechselhaft. 
Nach einem eher kühlen Monatsbeginn mit frostigen Nächten kletterten die Temperaturen bis zur zweiten Dekade in frühlingshafte Höhen, bevor sich eine unbeständige Wetterlage mit zahlreichen Niederschlägen bis hin zum Monatsende einstellte.

--- 

Auch in diesem Winter wollte sich einfach keine winterliche Wetterlage einstellen. 
Aufgrund der zu hohen Temperaturen fielen die Niederschläge in NRW in den Monaten Dezember, Januar und Februar überwiegend als Regen denn als Schnee und mehrere aufeinanderfolgende Tiefdrucksysteme im Februar sorgten zudem für außergewöhnliche Sturmlagen (siehe dazu Einordnung Februar 2022).

--- 

Der November 2024 brachte wenig Überraschendes und insgesamt viel Durchschnitt. 
Ganz wie man einen November erwartet, war er trüb, zeitweise nass, insgesamt noch nicht sonderlich kalt aber durchaus mit dem ersten Frost garniert. 
Gerade zu Beginn des Monats herrschte bei uns jedoch eine stabile Hochdruckwetterlage, die zu dieser Jahreszeit allerdings kein Garant mehr für viel Sonnenschein ist. 
Bedingt durch das hier vorherrschende stabile Hoch und dem Trend zu häufigeren blockierenden Wetterlagen, ereignete sich jedoch in Spanien eine Flutkatastrophe ernormen Ausmaßes. Im späteren Monatsverlauf zogen auch über NRW stärkere Tiefdruckgebiete mit größeren Regenmengen und Sturmböen hinweg, die aber als normal bezeichnet werden können. 
So ergeben sich in allen beobachteten Bereichen Werte die knapp über oder unter dem langjährigen Durchschnitt liegen.

--- 

Der Sommer 2024 startete temperaturmäßig im Juni dank einer ausgeprägten Schafskälte verglichen zur aktuellen Klimanormalperiode 1991-2020 leicht unterdurchschnittlich, um dann mit einer deutlichen Temperaturabweichung nach oben doch noch dem allgemeinen Trend zu immer höheren Temperaturen zu folgen. Bei den Sommermonaten in NRW gab es keine neuen Temperaturrekorde, im Gegensatz dazu waren die Sommermonate global laut dem EU-Klimadienst Copernicus die bisher wärmsten seit Beginn der Wetteraufzeichnungen. 
In NRW gab zahlreiche Gewitter und Starkregen, die regelmäßig für Schlagzeilen hinsichtlich überschwemmter Keller sorgten. 
Dennoch blieb die Niederschlagssumme insgesamt eher durchschnittlich. Damit setzt sich die Erholung von den Trockenjahren 2018-2022 fort. 
Während die Sonne im Juni und Juli noch durchschnittlich lange schien, musste zumindest im August mit deutlich überdurchschnittlichen Sonnenscheinlängen auch öfters einmal die Sonnencreme zum Einsatz kommen. 

---

Der Februar 2025 war überwiegend von Hochdruck geprägt. Das führte letztlich dazu, dass insbesondere die Niederschlagsbilanz in NRW seit längerer Zeit erstmals wieder deutlich unterdurchschnittlich ausfiel. Ebenfalls durch die verbreitete Hochdruckwetterlage bedingt, herrschten insbesondere in der ersten Monatshälfte eher kalte Temperaturen vor, bevor das Temperaturniveau in der letzten Februarwoche deutlich anstieg und zum Teil recht hohe zweistellige Temperaturwerte brachte. 
Unterm Strich lag der Februar daher letztlich im für die aktuelle Klimanormalperiode 1991-2020 normalen Bereich, sprich, knapp über dem Durchschnitt, und entsprechend deutlicher über dem Durchschnitt der Referenzperiode 1961-1990. Im Unterschied zu den Vormonaten bedeutet Hochdruck im Februar, aufgrund des bereits wieder höheren Sonnenstandes, nicht mehr automatisch auch neblig-trübes Wetter, so dass auch die Sonnenscheinstunden in diesem Jahr deutlich überdurchschnittlich ausfielen.



 """



def template_handler(paragraph: str, time_unit: str = None):

    # Winter
    if time_unit in settings.winter_template_set and settings.CoT and paragraph == "_station":
        return template_wetterstation_winter_CoT
    
    elif time_unit in settings.winter_template_set and settings.zero_shot and paragraph == "_station": 
        return template_wetterstation_winter_zero_shot
    
    elif time_unit in settings.winter_template_set and settings.few_shot and paragraph == "_station":
        return template_wetterstation_winter_few_shots
    
   # Übergangsmonate
    elif time_unit in settings.trans_season_set and settings.CoT and paragraph == "_station":
        return template_wetterstation_trans_CoT
    
    elif time_unit in settings.trans_season_set and settings.zero_shot and paragraph == "_station": 
        return template_wetterstation_trans_zero_shot
    
    elif time_unit in settings.trans_season_set and settings.few_shot and paragraph == "_station": 
        return template_wetterstation_trans_few_shots
    
    # Sommer
    elif time_unit in settings.sommer_template_set and settings.CoT and paragraph == "_station": 
        return template_wetterstation_Sommer_CoT 
    
    elif time_unit in settings.sommer_template_set and settings.zero_shot and paragraph == "_station": 
        return template_wetterstation_Sommer_zero_shot
    
    elif time_unit in settings.sommer_template_set and settings.few_shot and paragraph == "_station": 
        return template_wetterstation_sommer_few_shots
    
    # Jahr
    elif time_unit in settings.Jahr_template_set and settings.CoT and paragraph == "_station": 
        return template_wetterstation_jahr_CoT
    
    elif time_unit in settings.Jahr_template_set and settings.zero_shot and paragraph == "_station": 
        return template_wetterstation_jahr_zero_shot

    elif time_unit in settings.Jahr_template_set and settings.few_shot and paragraph == "_station": 
        return template_wetterstation_jahr_few_shot
    
    # CoT Temp, Rain, sun
    elif settings.CoT and paragraph == "_temp":
        return template_temp_CoT
    
    elif settings.CoT and paragraph == "_rain": 
        return template_rain_CoT 
    
    elif settings.CoT and paragraph == "_sun": 
        return template_sun_CoT

    # zero_shot Temp, Rain, sun
    elif settings.zero_shot and paragraph == "_temp":
        return template_temp_zero_shot
    
    elif settings.zero_shot and paragraph == "_rain": 
        return template_rain_zero_shot
    
    elif settings.zero_shot and paragraph == "_sun": 
        return template_sun_zero_shot
    
    # few_shot Temp, Rain, sun
    elif settings.few_shot and paragraph == "_temp":
        return template_temp_few_shot
    
    elif settings.few_shot and paragraph == "_rain": 
        return template_rain_few_shot
    
    elif settings.few_shot and paragraph == "_sun": 
        return template_sun_few_shot
    
    # Introduction 
    elif settings.zero_shot and paragraph == "_intro": 
        return template_introduction_zero_shot
    
    elif settings.CoT and paragraph == "_intro": 
        return template_introduction_CoT
    
    elif settings.few_shot and paragraph == "_intro": 
        return template_introduction_few_shot

