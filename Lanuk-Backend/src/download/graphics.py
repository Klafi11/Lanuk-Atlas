import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle, Patch
from matplotlib.lines import Line2D
from matplotlib.legend_handler import HandlerBase, HandlerLine2D
import matplotlib.image as mpimg
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from src.db import read_sql_query
from sqlalchemy import text
from io import BytesIO
from matplotlib import image as mpimg
import os
from matplotlib.ticker import MaxNLocator, FuncFormatter
from src.settings import get_settings


"""
graphics.py
================

Erzeugt drei SVG-Diagramme (Temperatur, Niederschlag, Sonnenscheindauer) als
Byte-Strings für Wetterberichte. Die Visualisierung basiert auf Matplotlib
(Balkendiagramm der Abweichungen zur Referenz 1961–1990) und blendet
Referenzlinien für Klimaperioden ein.

Hauptfunktionen
---------------
- `report_graphics_svg(year, time_unit, time_series_data)`: Generiert alle drei
  Diagramme und gibt sie als Dict {<dateiname.svg>: bytes} zurück.
- `report_graphics(metric_id, metric_type, year, time_unit, time_series_data)`:
  Rendert ein einzelnes Diagramm und gibt dessen SVG-Bytes zurück.

"""

settings = get_settings()



def report_graphics_svg(year:int, time_unit:str, time_series_data: dict):
    """
    Generiert alle 3 SVG-Charts und gibt sie als Dictionary zurück
    
    Args
    ---------------
    time_unit : str
            Zeiteinheit
    year : int
            Jahr
    time_series_data : dict      
            Zeitreihendaten für die Grafiken
    Returns
    -------
    dict : SVG-Bytes aller Grafiken

    """
    svg_charts = {}
    metric_types = ["temp", "rain", "sun"]
    
    for metric_id, metric_type in enumerate(metric_types):
        try:
            svg_bytes = report_graphics(metric_id, metric_type, year, time_unit, time_series_data)
            svg_charts[f"{metric_type}_chart.svg"] = svg_bytes
        except Exception as e:
            print(f"Fehler beim Generieren von {metric_type} Chart: {e}")
            # Fallback: Dummy SVG
            svg_charts[f"{metric_type}_chart.svg"] = b'<svg xmlns="http://www.w3.org/2000/svg"><text>Error</text></svg>'
    
    return svg_charts



# Aktuller Pfad
current_dir = os.path.dirname(os.path.abspath(__file__))
# Pfad zum Logo
img_path = os.path.join(current_dir, 'Icon_Klimaatlas.png')
# Laden des Logos
img = mpimg.imread(img_path)



