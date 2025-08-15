from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from langchain_openai import ChatOpenAI
from src.settings import get_model_settings
from .models import RelatedSubjects, structuredSum
from .templates_s import related_topics_prompt, summarize_prompt_f, summarize_prompt
import asyncio
from tavily import AsyncTavilyClient

# clients & settings
settings = get_model_settings()

llm_sum = ChatOpenAI(model = settings.gpt_4_1,  openai_api_base = settings.OPENROUTER_BASE_URL, openai_api_key = settings.OPENROUTER_API_KEY)
llm_sum_nano = ChatOpenAI(model = settings.gpt_4_1_nano, openai_api_base = settings.OPENROUTER_BASE_URL, openai_api_key = settings.OPENROUTER_API_KEY)
tavily_client = AsyncTavilyClient(api_key=settings.TVLY_API_KEY)


def expand_topics(Bericht:dict, year:int, time_unit:str):

    """Expandiert Themen aus dem Klimaatlasbericht.

    Die Absätze werden in eine feste, lesbare Reihenfolge gebracht und
    an ein LLM übergeben, das verwandte Themenvorschläge erzeugt.

    Args
    ---------------
    year : int
        Jahr
    time_unit : str        
        Zeiteinheit
    Bericht : dict
        Berichtsabschnitte.

    Returns
    -------
    Liste von Themenvorschlägen (Queries) für die weitere Recherche
    """

    Items_string = """

    {Absatz}:
    {content}
    """ 


    items_list = []
    for index, content in Bericht.items():
        
        if index == "4":
            value = Items_string.format(Absatz = "Einleitung", content = content)

        elif index == "0":
            value = Items_string.format(Absatz = "Temperatur", content = content)

        elif index == "1": 
            value = Items_string.format(Absatz = "Niederschlag", content = content)

        elif index == "2": 
            value = Items_string.format(Absatz = "Sonnenscheindauer", content = content)
        else: 
            continue
        items_list.append(value)


    Bericht = "\n".join(items_list[i] for i in [3,0,1,2])


    expand_chain = related_topics_prompt | llm_sum_nano.with_structured_output(RelatedSubjects)
    
    queries = expand_chain.invoke({"bericht": Bericht, "year":year, "time_unit": time_unit})

    return queries.topics

async def pre_summarization(queries:list[str], year:int, time_unit:str):

    """Sucht hochwertige Quellen zu Themenvorschlägen und erstellt Roh-Zusammenfassungen.

    1) Sucht pro Query (Tavily) bis zu MAX_RESULTS_PER_QUERY Ergebnisse.
    2) Filtert nach Score, meidet BLOCKED_DOMAINS, dedupliziert und senkt
       iterativ die Score-Schwelle, bis TARGET_URL_COUNT erreicht ist
       (oder MIN_THRESHOLD unterschritten wird).
    3) Extrahiert die Inhalte und erzeugt pro Quelle eine kurze LLM-Zusammenfassung zu Wetterereignissen.

    Args
    ---------------
        queries : list[str]
            Themenvorschläge aus expand_topics für die Recherche.
        year : int
            Jahr.
        time_unit : str
            Zeiteinheit.
    Returns
    -------
        Liste aus Dicts mit "out" (Kurzsummary) und "url".
    """

    list_q = [{"query": i, "search_depth": "advanced", "max_results": 2} for i in queries]



    responses = await asyncio.gather(*[tavily_client.search(**q) for q in list_q])

    blocked_domains = ["klimaatlas.nrw.de"]

    relevant_urls = []
    threshold = 0.9

    while len(relevant_urls) < 7:
        for response in responses:
            for result in response.get('results', []):
                url = result.get("url", "")
                score = result.get('score', 0)
                if score > threshold and not any(domain in url for domain in blocked_domains):
                    if url not in relevant_urls:
                        relevant_urls.append(url)
        threshold -= 0.05




    extracted_data = await asyncio.gather(*(tavily_client.extract(url) for url in relevant_urls))

    data_sum = [data["results"][0] for data in extracted_data if data.get("results") and len(data["results"]) > 0]

    
    
    sum_chain = summarize_prompt_f | llm_sum_nano

    async def run_summary(v):
        out = await sum_chain.ainvoke({
        "inhalt": v.get("raw_content"),
        "year": year,
        "time_unit": time_unit
    })
    
        return {"out": out.content, "url": v.get("url")}


    res = await asyncio.gather(*[run_summary(v) for v in data_sum])

    return res

def summarization(pre_result:list[dict], year:int, time_unit:str):

    """Fügt mehrere Kurz-Zusammenfassungen zu einer strukturierten Endsummary zusammen.

    Args
    ---------------
        pre_result : list[dict] 
            Liste aus Roh-Zusammenfassungen und URLs von pre_summarization.
        year : int
            Jahr
        time_unit: str
            Zeiteinheit
    Returns
    -------
        Instanz von `structuredSum` (Pydantic-Modell), erzeugt über LLM structured output.
    """
    
    item_format = """
    Inhalt {i}:
    {content}
    Url des Content:
    {url}
    ------------------------------
    """

    repeated_section = "\n".join(
        item_format.format(i=idx + 1, content=content["out"], url = content["url"])
        for idx, content in enumerate(pre_result)
    )


    result_chain = summarize_prompt | llm_sum.with_structured_output(structuredSum)
    output = result_chain.invoke({"inhalt": repeated_section, "year": year, "time_unit": time_unit})

    return output