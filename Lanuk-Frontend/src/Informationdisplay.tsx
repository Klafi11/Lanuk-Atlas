import React from "react";
import {StructuredSum, DataReport, HeadingStruc, TimeSeriesData, Page} from './BaseModels';
import { TooltipProps } from 'recharts';
import { ValueType, NameType } from 'recharts/types/component/DefaultTooltipContent';
import mapping_table_headers from "./utils";
import "./LoadingSpinner.css";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ReferenceLine,
  ResponsiveContainer,
  Legend,
  Cell,
} from "recharts";


/**
 * Informationskomponente für den Berichtsgenerator.
 *
 * Diese Komponente zeigt drei Reiter:
 * 1) **Daten** – Tabellen & Zeitreihen (Recharts) für den gewählten Abschnitt
 * 2) **PDF-Vorschau** – eingebettete PDF-Preview via Blob-URL
 * 3) **Information** – Websuche (mit Quellen) und DWD-Wettertext
 */


interface PdfPrevProps {
  PdfUrl: string | null;
  currentTab: number;
  setcurrentTab: (prev: number) => void;
  WebSearch: StructuredSum | null;
  ReportData: DataReport | null;
  CurrentParagraph: number
  ReportYear: string
  get_heading: () => void;
  Heading: HeadingStruc | null;
  selectedItem: number | null;
  setSelectedItem: (value:number) => void;
  visibleItems: number[]
  TimeSData: TimeSeriesData | null; 
  isAnimating: boolean
  HeadingLoading: boolean
  paragraphs: Page | null;
  DWDWetter: null
  isAnimatingDWD: boolean
  StationData: Record<string, number[] | string[]>;
  reportDate: string
  ChangeKParam: (newPeriod:string)=> void;
  reportType: string
  isloading: boolean;
}

