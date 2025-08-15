import React from 'react';
import {Page} from './BaseModels';
import ButtonGrid from './ButtonGrid';


/**
 * Navigations- und Steuer-Komponente für den Berichtsgenerator.
 *
 * Verantwortlichkeiten:
 * - Auswahl von Berichtstyp, Jahr und Zeitraum (Monat/Quartal).
 * - Umschalten zwischen "standard" und "advanced"-Modus.
 * - Triggern der Hauptaktionen: Generierung, PDF-Vorschau, Websuche, DWD-Wetterabruf sowie ZIP-Download.
 * - 3x3 Grid zur Stationsauswahl (Feature außerhalb der Berichtsgenerierung)
 *
 */


interface NavbarProps {

    /**
     * Props für <NavbarMenu>.
     */

    onReportTypeChange: (type: string) => void;
    onDateChange: (date: string) => void;
    currentReportType: string;
    selectedDate: string;
    currentReportYear: string;
    onYearChange: (year: string) => void;
    onGenerateVariations: () => void;
    isloading: boolean;
    handleDownload: (format: 'docx' | 'pdf') => void;
    paragraphs: Page | null;
    handle_pdf_preview: () => void;
    handle_web_search: () => void;
    togglemode: string
    settogglemode: (togle: string) => void;
    isAnimating: boolean
    handle_dwd_wetter: () => void;
    isAnimatingDWD: boolean;
    selectedButtons: Set<string>;
    setSelectedButtons: React.Dispatch<React.SetStateAction<Set<string>>>;
    ApiStation: () => void;
    handlereportdownload: () => void;

}

