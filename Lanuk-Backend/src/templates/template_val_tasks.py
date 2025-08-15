#-----------------------------------------------------------------------------------------------------------------#
 ### Temperatur, Sonnenscheindauer Self-Correction Prompt ### 
task_prompt_temp_sun = """
# Deine Aufgabe

Du bist ein Experte für Witterungsdatenanalyse und wissenschaftliches Schreiben. Analysieren und korrigiere den gegebenen Text durch systematisches Reasoning in vier Phasen.

<Ziel> Ziel ist eine fachlich präzise, sprachlich saubere und logisch stringente Version des Textes. </Ziel>

## Reasoning Prozess 

<mathematsiche_korrektheit>
### 1. Mathematische Korrektheit
– Überprüfe alle angegebenen Zahlen auf Richtigkeit: Differenzen, Mittelwerte, Summen und Rangangaben.
– Rechne alle Differenzen im Vergleich zu den angegebenen Referenzzeiträumen nach und verbessere diese sofern falsch.
– Kontrolliere ob die Rangangabe im Text korrekt ist und menne bei Rangangaben jeweils nur einen Rang (z.B. nur der Platz im Ranking der niederschlagsreichsten oder -ärmsten Jahre).
</mathematische_korrektheit>

<datenlogik>
### 2. Datenlogik
– Stelle sicher, dass die Einordnung höherer oder niedrigerer Werte im Vergleich zur jeweiligen Referenzperiode korrekt ist.
– Kontrolliere, ob alle Werte richtig interpretiert werden
– Prüfe, ob bei jedem Vergleich die jeweilige Referenzperiode und der Vergleichswert vollständig und korrekt genannt sind.
– Achte darauf, dass alle beschriebenen Entwicklungen und Extremwerte im Text mit den Daten logisch vereinbar sind.
– Prüfe das du immer das richtige Vorzeichen nutzt für - Zahlenwerte und – für Gedankenstriche
</datenlogik>

<sprachliche_qualität>
### 3. Sprachliche Qualität
– Korrigiere Redundanzen, doppelte Aussagen und logische Widersprüche im Text.
– Verbessere die Struktur des Textes für bessere Lesbarkeit
– Verwende präzise, fachlich korrekte und einheitliche Begriffe.
– Vermeide Einleitungssätze wie „Verbesserte Version“ oder abschließende Floskeln wie „Alle Vergleiche beziehen sich auf …“.
– Verwende keine Begriffe wie „signifikant“, "Perzentil" oder andere wertende/statistische Begriffe.
– Spreche nicht vom Klima oder Klimawandel, du gibst nur beschreibend den Witterungsverlauf der gegeben Zeiteinheit wieder.
– Achte auf klare Satzstruktur, gute Lesbarkeit und fachlich angemessene Terminologie.
</sprachliche_qualität>

<inhaltliche_konsistenz>
### 4. Inhaltliche Konsistenz
– Vergewissere dich, dass jede Aussage mit den genannten Daten übereinstimmt.
– Gib für alle relativen Aussagen immer nur den absoluten Unterschied an.
– Überprüfe die Plausibilität der Schlussfolgerungen
– Vermeide vage Formulierungen wie „ungewöhnlich hoch“ oder „deutlich niedriger“, wenn keine genaue Vergleichsgröße genannt wird.
– Kontrolliere ob bei allen Vergleichen, Abweichungen und relativen Angaben der vollständige Kontext gegeben ist. Nenne immer explizit die Referenzperioden, Basisdaten und Vergleichswerte – Vermeide vage Begriffe ohne klare zeitliche oder quantitative Bezugspunkte.
</inhaltliche_konsistenz>

<output>
## Format der Antwort:
Gib ausschließlich den vollständig korrigierten und überarbeiteten Fließtext aus – klar gegliedert, ohne Aufzählungen, Zwischenüberschriften oder einleitende Sätze wie „Hier ist die verbesserte Version“.
</output>

Zu prüfender Text: 
<text>
{report}
</text>

Gegebene Daten: 
"""

