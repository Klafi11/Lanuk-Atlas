
# G-Eval Template 

eval_template = """Du bist ein Evaluator für Klimaatlas Berichte.
Du erhälst einen Klimaatlas Bericht, Bitte bewerte den Klimaatlas Bericht gemäß den
Bewertungskriterien und folge dabei den Evaluierungsschritten. 
Stelle sicher, dass du die Anweisungen sorgfältig liest und verstehst. 
Bitte Bewerte fair, offen und stabil. 

Bewertungssmetrik:
{criteria_titel}

Bewertungsbeschreibung: 
{criteria_description}

Bewertungskriterien: 
Score 1: {score1_description}
Score 2: {score2_description}
Score 3: {score3_description}
Score 4: {score4_description}
Score 5: {score5_description}
Score 6: {score6_description}

----- 

Evaluationschritte: 

1. Schreibe ein detailliertes Feedback, das die Qualität der Antwort strikt basierend auf der gegebenen Bewetungsmetrik, Bewertungsbeschreibung und den Bewertungskriterien beurteilt, ohne allgemein zu bewerten.
2. Nach dem Schreiben des Feedbacks, gebe eine Punktzahl an, die eine ganze Zahl zwischen 1 und 6 ist. Die Zahl sollt sich auf die Bewertungskriterien beziehen.
3. Das Ausgabeformat sollte wie folgt aussehen: "Feedback: (Schreibe ein Feedback für das Bewertungskriterium) [ERGEBNIS] (eine ganze Zahl von 1 bis 6).
4. Bitte generiere keine Eröffnung, Schlussfolgerung und Erklärung.

{clima_report}

### Feedback: 

"""