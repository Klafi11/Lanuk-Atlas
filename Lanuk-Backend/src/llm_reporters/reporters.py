from openai import OpenAI
from anthropic import Anthropic
from src.settings import get_model_settings
from src.utils import cost_latency
import asyncio

"""
reporters.py
===================

Startet parallele Anfragen an unterschiedliche LLMs
(über OpenRouter) und liefert deren Antworten zurück.

Komponenten
-----------
Clients
    - Openai_client:   OpenAI-kompatibler Client (OpenRouter) für GPT-Modelle.
    - Anthropic_client: OpenAI-kompatibler Client (OpenRouter) für Claude-Modelle.
    - Deepseek_client: OpenAI-kompatibler Client (OpenRouter) für DeepSeek-Modelle.

Reporter-Funktionen
    - gpt_reporter(prompt, input, model, run_id)
    - claude_reporter(prompt, input, model, run_id)
    - deepseek_reporter(prompt, input, model, run_id)

"""

model_settings = get_model_settings()

# Clients

#Openai_client = OpenAI(api_key = model_settings.OPENAI_API_KEY)
Openai_client = OpenAI(base_url = model_settings.OPENROUTER_BASE_URL, api_key = model_settings.OPENROUTER_API_KEY)

#Anthropic_client = Anthropic(api_key = model_settings.ANTHROPIC_API_KEY)

Anthropic_client = OpenAI(base_url = model_settings.OPENROUTER_BASE_URL, api_key = model_settings.OPENROUTER_API_KEY)

#Deepseek_client = OpenAI(api_key = model_settings.DEEPSEEK_API_KEY, base_url = "https://api.deepseek.com")

Deepseek_client = OpenAI(base_url = model_settings.OPENROUTER_BASE_URL, api_key = model_settings.OPENROUTER_API_KEY)


# DeepSeek Berichtsreporter
#@cost_latency
def deepseek_reporter(prompt: str, input:str, model: str, run_id: str): 
    response = Deepseek_client.chat.completions.create(
        model= model,
        messages=[
            {"role": "system", "content": prompt.format(**input)},
            #{"role": "user", "content": "Hello"},
        ],
        stream=False)
    return response

# OpenAI Berichtsreporter
#@cost_latency
def gpt_reporter(prompt:str, input:str, model: str, run_id: str):
    response = Openai_client.chat.completions.create(
        model = model,
        messages = [
            {"role": "system", "content": prompt.format(**input)},
            #{"role": "user", "content": input},
        ]
    )
    return response

# Antrophic Berichtsreporter
#@cost_latency
def claude_reporter(prompt:str, input:str, model: str, run_id: str):
    response = Anthropic_client.chat.completions.create(
        model = model,
        messages = [
           
           {"role": "user", "content": prompt.format(**input)}
    
        ]
    ) 
    return response


async def get_all_reports(prompt:str, data:dict, run_id:str):

    """"Führt parallele Modellaufrufe (GPT, Claude, DeepSeek) aus und sammelt die Antworten.
    
    Query-Parameter
    ---------------
    prompt : str
            jeweilige Prompt
    data : dict
            alle relevanten Daten für die Prompt
    run_id : str
            Tracking des run (optional)
    Returns
    -------
    dict : Dictionary der generierten Berichtabschnitte der jeweiligen Sprachmodelle
    
    """
    
    value_llms = {}

    llm_reporters = [
        (gpt_reporter, model_settings.gpt_4_1),
        (claude_reporter, model_settings.an_son_4),
        (deepseek_reporter, model_settings.v3_se)
    ]
    
    loop = asyncio.get_event_loop()
    async def run_reporter(index, reporter_func, model):
        
        result = await loop.run_in_executor(
                None,
                lambda: reporter_func(prompt, data, model, run_id)
            )
        return index, result
    

    tasks = [run_reporter(i, v[0], v[1]) for i, v in enumerate(llm_reporters)]
    

    results = await asyncio.gather(*tasks)
    
    for index, result in results:
            value_llms[index] = result
        
    return value_llms


def eval_reporter(prompt, input): 
    response = Openai_client.chat.completions.create(
        model = model_settings.gpt_o1,
        messages = [
            {"role": "system", "content": prompt.format(**input)},
            #{"role": "user", "content": input},
        ]
    )
    return response
