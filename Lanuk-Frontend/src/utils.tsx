
const mapping_table_headers = (CurrentIndex: number, year: string, Saison: string) => {

    /* Funktion für das Anpassen der Tabellenüberschriften im Informationsreiter Daten*/
    
    if (CurrentIndex === 0) {
        return {
            "m_temp_80_10": "1881–1910",
            "m_temp_60_90": "1961–1990",
            "m_temp_90_20": "1991–2020",
            "m_temp": year,
            "ranking_temp": "Rang Temp."
          };
        }
    if (CurrentIndex === 1) {
        return {
            "m_rain_80_10": "1881–1910",
            "m_rain_60_90": "1961–1990",
            "m_rain_90_20": "1991–2020",
            "m_rain": year,
            "ranking_rain": "Rang Nieds.↑",
            "ranking_rain_min": "Rang Nieds.↓"
          };
        }
    
    if (CurrentIndex === 2) {
        return {
            "m_sun_50_80": "1951–1980",
            "m_sun_60_90": "1961–1990",
            "m_sun_90_20": "1991–2020",
            "m_sun": year,
            "ranking_sun": "Rang Sonnenschd.↑",
            "ranking_sun_min": "Rang Sonnenschd.↓"
          };

        }
    
        if (CurrentIndex === 3) {
        
        if (Saison === "Sommer") {
            
            return {
                "sommertage": "Sommertage",
                "heißetage": "Heiße Tage",
                "tropennächte":"Tropennächte",
                "tiefsttemperatur": "Tiefsttemperaturen",
                "höchsttemperatur": "Höchsttemperaturen"
            }
        }
        if (Saison === "Winter") {

            return {
                "frost": "Frosttage",
                "eis": "Eistage",
                "tiefsttemperatur": "Tiefsttemperaturen",
                "höchsttemperatur": "Höchsttemperaturen"
            }

            }
        if (Saison === "Herbst" || Saison === "Frühling" || Saison === "Jahr_agg") {
            return {
                "frost": "Frosttage",
                "eis": "Eistage",
                "sommertage": "Sommertage",
                "heißetage": "Heiße Tage",
                "tropennächte":"Tropennächte",
                "tiefsttemperatur": "Tiefsttemperaturen",
                "höchsttemperatur": "Höchsttemperaturen"

            }
        }
            


    }

    }
        

export default mapping_table_headers;

    
