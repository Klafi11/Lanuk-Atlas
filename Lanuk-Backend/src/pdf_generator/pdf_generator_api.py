from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from datetime import date
from reportlab.lib.colors import HexColor
import os
import cairosvg
from src.retrieval_functions import get_temp, get_rain, get_sun, get_station
from src.settings import get_settings
from io import BytesIO

"""
pdf_generator_api.py
=================
Dieses Modul erstellt PDF-Wetterberichte auf Basis historischer und aktueller Klimadaten.

Funktionen:
    create_weather_report_api(year, time_unit, data):
        Erstellt einen PDF-Wetterbericht für ein bestimmtes Jahr und Zeiteinheit
        (z. B. Jahr, Saison) mit Temperatur-, Niederschlags-, Sonnenschein- und Stationsdaten.

Klassen:
    BackgroundDocTemplate:
        Eine angepasste Version von `SimpleDocTemplate`, die beim Beginn jeder Seite einen
        farbigen Hintergrund und ein Logo rendert.

"""


settings = get_settings()

# Remove custom font registration and use default fonts
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='Date', fontName='Helvetica', fontSize=10, textColor=colors.black))
styles.add(ParagraphStyle(name='Normal_custom', fontName='Helvetica', fontSize=10, leading=14, alignment=4, firstLineIndent=0))

# Laden des Logos
svg_logo_path = settings.svg_path
png_logo_path = settings.image_path

class BackgroundDocTemplate(SimpleDocTemplate):

    # Custom Hintergrund Funktion

    def handle_pageBegin(self):
        self.canv.saveState()
        self.canv.setFillColor(HexColor("#E6F0FF"))
        self.canv.rect(0, 0, self.width + 2 * self.leftMargin, self.height + 2 * self.topMargin, fill=1, stroke=0)
        
        # Logo code 
        if os.path.exists(png_logo_path):
            logo_width, logo_height = 120, 100
            x_position = self.width + self.leftMargin - 90
            y_position = self.height + self.topMargin - 20
            self.canv.drawImage(png_logo_path, x_position, y_position, width=logo_width, height=logo_height, preserveAspectRatio=True, mask="auto")
        
        self.canv.restoreState()
        return super().handle_pageBegin()



