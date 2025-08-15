import os
import pdfplumber
import json
from openai import OpenAI


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

1. Schreibe ein detailliertes Feedback, das die Qualität der Antwort strikt basierend auf den gegebenen Bewertungskriterien beurteilt, ohne allgemein zu bewerten.
2. Nach dem Schreiben des Feedbacks, gebe eine Punktzahl an, die eine ganze Zahl zwischen 1 und 6 ist. Die Zahl sollt sich auf die Bewertungskriterien beziehen.
3. Das Ausgabeformat sollte wie folgt aussehen: "Feedback: (Schreibe ein Feedback für das Bewertungskriterium) [ERGEBNIS] (eine ganze Zahl von 1 bis 6).
4. Bitte generiere keine Eröffnung, Schlussfolgerung und Erklärung.

{clima_report}

### Feedback: 

"""


Openai_client = OpenAI(api_key = "")

def eval_reporter(prompt, input): 
    response = Openai_client.chat.completions.create(
        model = "gpt-4o",
        messages = [
            {"role": "system", "content": prompt.format(**input)},
            #{"role": "user", "content": input},
        ]
    )
    return response



def evaluation(): 
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    join_dir = os.path.join(base_dir, "../reports_first_it")
    target_dir = os.listdir(os.path.abspath(join_dir))
    
    for report in target_dir: 
        
        reports = os.path.join(base_dir, "../reports_first_it/", report)

        filename = os.path.basename(reports)
        filename = filename.split('/')[0].split(".")[0]
        

        with pdfplumber.open(reports) as pdf:
            all_text = "\n".join([page.extract_text(layout = True) for page in pdf.pages if page.extract_text()])

        
        with open("/home/falk-stankat/Lanuv_report/lanuv_report/evaluation/eval_rubric.json") as file:
            metrics = json.load(file)
        
        os.makedirs(f"./evaluation/{filename}", exist_ok= True)
        
        for metric in metrics: 
            
            metric["clima_report"] = all_text

            output = eval_reporter(eval_template, metric)

        
        
            with open(f"./evaluation/{filename}/{metric["criteria_titel"].replace(" ", "_")}.txt", "w") as f:
                    f.write(output.choices[0].message.content)


evaluation()


