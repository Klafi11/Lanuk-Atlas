import uuid
from src.settings import get_model_settings, get_settings, setup_logging
from src.retrieval_functions import Page, Tag, DataRetriever, retrieval_functions, get_temp, get_rain, get_sun, get_station, Data_report, get_weather_intro_adv
from src.pdf_generator import create_weather_report_api
from src.Websearch import expand_topics, pre_summarization, summarization
from src.heading import generate_heading
from flask import Flask, request, jsonify, Response, send_file
from flask_cors import CORS
from src.time_series import get_time_series_data
import traceback
from asgiref.wsgi import WsgiToAsgi
from urllib.parse import quote
import logging
from src.download import report_graphics_svg
import zipfile
from io import BytesIO
from src.db import upsert_report_data
import asyncio

"""Flask Weather Reports API 

Dieses Modul stellt eine REST/HTTP-API zur Verfügung, um Klima- und Wetterberichte
sowie Zeitreihen- und Stationsdaten zu erzeugen und abzurufen. Es bindet die
fachliche Logik aus dem lokalen `src`-Paket ein (Datenabruf, Textgenerierung,
PDF-Erzeugung, Websuche, Diagramme usw.) und exponiert diese als Endpunkte.

Voraussetzungen
---------------
- Python 
- Flask 2.0+ (mit Async-Unterstützung)
- asgiref (für `WsgiToAsgi`) zur Bereitstellung via ASGI-Server 

Endpunkt-Übersicht
------------------
GET  /api/retrieveReports           → Generierung der Berichtsabschnitte laden (async)
POST /api/pdfreports?param1&param2  → PDF-Report erzeugen für PDF-Preview (sync)
POST /api/websearch?param1&param2   → Websuche Tool (async)
GET  /api/tabellendaten             → Basis-Tabellendaten (sync)
POST /api/heading                   → Überschriftengenerator (sync)
GET  /api/timeseries                → Zeitreihen für Diagramme (sync)
GET  /api/dwdwetter                 → Aufbereitete DWD-Wetterdaten (async)
POST /api/stationdata               → Stationsdaten Für ButtonGrid (sync)
POST /api/downloadfiles             → Daten speichern, PDF + SVG erzeugen, ZIP senden (sync)
"""

app = Flask(__name__)

setup_logging()

CORS(app, origins=[
    "http://frontend:3000",
    "http://localhost:5173", 
    "http://simplex4learning.disy.net:5173",
    "https://simplex4learning.disy.net:5173",
    "http://textgenerierung-simplex4learning.disy.net:5173",
    "https://textgenerierung-simplex4learning.disy.net:5173"
])

settings = get_settings()
logger = logging.getLogger(__name__)

