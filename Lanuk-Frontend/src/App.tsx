import { useState, useEffect } from 'react';
import Navbar from './Navigationsbar';
import {Page, StructuredSum, DataReport, HeadingStruc, TimeSeriesData} from './BaseModels';
import Variationdisplay from './Variationsdisplay';
import axios from "axios";
import PdfPreview from "./Informationdisplay";

/**
 * Haupt‑Komponente der Anwendung.
 *
 * Diese Komponente steuert den kompletten Berichtsgenerator‑Workflow:
 * 1. Auswahl von Berichtstyp, Zeitintervall und Jahr, Download  PDF‑/ZIP‑Download über die <Navbar>.
 * 3. Editieren von Textvarianten in <Variationdisplay>.
 * 4. Zeitreihen‑Daten-Vorschau, Web‑Suche, DWD-Wetterbericht, usw. in <PdfPreview>.
 *
 * Der State wird ausschließlich hier gehalten und per Props an die
 * Kind‑Komponenten gereicht. API‑Aufrufe sind vollständig gekapselt
 * in dedizierten *async*‑Funktionen.
 */



export default function App() {
    
  /* ------------------------------------------------------------------
  * React State Hooks
  * ------------------------------------------------------------------ */

    /** Absatzabschnitte des aktuellen Reports */
  const [paragraphs, setparagraphs] = useState<Page | null>(null);
  /** Gewählter Berichtstyp (z. B. "Monatsberichte") */
  const [reportType, setReportType] = useState("");
  /** Gewähltes Zeitintervall (z. B. "März", "Jahr_agg" …) */
  const [reportDate, setReportDate] = useState("Jahr_agg");
  /** Gewähltes Jahr (ISO‑String, z. B. "2025") */ 
  const [reportYear, setReportYear] = useState("");
  /** Ladespinner für API‑Aufrufe */
  const [isloading, setisloading] = useState(false)
  /** Index des aktuell aktiven Paragraphen (0‑4) */
  const [CurrentParagraph, setCurrentParagraph] = useState<number>(4)
  /** Vom Benutzer bearbeitete Texte" */
  const [editedTexts, setEditedTexts] = useState<Record<string, string>>({});
  /** Auswahl an Text‑Modellen je Paragraph */
  const [selectedModels, setSelectedModels]= useState<Record<number, number>>({});
  /** Temporärer PDF‑Blob‑URL für die Vorschau */
  const [PdfUrl, setPdfUrl] = useState<string | null>(null);
  /** Aktiver Tab in <PdfPreview> (1=Daten,2=PDF-Vorschau, 3=Informationen) */
  const [currentTab, setcurrentTab] = useState<number>(1);
  /** Ergebnis einer Web‑Recherche (zusammengefasst) */
  const [WebSearch, SetWebSearch] = useState<StructuredSum | null>(null);
  /** Tabellen‑/Kennzahlendaten */
  const [ReportData, setReportData] = useState<DataReport | null >(null);
  /** Überschriftenvorschläge */ 
  const [Headings, setHeadings] = useState<HeadingStruc | null >(null);
  /** Sichtbare Überschriften‑Indices (für Fade‑In‑Animation) */
  const [visibleItems, setVisibleItems] = useState<number[]>([])
  /** Vom Nutzer ausgewählte Überschrift */
  const [selectedItem, setSelectedItem] = useState<number | null>(null)
  /** Anzeigemodus ("standard" | "advanced") */
  const [togglemode, settogglemode] = useState<string>("standard")
  /** Zeitreihen für Charts */
  const [TimeSData, setTimeSData] = useState<TimeSeriesData | null>(null)
  /** Flag für allgemeine Animationen */
  const [IsAnimating, setIsAnimating] = useState<boolean> (false)
  /** Triggert globales Zurücksetzen des States */
  const [resetTrigger, setResetTrigger] = useState<boolean> (false)
  /** Ladespinner für Heading‑Generierung */
  const [HeadingLoading, setHeadingLoading] = useState<boolean>(false)
  /** Wetterbericht des DWD */
  const [DWDWetter, setDWDWetter] = useState(null)
  /** Animation "DWD wird geladen" */
  const [isAnimatingDWD, setisAnimatingDWD] = useState<boolean>(false)
  /** Fehlerflag für Error‑Handling in der Anwendung */
  const [ErrorMess, setErrorMess] = useState<boolean>(false)
  /** Ausgewählte Station-Buttons Grid Element (Set wegen einfacher Add/Remove‑Logik) */
  const [selectedButtons, setSelectedButtons] = useState<Set<string>>(new Set());
  /** Stations‑Tabellen‑Daten */
  const [StationData, setStationData] = useState<Record<string, number[] | string[]>>({})

  /* ------------------------------------------------------------------
    * Lifecycle Effects
    * ------------------------------------------------------------------ */

  /**
   * Setzt nahezu den gesamten State zurück, wenn *resetTrigger* auf
   * *true* gesetzt wird. Dadurch startet der UI‑Flow nach einem
   * API‑Aufruf für die Berichtsgenerierung neu.
   */

  useEffect(() => {
    if (resetTrigger) {
      setErrorMess(false)
      setCurrentParagraph(4);
      setEditedTexts({});
      setSelectedModels({});
      setPdfUrl(null);
      setcurrentTab(1);
      SetWebSearch(null);
      setReportData(null);
      setHeadings(null);
      setSelectedItem(null);
      setTimeSData(null);
      setIsAnimating(false);
      setDWDWetter(null);

    
      setResetTrigger(false);
    }
  }, [resetTrigger]);

  /**
   * Räumt den durch *URL.createObjectURL* erzeugten Blob‑URL auf,
   * sobald sich *PdfUrl* ändert oder die Komponente unmountet.
   */
  useEffect(() => {
      return () => {
        if (PdfUrl) {
          URL.revokeObjectURL(PdfUrl);
        }
      };
  }, [PdfUrl]);



 /* ------------------------------------------------------------------
  * Veränderungs‑Handler (Navbar) Berichtstyp, Berichtsjahr, Zeiteinheit
  * ------------------------------------------------------------------ */

  
  const handleReportTypeChange = (type: string) => {
    setReportType(type);
    setReportDate("Jahr_agg")
  }

  const handleReportDateChange = (date: string) => {
    setReportDate(date)
  }

  const handleReportYearChange = (year: string) => {
    setReportYear(year)

  }

  /* ------------------------------------------------------------------
   * API‑Aufrufe
   * ------------------------------------------------------------------ */

    
  const api_call = async() => {

    /**
     * Ruft Basisdaten Berichtsabschnitte, Tabellen, Zeitreihen) für die jeweils
     * ausgewählten Parameter *reportType*, *reportDate* und *reportYear*
     * parallel vom Backend ab.
     *
     * @async
     * @returns void
     */

    setResetTrigger(true);

    try {
      setisloading(true);
    
      const time_unit = reportType === "Jahresberichte" ? "Jahr_agg" : reportDate;

      const reportPromise = fetch(`/api/retrieveReports?year=${reportYear}&time_unit=${time_unit}&type=${togglemode}`);
      const DataTablePromise = fetch(`/api/tabellendaten?year=${reportYear}&time_unit=${time_unit}`); 
      const TimeSeriesPromise = fetch(`/api/timeseries?year=${reportYear}&time_unit=${time_unit}`)

      const [TextResponse, DataResponse, TimeSeriesResponse] = await Promise.all([reportPromise, DataTablePromise, TimeSeriesPromise]);


      if (!TextResponse.ok || !DataResponse.ok || !TimeSeriesResponse.ok ) {
        setErrorMess(true)
        throw new Error("One or more network responses were not ok");
      }
    
      const TextData = await TextResponse.json();
      const ReportData = await DataResponse.json();
      const TimeSeriesData = await TimeSeriesResponse.json();

      console.log(TextData)
      
    
      setparagraphs(TextData);
      setReportData(ReportData);
      setTimeSData(TimeSeriesData)

    
      setEditedTexts({});
    } catch (error) {
      console.error("Error fetching data:", error);
    } finally {
      setisloading(false);
    }

  }

  /* ------------------------------------------------------------------
   * PDF-Vorschau / Web‑Search / DWD‑Wetter / Überschriftengenerator
   * ------------------------------------------------------------------ */


  const handle_pdf_preview = () => {
  
    /**
     * Fordert beim Backend eine PDF‑Vorschau der aktuell gewählten Texte
     * an und legt die erhaltene Blob‑URL in *PdfUrl* ab.
     */

    const api_object = get_current_text()

    if (selectedItem !== null) {
      api_object["5"] = Headings?.headings[selectedItem].toString() || ""; 
    }

    const sendData = async() => {
      
      try {
        const response = await axios.post(
          `/api/pdfreports?param1=${reportYear}&param2=${reportDate}`, 
          api_object,
          {
            responseType: "blob"
          })
        
        const blob = new Blob([response.data], {type: "application/pdf"})

        const url = URL.createObjectURL(blob)

        setPdfUrl(url)

          
      } catch (error) {
        console.error("error fetching pdf")
      }
      
      
      
    }

    sendData();
  }
    
  /*------------------------------------------------------------------*/

  const handle_web_search = async() => {

  /**
   * Erstellt eine strukturierte Kurzfassung relevanter Wettererignisse zu der jeweiligen Zeiteinheit über Tavily Search.
   */

    setIsAnimating(true)
    const api_object = get_current_text()

    try {
    const response = await axios.post(`/api/websearch?param1=${reportYear}&param2=${reportDate}`, 
      api_object)

    SetWebSearch(response.data)

    setIsAnimating(false)
    } catch (error) {
      console.error("Error fetching Websearch:", error);
    } 

  }

  /*------------------------------------------------------------------*/

  const handle_dwd_wetter = async() => {
  
    /**
   * Erstellt eine strukturierte Kurzfassung relevanter Wettererignisse zu der jeweiligen Zeiteinheit über die DWD Wetterberichte.
   */

    setisAnimatingDWD(true)
    try{
    const response = await axios.get(`/api/dwdwetter?year=${reportYear}&time_unit=${reportDate}`)
    setDWDWetter(response.data)
    setisAnimatingDWD(false)
    } catch (error) {
      console.error("Error fetching DWD Wetterbericht:", error);
    } 

  }

  /*------------------------------------------------------------------*/
  
  const get_heading = async () => {

  /**
   * Lässt von einem LLM Überschriften generieren und
   * blendet sie anschließend sequenziell ein (Animation).
   */
    
    setVisibleItems([]);
    const api_object = get_current_text();
    setHeadings(null);
    setSelectedItem(null)
    setHeadingLoading(true);

    try {
      const Response = await axios.post(
        `/api/heading?year=${reportYear}&time_unit=${reportDate}`,
        api_object);
        
        const NewHeading = Response.data
        setHeadings(NewHeading);
        
        if (NewHeading?.headings?.length > 0) {
          NewHeading.headings.forEach((_:any, index:number) => {
            setTimeout(() => {
              setVisibleItems(prev => [...prev, index]);
 
              if (index === NewHeading.headings.length - 1) {
              }
            }, index * 300);
          });
        } 
    } catch (error) {
      console.error("Error fetching headings:", error);
    } finally{setHeadingLoading(false)}
  };

  const api_station = async() => {
    const Response = await axios.post(
      `/api/stationdata?year=${reportYear}&time_unit=${reportDate}`, 
        {items: [...selectedButtons],}
    )

    const TableData = Response.data
    setStationData(TableData)

  }

  /* ------------------------------------------------------------------
   * Berichtsdownload
   * ------------------------------------------------------------------ */

  const handlereportdownload = async () => {

  /**
   * Bündelt aktuelle Texte, Überschrift und Tabellen in einem ZIP‑Archiv
   * und löst den Browser‑Download aus.
   */

    const api_object = get_current_text();
    if (selectedItem !== null) {
      api_object["5"] = Headings?.headings[selectedItem].toString() || "";
    }

    try {
      const response = await axios.post(
        `/api/downloadfiles?param1=${reportYear}&param2=${reportDate}`,
        api_object,
        {
          responseType: "blob"
        }
      );

      
      const blob = response.data; 
      
      
      const contentDisposition = response.headers['content-disposition']; 
      let filename = `${reportType}-${reportDate}-${reportDate}.zip`;
      
      if (contentDisposition) {
        const filenameMatch = contentDisposition.match(/filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/);
        if (filenameMatch) {
          filename = filenameMatch[1].replace(/['"]/g, '');
        }
      }
      
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = filename;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
      
    } catch (error) {
      console.error('Fehler beim Download:', error);
      alert('Fehler beim Download der Dateien');
    }
  }

  /* ------------------------------------------------------------------
   * Hilfsfunktionen
   * ------------------------------------------------------------------ */

  const change_k_parameter = async(newPeriod:string) => {
      
    /** 
     * Hilfsfunktion Wird aufgerufen, wenn der Nutzer im Datenreiter den Zeitraum wechselt
     * ("k‑Parameter"). Ruft die entsprechenden Daten für das Zeitreihendiagramm neu ab.
     *
     * @param newPeriod - Neues Zeitintervall (Monat / Quartal / Jahr).
     */ 


      const yearNum = parseInt(reportYear, 10);

      const effectiveYear = newPeriod === "Dezember" && reportType === "Quartalsberichte" ? (yearNum - 1).toString() : reportYear;

      const DataTablePromise = fetch(`/api/daten?year=${effectiveYear}&time_unit=${newPeriod}`); 
      const TimeSeriesPromise = fetch(`/api/timeseries?year=${effectiveYear}&time_unit=${newPeriod}`)


      const [DataResponse, TimeSeriesResponse] = await Promise.all([DataTablePromise, TimeSeriesPromise]);


        if (!DataResponse.ok || !TimeSeriesResponse.ok ) {
          setErrorMess(true)
          throw new Error("One or more network responses were not ok");
        }
      

        const ReportData = await DataResponse.json();
        const TimeSeriesData = await TimeSeriesResponse.json();

        setReportData(ReportData);
        setTimeSData(TimeSeriesData)
  }

  /*------------------------------------------------------------------*/

  const get_current_text = () => {

      /**
       * Liefert ein Objekt mit dem aktuell sichtbaren Textzustand aller
       * Paragraphen: Entweder die vom User bearbeiteten Varianten oder
       * die Original unbearbeiteten Varianten 
       */

      const get_keys: {[key: string]: number} = {"0":0, "1":0, "2":0, "3":0, "4":0}

      if (Object.keys(selectedModels).length > 0){
        Object.entries(selectedModels).forEach(([key, value]:[string, number]) => {

          get_keys[key] = value

        })
      }

      const api_object:{[key: string]: string | undefined} = {"0":"", "1":"", "2":"", "3":"", "4":""}
      
     
        
      const getEditKey = (paragraphIndex: string, modelIndex: number) => {
          return paragraphIndex+"-"+`${modelIndex}`;}
          
      Object.entries(get_keys).forEach(([key, value]:[string, number]) => {

        if (editedTexts[getEditKey(key, value)]) {
          api_object[key] = editedTexts[getEditKey(key,value)]
        } else {
          api_object[key] = paragraphs?.tags[parseInt(key)].value[0][value];
        }

      })
      return api_object
  }

  /* ------------------------------------------------------------------
   * TSX‑Return
   * ------------------------------------------------------------------ */
  
    return (
        <div className = "font-sans bg-blue-50">
            <Navbar onReportTypeChange={handleReportTypeChange}
                    currentReportType={reportType}
                    selectedDate = {reportDate}
                    onDateChange={handleReportDateChange}
                    currentReportYear = {reportYear}
                    onYearChange = {handleReportYearChange}
                    isloading={isloading}
                    handleDownload={handleDownload}
                    onGenerateVariations={api_call}
                    paragraphs = {paragraphs}
                    handle_pdf_preview = {handle_pdf_preview}
                    handle_web_search = {handle_web_search}
                    togglemode = {togglemode}
                    settogglemode = {settogglemode}
                    isAnimating = {IsAnimating}
                    handle_dwd_wetter = {handle_dwd_wetter}
                    isAnimatingDWD = {isAnimatingDWD}
                    selectedButtons = {selectedButtons}
                    setSelectedButtons = {setSelectedButtons}
                    ApiStation = {api_station}
                    handlereportdownload = {handlereportdownload}
                    
             />
             <div className = "flex gap-5">
              <Variationdisplay
                isloading={isloading}
                paragraphs={paragraphs}
                CurrentParagraph={CurrentParagraph}
                setCurrentParagraph={setCurrentParagraph}
                editedTexts = {editedTexts}
                setEditedTexts = {setEditedTexts}
                selectedModels = {selectedModels}
                setSelectedModels = {setSelectedModels}
                ErrorMess = {ErrorMess}
                
              />
              <PdfPreview 
                PdfUrl = {PdfUrl}
                currentTab = {currentTab}
                setcurrentTab = {setcurrentTab}
                WebSearch={WebSearch}
                ReportData = {ReportData}
                CurrentParagraph = {CurrentParagraph}
                ReportYear = {reportYear}
                get_heading = {get_heading}
                Heading = {Headings}
                selectedItem = {selectedItem}
                setSelectedItem = {setSelectedItem}
                visibleItems={visibleItems}
                TimeSData = {TimeSData}
                isAnimating = {IsAnimating}
                HeadingLoading = {HeadingLoading}
                paragraphs = {paragraphs}
                DWDWetter={DWDWetter}
                isAnimatingDWD = {isAnimatingDWD}
                StationData = {StationData}
                reportDate = {reportDate}
                ChangeKParam = {change_k_parameter}
                reportType = {reportType}
                isloading = {isloading}
              />
             </div>
        </div>
    );
}

