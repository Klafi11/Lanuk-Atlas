
#-----------------------------------------------------------------------------------------------------------------#
 ### Daten für die jeweilge Zeiteinheit (verschiedene Ausprägungen je Berichtstyp ### 

# data Month
data_temp_month = """ 
Hiermit erhälst du die Daten für den die jeweilige aktuelle Zeiteinheit:
<data>
- Berichtszeitraum aktuelles Jahr: {year} 
- Berichtszeitraum aktueller Monat: {time_unit}
- Ranglistenplatz des aktuellen Monats seit 1881 für die Temperatur höchste Rangfolge: {ranking_temp}
- Durchschnittliche Temperatur des aktuellen Monats: {m_temp} °C
- Durchschnittliche monatliche Temperatur der Klimanormalperiode in den Jahren 1881-1910: {m_temp_80_10} °C
- Durchschnittliche monatliche Temperatur der Klimanormalperiode in den Jahren 1961-1990: {m_temp_60_90} °C
- Durchschnittliche monatliche Temperatur der Klimanormalperiode in den jahren 1991-2020: {m_temp_90_20} °C
</data>
"""

data_rain_month = """
<data>
Hier die gegebenen Daten:                           
- Berichtszeitraum aktuelles Jahr: {year} 
- Berichtszeitraum aktueller Monat: {time_unit}
- Ranglistenplatz des aktuellen Monats seit 1881 für die niederschlagreichste Rangfolge: {ranking_rain}
- Ranglistenplatz des aktuellen Monats seit 1881 für die niederschlagärmste Rangfolge: {ranking_rain_min}
- Durchschnittlicher Niederschlag des aktuellen Monats: {m_rain} l/m²
- Durchschnittlicher monatlicher Niederschlag der Klimanormalperiode in den Jahren 1881-1910: {m_rain_80_10} l/m²
- Durchschnittlicher monatlicher Niederschlag der Klimanormalperiode in den Jahren 1961-1990: {m_rain_60_90} l/m²
- Durchschnittlicher monatlicher Niederschlag der Klimanormalperiode in den Jahren 1991-2020: {m_rain_90_20} l/m²
</data>
"""


data_sun_month = """
<data>
Hier die gegebenen Daten:                          
- Berichtszeitraum aktuelles Jahr: {year} 
- Berichtszeitraum aktueller Monat: {time_unit}
- Ranglistenplatz des aktuellen Monats seit 1951 für die sonnenscheinreichste Rangfolge: {ranking_sun}
- Ranglistenplatz des aktuellen Monats seit 1951 für die sonnenscheinärmste Rangfolge: {ranking_sun_min}
- Durchschnittliche Sonnenscheindauer des aktuellen Monats: {m_sun} h
- Durchschnittliche monatliche Sonnenscheindauer der Klimanormalperiode in den Jahren 1951-1980: {m_sun_50_80} h
- Durchschnittliche monatliche Sonnenscheindauer der Klimanormalperiode in den Jahren 1961-1990: {m_sun_60_90} h
- Durchschnittliche monatliche Sonnenscheindauer der Klimanormalperiode in den Jahren 1991-2020: {m_sun_90_20} h
</data>
"""

# Data Seasion
data_temp_season = """
<data>
Hier die gegebenen Daten:                                  
- Berichtszeitraum aktuelles Jahr: {year} 
- Berichtszeitraum aktuelle Saison: {time_unit}
- Ranglistenplatz der aktuellen Saison seit 1881 für die Temperatur höchste Rangfolge: {ranking_temp}
- Durchschnittliche Temperatur der aktuellen Saison: {m_temp} °C
- Durchschnittliche saisonale Temperatur der Klimanormalperiode in den Jahren 1881-1910: {m_temp_80_10} °C
- Durchschnittliche saisonale Temperatur der Klimanormalperiode in den Jahren 1961-1990: {m_temp_60_90} °C
- Durchschnittliche saisonale Temperatur der Klimanormalperiode in den jahren 1991-2020: {m_temp_90_20} °C
</data>
"""

data_rain_season = """
<data>
Hier die gegebenen Daten:                           
- Berichtszeitraum aktuelles Jahr: {year} 
- Berichtszeitraum aktuelle Saison: {time_unit}
- Ranglistenplatz der aktuellen Saison seit 1881 für die niederschlagreichste Rangfolge: {ranking_rain}
- Ranglistenplatz der aktuellen Saison seit 1881 für die niederschlagärmste Rangfolge: {ranking_rain_min}
- Durchschnittlicher Niederschlag der aktuellen Saison: {m_rain} l/m²
- Durchschnittlicher saisonaler Niederschlag der Klimanormalperiode in den Jahren 1881-1910: {m_rain_80_10} l/m²
- Durchschnittlicher saisonaler Niederschlag der Klimanormalperiode in den Jahren 1961-1990: {m_rain_60_90} l/m²
- Durchschnittlicher saisonaler Niederschlag der Klimanormalperiode in den Jahren 1991-2020: {m_rain_90_20} l/m²
</data>"""