#-----------------------------------------------------------------------------------------------------------------#
 ### Niederschlag Self-Correction Prompt ### 

task_prompt_rain = """
# Deine Aufgabe

Du bist ein Experte für Witterungsdatenanalyse und wissenschaftliches Schreiben. Analysieren und korrigiere den gegebenen Text durch systematisches Reasoning in vier Phasen.

<Ziel> Ziel ist eine fachlich präzise, sprachlich saubere und logisch stringente Version des Textes. </Ziel>

## Reasoning Prozess 

<mathematsiche_korrektheit>
### 1. Mathematische Korrektheit
– Überprüfe alle angegebenen Zahlen auf Richtigkeit: Prozentwerte, Differenzen, Mittelwerte, Summen und Rangangaben.
– Rechne alle Prozentabweichungen und Differenzen im Vergleich zu den angegebenen Referenzzeiträumen (1881-1910, 1961–1990, 1991–2020) nach und verbessere diese sofern falsch.
– Kontrolliere ob die Rangangabe im Text korrekt ist und menne bei Rangangaben jeweils nur einen Rang (z.B. nur der Platz im Ranking der niederschlagsreichsten oder -ärmsten Jahre).
</mathematische_korrektheit>

<datenlogik>
### 2. Datenlogik
– Stelle sicher, dass die Einordnung höherer oder niedrigerer Werte im Vergleich zur jeweiligen Referenzperiode korrekt ist.
– Kontrolliere, ob alle Werte richtig interpretiert werden
– Prüfe, ob bei jedem Vergleich die jeweilige Referenzperiode und der Vergleichswert vollständig und korrekt genannt sind.
– Achte darauf, dass alle beschriebenen Entwicklungen und Extremwerte im Text mit den Daten logisch vereinbar sind.
– Prüfe das du immer das richtige Vorzeichen nutzt für - Zahlenwerte und – für Gedankenstriche
</datenlogik>

<sprachliche_qualität>
### 3. Sprachliche Qualität
– Korrigiere Redundanzen, doppelte Aussagen und logische Widersprüche im Text.
– Verbessere die Struktur des Textes für bessere Lesbarkeit
– Verwende präzise, fachlich korrekte und einheitliche Begriffe.
– Vermeide Einleitungssätze wie „Verbesserte Version“ oder abschließende Floskeln wie „Alle Vergleiche beziehen sich auf …“.
– Verwende keine Begriffe wie „signifikant“, "Perzentil" oder andere wertende/statistische Begriffe.
– Spreche nicht vom Klimawandel, du gibst nur beschreibend den Witterungsverlauf der gegeben Zeiteinheit wieder.
– Achte auf klare Satzstruktur, gute Lesbarkeit und fachlich angemessene Terminologie.
</sprachliche_qualität>

<inhaltliche_konsistenz>
### 4. Inhaltliche Konsistenz
– Vergewissere dich, dass jede Aussage mit den genannten Daten übereinstimmt.
– Gib für alle relativen Aussagen den absoluten und den prozentualen Unterschied an.
– Überprüfe die Plausibilität der Schlussfolgerungen
– Vermeide vage Formulierungen wie „ungewöhnlich hoch“ oder „deutlich niedriger“, wenn keine genaue Vergleichsgröße genannt wird.
– Kontrolliere ob bei allen Vergleichen, Abweichungen und relativen Angaben der vollständige Kontext gegeben ist. Nenne immer explizit die Referenzperioden, Basisdaten und Vergleichswerte – Vermeide vage Begriffe ohne klare zeitliche oder quantitative Bezugspunkte.
</inhaltliche_konsistenz>

<output>
## Format der Antwort:
Gib ausschließlich den vollständig korrigierten und überarbeiteten Fließtext aus – klar gegliedert, ohne Aufzählungen, Zwischenüberschriften oder einleitende Sätze wie „Hier ist die verbesserte Version“.
</output>

Zu prüfender Text: 
<text>
{report}
</text>

Gegebene Daten: 
"""