@app.route("/api/retrieveReports", methods=["get"])
async def main():

    """
    Berichtsabschnitte zu den jeweiligen Query-Parametern werden über diesen Endpunkt generiert.
    Stößt die Hauptberichtspipeline zum generieren der Berichte an. 
    
    Query-Parameter
    ---------------
    year : int
        Zieljahr für den Bericht.
    time_unit : str
        Zeitgranularität (Monat/Jahreszeit/Jahr). 
    report_pip : str
        Report-Pipeline/Variante ('Standard', 'Adnvanced'); 

    Returns
    -------
    flask.Response
        JSON-Objekt aus `retriever.get_data` der jeweilig generierten Berichtsabschnitte über die eingesetzten Sprachmodelle.
    """
    
    logger.info(f"Retrieve reports called with year: {request.args.get('year')}, time_unit: {request.args.get('time_unit')}")
    
    try:
        year = int(request.args.get("year"))
        time_unit = request.args.get("time_unit")
        report_pip = request.args.get("type")
        run_id = str(uuid.uuid4())

        # Aufbau der Berichte mit den jeweiligen Retrieval Funktionen, die an als Schema an den DataRetriever gegeben werden.
        if time_unit in settings.months:
            klima_report_layout = Page(tags = [Tag(id = "get_temp_report_month", value = list()),
                                            Tag(id = "get_rain_report_month", value = list()),
                                            Tag(id = "get_sun_report_month",  value=list()),
                                            Tag(id = "get_station_report_month", value = list()),
                                            Tag(id = "get_report_introduction", value = list())
                                            ]) 
        elif time_unit in settings.seasons: 
            klima_report_layout = Page(tags = [Tag(id = "get_temp_report_quarter", value = list()),
                                            Tag(id = "get_rain_report_quarter", value = list()),
                                            Tag(id = "get_sun_report_quarter",  value=list()),
                                            Tag(id = "get_station_report_quarter", value = list()),
                                            Tag(id = "get_report_introduction", value = list())
                                            ]) 
        elif time_unit in settings.year: 
            klima_report_layout = Page(tags = [Tag(id = "get_temp_report_year", value = list()),
                                            Tag(id = "get_rain_report_year", value = list()),
                                            Tag(id = "get_sun_report_year",  value=list()),
                                            Tag(id = "get_station_report_year", value = list()),
                                            Tag(id = "get_report_introduction", value = list())
                                            ]) 
       
        # DataRetriever
        retriever = DataRetriever(year = year, time_unit = time_unit,
                                report_schema = klima_report_layout,
                                retrieval_functions = retrieval_functions, run_id= run_id, report_pipe = report_pip)

        
        tasks = [retriever.populate_tag(tag) for tag in retriever.report_schema.tags if tag.id != "get_report_introduction"]
        
        
        await asyncio.gather(*tasks)
        
        await retriever.populate_tag(retriever.report_schema.tags[-1])

        logger.info(f"Successfully processed report")

        return retriever.get_data
    
    except Exception as e:
        logger.error(f"Exception in retrieveReports: {str(e)}", exc_info=True)
        traceback.print_exc() 
        return jsonify({"error": str(e), "traceback": traceback.format_exc()}), 500



@app.route("/api/pdfreports", methods=["POST"])
def generate_pdf(): 


    """ PDF-Report aus bereitgestellten Daten erzeugen und als PDF-Objekt senden.
    
    Query-Parameter
    ---------------
    data : dict
        Dictonary der jeweiligen Berichtsabschnitte zur Erstellung der PDF
    year : int
        Zieljahr für den Bericht.
    time_unit : str
        Zeitgranularität (Monat/Jahreszeit/Jahr). 

    Returns
    -------
    flask.Response
        PDF-Stream mit gesetztem `Content-Disposition`-Header
    """
    
    logger.info(f"Start Process PDF Generation")
    try: 
        data = request.get_json()
        year = request.args.get("param1")
        time_unit = request.args.get("param2")

        pdf = create_weather_report_api(year, time_unit, data)

        raw_filename = f"{year}-{time_unit}-report.pdf"
        fallback_filename = "report.pdf"
        quoted_filename = quote(raw_filename)

        content_disposition = (
            f"attachment; filename={fallback_filename}; filename*=UTF-8''{quoted_filename}"
        )

        logger.info(f"Successfully finished PDF Generation")
        return Response(
            pdf,
            mimetype="application/pdf",
            headers={
                "Content-Disposition": content_disposition
            }
        )
    except Exception as e:
        logger.error(f"Exception in Pdf Generator: {str(e)}", exc_info=True)



@app.route("/api/websearch", methods=["POST"])
async def Websearch():

    """ Websuche Tool für relevante Wetterereignisse.
    
    Query-Parameter
    ---------------
    data : dict
        Dictonary der jeweiligen Berichtsabschnitte zur Erstellung der Suchqueries
    year : int
        Zieljahr für den Bericht.
    time_unit : str
        Zeitgranularität (Monat/Jahreszeit/Jahr). 
    Returns
    -------
        JSON-Objekt aus `sum_out.model_dump` für Quellen und Websucheabsatz.
    """
    
    logger.info(f"Start Process Websearch")
    try:
        data = request.get_json()
        year = request.args.get("param1")
        time_unit = request.args.get("param2")
        
  
        if not data or not year or not time_unit:
            return jsonify({"error": "Missing required parameters"}), 400
            
        queries = expand_topics(data, year, time_unit)
        pre_sum = await pre_summarization(queries, year, time_unit)
        sum_out = summarization(pre_sum, year, time_unit)
        sum_out_jsonify = sum_out.model_dump()
        
        logger.info(f"Successfully finished Process Websearch")
        return jsonify(sum_out_jsonify), 200
        
    except Exception as e:
        logger.error(f"Exception in Websearch: {str(e)}", exc_info=True)
        return jsonify({"error": str(e)}), 500