data_sun_season = """
<data>
Hier die gegebenen Daten:                                    
- Berichtszeitraum aktuelles Jahr: {year} 
- Berichtszeitraum aktuelle Saison: {time_unit}
- Ranglistenplatz der aktuellen Saison seit 1951 für die sonnenscheinreichste Rangfolge: {ranking_sun}
- Ranglistenplatz der aktuellen Saison seit 1951 für die sonnenscheinärmste Rangfolge: {ranking_sun_min}
- Durchschnittliche Sonnenscheindauer der aktuellen Saison: {m_sun} h
- Durchschnittliche saisonale Sonnenscheindauer der Klimanormalperiode in den Jahren 1951-1980: {m_sun_50_80} h
- Durchschnittliche saisonale Sonnenscheindauer der Klimanormalperiode in den Jahren 1961-1990: {m_sun_60_90} h
- Durchschnittliche saisonale Sonnenscheindauer der Klimanormalperiode in den Jahren 1991-2020: {m_sun_90_20} h
</data>
"""

#data year 

data_temp_year = """
<data>
Hier die gegebenen Daten:                               
- Berichtszeitraum aktuelles Jahr: {year} 
- Berichtszeitraum aktuelles Jahr: {time_unit}
- Ranglistenplatz des aktuellen Jahres seit 1881 für die Temperatur höchste Rangfolge: {ranking_temp}
- Durchschnittliche Temperatur des aktuellen Jahres: {m_temp} °C
- Durchschnittliche Temperatur der Klimanormalperiode in den Jahren 1881-1910: {m_temp_80_10} °C
- Durchschnittliche Temperatur der Klimanormalperiode in den Jahren 1961-1990: {m_temp_60_90} °C
- Durchschnittliche Temperatur der Klimanormalperiode in den jahren 1991-2020: {m_temp_90_20} °C
</data>"""

data_rain_year = """
<data>
Hier die gegebenen Daten:                                
- Berichtszeitraum aktuelles Jahr: {year} 
- Berichtszeitraum aktuelles Jahr: {time_unit}
- Ranglistenplatz des aktuellen Jahres seit 1881 für die niederschlagreichste Rangfolge: {ranking_rain}
- Ranglistenplatz des aktuellen Jahres seit 1881 für die niederschlagärmste Rangfolge: {ranking_rain_min}
- Durchschnittlicher Niederschlag des Berichtszeitraums der aktuellen Zeiteinheit: {m_rain} l/m²
- Durchschnittlicher Niederschlag der Klimanormalperiode in den Jahren 1881-1910: {m_rain_80_10} l/m²
- Durchschnittlicher Niederschlag der Klimanormalperiode in den Jahren 1961-1990: {m_rain_60_90} l/m²
- Durchschnittlicher Niederschlag der Klimanormalperiode in den Jahren 1991-2020: {m_rain_90_20} l/m²
</data>
"""

data_sun_year = """
<data>
Hier die gegebenen Daten:                                     
- Berichtszeitraum aktuelles Jahr: {year} 
- Berichtszeitraum aktuelles Jahr: {time_unit}
- Ranglistenplatz des aktuellen Jahres seit 1951 für die sonnenscheinreichste Rangfolge: {ranking_sun}
- Ranglistenplatz des aktuellen Jahres seit 1951 für die sonnenscheinärmste Rangfolge: {ranking_sun_min}
- Durchschnittliche Sonnenscheindauer des Berichtszeitraums der aktuellen Zeiteinheit: {m_sun} h
- Durchschnittliche Sonnenscheindauer der Klimanormalperiode in den Jahren 1951-1980: {m_sun_50_80} h
- Durchschnittliche Sonnenscheindauer der Klimanormalperiode in den Jahren 1961-1990: {m_sun_60_90} h
- Durchschnittliche Sonnenscheindauer der Klimanormalperiode in den Jahren 1991-2020: {m_sun_90_20} h
</data>
"""
# data Wetterstationen 

data_station_winter = """
<data>
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
</data>
"""

data_station_sommer = """
<data>
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
</data>
"""

data_station_trans = """
<data>
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
</data>
"""

data_station_year = """
<data>
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
</data>
"""