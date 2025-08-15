#-----------------------------------------------------------------------------------------------------------------#
 ### Strukturierter Aufbau der jeweiligen Berichtsabschnitte ### 

template_aufbau_temp = """
<aufbau>
Folge dem Aufbau sowie dem Inhalt für die Monatsberichte in <reference_materials> <previous_months> und halte dich an diese Struktur:
## Textstruktur:

### Einordnung des analysierten Zeitraums
– Beispiel: "Die Durchschnittstemperatur lag im [Monat] [Jahr] bei 13,6 °C und damit zum Teil deutlich über den Mittelwerten aller Klimanormalperioden (...)

### Klimanormalperioden-Abweichungen:
– Berechnung und Darstellung der Abweichungen des aktuellen zu allen relevanten Klimanormalperioden
– Explizite Nennung der Referenzperioden
– Einordnung der Abweichungswerte in Kelvin 
– Beispiel: "Gegenüber der Referenzperiode 1961-1990 ergibt sich eine positive Abweichung von 1,2 K, während die Abweichung zur aktuellen Klimanormalperiode 1991-2020 lediglich 0,3 K betrug. 
Dieser [Monat] liegt im oberen Mittelfeld der wärmsten [Monat] monate seit Beginn der Aufzeichnungen 1881.
  
### Vergleich der Klimanormalperioden:
– Abschließender Verlaufsvergleich zwischen den verschiedenen Klimanormalperioden
– Darstellung der Entwicklung/Veränderung zwischen den Perioden
– Keine Interpretation oder Abweichungsberechnungen der Vergleichsperioden, du gibst nur beschreibend den Verlauf wieder
– Beispiel: "Der Vergleich der Klimanormalperioden 1881-1910 (12,2 °C), 1961-1990 (12,4 °C) und 1991-2020 (13,3 °C) verdeutlicht den kontinuierlichen Anstieg der Lufttemperatur um insgesamt 1,1 K seit Messbeginn."
</aufbau>
"""

template_aufbau_rain = """
<aufbau>
Folge dem Aufbau sowie dem Inhalt für die Monatsberichte in <reference_materials> <previous_months> und halte dich an diese Struktur:
## Textstruktur:

### Einordnung des analysierten Zeitraums
– Beispiel: "Der [Monat] [Jahr] präsentierte sich in Nordrhein-Westfalen mit 48 l/m² Niederschlag letztlich als moderat feuchter Monat (...)"

### Klimanormalperioden-Abweichungen:
– Berechnung und Darstellung der Abweichungen des aktuellen Wertes zu allen relevanten Klimanormalperioden
– Explizite Nennung der Referenzperioden
– Einordnung der Abweichungswerte in l/m² und %
– Beispiel: "Im Vergleich zur aktuellen Klimanormalperiode 1991-2020 (177 l/m²) wurde ein Defizit von 62 l/m² (-35%) verzeichnet, während die Abweichung zur Referenzperiode 1961-1990 mit -90 l/m² (-44%) noch deutlicher ausfiel."
        
### Vergleich der Klimanormalperioden:
– Abschließender Verlaufsvergleich zwischen den verschiedenen Klimanormalperioden
– Darstellung der Entwicklung/Veränderung zwischen den Perioden
– Keine Interpretation oder Abweichungsberechnungen der Vergleichsperioden, du gibst nur beschreibend den Verlauf wieder
– Beispiel: "Im Vergleich der Klimanormalperioden wird deutlich, dass die aktuelle Klimanormalperiode 1991-2020 (64 l/m²) einen ähnlich niedrigen Wert wie die erste Klimanormalperiode 1881-1910 (60 l/m²) aufweist, während der Referenzzeitraum 1961-1990 (72 l/m²) ein wenig feuchter ausfiel.
</aufbau>
"""

template_aufbau_sun = """
<aufbau>
Folge dem Aufbau sowie dem Inhalt für die Monatsberichte in <reference_materials> <previous_months> und halte dich an diese Struktur:
## Textstruktur:
### Einordnung des analysierten Zeitraums
– Beispiel: "Der Mai 2025 war mit 257 Sonnenstunden erneut außergewöhnlich sonnig (...)"

### Klimanormalperioden-Abweichungen:
– Berechnung und Darstellung der Abweichungen des aktuellen Wertes zu allen relevanten Klimanormalperioden
– Explizite Nennung der Referenzperioden
– Einordnung der Abweichungswerte in h
– Beispiel: "Verglichen mit den beiden betrachteten Vergleichsperioden lag dieser [Monat] im Durchschnitt der Referenzperiode 1961-1990 (42 h), aber gegenüber der aktuellen Klimanormalperiode 1991-2020 (51 h) acht Stunden im Minus."
        
### Vergleich der Klimanormalperioden:
– Abschließender Verlaufsvergleich zwischen den verschiedenen Klimanormalperioden
– Darstellung der Entwicklung/Veränderung zwischen den Perioden
– Keine Interpretation oder Abweichungsberechnungen der Vergleichsperioden, du gibst nur beschreibend den Verlauf wieder
– Beispiel: "Der Vergleich der Klimanormalperioden 1951-1980 (154 h), 1961-1990 (148 h) und 1991-2020 (174 h) verdeutlicht den kontinuierlichen Anstieg der Sonnenstunden, um insgesamt 20 h seit Messbeginn."
</aufbau>
"""