const NavbarMenu: React.FC<NavbarProps> = ({ 
    onReportTypeChange, 
    onDateChange,
    currentReportType,
    selectedDate,
    currentReportYear,
    onYearChange,
    onGenerateVariations,
    isloading,
    paragraphs,
    handle_pdf_preview,
    handle_web_search,
    togglemode,
    settogglemode,
    isAnimating,
    handle_dwd_wetter,
    isAnimatingDWD,
    selectedButtons,
    setSelectedButtons,
    ApiStation,
    handlereportdownload
}) => {
    const reportTypes = ["", "Monatsberichte", "Quartalsberichte", "Jahresberichte"];


       /* ------------------------------------------------------------------
        * Hilfsfunktionen
        * ------------------------------------------------------------------ */
    
    const getDateOptions = (ReportType: string = currentReportType) => {

        /* 
        * Hilfsfunktion zum erstellen der Dropdowns für die verschiednene Berichttypen
        */
        switch(ReportType) {
            case 'Monatsberichte':
                return ['', 'Januar', "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"];
            case 'Quartalsberichte':
                return ['', 'Winter', "Frühling", "Sommer", "Herbst"];
            case 'Jahresberichte':
                return ['', '2024', '2025', '2026'];
            default:
                return [''];
        }
    };

    const getYearOptions = () => {

        /* 
        * Hilfsfunktion für Jahre des Dropdown Menu der Jahresberichte 
        */

        const currentYear = new Date().getFullYear();
        return ['', ...Array.from({ length: 11 }, (_, i) => (currentYear - 5 + i).toString())];
    };

    const getDateLabel = () => {

        /* 
        * Hilfsfunktion für Daten Labels
        */
        switch(currentReportType) {
            case 'Monatsberichte':
                return 'Monat';
            case 'Quartalsberichte':
                return 'Quartal';
            case 'Jahresberichte':
                return 'Jahr';
            default:
                return 'Zeitraum';
        }
    };

    const dateOptions = getDateOptions();
    const yearOptions = getYearOptions();
    const dateLabel = getDateLabel();

    
    const isGenerateDisabled = () => {

        /* 
        * Hilfsfunktion für Button Disabeling
        */

        if (isloading) return true;
        if (isAnimating) return true;
        if (isAnimatingDWD) return true;
        if (!currentReportType) return true;
        if (!currentReportYear) return true;
        if (currentReportType !== 'Jahresberichte' && !selectedDate) return true;
        if (currentReportType === "Monatsberichte" && !getDateOptions("Monatsberichte").includes(selectedDate)) return true;
        if (currentReportType === "Quartalsberichte" && !getDateOptions("Quartalsberichte").includes(selectedDate)) return true;
        return false;
    };

    const toggle = () => {

        /* 
        * Toggle Button für beide Modi (Standard, Advanced)
        */
        
        const isAdvanced = togglemode === "advanced"

        const toggleswitch = () =>{
            const newMode = isAdvanced? "standard" : "advanced"
            settogglemode(newMode)
        }

        return (
            <div className="flex items-center space-x-3 pr-3">
              <button
                type="button"
                role="switch"
                aria-checked={isAdvanced}
                onClick={toggleswitch}
                className={`relative inline-flex h-7 w-14 items-center rounded-full transition-colors focus:outline-none ${
                  isAdvanced ? 'bg-blue-600' : 'bg-gray-400'
                }`}
              >
                <span
                  className={`inline-block h-7 w-7 transform rounded-full bg-white transition-transform ${
                    isAdvanced ? 'translate-x-8' : 'translate-x-0'
                  }`}
                />
              </button>
              <span className={`text-ml font-bold ${isAdvanced ? "text-blue-600" : "text-gray-600"}`}>
                {isAdvanced ? 'Advanced' : 'Standard'}
              </span>
            </div>
          );
    }

  /* ------------------------------------------------------------------
   * TSX‑Return
   * ------------------------------------------------------------------ */

   return (
    <div className="flex flex-col gap-2.5 m-5 p-5 bg-gray-200 shadow-md rounded-lg sticky top-0 z-10 mb-5">
        {/* Logo */}
        <div className="absolute top-9 right-9">
            <img src="/Icon_Klimaatlas.png" className="max-w-96 max-h-96"/>
        </div>


        <div className="flex gap-5">
            <div className="flex flex-col gap-2.5 w-fit pr-3 mr-6">
                {/* Dropdown Menuauswahl*/}
                <div className="flex items-end gap-5">
                    <div className="flex flex-col">
                        <label className="text-sm text-gray-700 mb-1">Report Type</label>
                        <select 
                            className="appearance-none shadow-md bg-gray-100 border border-gray-300 rounded-lg py-3 px-4 pr-10 text-base text-gray-700 cursor-pointer transition-all hover:border-gray-400 focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100 min-w-[200px]"
                            value={currentReportType} 
                            onChange={(e) => onReportTypeChange(e.target.value)}
                            style={{
                                backgroundImage: `url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='%23374151'%3E%3Cpath d='M7 10l5 5 5-5z'/%3E%3C/svg%3E")`,
                                backgroundRepeat: 'no-repeat',
                                backgroundPosition: 'right 12px center',
                                backgroundSize: '20px',
                            }}
                        >
                            {reportTypes.map((type, index) => (
                                <option key={type || `empty-${index}`} value={type}>
                                    {type || "-- Bitte auswählen --"}
                                </option>
                            ))}
                        </select>
                    </div>

                        <>
                            <div className='flex flex-col'>
                                <label className='text-sm text-gray-700 mb-1'>Jahr</label>
                                <select 
                                    className='appearance-none shadow-md bg-gray-100 border border-gray-300 rounded-lg py-3 px-4 pr-10 text-base text-gray-700 cursor-pointer transition-all hover:border-gray-400 focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100 min-w-[200px]'
                                    value={currentReportYear}
                                    onChange={(e) => onYearChange(e.target.value)}
                                    style={{
                                        backgroundImage: `url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='%23374151'%3E%3Cpath d='M7 10l5 5 5-5z'/%3E%3C/svg%3E")`,
                                        backgroundRepeat: 'no-repeat',
                                        backgroundPosition: 'right 12px center',
                                        backgroundSize: '20px',
                                    }}                           
                                >
                                    {yearOptions.map((year, index) => (
                                        <option key={year || `empty-year-${index}`} value={year}>
                                            {year || "-- Jahr auswählen --"}
                                        </option>
                                    ))}
                                </select>
                            </div>
                            
                        
                            {currentReportType !== 'Jahresberichte' && (
                                <div className="flex flex-col">
                                    <label className="text-sm text-gray-700 mb-1">{dateLabel}</label>
                                    <select 
                                        className="appearance-none shadow-md bg-gray-100 border border-gray-300 rounded-lg py-3 px-4 pr-10 text-base text-gray-700 cursor-pointer transition-all hover:border-gray-400 focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100 min-w-[200px]"
                                        value={selectedDate} 
                                        onChange={(e) => onDateChange(e.target.value)}
                                        style={{
                                            backgroundImage: `url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='%23374151'%3E%3Cpath d='M7 10l5 5 5-5z'/%3E%3C/svg%3E")`,
                                            backgroundRepeat: 'no-repeat',
                                            backgroundPosition: 'right 12px center',
                                            backgroundSize: '20px',
                                        }}
                                    >
                                        {dateOptions.map((date, index) => (
                                            <option key={date || `empty-date-${index}`} value={date}>
                                                {date || `-- ${dateLabel} auswählen --`}
                                            </option>
                                        ))}
                                    </select>
                                </div>
                            )}
                        </>
                    {toggle()}                     
                </div>

                {/* Auwahl Buttons der Anwendung (Download, Websuche, DWD Wetterbericht, ...) */}
                <div className="flex justify-between items-center mt-4">
                    <button 
                        onClick={onGenerateVariations} 
                        disabled={isGenerateDisabled()}
                        className={`
                            bg-blue-500 text-white rounded-lg px-6 py-3 text-base shadow-md font-bold h-12 transition-colors 
                            ${isGenerateDisabled() ? 'bg-gray-400 cursor-not-allowed' : 'hover:bg-blue-600'}
                        `}
                    >
                        {isloading ? 'Generierung...' : 'Dokument generieren'}
                    </button>
                    
                    {paragraphs && (
                        <div className="relative mr-auto ml-4">
                 
                            <button 
                                className={`bg-blue-500 text-white rounded-lg px-6 py-3 text-base font-bold h-12 transition-colors ${isloading ? 'bg-gray-400 cursor-not-allowed' : 'hover:bg-blue-600' }`}
                                onClick={handle_pdf_preview}
                                disabled={isloading}
                            >
                                PDF-Vorschau
                            </button>
                            <button 
                                className={`bg-blue-500 text-white ml-4 rounded-lg px-6 py-3 text-base font-bold h-12 ${isAnimating || isloading || isAnimatingDWD ? 'bg-gray-400 cursor-not-allowed' : 'hover:bg-blue-600' } transition-colors hover:bg-blue-600 group`}
                                onClick={handle_web_search}
                                disabled={isAnimating || isloading || isAnimatingDWD}
                            >
                                {isAnimating ? 'Generierung...' : 'Websuche'}
                            </button>
                            {Number(currentReportYear) >= 2025 && ["April", "Mai", "Juni", "Juli"].includes(selectedDate) && togglemode === "standard" && paragraphs.tags[4].intro === null && (
                                <button
                                    className={`bg-blue-500 text-white ml-4 rounded-lg px-6 py-3 text-base font-bold h-12 ${isAnimating || isloading || isAnimatingDWD ? 'bg-gray-400 cursor-not-allowed' : 'hover:bg-blue-600'} transition-colors hover:bg-blue-600 group`}
                                    onClick={handle_dwd_wetter}
                                    disabled={isAnimating || isloading || isAnimatingDWD}
                                >
                                    {isAnimatingDWD ? 'Generierung...' : 'DWD Wetterbericht'}
                                </button>
                            )}
                            {!isloading && paragraphs && (
                            <button
                                className={`bg-orange-500 hover:bg-orange-600 text-white ml-4 rounded-lg px-6 py-3 text-base font-bold h-12 ${isAnimating || isloading || isAnimatingDWD ? 'bg-gray-400 cursor-not-allowed' : 'hover:bg-orange-600'} transition-colors`}
                                onClick={handlereportdownload}
                                disabled={isAnimating || isloading || isAnimatingDWD}
                            >
                                Download & Save
                            </button>
                            )}
                        </div>
                    )}
                </div>
            </div>
            {!paragraphs && !isloading && (
            {/* ButtonGrid */}       
            <div className="flex-1">
                <ButtonGrid 
                    selectedButtons={selectedButtons}
                    setSelectedButtons={setSelectedButtons}
                    onApiCall={ApiStation}
                    isGenerateDisabled = {isGenerateDisabled}
                />
            </div>
            )}

        </div>
    </div>
);
};

export default NavbarMenu;