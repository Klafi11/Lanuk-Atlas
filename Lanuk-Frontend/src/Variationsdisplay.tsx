import React, { useState, useEffect } from 'react';
import {Page} from './BaseModels';
import "./LoadingSpinner.css"
import { ChevronLeft, ChevronRight, Save } from "lucide-react";
import TextareaAutosize from 'react-textarea-autosize';


/**
 * # Variationdisplay
 *
 * ----------------------------
 * Diese React-Komponente zeigt für einen ausgewählten Absatz ("Paragraph")
 * verschiedene Text-Variationen an, die jeweils von unterschiedlichen
 * Sprachmodellen(GPT, Claude, Deepseek) erzeugt wurden. Nutzer:innen können pro Absatz ein Modell
 * auswählen, den vorgeschlagenen Text per Doppelklick in einen
 * Bearbeitungsmodus versetzen und die Änderungen lokal speichern. Zudem steht
 * eine Navigation zwischen den Absätzen zur Verfügung.
 *
 * **Hauptfeatures**
 * - Modellwahl je Absatz (visuell durch farbige Rahmen und Legende)
 * - Editiermodus mit Autosize-Textarea und Speichern-Button
 * - Absatz-Navigation via Chevron-Buttons
 * - Ladezustand mit animierten Punkten und Spinner
 */


interface VariationsPanelProps {
    isloading: boolean;
    paragraphs: Page | null;
    CurrentParagraph: number;
    setCurrentParagraph:  React.Dispatch<React.SetStateAction<number>>;
    editedTexts: Record<string, string>;
    setEditedTexts: React.Dispatch<React.SetStateAction<Record<string, string>>>;
    selectedModels: Record<number, number>;
    setSelectedModels: React.Dispatch<React.SetStateAction<Record<number, number>>>
    ErrorMess: boolean


}