template_aufbau_temp_season = """
<aufbau>
Folge dem Aufbau sowie dem Inhalt für die Saisonberichte in <reference_materials> <previous_saisons> und halte dich an diese Struktur:
## Textstruktur:

### Einordnung des analysierten Zeitraums
– Beispiel: "Die Durchschnittstemperatur lag im [Monat] [Jahr] bei 13,6 °C und damit zum Teil deutlich über den Mittelwerten aller Klimanormalperioden (...)

### Klimanormalperioden-Abweichungen:
– Berechnung und Darstellung der Abweichungen des aktuellen Zeitraums zu allen relevanten Klimanormalperioden
– Explizite Nennung der Referenzperioden
– Einordnung der Abweichungswerte in Kelvin
– Beispiel: "Gegenüber der Referenzperiode 1961-1990 ergibt sich eine positive Abweichung von 1,2 K, während die Abweichung zur aktuellen Klimanormalperiode 1991-2020 lediglich 0,3 K betrug. 
Dieser [Saison] liegt im oberen Mittelfeld der wärmsten [Saison] seit Beginn der Aufzeichnungen 1881.

### Einordnung der Monate in den Kontext der Saison
– Monatsverlaufsdarstellung
– Achte dabei darauf die Monate nur wie im Beispiel darzustellen, ohne Abweichungsberechnung
– Beispiel: "Eine Betrachtung der Einzelmonate zeigt, dass [Monat] (7,0 °C) und [Monat] (11,0 °C) im oberen Bereich ihrer jeweiligen Zeitreihen lagen und auch der diesjährige [Monat] überdurchschnittlich warm ausfiel, 
was das anhaltend milde Temperaturniveau in der aktuellen [Saison] zusätzlich unterstreicht.
        
### Vergleich der Klimanormalperioden:
– Abschließender Verlaufsvergleich zwischen den verschiedenen Klimanormalperioden
– Darstellung der Entwicklung/Veränderung zwischen den Perioden
– Keine Interpretation oder Abweichungsberechnungen der Vergleichsperioden, du gibst nur beschreibend den Verlauf wieder
– Beispiel: "Der Vergleich der Klimanormalperioden 1881-1910 (12,2 °C), 1961-1990 (12,4 °C) und 1991-2020 (13,3 °C) verdeutlicht den kontinuierlichen Anstieg der Lufttemperatur um insgesamt 1,1 K seit Messbeginn." 
</aufbau>
"""

template_aufbau_rain_season = """
<aufbau>
Folge dem Aufbau sowie dem Inhalt für die Saisonberichte in <reference_materials> <previous_saisons> und halte dich an diese Struktur:
## Textstruktur:

### Einordnung des analysierten Zeitraums
– Beispiel: "Der [Saison] [Jahr] war mit nur 115 l/m² Niederschlag (...)"

### Klimanormalperioden-Abweichungen:
– Berechnung und Darstellung der Abweichungen des aktuellen Zeitraums zu allen relevanten Klimanormalperioden
– Explizite Nennung der Referenzperioden
– Einordnung der Abweichungswerte in l/m² und %
Beispiel: "Im Vergleich zur aktuellen Klimanormalperiode 1991-2020 (177 l/m²) wurde ein Defizit von 62 l/m² (-35%) verzeichnet, während die Abweichung zur Referenzperiode 1961-1990 mit -90 l/m² (-44%) noch deutlicher ausfiel."

### Einordnung der Monate in den Kontext der Saison
– Monatsverlaufsdarstellung
– Achte dabei darauf die Monate nur wie im Beispiel darzustellen, ohne Abweichungsberechnung
Beispiel: "Ein Blick in die Einzelmonate zeigt, dass sich hinter der recht niedrigen Gesamtsumme erhebliche monatliche Unterschiede verbergen: Während der [Monat] [Jahr] mit 10 l/m² den zweittrockensten [Monat] seit Messbeginn darstellte, war der [Monat] mit immerhin 58 l/m² Gesamtniederschlag relativ durchschnittlich. Im [Monat] [Jahr] hingegen fiel mit 48 l/m² wieder deutlich weniger Niederschlag."

### Vergleich der Klimanormalperioden:
– Abschließender Verlaufsvergleich zwischen den verschiedenen Klimanormalperioden
– Darstellung der Entwicklung/Veränderung zwischen den Perioden
– Keine Interpretation oder Abweichungsberechnungen der Vergleichsperioden, du gibst nur beschreibend den Verlauf wieder
Beispiel: "Im Vergleich der Klimanormalperioden seit 1881 verzeichneten die [Saison] Niederschläge zunächst einen Anstieg von ursprünglich 172 l/m² (1881-1910) auf 205 l/m² (1961-1990), ehe sie wieder annähernd auf das Ausgangsniveau sanken (1991-2020) 177 l/m²."
</aufbau>
"""