def report_graphics(metric_id:int, metric_type:str, year:int, time_unit:str, time_series_data:dict):
      
    """Rendert ein einzelnes Abweichungs-Balkendiagramm als SVG.
    
    Args
    ---------------
    metric_id : int
            metric_id (0,1,2)
    year : int
            Jahr
    time_unit : str        
            Zeiteinheit
    metric_type : str
            (Temperatur, Niederschlag, Sonnenscheindauer)
    time_series_data : dict
            Zeitreihen Daten
    Returns
    -------
    SVG Bytes : einer einzelnen Grafik (Temperatur, Niederschlag, Sonnenscheindauer)
    
    """
    
    
    plt.switch_backend('svg')
    
    # Daten extrahieren
    years = [deviation.Jahr for deviation in time_series_data.root[metric_id].values]
    temp_deviations = [deviation.Abweichung for deviation in time_series_data.root[metric_id].values]


    # Figure erstellen
    fig, ax = plt.subplots(figsize=(10.1, 6.31))
    fig.patch.set_facecolor('#f0f0f0')
    ax.set_facecolor("lightgray")

    if metric_type == "temp":
        colors = ['red' if x > 0 else 'cornflowerblue' for x in temp_deviations]
    if metric_type == "rain":
        colors = ['cornflowerblue' if x > 0 else 'red' for x in temp_deviations]
    if metric_type == "sun":
         colors = ['gold' if x > 0 else 'dimgrey' for x in temp_deviations]

    

    # Bar Chart erstellen
    ax.bar(years, temp_deviations, color=colors, width=0.8, alpha=0.9, edgecolor='black')

    # Referenzperioden-Mittelwerte berechnen
    if metric_type in ["rain", "temp"]:
        query_ref = text(f"""
        SELECT index, "{time_unit}_{metric_type}_avg" 
        FROM dwd_{metric_type}_ref 
        WHERE index IN ('1881-1910', '1961-1990', '1991-2020')
        """)
    else:
        query_ref = text(f"""
        SELECT index, "{time_unit}_{metric_type}_avg" 
        FROM dwd_{metric_type}_ref 
        WHERE index IN ('1951-1980', '1961-1990', '1991-2020')
        """)

    ref = read_sql_query(query_ref)
    
    # Referenzlinien hinzufügen
    if metric_type in ["rain", "temp"]:
        ref_value_1 = ref.loc[ref["index"] == "1881-1910", f"{time_unit}_{metric_type}_avg"].values[0] - ref.loc[ref["index"] == "1961-1990", f"{time_unit}_{metric_type}_avg"].values[0] 
        ref_value_2 = ref.loc[ref["index"] == "1991-2020", f"{time_unit}_{metric_type}_avg"].values[0] - ref.loc[ref["index"] == "1961-1990", f"{time_unit}_{metric_type}_avg"].values[0]


        ax.hlines(y=ref_value_1, xmin=1881, xmax=1910, 
                color='#ff8c00', linewidth=4, linestyle='-', alpha=0.9)
        ax.hlines(y=ref_value_2, xmin=1991, xmax=2020, 
                color='#ff8c00', linewidth=4, linestyle='-', alpha=0.9)
        ax.hlines(y=0, xmin=1881, xmax=2020, color='black', linewidth=1, linestyle='-', alpha=0.9)
    else: 
        ref_value_1 = ref.loc[ref["index"] == "1951-1980", f"{time_unit}_{metric_type}_avg"].values[0] - ref.loc[ref["index"] == "1961-1990", f"{time_unit}_{metric_type}_avg"].values[0] 
        ref_value_2 = ref.loc[ref["index"] == "1991-2020", f"{time_unit}_{metric_type}_avg"].values[0] - ref.loc[ref["index"] == "1961-1990", f"{time_unit}_{metric_type}_avg"].values[0] 


        ax.hlines(y=ref_value_1, xmin=1951, xmax=1980, 
                color='#C71585', linewidth=4, linestyle='-', alpha=0.9)
        ax.hlines(y=ref_value_2, xmin=1991, xmax=2020, 
                color='#C71585', linewidth=4, linestyle='-', alpha=0.9)
        ax.hlines(y=0, xmin=1951, xmax=2020, color='black', linewidth=1, linestyle='-', alpha=0.9)

    # Achsenbeschriftungen und Titel
    ax.set_xlabel('', fontsize=11)

    if time_unit in settings.months:
        if metric_type == "temp":

            ax.set_ylabel(f'Abweichung von der Referenzmitteltemperatur\n1961-1990 von {ref.loc[ref["index"] == "1961-1990", f"{time_unit}_{metric_type}_avg"].values[0]} °C in K', 
                        fontsize=10, color='#333333')
            ax.set_title(f'Mittlere monatliche Lufttemperatur in NRW\n{time_unit}', 
                        fontsize=12, fontweight='bold', color='#333333', pad=15)
        if metric_type == "rain":

            ax.set_ylabel(f'Abweichung von der Referenzniederschlagssumme\n1961-1990 von {ref.loc[ref["index"] == "1961-1990", f"{time_unit}_{metric_type}_avg"].values[0]} mm in mm', 
                        fontsize=10, color='#333333')
            ax.set_title(f'Mittlere monatliche Niederschlagssumme in NRW\n{time_unit}', 
                        fontsize=12, fontweight='bold', color='#333333', pad=15)
        if metric_type == "sun":

            ax.set_ylabel(f'Abweichung von der Referenzsonnenscheindauer\n1961-1990 von {ref.loc[ref["index"] == "1961-1990", f"{time_unit}_{metric_type}_avg"].values[0]} h in h', 
                        fontsize=10, color='#333333')
            ax.set_title(f'Mittlere monatliche Sonnenscheindauer in NRW\n{time_unit}', 
                        fontsize=12, fontweight='bold', color='#333333', pad=15)
    
    if time_unit in settings.seasons:
        if metric_type == "temp":

            ax.set_ylabel(f'Abweichung von der Referenzmitteltemperatur\n1961-1990 von {ref.loc[ref["index"] == "1961-1990", f"{time_unit}_{metric_type}_avg"].values[0]} °C in K', 
                        fontsize=10, color='#333333')
            ax.set_title(f'Mittlere Jahreszeitenlufttemperatur in NRW\n{time_unit}', 
                        fontsize=12, fontweight='bold', color='#333333', pad=15)
        if metric_type == "rain":

            ax.set_ylabel(f'Abweichung von der Referenzniederschlagssumme\n1961-1990 von {ref.loc[ref["index"] == "1961-1990", f"{time_unit}_{metric_type}_avg"].values[0]} mm in mm', 
                        fontsize=10, color='#333333')
            ax.set_title(f'Mittlere Jahreszeitenniederschlagssumme in NRW\n{time_unit}', 
                        fontsize=12, fontweight='bold', color='#333333', pad=15)
        if metric_type == "sun":

            ax.set_ylabel(f'Abweichung von der Referenzsonnenscheindauer\n1961-1990 von {ref.loc[ref["index"] == "1961-1990", f"{time_unit}_{metric_type}_avg"].values[0]} h in h', 
                        fontsize=10, color='#333333')
            ax.set_title(f'Mittlere Jahreszeitensonnenscheindauer in NRW\n{time_unit}', 
                        fontsize=12, fontweight='bold', color='#333333', pad=15)
    
    if time_unit in settings.year:
        if metric_type == "temp":

            ax.set_ylabel(f'Abweichung von der Referenzmitteltemperatur\n1961-1990 von {ref.loc[ref["index"] == "1961-1990", f"{time_unit}_{metric_type}_avg"].values[0]} °C in K', 
                        fontsize=10, color='#333333')
            ax.set_title(f'Mittlere Jahreslufttemperatur in NRW', 
                        fontsize=12, fontweight='bold', color='#333333', pad=15)
        if metric_type == "rain":

            ax.set_ylabel(f'Abweichung von der Referenzniederschlagssumme\n1961-1990 von {ref.loc[ref["index"] == "1961-1990", f"{time_unit}_{metric_type}_avg"].values[0]} mm in mm', 
                        fontsize=10, color='#333333')
            ax.set_title(f'Mittlere Jahresniederschlagssumme in NRW', 
                        fontsize=12, fontweight='bold', color='#333333', pad=15)
        if metric_type == "sun":

            ax.set_ylabel(f'Abweichung von der Referenzsonnenscheindauer\n1961-1990 von {ref.loc[ref["index"] == "1961-1990", f"{time_unit}_{metric_type}_avg"].values[0]} h in h', 
                        fontsize=10, color='#333333')
            ax.set_title(f'Mittlere jährliche Sonnenscheindauer in NRW', 
                        fontsize=12, fontweight='bold', color='#333333', pad=15)
        


    if metric_type in ["rain", "temp"]:
        ax.set_xlim(1875, 2030)
    else: 
        ax.set_xlim(1947, 2030)


    if metric_type in ["rain", "temp"]:
        ax.set_xticks(range(1880, 2030, 20))
        ax.set_xticks(range(1880, 2030, 10), minor=True)
    else: 
        ax.set_xticks(range(1950, 2030, 10))
        ax.set_xticks(range(1950, 2030, 5), minor=True)

    if metric_type == "temp":
        ax.yaxis.set_major_locator(MaxNLocator(nbins="auto"))
        ax.yaxis.set_major_formatter(FuncFormatter(lambda y, _: f'{y:.1f}'))
    else:
        ax.yaxis.set_major_locator(MaxNLocator(nbins="auto", integer = True))
        ax.yaxis.set_major_formatter(FuncFormatter(lambda y, _: f'{int(y)}'))


    # Grid-Styling
    ax.grid(True, alpha=0.4, linestyle='-', linewidth=1.4, color='white', which='major')
    ax.grid(True, which='minor', alpha=0.4, linestyle='-', linewidth=1, color='white')
    ax.set_axisbelow(True)

    # Spines entfernen
    for spine in ax.spines.values():
        spine.set_visible(False)

    # Tick-Styling
    ax.tick_params(axis='both', which='major', labelsize=12, color='#666666')
    ax.tick_params(axis='x', which='major', length=4, width=1)
    ax.tick_params(axis='y', which='major', length=4, width=1)
    ax.tick_params(axis='x', which='minor', length=0, width=0)

    # Custom Legend Handler
    class HandlerDoubleRectangle(HandlerBase):
        def create_artists(self, legend, orig_handle,
                          xdescent, ydescent, width, height, fontsize, trans):
            
            rect_width = width * 0.4   
            extension = width * 0.1   

            if metric_type in ["temp"]: 
            
                rect1 = Rectangle((xdescent, ydescent), rect_width, height*1.6,
                                facecolor='#d73027', edgecolor='black')
                rect2 = Rectangle((xdescent + rect_width + width *0.04, ydescent), rect_width, height*0.8,
                                facecolor='#d73027', edgecolor='black')
                rect3 = Rectangle((xdescent + rect_width*2.0 + width* 0.09, ydescent*(19.1)), rect_width, height*1,
                                facecolor='#4575b4', edgecolor='black')
            
            if metric_type in ["rain"]:
                
                rect1 = Rectangle((xdescent, ydescent), rect_width, height*1.6,
                                facecolor='#4575b4', edgecolor='black')
                rect2 = Rectangle((xdescent + rect_width + width *0.04, ydescent), rect_width, height*0.8,
                                facecolor='#4575b4', edgecolor='black')
                rect3 = Rectangle((xdescent + rect_width*2.0 + width* 0.09, ydescent*(19.1)), rect_width, height*1,
                                facecolor='#d73027', edgecolor='black')
            
            if metric_type in ["sun"]:
                rect1 = Rectangle((xdescent, ydescent), rect_width, height*1.6,
                                facecolor='#FFD700', edgecolor='black')
                rect2 = Rectangle((xdescent + rect_width + width *0.04, ydescent), rect_width, height*0.8,
                                facecolor='#FFD700', edgecolor='black')
                rect3 = Rectangle((xdescent + rect_width*2.0 + width* 0.09, ydescent*(19.1)), rect_width, height*1,
                                facecolor='#696969', edgecolor='black')

                
            
            line = Line2D(
                [xdescent - extension, xdescent + 3*rect_width + extension + width*0.1],
                [ydescent, ydescent],
                color='black',
                linewidth=1
            )
            
            for patch in [rect1, rect2, rect3]:
                patch.set_edgecolor("black")
                patch.set_linewidth(0.6)
                patch.set_transform(trans)
            
            return [rect1, rect2, rect3, line]

    if metric_type in ["temp"]:
        legend_elements = [
            Patch(facecolor='black', label=f'Temperaturabweichung'),
            Line2D([0],[0], color='#ff8c00', lw=4, label='Mittelwerte 1881-1910 und 1991-2020')
        ]
    if metric_type in ["rain"]:
        legend_elements = [
            Patch(facecolor='black', label='Niederschlagsabweichung'),
            Line2D([0],[0], color='#ff8c00', lw=4, label='Mittelwerte 1881-1910 und 1991-2020')
        ]
    if metric_type in ["sun"]:
        legend_elements = [
            Patch(facecolor='black', label='Sonnenstundenabweichung'),
            Line2D([0],[0], color='#C71585', lw=4, label='Mittelwerte 1951-1980 und 1991-2020')
        ]

    ax.legend(
        handles=legend_elements,
        handler_map={
            Patch: HandlerDoubleRectangle(),
            Line2D: HandlerLine2D()
        },
        loc='center',
        handleheight=0.6,
        handlelength=2,
        bbox_to_anchor=(0.5, -0.14),
        handletextpad=1,
        fontsize=10,
        ncol=2,
        columnspacing=1,
        frameon=False,
        fancybox=False, 
        shadow=False,
        prop={"weight": "bold", "size": 10}
    )

    # Logo hinzufügen
    imagebox = OffsetImage(img, zoom=0.28)
    ab = AnnotationBbox(imagebox, 
                    (0.19, 1.15), 
                    box_alignment=(1, 1),
                    frameon=False, 
                    xycoords='axes fraction')
    ax.add_artist(ab)

    # Layout anpassen
    plt.subplots_adjust(
        left=0.08,
        right=0.95,
        top=0.85,
        bottom=0.25
    )

    # SVG als Byte-Objekt speichern
    svg_buffer = BytesIO()
    plt.savefig(svg_buffer, format='svg', dpi=300, bbox_inches='tight')
    svg_buffer.seek(0)
    svg_bytes = svg_buffer.getvalue()
    
    # Figure schließen um Speicher freizugeben
    plt.close(fig)
    
    return svg_bytes