@app.route("/api/tabellendaten", methods = ["GET"])
def report_data(): 

    """Basistabellen (Temperatur, Niederschlag, Sonne, Stationen) für das Frontend.

    Query-Parameter
    ---------------
    year : int
        Zieljahr.
    time_unit : str
        Zeitgranularität (Monat/Jahreszeit/Jahr).

    Returns
    -------
    flask.Response
        JSON, `Data_report`-Struktur (`data.model_dump`)
    """

    logger.info(f"Start Process Table Data")
    try:
        year = int(request.args.get("year"))
        time_unit = request.args.get("time_unit")
        
        temp = get_temp(year, time_unit)
        rain = get_rain(year, time_unit)
        sun = get_sun(year, time_unit)
        station = get_station(year, time_unit, ["WAST", "VKTU"])

        data = Data_report(data=[{0:temp, 1: rain, 2:sun, 3:station}])


        data = data.model_dump()

        logger.info(f"Successfully finished Process Table Data")

        return jsonify(data)
    
    except Exception as e:

        logger.error(f"Exception in Report Data for Graphics: {str(e)}", exc_info=True)



@app.route("/api/heading", methods = ["POST"])
def report_heading():

    """Überschriftengenerator zum erzeugen von passenden Überschrift für die Berichte.

    Query-Parameter
    ---------------
    year : int
        Zieljahr.
    time_unit : str
        Zeitgranularität (Monat/Jahreszeit/Jahr).
     data : dict
        Dictonary der jeweiligen Berichtsabschnitte zur Erstellung der Überschriften.

    Returns
    -------
    dict
        Liste der generieten Überschriften (`res.model_dump`).
    """
    
    logger.info("Start Process Heading Generation")
    try: 
        year = int(request.args.get("year"))
        time_unit = request.args.get("time_unit")
        data = request.get_json()
        
        res = generate_heading(data, year, time_unit)

        res = res.model_dump()

        logger.info("Successfully finished Process Heading Generation")

        return res
    
    except Exception as e:
        logger.error(f"Exception in Heading Generation: {str(e)}", exc_info=True)


@app.route("/api/timeseries", methods = ["GET"])
def time_series_data():

    """Zeitreihen-Daten für Diagramme im Frontend abrufen.

    Query-Parameter
    ---------------
    year : int
        Zieljahr.
    time_unit : str
        Zeitgranularität (Monat/Jahreszeit/Jahr).

    Returns
    -------
    flask.Response
        JSON Objekt für Zeitreihendaten (`res.model_dump`).
    """
    
    logger.info("Start Process Time Series Data")
    try:
    
        year = int(request.args.get("year"))
        time_unit = request.args.get("time_unit")

        res = get_time_series_data(year, time_unit)

        logger.info("Successfully finished Process Time Series Data")
        return jsonify(res.model_dump())
        
    except Exception as e:
        logger.error(f"Exception in Time Series Data: {str(e)}", exc_info=True)
        traceback.print_exc() 
        return jsonify({"error in time_series": str(e), "traceback": traceback.format_exc()}), 500