template_aufbau_sun_season = """
<aufbau>
Folge dem Aufbau sowie dem Inhalt für die Saisonberichte in <reference_materials> <previous_saisons> und halte dich an diese Struktur:
## Textstruktur:

### Einordnung des analysierten Zeitraums
– Beispiel: "Der Frühling 2025 verzeichnete in Nordrhein-Westfalen mit 717 Sonnenscheinstunden einen extrem überdurchschnittlichen Wert, (...)" 

### Klimanormalperioden-Abweichungen:
– Berechnung und Darstellung der Abweichungen des aktuellen Zeitraums zu allen relevanten Klimanormalperioden
– Explizite Nennung der Referenzperioden
– Einordnung der Abweichungswerte in h
– Beispiel: "der ganze 276 Stunden über dem Referenzmittel der Periode 1961-1990 (441 h) sowie 220 Stunden unter dem aktuellen Klimanormalwert 1991-2020 (497 h) liegt."

### Einordnung der Monate in den Kontext der Saison
– Monatsverlaufsdarstellung
– Achte dabei darauf die Monate nur wie im Beispiel darzustellen, ohne Abweichungsberechnung
– Beispiel: "Besonders prägend war der außergewöhnlich sonnige [Monat] mit rund 213 Stunden, doch auch die Monate [Monat] (248 h) und [Monat] (257 h) landeten jeweils in den Top 10 ihrer jeweiligen Zeitreihen."

### Vergleich der Klimanormalperioden:
– Abschließender Verlaufsvergleich zwischen den verschiedenen Klimanormalperioden
– Darstellung der Entwicklung/Veränderung zwischen den Perioden
– Keine Interpretation oder Abweichungsberechnungen der Vergleichsperioden, du gibst nur beschreibend den Verlauf wieder
Beispiel: "Im Vergleich zu den drei betrachteten Klimanormalperioden zeigt sich eine kontinuierliche Zunahme der Sonnenscheindauer. Historisch betrachtet reiht er sich in die Phase der letzten Jahre ein, in der überdurchschnittliche Werte dominieren und lediglich der [Saison] 2024 diesen Trend leicht unterschreitet."
</aufbau>
"""

template_aufbau_temp_year = """
<aufbau>
Folge dem Aufbau sowie dem Inhalt für die Jahresberichte in <reference_materials> <previous_years> und halte dich an diese Struktur:
## Textstruktur:

### Einordnung des analysierten Zeitraums
– Beispiel: "Die Durchschnittstemperatur lag im [Jahr] bei 13,6 °C und damit zum Teil deutlich über den Mittelwerten aller Klimanormalperioden (...)

### Klimanormalperioden-Abweichungen:
– Berechnung und Darstellung der Abweichungen des aktuellen Zeitraums zu allen relevanten Klimanormalperioden
– Explizite Nennung der Referenzperioden
– Einordnung der Abweichungswerte in Kelvin
– Beispiel: "Gegenüber der Referenzperiode 1961-1990 ergibt sich eine positive Abweichung von 1,2 K, während die Abweichung zur aktuellen Klimanormalperiode 1991-2020 lediglich 0,3 K betrug. 
Dieses [Jahr] liegt im oberen Mittelfeld der wärmsten Jahre seit Beginn der Aufzeichnungen 1881.

### Einordnung der Monate in den Kontext des Jahres
– Monatsverlaufsdarstellung
– Achte dabei darauf die Monate aggregiert nur wie im Beispiel darzustellen, ohne Abweichungsberechnung
– Beispiel: "Im Vergleich zur aktuellen Klimanormalperiode 1991-2020 gilt dies ebenfalls für alle Monate, mit einer Ausnahme: der [Monat] fiel ganz leicht unterdurchschnittlich aus. Insbesondere die Frühjahrsmonate sowie Spätsommer und Herbst zeigen deutlich überdurchschnittliche Temperaturwerte."
        
### Vergleich der Klimanormalperioden:
– Abschließender Verlaufsvergleich zwischen den verschiedenen Klimanormalperioden
– Darstellung der Entwicklung/Veränderung zwischen den Perioden
– Keine Interpretation oder Abweichungsberechnungen der Vergleichsperioden, du gibst nur beschreibend den Verlauf wieder
– Beispiel: "Der Vergleich der Klimanormalperioden 1881-1910 (12,2 °C), 1961-1990 (12,4 °C) und 1991-2020 (13,3 °C) verdeutlicht den kontinuierlichen Anstieg der Lufttemperatur um insgesamt 1,1 K seit Messbeginn." 
</aufbau>
"""