const Variationdisplay: React.FC<VariationsPanelProps> = ({
    isloading,
    paragraphs,
    CurrentParagraph,
    setCurrentParagraph,
    setEditedTexts,
    editedTexts,
    selectedModels,
    setSelectedModels,
    ErrorMess

}) => {


    const [dots, setDots] = useState("");
    const [isEditing, setIsEditing] = useState(false)


    /* ------------------------------------------------------------------
    * Hilfsfunktionen
    * ------------------------------------------------------------------ */
    

    useEffect(() => {
        if (!isloading) {
            setDots("");
            return;
        }

        const interval = setInterval(() => {
            setDots((prev) => (prev.length < 3 ? prev + "." : ""));
        }, 500);

        return () => clearInterval(interval);
    }, [isloading]);



   
    const llmModels = ['OpenAI-GPT', 'Claude-Sonnet', 'Deepseek-V'];
    const modelColors = ['#FF6B6B', '#4ECDC4', '#3b82f6'];
    const idMapping: { [key: string]: string } = {
        "get_temp_report_month": "Temperatur",
        "get_temp_report_quarter": "Temperatur",
        "get_temp_report_year": "Temperatur",
        "get_sun_report_month": "Sonnenscheindauer",
        "get_sun_report_quarter": "Sonnenscheindauer",
        "get_sun_report_year": "Sonnenscheindauer",
        "get_rain_report_month": "Niederschlag",
        "get_rain_report_quarter": "Niederschlag", 
        "get_rain_report_year": "Niederschlag",
        "get_station_report_month": "Kenntageauswertung",
        "get_station_report_year": "Kenntaugeauswertung",
        "get_station_report_quarter":"Kenntageauswertung",
        "get_report_introduction": "Einleitung"
    }

    const handleModelSelect = (index:number) => {
      /** Wählt ein Modell (per Index) für den aktuellen Absatz aus. */
      setSelectedModels(prev => ({
        ...prev,
        [CurrentParagraph]: index
      }));
    };
  
    const renderLegend = () => {
      /**
       * Rendert die Modell-Legende (Buttons) und markiert das aktuell
       * ausgewählte Modell.
       */
      const currentModelIndex = selectedModels[CurrentParagraph] || 0;
    
    return(

        <div className="flex flex-wrap gap-2.5 mr-2-5 item-center">
          {llmModels.map((model, index) => (
            <button
              key={model}
              onClick={() => handleModelSelect(index)}
              disabled = {isEditing}
              className={`bg-white flex border-4 shadow-md rounded-md px-2 py-1 font-bold text-x text-center hover:shadow-md min-w-[80px] transition-all ${currentModelIndex === index ? 'ring-4 ring-black' : ''}`}
              style={{ borderColor: modelColors[index] }}
            >
              {model}
            </button>
          ))}
        </div>
      );
    }

    const getEditKey = (paragraphIndex: number, modelIndex: number) => {
      /* Gibt Key-Schlüsselpaar zurück 
      */

      return `${paragraphIndex}-${modelIndex}`;
    };

    const getCurrentText = (paragraphIndex: number, modelIndex: number, variationsDict: Record<number, string>) => {
      /**
       * Liefert den anzuzeigenden Text für den gegebenen Absatz-/Modellindex.
       * Gibt bevorzugt einen lokal editierten Text zurück, fällt ansonsten auf
       * die Variation aus `variationsDict` zurück.
       */ 

      const editKey = getEditKey(paragraphIndex, modelIndex);
      
 
      const variationKeys = Object.keys(variationsDict)
        .map(Number)
        .sort((a, b) => a - b);
      
  
      const currentKey = variationKeys[modelIndex];
      
     
      return editedTexts[editKey] !== undefined ? 
        editedTexts[editKey] : 
        variationsDict[currentKey];
    };

    const handleTextChange = (e: React.ChangeEvent<HTMLTextAreaElement>, paragraphIndex: number, modelIndex: number) => { 
      /**
       * Aktualisiert den lokalen Edit-Puffer beim Tippen.
       */

      const editKey = getEditKey(paragraphIndex, modelIndex);
      setEditedTexts(prev => ({
        ...prev,
        [editKey]: e.target.value
      }));
    };

    const handleSave = () => {
      /**
       * Beendet den Editiermodus und belässt die Änderungen im lokalen State.
       */
      if (!paragraphs) return;
      setIsEditing(false);
    };

    const VariationsContainer = () => {
      /**
       * Container für den Variationsbereich (Anzeige + Editieren eines Textes).
       * Kapselt Datensichtung, Fallbacks und die Edit-Interaktionen.
       */

      if (!paragraphs) {
        return <div className="text-red-500 p-4">No data available</div>;
      }

      const variationsDict = paragraphs.tags[CurrentParagraph]?.value?.[0];
      const currentModelIndex = selectedModels[CurrentParagraph] || 0;

      if (!variationsDict) {
        return <div className="text-red-500 p-4">No variations data available</div>;
      }
      
      const variationKeys = Object.keys(variationsDict)
        .map(Number)
        .sort((a, b) => a - b);
        
      if (variationKeys.length === 0) {
        return <div className="text-red-500 p-4">No variations found</div>;
      }

   
      const currentText = getCurrentText(CurrentParagraph, currentModelIndex, variationsDict);
      
     
      const editKey = getEditKey(CurrentParagraph, currentModelIndex);

      const handleStartEditing = () => {

        /**
         * Startet den Editiermodus. Falls noch kein lokaler Text vorhanden ist,
         * wird der aktuelle Text als Ausgangsbasis in den Edit-Puffer gelegt.
         */
    
        if (editedTexts[editKey] === undefined) {
          setEditedTexts(prev => ({
            ...prev,
            [editKey]: currentText
          }));
        }
        setIsEditing(true);
      };

      return (
        <div className="flex p-4 justify-center bg-gray-100 rounded-md shadow-md mb-4 mt-10 relative">

            <div
              className=" flex bg-white border-4 rounded-md shadow-md p-4 break-words whitespace-pre-wrap max-h-[58vh] min-w-[70vh] overflow-auto"
              style={{ borderColor: modelColors[currentModelIndex] }}
            >
              {isEditing ? (
                <>
                  <TextareaAutosize
                    value={editedTexts[editKey] !== undefined ? editedTexts[editKey] : currentText}
                    minRows={20}
                    lang='de'
                    onChange={(e) => {
                      handleTextChange(e, CurrentParagraph, currentModelIndex)}}
                    className="w-full p-2 border border-gray-300 focus:outline-none shadow-md focus:ring-2 focus:ring-blue-500 text-lg rounded-md overflow-auto"
                  />
                  <button
                    onClick={() => handleSave()}
                    className=" absolute bottom-7 right-7 p-2 bg-green-500 text-white rounded-full shadow-md hover:bg-green-600 transition flex items-center justify-center"
                    title="Save changes"
                  >
                    <Save size={24} />
                  </button>
                </>
              ) : (
                <div 
                  onDoubleClick={handleStartEditing}
                  className="cursor-text"
                >
                  {currentText}
                </div>
              )}
            </div>
          </div>
      );
    };
    
  const goToPrev = () => {
    /** Wechselt zum vorherigen Absatz (mit Wrap-around). */

    if (!paragraphs) return; // early return if null
    setCurrentParagraph((prev: number) =>
      (prev - 1 + paragraphs.tags.length) % paragraphs.tags.length
    );
  };

  const goToNext = () => {
    /** Wechselt zum nächsten Absatz (mit Wrap-around). */
    
    if (!paragraphs) return; // early return if null
    setCurrentParagraph((prev: number) =>
      (prev + 1) % paragraphs.tags.length
    );
  };

  /* ------------------------------------------------------------------
  * TSX-Return
  * ------------------------------------------------------------------ */

  return (
    <div className={`w-[45%] flex flex-col gap-5 p-5 shadow-md bg-gray-200 rounded-lg h-[calc(96vh-240px)] relative ml-5 ${!isloading && !paragraphs ? "" : "items-center justify-center"}`}>
      {ErrorMess ? (
        <div className='bg-white shadow-md px-2 py-2 rounded-md font-bold'> 
          Ein Fehler ist aufgetreten. Bitte klicken Sie erneut auf „Dokument generieren“. Sollte die Anwendung auch nach mehreren Versuchen weiterhin abstürzen, kontaktieren Sie mich bitte: falk.stankat@disy.net.
        </div>
      ) : (
        !isloading && !paragraphs ? (
        <div className="overflow-y-auto pr-2 flex flex-col gap-3 w-full h-full px-2 py-2">
          <div className="self-center text-2xl font-semibold">
            Willkommen bei meinem Prototyp! 😊
          </div>
            <p className="text-xl font-semibold underline">Einleitung</p>
            <p>
              Vielen Dank, dass Sie an meiner zweiten Evaluation teilnehmen. Diese Anwendung ermöglicht es Ihnen, Klimaatlas-Berichte mithilfe von Sprachmodellen zu erstellen.
            </p>
            <p className="text-xl font-semibold underline mb-1 mt-4">Bedienungsanleitung</p>
            <p className="mb-0">
              Die Anwendung gliedert sich in drei Hauptkomponenten:
            </p>
            <ul className="list-disc pl-4 mt-0">
              <li><strong> Navigationsleiste </strong>(oben)</li>
              <li> <strong> Textansicht </strong> der Absätze (links)</li>
              <li><strong>Informationsbereich</strong>: Daten / PDF-Vorschau / Information (rechts)</li>
            </ul>
            <p className="mb-0 mt-4">
              Zur Nutzung wählen Sie zunächst in der Navigationsleiste den Report-Typ, das Jahr und den Monat aus. Nachdem Sie alle drei Dropdown-Menüs ausgefüllt haben,
              können Sie den Bericht entweder im Standard-Modus oder im Advanced-Modus generieren (über den Toggle-Button).
            </p>
            <ul className="list-disc pl-4 mt-0">
              <li><strong>Standard-Modus:</strong> Erzeugt einen klassischen Textrohling, ähnlich dem aus der ersten Evaluation.</li>
              <li><strong>Advanced-Modus:</strong> Bietet erweiterte Zeitreihen-Interpretationen für Temperatur, Niederschlag und Sonnenscheindauer.
                Zusätzlich wird in der Einleitung der Witterungsverlauf des gewählten Zeitraums basierend auf den täglichen DWD-Berichten beschrieben.
                <br />(Hinweis: Da die Sammlung der DWD-Wetterberichte erst im April begann, ist diese Funktion für die Einleitung nur für den April in vollem Umfang verfügbar.)
              </li>
            </ul>
            <p>
              Im rechten Bereich finden Sie ein Tab-Menü mit den Reitern <strong>"Daten"</strong>, <strong>"PDF-Vorschau"</strong> und <strong>"Information"</strong>.
              Bitte klicken Sie sich durch das Menü und lesen Sie aufmerksam die Beschreibungen der einzelnen Reiter.
            </p>
            <p>
              Nachdem Sie alle Informationen gelesen und verstanden haben, klicken Sie mit den ausgewählten Dropdown-Feldern auf <strong>Dokument generieren</strong>.
              <br />
              Daraufhin erscheint die Textansicht mit den verschiedenen Absätzen. Über die Buttons der Sprachmodelle können Sie für jeden Absatz die Texte auswählen,
              die von unterschiedlichen Sprachmodellen generiert wurden.
            </p>
            <p>
              Durch einen Doppelklick auf die weißen Textfelder gelangen Sie in den Bearbeitungsmodus und können die Texte nach Ihren Wünschen anpassen. Der grüne Button
              in der rechten unteren Ecke speichert Ihre Änderungen. Solange Sie sich im Bearbeitungsmodus befinden, müssen Sie zuerst speichern, bevor Sie wieder das Chevron-Symbol oder andere Texte der Sprachmodelle auswählen können.
            </p>
            <p>Über die roten Chevron-Buttons navigieren Sie zwischen den verschiedenen Abschnitten des Berichts.</p>
            <p>
              Nachdem Sie Ihre ersten Berichte generiert haben, erscheinen in der Navigationsleiste – basierend auf dem gewählten Modus – zusätzlich die Buttons <strong>"PDF-Vorschau"</strong>, <strong>"Websuche"</strong> und <strong>"DWD Bericht"</strong> (nur im Standard-Modus).
            </p>
            <ul className="list-disc pl-4 mt-0"> 
              <li>
                Über den Button <strong>"PDF-Vorschau"</strong> können Sie die ausgewählten Absätze der verschiedenen Sprachmodelle in einer fertigen PDF-Ansicht betrachten.
                Navigieren Sie dazu auf den Reiter <strong>"PDF-Vorschau"</strong> im Informationsbereich.
                Sollten Sie Änderungen an den Texten vorgenommen haben, aktualisieren Sie die Ansicht, indem Sie erneut auf den <strong>"PDF-Vorschau"</strong>-Button klicken.
              </li>
              <li>
                Über den Button <strong>"Websuche"</strong> können Sie eine intelligente Suche (Tavily Search) nach aktuellen Wetterereignissen für einen bestimmten Zeitraum (Monat, Quartal, Jahr) starten.
                Im Reiter <strong>"Information"</strong> wird Ihnen ein entsprechender Witterungsabschnitt inklusive relevanter Website-Links angezeigt.
                <br />
                <em>Hinweis:</em> Da es sich um ein experimentelles Feature handelt, können die Informationen fehlerhaft sein. Verifizieren Sie daher alle Inhalte über die verlinkten Quellen,
                bevor Sie sie in Ihre Texte übernehmen. Ziel ist es, Ihnen einen schnellen Überblick über das Wettergeschehen des gewählten Zeitraums zu bieten und so weiterführende Recherchen zu erleichtern.
              </li>
              <li>
                Über den Button <strong>"DWD Bericht"</strong> erhalten Sie eine Zusammenfassung der DWD-Wetterberichte für den ausgewählten Zeitraum.
                Im Advanced-Modus wird diese automatisch in die Einleitung integriert und im Reiter <strong>"Information"</strong> angezeigt.
                Im Standard-Modus müssen Sie den Button manuell anklicken, um die Zusammenfassung ebenfalls im Reiter <strong>"Information"</strong> zu sehen.
              </li>
            </ul>
            <p><strong>Viel Spaß beim Testen meines Prototyps!</strong></p>
        </div>
        ) : (
          <>
            {!isloading && paragraphs && (
              <button
                onClick={goToPrev}
                className="absolute left-[-24px] p-2 bg-red-300 rounded-full shadow-md hover:bg-red-400 transition"
                disabled={isEditing}
              >
                <ChevronLeft size={24} />
              </button>
            )}

            <div>
              {isloading && (
                <div className="inset-0 flex flex-col items-center justify-center">
                  <h2 className="mb-6 text-3xl font-extrabold text-gray-600 [text-shadow:_0_2px_0_rgb(0_0_0_/_50%)] md:text-3xl lg:text-5xl">
                    Generierung Variationen{dots}
                  </h2>
                  <div className="loader mx-auto"></div>
                </div>
              )}

              {!isloading && paragraphs && (
                <>
                  <div className="flex flex-col gap-3">
                    <div className="absolute top-3 left-4 flex justify-between -mb-7">
                      <h2 className="text-2xl pt-2 pr-3 [text-shadow:_0_1px_0_rgb(0_0_0_/_50%)] font-semibold">
                        Generiert von:
                      </h2>
                      {renderLegend()}
                    </div>
                    <div className="absolute top-4 bg-white border-4 border-black shadow-md rounded-md px-2 py-1 font-bold text-x text-center min-w-[80px] right-6 text-lg">
                      {idMapping[paragraphs.tags[CurrentParagraph].id] || "Unknown"}
                    </div>
                  </div>
                  <div>{VariationsContainer()}</div>
                </>
              )}
            </div>

            {!isloading && paragraphs && (
              <button
                onClick={goToNext}
                className="absolute right-[-24px] p-2 bg-red-300 rounded-full shadow-md hover:bg-red-400 transition"
                disabled={isEditing}
              >
                <ChevronRight size={24} />
              </button>
            )}
          </>
        )
      )}
    </div>
  );
};

export default Variationdisplay;