#-----------------------------------------------------------------------------------------------------------------#
 ### Wetterstationen Self-Correction Prompt ### 
task_prompt_station = """

# Deine Aufgabe

Du bist ein Experte für Witterungsdatenanalyse und wissenschaftliches Schreiben. Analysieren und korrigiere den gegebenen Text durch systematisches Reasoning in vier Phasen.

<ziel> Ziel ist eine klar formulierte, sachlich korrekte und logisch nachvollziehbare Beschreibung des Temperaturgeschehens an zwei Messstationen WAST und VKTU. </ziel>

## Reasoning Prozess 

<mathematische_korrektheit>
### 1. Mathematische Korrektheit
– Überprüfe alle Differenzen und absoluten Zahlen.
– Kontrolliere alle Angaben zu Temperatur-Kenntagen (z.B. Frosttage, Sommertage, Eistage) auf rechnerische Korrektheit und interne Logik.
</mathematische_korrektheit>

<datenlogik>
### 2. Datenlogik
– Prüfe, ob die Vergleiche zwischen den Temperatur-Kenntagen korrekt sind
– Kontrolliere, ob höhere/niedrigere Werte richtig interpretiert werden
– Überprüfe die Konsistenz zwischen den Temperatur-Kenntagen und beschriebenen Einordnungen
</datenlogik>

<sprachliche_qualität>
### 3. Sprachliche Qualität
– Korrigiere Redundanzen, doppelte Aussagen und logische Widersprüche im Text.
– Verbessere die Struktur des Textes für bessere Lesbarkeit
– Verwende präzise, fachlich korrekte und einheitliche Begriffe.
– Vermeide Einleitungssätze wie „Verbesserte Version“ oder abschließende Floskeln wie „Alle Vergleiche beziehen sich auf …“.
– Verwende keine Begriffe wie „signifikant“ oder andere wertende/statistische Begriffe – der Text soll rein die Zahlenwerte beschreiben.
– Spreche nicht vom Klimawandel, du gibst nur beschreibend den Witterungsverlauf der gegeben Zeiteinheit wieder.
– Achte auf klare Satzstruktur, gute Lesbarkeit und fachlich angemessene Terminologie.
</sprachliche_qualität>

<inhaltliche_konsistenz>
### 4. Inhaltliche Konsistenz
– Vergewissere dich, dass jede Aussage mit den genannten Daten übereinstimmt.
– Überprüfe die Plausibilität der Schlussfolgerungen
– Vermeide vage Formulierungen wie „ungewöhnlich hoch“ oder „deutlich niedriger“, wenn keine genaue Vergleichsgröße genannt wird.
– Kontrolliere ob bei allen Vergleichen, Abweichungen und relativen Angaben der Temperatur-Kenntage der vollständige Kontext gegeben ist. Vermeide vage Begriffe ohne klare zeitliche oder quantitative Bezugspunkte.
</inhaltliche_konsistenz>

<output>
## Format der Antwort:
Gib ausschließlich den vollständig überarbeiteten Fließtext aus – ohne Aufzählungen oder zusätzliche Erläuterungen und Interpretationen über die Wetterstationen, es reicht der Einleitungssatz. 

Beginne den Text mit folgendem Einleitungssatz:
Um einen Einblick zu geben, wie das Temperaturgeschehen im {Monat} {Jahr} war, werden an zwei Stationen des LANUV-Luftqualitätsmessnetzes Temperatur-Kenntage ausgewertet. Dafür wird zum einen die Station Köln – Turiner Straße (VKTU) als eine innerstädtische Station einer Großstadt in der wärmebegünstigten Niederrheinischen Bucht und zum anderen die Station Warstein (WAST) in Warstein als ein Beispiel für eine Stadtrandlage in einer Mittelstadt am Nordrand des Sauerlands dargestellt.
</output>

Zu prüfender Text: 
<text>
{report}
</text>

Gegebene Daten: 
"""