@app.route("/api/dwdwetter", methods= ["GET"])
async def dwdwetter():
    
    """DWD Wetterbericht Tool.

    Query-Parameter
    ---------------
    year : int
        Zieljahr.
    time_unit : str
        Zeitgranularität (Monat/Jahreszeit/Jahr).

    Returns
    -------
        JSON Objekt mit dem DWD Wetterbericht.
    """

    logger.info("Start Process DWD Wetter data")
    try:
        logger.info("Start DWD Wetter API")
        year = int(request.args.get("year"))
        time_unit = request.args.get("time_unit")
        
        result = await get_weather_intro_adv(year, time_unit)
        logger.info("Succesfully transformed DWD Wetter data")
        return jsonify(result)
    
        
    except Exception as e:
        logger.error(f"Exception in DWD Wetter Data: {str(e)}", exc_info=True)
        return jsonify({"error": str(e)}), 500


@app.route("/api/stationdata", methods=["POST"])
def stationdata():
    
    """Stationsdaten für ausgewählte Stationen abrufen (Buttongrid - Frontend)

    Query-Parameter
    ---------------
    year : int
        Zieljahr.
    time_unit : str
        Zeitgranularität (Monat/Jahreszeit/Jahr).
    data : dict
        Dictonary der jeweilig ausgewählten Stationen.

    Returns
    -------
    flask.Response
        JSON mit den zugehörigen Stationsdaten.
    """

    try:
        logger.info("Start Station data API")
        
        year = int(request.args.get("year"))
        time_unit = request.args.get("time_unit")
        data = request.get_json()
 
        selected_stations = data.get("items", []) 

        result = get_station(year, time_unit, selected_stations)

        return jsonify(result)
        
        
    except Exception as e:
        logger.error(f"Exception in Station data API: {str(e)}", exc_info=True)
        return jsonify({"error": str(e)}), 500


@app.route("/api/downloadfiles", methods = ["POST"])
def download_files():

    """Berichtsabschnitte persistieren, PDF und SVG-Diagramme erzeugen und als ZIP senden.

    Query-Parameter
    ---------------
    param1 : int
        Jahr.
    param2 : str
        Zeitgranularität (Monat/Jahreszeit/Jahr).
    data : dict
        Dictonary der jeweiligen Berichtsabschnitte zur Erstellung des Berichts für den download.


    Returns
    -------
    flask.send_file
        ZIP-Archiv mit PDF und SVG-Grafiken als Download.
    """

    try:
     
        data_text = request.get_json()
        year = int(request.args.get("param1"))
        time_unit = request.args.get("param2")
        
   
        upsert_report_data(year, time_unit, data_text)

      
        pdf_bytes = create_weather_report_api(year, time_unit, data_text)
        

        time_series_data = get_time_series_data(year, time_unit)
        svg_charts = report_graphics_svg(year, time_unit, time_series_data)
        

        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
    
            if hasattr(pdf_bytes, 'read'):
                pdf_data = pdf_bytes.read()
            else:
                pdf_data = pdf_bytes
            zip_file.writestr(f"{year}-{time_unit}-report.pdf", pdf_data)
            
        
            for svg_filename, svg_content in svg_charts.items():
               
                if isinstance(svg_content, str):
                    svg_bytes = svg_content.encode('utf-8')
                else:
                    svg_bytes = svg_content
                zip_file.writestr(svg_filename, svg_bytes)
        

        zip_buffer.seek(0)
        
        return send_file(
            zip_buffer,
            mimetype='application/zip',
            as_attachment=True,
            download_name=f"{year}-{time_unit}.zip"
        )
        
    except Exception as e:
        logger.error(f"Exception in download_files: {str(e)}", exc_info=True)
        return jsonify({"error": str(e)}), 500



# ASGI-Wrapper für Betrieb mit ASGI-Servern
asgi_app = WsgiToAsgi(app)

# Hinweis: Für die lokale Entwicklung kann folgender Block genutzt werden.
# Er wird hier absichtlich deaktiviert, da die App typischerweise via ASGI
# bereitgestellt wird. Zum Aktivieren auskommentieren.

# For development
#if __name__ == '__main__':
    #uvicorn.run(asgi_app, host="0.0.0.0", port=8000)