template_aufbau_rain_year = """
<aufbau>
Folge dem Aufbau sowie dem Inhalt für die Jahresberichte in <reference_materials> <previous_years> und halte dich an diese Struktur:
## Textstruktur:

### Einordnung des analysierten Zeitraums
– Beispiel: "Das [Jahr] war mit nur 1012 l/m² Niederschlag (...)"

### Klimanormalperioden-Abweichungen:
– Berechnung und Darstellung der Abweichungen des aktuellen Zeitraums zu allen relevanten Klimanormalperioden
– Explizite Nennung der Referenzperioden
– Einordnung der Abweichungswerte in l/m² und %
Beispiel: "Im Vergleich zur aktuellen Klimanormalperiode 1991-2020 (177 l/m²) wurde ein Defizit von 62 l/m² (-35%) verzeichnet, während die Abweichung zur Referenzperiode 1961-1990 mit -90 l/m² (-44%) noch deutlicher ausfiel."

### Einordnung der Monate in den Kontext des Jahres
– Monatsverlaufsdarstellung
– Achte dabei darauf die Monate aggregiert nur wie im Beispiel darzustellen, ohne Abweichungsberechnung
– Beispiel: "Das Jahr setzte sich eher feucht fort. Im Vergleich zur Referenzperiode 1961-1990 lag die Niederschlagssumme in fast allen Monaten - mit Ausnahme des [Monat] und des [Monat] - über dem langjährigen Mittelwert. Im Vergleich mit der aktuellen Klimanormalperiode hatten nur der [Monat] und der [Monat] eine unterdurchschnittliche Niederschlagssumme."

### Vergleich der Klimanormalperioden:
– Abschließender Verlaufsvergleich zwischen den verschiedenen Klimanormalperioden
– Darstellung der Entwicklung/Veränderung zwischen den Perioden
– Keine Interpretation oder Abweichungsberechnungen der Vergleichsperioden, du gibst nur beschreibend den Verlauf wieder
Beispiel: "Im Vergleich der Klimanormalperioden seit 1881 verzeichneten das [Jahr] Niederschläge zunächst einen Anstieg von ursprünglich 172 l/m² (1881-1910) auf 205 l/m² (1961-1990), ehe sie wieder annähernd auf das Ausgangsniveau sanken (1991-2020) 177 l/m²."
</aufbau>
"""

template_aufbau_sun_year = """
<aufbau>
Folge dem Aufbau sowie dem Inhalt für die Jahresberichte in <reference_materials> <previous_saisons> und halte dich an diese Struktur:
## Textstruktur:

### Einordnung des analysierten Zeitraums
– Beispiel: "Das Jahr 2025 verzeichnete in Nordrhein-Westfalen mit 1453 Sonnenscheinstunden einen extrem überdurchschnittlichen Wert, (...)" 

### Klimanormalperioden-Abweichungen:
– Berechnung und Darstellung der Abweichungen des aktuellen Zeitraums zu allen relevanten Klimanormalperioden
– Explizite Nennung der Referenzperioden
– Einordnung der Abweichungswerte in h
– Beispiel: "der ganze 276 Stunden über dem Referenzmittel der Periode 1961-1990 (441 h) sowie 220 Stunden unter dem aktuellen Klimanormalwert 1991-2020 (497 h) liegt."

### Einordnung der Monate in den Kontext des Jahres
– Monatsverlaufsdarstellung
– Achte dabei darauf die Monate aggregiert nur wie im Beispiel darzustellen, ohne Abweichungsberechnung
– Beispiel: "Besonders prägend war der außergewöhnlich sonnige [Monat] mit rund 213 Stunden, doch auch die Monate [Monat] (248 h) und [Monat] (257 h) landeten jeweils in den Top 10 ihrer jeweiligen Zeitreihen."

### Vergleich der Klimanormalperioden:
– Abschließender Verlaufsvergleich zwischen den verschiedenen Klimanormalperioden
– Darstellung der Entwicklung/Veränderung zwischen den Perioden
– Keine Interpretation oder Abweichungsberechnungen der Vergleichsperioden, du gibst nur beschreibend den Verlauf wieder
Beispiel: "Im Vergleich zu den drei betrachteten Klimanormalperioden zeigt sich eine kontinuierliche Zunahme der Sonnenscheindauer. Historisch betrachtet reiht er sich in die Phase der letzten Jahre ein, in der überdurchschnittliche Werte dominieren und lediglich das Jahr diesen Trend leicht unterschreitet."
</aufbau>
"""