def create_weather_report_api(year:int, time_unit:str, data:dict):
    
    
    """
    Erstellen des PDF-Reports aus den Berichtsabschnitten

    Args
    ---------------
    year : int
            Jahr
    time_unit : str        
            Zeiteinheit
    data : dict
            Daten für den PDF-Report
    Returns
    -------
    PDF-Report : Rückgabe des PDF-Reports
    """

    elements = []

    svg_logo_path = "/home/falk-stankat/Downloads/Icon_Klimaatlas.svg"
    png_logo_path = "Icon_Klimaatlas.png"


    year = int(year)
    
    if os.path.exists(svg_logo_path) and not os.path.exists(png_logo_path):
        cairosvg.svg2png(url=svg_logo_path, write_to=png_logo_path)
    


    if settings.CoT: 
        incontext = "CoT"
    elif settings.few_shot: 
        incontext = "few_shot"
    elif settings.zero_shot: 
        incontext = "zero_shot"

    buffer = BytesIO()

    # Hintergrund

    doc = BackgroundDocTemplate(buffer, pagesize=A4, leftMargin=2*cm, rightMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm)
    doc.title = f"{year}-{time_unit}-{incontext}"
       
    # Titel

    title = Paragraph(str(data.get("5")), styles["Title"]) if data.get("5") else Paragraph(f"Der {time_unit} {year}", styles["Title"]) if time_unit != "Jahr_agg" else Paragraph(f"Das Jahr: {year}", styles["Title"]) 
    elements.append(title)
    
    # Datum

    today = date.today().strftime("%d.%m.%Y")
    date_text = Paragraph(f"{today}", styles['Date'])
    elements.append(date_text)
    elements.append(Spacer(1, 5*mm))

    # Einleitungstext

    #title_intro_op = Paragraph("OpenAI", styles['Heading4'])
    intro_text_op = f"""{data["4"]}"""
    #elements.append(title_intro_op)
    elements.append(Paragraph(intro_text_op, styles['Normal_custom']))

    #title_intro_claude = Paragraph("Claude", styles['Heading4'])
    #intro_text_claude = f"""{data["tags"][4]["value"][0][1]}"""
    #elements.append(title_intro_claude)
    #elements.append(Paragraph(intro_text_claude, styles['Normal_custom']))

    #title_intro_deeps = Paragraph("Deepseek", styles['Heading4'])
    #intro_text_deeps = f"""{data["tags"][4]["value"][0][2]}"""
    #elements.append(title_intro_deeps)
    #elements.append(Paragraph(intro_text_deeps, styles['Normal_custom']))


    #Temperatur Paragraph

    title_temp = Paragraph("Temperatur", styles['Heading3'])
    elements.append(title_temp)
    elements.append(Spacer(1, 5*mm))

    # Temperatur Tabelle

    temp_values = get_temp(year, time_unit)
    
    table_style_t_r_s = TableStyle([
        ('BACKGROUND', (0, 0), (3, 0), colors.darkblue),
        ('TEXTCOLOR', (0, 0), (3, 0), colors.white),
        ('ALIGN', (0, 0), (3, 1), 'CENTER'),
        ('FONTNAME', (0, 0), (3, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (3, 1), 9),
        ('GRID', (0, 0), (3, 1), 0.5, colors.black)])
    
    temp_data = [['1881-1910', '1961-1990', '1991-2020', str(year)], [f"{temp_values["m_temp_80_10"]} °C", 
                                                                   f'{temp_values["m_temp_60_90"]} °C', 
                                                                   f'{temp_values["m_temp_90_20"]} °C',
                                                                   f'{temp_values["m_temp"]} °C']]
    
    temp_table = Table(temp_data, colWidths=[4*cm, 4*cm, 4*cm, 4*cm])
    temp_table.setStyle(table_style_t_r_s)

    elements.append(temp_table)
    elements.append(Spacer(1, 5*mm))

    #title_temp_op = Paragraph("OpenAI", styles['Heading4'])
    #elements.append(title_temp_op)
    temp_text_op= f"""{data["0"]} """
    elements.append(Paragraph(temp_text_op, styles["Normal_custom"]))

    #title_temp_claude = Paragraph("Claude", styles['Heading4'])
    #elements.append(title_temp_claude)
    #temp_text_claude = f"""{data["tags"][0]["value"][0][1]} """
    #elements.append(Paragraph(temp_text_claude, styles["Normal_custom"]))

    #title_temp_deeps = Paragraph("Deepseek", styles['Heading4'])
    #elements.append(title_temp_deeps)
    #temp_text_deeps = f"""{data["tags"][0]["value"][0][2]} """
    #elements.append(Paragraph(temp_text_deeps, styles["Normal_custom"]))   

    
    
    # Niederschlag Tabelle
    title_rain = Paragraph("Niederschlag", styles['Heading3'])
    elements.append(title_rain)
    elements.append(Spacer(1, 5*mm))
    rain_values = get_rain(year, time_unit)
    
    rain_data = [['1881-1910', '1961-1990', '1991-2020', str(year)], [f"{rain_values["m_rain_80_10"]} l/m²", 
                                                                   f'{rain_values["m_rain_60_90"]} l/m²', 
                                                                   f'{rain_values["m_rain_90_20"]} l/m²',
                                                                   f'{rain_values["m_rain"]} l/m²']]
    rain_table = Table(rain_data, colWidths=[4*cm, 4*cm, 4*cm, 4*cm])
    rain_table.setStyle(table_style_t_r_s)
    elements.append(rain_table)
    elements.append(Spacer(1, 5*mm))

    # Niederschlag Paragraph
    
    #title_rain_op = Paragraph("OpenAI", styles['Heading4'])
    rain_text_op = f"""{data["1"]}"""
    #elements.append(title_rain_op)
    elements.append(Paragraph(rain_text_op, styles["Normal_custom"]))

    #title_rain_claude = Paragraph("Claude", styles['Heading4'])
    #rain_text_claude = f"""{data["tags"][1]["value"][0][1]}"""
    #elements.append(title_rain_claude)
    #elements.append(Paragraph(rain_text_claude, styles["Normal_custom"]))

    #title_rain_deeps = Paragraph("Deepseek", styles['Heading4'])
    #rain_text_deeps = f"""{data["tags"][1]["value"][0][2]}"""
    #elements.append(title_rain_deeps)
    #elements.append(Paragraph(rain_text_deeps, styles["Normal_custom"]))

    # Sonnenscheindauer Paragraph

    title_sun = Paragraph("Sonnenscheindauer", styles['Heading3'])
    elements.append(title_sun)
    elements.append(Spacer(1, 5*mm))

    sun_values = get_sun(year, time_unit)

    # Sonnenscheindauer Tabelle

    sun_data = [['1951-1980', '1961-1990', '1991-2020', str(year)], [f"{sun_values["m_sun_50_80"]} h", 
                                                                   f'{sun_values["m_sun_60_90"]} h', 
                                                                   f'{sun_values["m_sun_90_20"]} h',
                                                                   f'{sun_values["m_sun"]} h']]
    sun_table = Table(sun_data, colWidths=[4*cm, 4*cm, 4*cm, 4*cm])
    sun_table.setStyle(table_style_t_r_s)
    elements.append(sun_table)
    elements.append(Spacer(1, 5*mm))

    #title_sun_op = Paragraph("OpenAI", styles['Heading4'])
    sun_text_op = f"""{data["2"]}"""
    #elements.append(title_sun_op)
    elements.append(Paragraph(sun_text_op, styles["Normal_custom"]))


    #title_sun_claude = Paragraph("Claude", styles['Heading4'])
    #sun_text_claude = f"""{data["tags"][2]["value"][0][1]}"""
    #elements.append(title_sun_claude)
    #elements.append(Paragraph(sun_text_claude, styles["Normal_custom"]))


    #title_sun_deeps = Paragraph("Deepseek", styles['Heading4'])
    #sun_text_deeps = f"""{data["tags"][2]["value"][0][2]}"""
    #elements.append(title_sun_deeps)
    #elements.append(Paragraph(sun_text_deeps, styles["Normal_custom"]))



    # StationsDaten Paragraph & Tabelle
    title_station = Paragraph("Kenntageauswertung", styles['Heading3'])
    elements.append(title_station)
    elements.append(Spacer(1, 5*mm))

    station_values = get_station(year, time_unit, ["VKTU", "WAST"])
    
    if time_unit in settings.winter_template_set:

        station_data = [[f"Kenntage im {time_unit} \n {year}", "WAST", "VKTU"], 
                        ["Frosttage",f"{station_values["WAST_frost"][0]}", f"{station_values["VKTU_frost"][0]}"], 
                        ["Eistage", f"{station_values["WAST_eis"][0]}", f"{station_values["VKTU_eis"][0]}"], 
                        ["Tiefsttemperatur", f"{station_values["WAST_tiefsttemperatur"][0]} °C", f"{station_values["VKTU_tiefsttemperatur"][0]} °C"], 
                        ["Höchsttemperatur", f"{station_values["WAST_höchsttemperatur"][0] } °C", f"{station_values["VKTU_höchsttemperatur"][0]} °C"]]   

    elif time_unit in settings.Jahr_template_set or time_unit in settings.trans_season_set:
        
        station_data = [[f"Kenntage", "WAST", "VKTU"], 
                        ["Frosttage", f"{station_values["WAST_frost"][0]}", f"{station_values["VKTU_frost"][0]}"], 
                        ["Eistage", f"{station_values["WAST_eis"][0]}", f"{station_values["VKTU_eis"][0]}"], 
                        ["Sommertage", f"{station_values["WAST_sommertage"][0]}", f"{station_values["VKTU_sommertage"][0]}"], 
                        ["Heiße Tage", f"{station_values["WAST_heißetage"][0]}", f"{station_values["VKTU_heißetage"][0]}"],
                        ["Tropennächte", f"{station_values["WAST_tropennächte"][0]}", f"{station_values["VKTU_tropennächte"][0]}"],
                        ["Tiefsttemperatur", f"{station_values["WAST_tiefsttemperatur"][0]} °C", f"{station_values["VKTU_tiefsttemperatur"][0]} °C"], 
                        ["Höchsttemperatur", f"{station_values["WAST_höchsttemperatur"][0]} °C", f"{station_values["VKTU_höchsttemperatur"][0]} °C"]]

    elif time_unit in settings.sommer_template_set:
        station_data = [[f"Kenntage im {time_unit} \n {year}", "WAST", "VKTU"], 
                        ["Sommertage", f"{station_values["WAST_sommertage"][0]}", f"{station_values["VKTU_sommertage"][0]}"], 
                        ["Heiße Tage", f"{station_values["WAST_heißetage"][0]}", f"{station_values["VKTU_heißetage"][0]}"],
                        ["Tropennächte", f"{station_values["WAST_tropennächte"][0]}", f"{station_values["VKTU_tropennächte"][0]}"],
                        ["Tiefsttemperatur", f"{station_values["WAST_tiefsttemperatur"][0]} °C", f"{station_values["VKTU_tiefsttemperatur"][0]} °C"], 
                        ["Höchsttemperatur", f"{station_values["WAST_höchsttemperatur"][0]} °C", f"{station_values["VKTU_höchsttemperatur"][0]} °C"]]


    
    station_table = Table(station_data, colWidths=[5*cm, 4*cm, 4*cm])
    station_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
        ('TEXTCOLOR', (0, 0), (3, 0), colors.white),
        ("TEXTCOLOR", (0, 0), (0, -1), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
        ("BACKGROUND", (0, 1), (0, -1), colors.darkblue),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('FONTNAME', (0, 0), (0, -1),'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black)]))
    
    elements.append(station_table)
    elements.append(Spacer( 1, 5*mm))
    


    #title_station_op = Paragraph("OpenAI", styles['Heading4'])
    station_text_op = f"""{data["3"]}"""
    #elements.append(title_station_op)
    elements.append(Paragraph(station_text_op, styles["Normal_custom"]))

    #title_station_claude = Paragraph("Claude", styles['Heading4'])
    #station_text_claude = f"""{data["tags"][3]["value"][0][1]}"""
    #elements.append(title_station_claude)
    #elements.append(Paragraph(station_text_claude, styles["Normal_custom"]))

    #title_station_deeps = Paragraph("Deepseek", styles['Heading4'])
    #station_text_deeps = f"""{data["tags"][3]["value"][0][2]}"""
    #elements.append(title_station_deeps)
    #elements.append(Paragraph(station_text_deeps, styles["Normal_custom"]))

    # Build des PDF-Files

    doc.build(elements)

    buffer.seek(0)

    return buffer




