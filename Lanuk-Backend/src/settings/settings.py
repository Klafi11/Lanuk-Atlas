import os
from pydantic_settings import BaseSettings
from pathlib import Path
from typing import List, Callable, Tuple
from functools import lru_cache


"""Settings für Lanuk-Backend"""

#BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

class ModelSettings(BaseSettings):


    OPENAI_API_KEY: str
    ANTHROPIC_API_KEY: str
    DEEPSEEK_API_KEY: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    TVLY_API_KEY: str
    AIRTABLE_API_KEY: str
    APP_ID_AIR: str
    TABLE_ID_AIR: str
    OPENROUTER_BASE_URL: str
    OPENROUTER_API_KEY: str


    gpt_o3: str = "openai/o3"
    gpt_o3_mini: str = "openai/o3-mini"
    gpt_4_o: str = "openai/gpt-4o"
    gpt_o1: str = "openai/o1"
    gpt_4_1: str = "openai/gpt-4.1"
    gpt_4_1_mini: str = "openai/gpt-4.1-mini"
    gpt_4_1_nano: str = "openai/gpt-4.1-nano"
    

    #gpt_o3: str = "o3"
    #gpt_o3_mini: str = "o3-mini"
    #gpt_4_o: str = "gpt-4o"
    #gpt_o1: str = "o1"
    #gpt_4_1: str = "gpt-4.1-2025-04-14"
    #gpt_4_1_mini: str = "gpt-4.1-mini-2025-04-14"
    #gpt_4_1_nano: str = "gpt-4.1-nano-2025-04-14"
    

    #an_son_4 : str = "claude-sonnet-4-20250514"
    #an_son_3_7: str = "claude-3-7-sonnet-latest"
    #an_son_3_5: str = "claude-3-5-sonnet-latest"
    #an_ha_3_5: str = "claude-3-5-haiku-latest"
    #claude_op_4: str = "claude-opus-4-20250514"


    an_son_4 : str = "anthropic/claude-sonnet-4"
    #an_son_3_7: str = "claude-3-7-sonnet-latest"
    #an_son_3_5: str = "claude-3-5-sonnet-latest"
    #an_ha_3_5: str = "claude-3-5-haiku-latest"
    #claude_op_4: str = "claude-opus-4-20250514"

    v3_se: str = "deepseek/deepseek-chat"
    r1_se: str = "deepseek-reasoner"

    csv_header: List[str] = ["Model","Durchlaufs_id", "InContext_method","Timestamp", "Latenz", "Input_tokens", "Output_tokens", "Gesamt_tokens", "Kosten_in_USD"]

    #reporters: List[Tuple[Callable, str]] = [(gpt_reporter, gpt_o3_mini), 
                     #(claude_reporter, an_son_3_7),
                    # (deepseek_reporter, v3_se)]
    
    #CoT: list[]

    class Config: 
        env_file = ".env"
        env_file_encoding = "utf-8"
    


class Settings(BaseSettings): 

    Season_agg : dict[str, str] = {
        "WAST_frost": "sum",
        "WAST_eis": "sum",
        "WAST_sommertage": "sum",
        "WAST_heißetage": "sum", 
        "WAST_höchsttemperatur": "max", 
        "WAST_tiefsttemperatur": "min",
        "WAST_tropennächte": "sum",
        "VKTU_frost": "sum",
        "VKTU_eis": "sum",
        "VKTU_sommertage": "sum",
        "VKTU_heißetage": "sum", 
        "VKTU_höchsttemperatur": "max", 
        "VKTU_tiefsttemperatur": "min",
        "VKTU_tropennächte": "sum",
    }

    months: list[str] = ["Januar", "Februar", "März", "April", "Mai", "Juni", 
                    "Juli", "August", "September", "Oktober", "November", "Dezember"]
    
    seasons: list[str] = ["Winter", "Frühling", "Sommer", "Herbst"]

    year: list[str] = ["Jahr_agg"]


    winter_template_set: list[str] = ["Winter", "Februar", "Januar", "Dezember", "November", "März"]

    sommer_template_set: list[str] = ["Sommer", "August", "Juli", "Juni", "Mai", "September"]

    trans_season_set: list[str] = ["Herbst", "Frühling", "April", "Oktober"]

    Jahr_template_set: list[str] = ["Jahr_agg"]

    CoT: bool = False

    zero_shot: bool = False

    few_shot: bool = True

    svg_path: str = "/home/falk-stankat/Downloads/Icon_Klimaatlas.svg"

    image_path: str = "Icon_Klimaatlas.png"



@lru_cache()
def get_model_settings():

    return ModelSettings()

@lru_cache()
def get_settings():

    return Settings()

__all__ = ["get_settings", "get_model_settings"]