const PdfPreview: React.FC<PdfPrevProps> = ({ PdfUrl, currentTab, setcurrentTab, WebSearch, ReportData, 
  CurrentParagraph, ReportYear, get_heading, Heading, selectedItem, setSelectedItem, isloading,
  visibleItems, TimeSData, isAnimating, HeadingLoading, paragraphs, DWDWetter, isAnimatingDWD, StationData, reportDate, ChangeKParam, reportType}) => {

  

    const handlePeriodChange = (newPeriod: string) => {ChangeKParam(newPeriod)}

    const PeriodDropdown = () => {

      /**
       * Dropdown zur Auswahl eines Zeitraums passend zum aktuellen *reportDate*.
       *
       */

      const getSeasonOptions = () => {
        switch (reportDate) {
          case "Frühling":
            return [
              { value: "Frühling", label: "Frühling" },
              { value: "März", label: "März" },
              { value: "April", label: "April" },
              { value: "Mai", label: "Mai" }
            ];
          case "Winter":
            return [
              { value: "Winter", label: "Winter" },
              { value: "Dezember", label: "Dezember" },
              { value: "Januar", label: "Januar" },
              { value: "Februar", label: "Februar" }
            ];
          case "Sommer":
            return [
              { value: "Sommer", label: "Sommer" },
              { value: "Juni", label: "Juni" },
              { value: "Juli", label: "Juli" },
              { value: "August", label: "August" }
            ];
          case "Herbst":
            return [
              { value: "Herbst", label: "Herbst" },
              { value: "September", label: "September" },
              { value: "Oktober", label: "Oktober" },
              { value: "November", label: "November" }
            ];
          case "Jahr_agg":
            return [
              { value: "Jahr_agg", label: "Jahr" },
              { value: "Dezember", label: "Dezember" },
              { value: "Januar", label: "Januar" },
              { value: "Februar", label: "Februar" },
              { value: "März", label: "März" },
              { value: "April", label: "April" },
              { value: "Mai", label: "Mai" },
              { value: "Juni", label: "Juni" },
              { value: "Juli", label: "Juli" },
              { value: "August", label: "August" },
              { value: "September", label: "September" },
              { value: "Oktober", label: "Oktober" },
              { value: "November", label: "November" },
              { value: "Winter", label: "Winter" },
              { value: "Frühling", label: "Frühling" },
              { value: "Sommer", label: "Sommer" },
              { value: "Herbst", label: "Herbst" },
            ];
            default:
            return [];
        }
      };

      const seasonOptions = getSeasonOptions();

      return (
      <div className="mb-4 flex justify-center">
        <select
          className="w-full bg-gray-200 border-2 border-gray-300 rounded-lg
          px-4 py-3 text-gray-800 font-medium text-center
          focus:outline-none focus:border-gray-500 focus:ring-2 focus:ring-gray-200
          hover:border-gray-400 hover:bg-gray-200
          transition-all duration-200 ease-in-out
          shadow-sm cursor-pointer
          flex items-center justify-center"
          defaultValue={reportDate}
          onChange={(e) => handlePeriodChange(e.target.value)}
        >
          {seasonOptions.map((option) => (
            <option key={option.value} value={option.value}>
              {option.label}
            </option>
          ))}
        </select>
      </div>
      );
    };
  
  const TimeSeriesVis = () => {

    /**
     * Visualisiert die Zeitreihendaten als Balkendiagramm mit Abweichungen
     * zur Referenzperiode. Farbgebung: Blau = negativ, Rot = positiv.
     *
     * Zusätze:
     * - CustomTooltip: zeigt Jahr, Abweichung und Messwert inkl. Einheit.
     * - CustomLegend: Farb-/Referenzcodierung.
     * - ReferenceLine: markiert Referenzperioden ("1881-1910"/"1951-1980", "1991-2020").
     */

    const currentEntry = TimeSData?.[CurrentParagraph];

    if (!currentEntry || !currentEntry.values || !currentEntry.ref) {
    return 
  }

  const renderCustomLegend = () => {

    /* FUnktion zum Anzeigen der Custom Legende im Zeitreihendigramm der Anwendung*/

  return (
    <div style={{ display: 'flex', justifyContent: 'center', gap: '20px' }}>
      <div style={{ display: 'flex', alignItems: 'center' }}>
        <div style={{
          width: '15px',
          height: '15px',
          backgroundColor: 'cornflowerblue',
          marginRight: '5px'
        }} />
        <span>Negative Abweichung</span>
      </div>
      <div style={{ display: 'flex', alignItems: 'center' }}>
        <div style={{
          width: '15px',
          height: '15px',
          backgroundColor: 'red',
          marginRight: '5px'
        }} />
        <span>Positive Abweichung</span>
      </div>
      <div style={{ display: 'flex', alignItems: 'center' }}>
        <div style={{
          width: '15px',
          height: '15px',
          backgroundColor: 'orange',
          marginRight: '5px'
        }} />
        <span>{[0,1].includes(CurrentParagraph) ? "1881-1910": "1951-1980"}</span>
      </div>
      <div style={{ display: 'flex', alignItems: 'center' }}>
        <div style={{
          width: '15px',
          height: '15px',
          backgroundColor: 'green',
          marginRight: '5px'
        }} />
        <span>1991-2020</span>
      </div>
          <div style={{ display: 'flex', alignItems: 'center' }}>
        <div style={{
          width: '15px',
          height: '15px',
          backgroundColor: 'grey',
          marginRight: '5px'
        }} />
        <span>1961-1990</span>
      </div>
      
    </div>
  );
};


  const CustomTooltip = ({active, payload, label }: TooltipProps<ValueType, NameType>) => {
    /**
     * Custom Tooltip für Zeitreihendiagramm.
     */

    if (active && payload && payload.length) {
      const dataItem = payload[0].payload;

      const unit = CurrentParagraph === 0 ? "K" : 
                CurrentParagraph === 1 ? "l/m²" : 
                "h";
      
      return (
        <div className="bg-white p-3 border border-gray-300 rounded shadow-lg">
          <p className="font-bold">{`Year: ${label}`}</p>
          <p className={dataItem.Abweichung< 0 ? "text-blue-600" : "text-red-600"}>{`Abweichung: ${dataItem.Abweichung} ${unit}`}</p>
          {dataItem.Temperatur && (
            <p className="text-gray-600">{` ${CurrentParagraph === 0 ? "Temperatur": CurrentParagraph === 1 ? "Niederschlag" : "Sonnenscheindauer" }: ${dataItem.Temperatur} ${CurrentParagraph !== 0 ? unit : "°C"}`} </p>
          )}
        </div>
      );
    }

    return null;
  };
  
  
  const { values: data, ref } = currentEntry;
    
    return (
      <div className="w-full h-[600px] ml-0">
        <ResponsiveContainer width="100%" height="100%"  minWidth={0} minHeight={0}>
          <BarChart
            data={data}
            margin={{ top: 40, right: 30, left: -6, bottom: 60 }}
          >
            <CartesianGrid strokeDasharray="8" />
            <XAxis dataKey="Jahr" />
            <YAxis
              label={{
                value: `${CurrentParagraph == 0 ? "Abweichung (K)": CurrentParagraph == 1 ? "Abweichung in l/m²": "Abweichung in h "}`,
                angle: -90,
                position: "Left",
                dx: -15
                
              }}
            />
            <Tooltip 
            content = {CustomTooltip}/>
            <Legend 
            content = {renderCustomLegend}/>
            <Bar
              dataKey="Abweichung"
              fill="#8884d8"
              radius={[4, 4, 0, 0]}
            >
              {data?.map((entry, index) => (
                <Cell
                  key={`cell-${index}`}
                  fill={entry.Abweichung < 0 ? "cornflowerblue" : "red"}
                />
              ))}
            </Bar>
            <ReferenceLine segment={[0, 1].includes(CurrentParagraph)? [{x: data?.[0].Jahr, y: ref["1881-1910"] - ref["1961-1990"] }, { x: 1910, y: ref["1881-1910"] - ref["1961-1990"]}] :
            [{x: data?.[0].Jahr, y: ref["1951-1980"] - ref["1961-1990"] }, { x: 1980, y: ref["1951-1980"] - ref["1961-1990"]}] }  stroke="orange" strokeWidth={9}/>
            <ReferenceLine segment={[{ x: 1991, y: ref["1991-2020"] - ref["1961-1990"] }, { x: 2020, y: ref["1991-2020"] - ref["1961-1990"] }]} stroke="green" strokeWidth={9}/>
          </BarChart>
        </ResponsiveContainer>
      </div>
    );
  };

  

  const DataTableStation = () => {

    /**
     * Rendert die Tabelle für die Stationsdaten des ButtonGrids.
     * 
     */

    const rm_key = ["Saison"]
    const data = StationData
    const Saison = (StationData?.Saison?.[0] as string) || "Jahr_agg";
    const labels = mapping_table_headers(3, ReportYear, Saison)
    const Stationnames = { ...StationData };


    if ("Saison" in Stationnames) {
    rm_key.forEach(element => { delete Stationnames?.[element] });}

    const prefixes = Object.keys(Stationnames || {}).map((key) =>(key.split('_')[0]))
    const uniquePrefixes = [...new Set(prefixes)];

    return(
        <table className = "w-full border-collapse rounded-2xl overflow-hidden text-center shadow-md">
          <thead> 
            <tr className = "bg-blue-800 text-white">
              <th className="px-4 py-2 border">Kenntage </th>
              {uniquePrefixes.map((key) => (
                <th key = {key} className="px-4 py-2 border"> {key}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {
              Object.entries(labels || {}).map(([up_key, value]) => (
                <tr  key = {up_key} className = "bg-white">
                  <td className="px-4 py-2 w-96 border bg-blue-800 text-white font-bold">{value}</td>
                  {uniquePrefixes.map((key) => 
                  <td key = {`${key}-${up_key}`} className="px-4 py-2 border">{data[`${key}_${up_key}`]} {" "} {up_key === "tiefsttemperatur" || up_key === "höchsttemperatur" ? "°C" : "" }</td> )}
                
                </tr>
              ))
            }
          
          </tbody>
        </table>

      )
  }

  
  const DataTable = () => {

    /**
     * Rendert die Datentabelle für den aktuell gewählten Paragraphen.
     *
     * Paragraph 0–2: Kennzahlenzeile mit Einheiten (°C, l/m², h)
     * Paragraph 3:   Stationsübergreifende Kenntage-Tabelle
     * Paragraph 4:   UI zur Überschriftenerzeugung (Button + Liste)
     */


    const rm_key = ["Jahr", "Saison", "Monat"]

    const data = ReportData?.["data"][0][CurrentParagraph] 
    const Saison = ReportData?.data?.[0]?.[3]?.Saison?.[0] || "Jahr_agg";
    const labels = mapping_table_headers(CurrentParagraph, ReportYear, Saison)
    const Stationnames = ReportData?.["data"][0][3]

    rm_key.forEach(element => {delete Stationnames?.[element]});
    const prefixes = Object.keys(Stationnames || {}).map((key) =>(key.split('_')[0]))
    const uniquePrefixes = [...new Set(prefixes)];




    if ([0, 1, 2].includes(CurrentParagraph)) {
      
      
      return (
        <table className="w-full mt-4 border-collapse rounded-2xl mb-2 overflow-hidden text-center shadow-md">
          <thead>
            <tr className = "bg-blue-800 text-white" >
              {
                Object.entries(labels || {}).map(([Key, value]) => (
                  <th className = "px-4 py-2 border" key = {Key}> 
                  {value} </th>
                ))
              }
            </tr>
          </thead>
          <tbody>
            <tr className="bg-white">
              {Object.keys(labels || {}).map((key) => (
                <td key={key} className="px-4 py-2 border">
                        {data[key]}{" "}
                        {CurrentParagraph === 0 && key !== "ranking_temp" ? "°C" 
                          : CurrentParagraph === 1  && key !== "ranking_rain" && key !== "ranking_rain_min"
                          ? "l/m²"
                          : CurrentParagraph === 2 && key !== "ranking_sun" && key !== "ranking_sun_min"
                          ? "h"
                          : ""}
                </td>
              ))}
            </tr>  
          </tbody>
        </table>
      );
    }

    if (CurrentParagraph === 3){

      return(
        <table className = "w-full border-collapse rounded-2xl overflow-hidden text-center shadow-md">
          <thead> 
            <tr className = "bg-blue-800 text-white">
              <th className="px-4 py-2 border">Kenntage </th>
              {uniquePrefixes.map((key) => (
                <th key = {key} className="px-4 py-2 border"> {key}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {
              Object.entries(labels || {}).map(([up_key, value]) => (
                <tr  key = {up_key} className = "bg-white">
                  <td className="px-4 py-2 w-96 border bg-blue-800 text-white font-bold">{value}</td>
                  {uniquePrefixes.map((key) => 
                  <td key = {`${key}-${up_key}`} className="px-4 py-2 border">{data[`${key}_${up_key}`]} {" "} {up_key === "tiefsttemperatur" || up_key === "höchsttemperatur" ? "°C" : "" }</td> )}
                
                </tr>
              ))
            }
          
          </tbody>
        </table>

      )

    }

    if (CurrentParagraph === 4) {
      return (
      <div className="flex flex-col justify-center items-center p-4">
        <button 
          className="px-4 py-2 font-bold text-white bg-blue-500 rounded-md hover:bg-blue-600 disabled:opacity-50"
          onClick={get_heading}
          disabled = {HeadingLoading}
        > {HeadingLoading ? "Loading..." : "generiere Überschrift"}
        </button>
        
        <div className="w-full max-w-md mt-6 flex justify-center items-center">
            <div className="w-full space-y-2">
              {Heading?.headings?.map((item, index) => (
                <div
                  key={index}
                  onClick={() => setSelectedItem(index)}
                  className={`transform transition-all duration-300 p-4 rounded-md border border-gray-200 shadow-sm hover:shadow-md cursor-pointer ${
                    selectedItem === index ? 'bg-blue-100 border-blue-300' : 'bg-white'
                  } ${
                    visibleItems.includes(index) ? 'translate-y-0 opacity-100' : 'translate-y-4 opacity-0'
                  }`}
                >
                  {item}
                </div>
              ))}
            </div>
        </div>
      </div>
    );
      
  }

  } 
  
  /* ------------------------------------------------------------------
   * TSX‑Return
   * ------------------------------------------------------------------ */
  
  return (
    <div className="w-[50%] flex flex-col shadow-md bg-gray-200 rounded-lg h-[calc(96vh-240px)] ml-10 overflow-hidden">
      <div className="w-full bg-gray-300 shadow-md rounded-t-lg flex">

        {/* Setzt den jeweiligen Reiter für Daten, PDF-Preview, Informationen*/}

        <button 
          className={`flex-1 font-medium ${currentTab === 1 ? 'bg-gray-400 text-gray-900' : 'text-gray-700'} rounded hover:text-gray-900 py-2 hover:bg-gray-400 text-center`}
          onClick={() => setcurrentTab(1)}
        >
          Daten
        </button>
        <button 
          className={`flex-1 font-medium ${currentTab === 2 ? 'bg-gray-400 text-gray-900' : 'text-gray-700'} rounded hover:text-gray-900 py-2 hover:bg-gray-400 text-center`}
          onClick={() => setcurrentTab(2)}
        >
          PDF-Vorschau
        </button>
        <button 
          className={`flex-1 font-medium ${currentTab === 3 ? 'bg-gray-400 text-gray-900' : 'text-gray-700'} rounded hover:text-gray-900 py-2 hover:bg-gray-400 text-center`}
          onClick={() => setcurrentTab(3)}
        >
          Information
        </button>
      </div>
      <div className={`w-full h-full ${currentTab === 3 ?"overflow-y-auto" : ""} `}>

        {/* Reiter Daten*/}
        {currentTab === 1 && (
          <div className="h-full w-full flex flex-col px-4 py-4 overflow-auto">
            <h2 className="text-xl font-semibold mb-4">Daten</h2>
            {ReportData && TimeSData && TimeSData !== null ? (
              <>
                {CurrentParagraph !== 4 && reportType !== "Monatsberichte" && (PeriodDropdown())}
                {DataTable()}
                {TimeSeriesVis()}
              </>
            ) : (
              <>
                {!isloading && StationData && Object.keys(StationData).length > 0 ? (
                  <>
                    <h3 className="text-lg font-medium mb-2">Stationsdaten</h3>
                    {DataTableStation()}
                  </>
                ) : (
                  <p className="text-gray-600">
                    In diesem Tab können Sie die Daten des entsprechenden Report-Abschnitts einsehen. 
                    <br></br>
                    Die Reiter <strong>Temperatur</strong>, <strong>Niederschlag</strong> und <strong>Sonnenscheindauer</strong> enthalten jeweils:
                    <ul className="list-disc pl-4 mt-0">
                        <li>Eine grafische Zeitreihendarstellung</li>
                        <li>Die zugehörige Datentabelle für die gewählte Zeiteinheit</li>
                    </ul>
                    <br></br>
                    Der Reiter <strong>Kenntageauswertung</strong> bietet eine tabellarische Übersicht der für die Zeiteinheit relevanten Kenndaten.
                    <br></br>
                    Wenn Sie über die <strong>Chevron-Pfeile</strong> zur Einleitung navigieren, können Sie sich über den Button <strong>"generiere Überschrift"</strong> automatisch passende Report-Überschriften generieren lassen.
                  </p>
                )}
              </>
            )}
          </div>
        )}
        {/* Reiter PDF-Preview*/}
        {currentTab === 2 && (
          <>
            {PdfUrl ? (
              <iframe
                src={PdfUrl}
                className="w-full h-full rounded shadow-md"
                title="PDF Preview"
              />
            ) : (
              <div className="p-4">
                <h2 className="text-xl font-semibold mb-4"> PDF-Vorschau</h2>
                <p className="text-gray-600">Durch einen Klick auf den <strong>„PDF-Vorschau“-Button</strong> erhalten Sie eine Vorschau des Berichts im PDF-Format.</p>
              </div>
            )}
          </>
        )}
        {/* Reiter Informationen*/}
        {currentTab === 3 && (
            <div className="p-4 w-full h-full mb-4 relative">
              <h2 className="text-xl font-semibold mb-4">Information</h2>
                
                {isAnimatingDWD ? (
                  <div className={`${WebSearch ? "flex flex-col items-center justify-center py-36": "absolute inset-0 flex flex-col items-center justify-center"}`}>
                      <span className="loader2"></span>
                  </div>
                ):
                DWDWetter && (
                  <>
                    <h2 className = "text-xl font-semibold mb-4">DWD Wetterbericht</h2>
                    <div className="bg-white p-4 rounded-md shadow mb-8">{DWDWetter}</div>
                  </>
                )}    
                {paragraphs?.tags[4]?.intro && (
                  <>
                    <h2 className = "text-xl font-semibold mb-4">DWD Wetterbericht</h2>
                    <div className="bg-white p-4 rounded-md shadow mb-8">{paragraphs.tags[4].intro}</div>
                  </>
                )}             
                
                {isAnimating ? (
                      <div className={`${paragraphs?.tags[4].intro || DWDWetter ? "flex flex-col items-center justify-center py-36": "absolute inset-0 flex flex-col items-center justify-center"}`}>
                          <span className="loader2"></span>
                      </div>                    
                    ):
                WebSearch ? (
                <>
                  <h2 className="text-xl font-semibold mb-4">Websuche</h2>
                  <div className="bg-white p-4 rounded shadow mb-4">
                  <p className="text-gray-800">{WebSearch.summarization}</p>
                  </div>
                  <div className="bg-white p-4 pb-7 rounded mb-8 shadow">
                    <h3 className="font-medium mb-2">Quellen:</h3>
                    <ul className="list-decimal pl-5">
                      {WebSearch.citations.map((citation, index) => (
                        <li key={index} className="mb-1">
                          <a
                            href={citation}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="text-blue-600 hover:underline"
                          >
                            {citation}
                          </a>
                        </li>
                      ))}
                    </ul>
                  </div>
                  <div className="h-5"></div>
                </>
                ) : (!isAnimatingDWD && !DWDWetter && !paragraphs?.tags[4]?.intro && !isAnimating && !WebSearch) &&  (
                <p className="text-gray-600">In diesem Reiter erhalten Sie weitere Informationen über die <strong>Websuche</strong> sowie die <strong>DWD Berichte</strong>.</p>
                )}
            </div>
        )}
      </div>
    </div>
  );
};

export default PdfPreview;