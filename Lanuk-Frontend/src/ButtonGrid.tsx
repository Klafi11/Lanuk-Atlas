import {ButtonGridProps} from './BaseModels';


/**
 * # ButtonGrid
 *
 * ----------------------------
 * Raster aus 3x3 Toggle-Buttons zur Auswahl von Messstationen (durch Kürzel wie
 * "SOLI", "EIFE" etc.). Die Auswahl wird als `Set<string>` geführt. Zusätzlich
 * gibt es einen Aktions-Button, der die aktuell selektierten Stationen an eine
 * Callback-Funktion übergibt und die jeweiligen Stationsdaten abruft und im Informationsdisplay
 * als Tabelle zu Verfügung stellt.
 *
*/


const ButtonGrid: React.FC<ButtonGridProps> = ({ 
  onApiCall,
  selectedButtons,
  setSelectedButtons,
  isGenerateDisabled

}) => {

const labels = [
    ['SOLI', 'EIFE', 'VACW'],
    ['RODE', 'WALS', 'MGRH'],
    ['ROTH', 'BOTT', 'NIED']
  ];



  const handleClick = (row: number, col: number) => {
    /**
     * Schaltet den Auswahlzustand für das angeklickte Feld um.
     * Nutzt eine neue `Set`-Instanz, damit React State-Änderungen erkennt.
     */

    const buttonLabel = labels[row][col];
    const newSelected = new Set(selectedButtons);
    
    if (newSelected.has(buttonLabel)) {
      newSelected.delete(buttonLabel);
    } else {
      newSelected.add(buttonLabel);
    }
    
    setSelectedButtons(newSelected);

  };

  const handleApiCall = () => {
    /**
     * Übergibt die selektierten Stationen an die bereitgestellte Callback-Funktion.
     * Ignoriert den Aufruf, wenn keine Callback-Funktion vorhanden ist.
     */
    
    const selectedStations = Array.from(selectedButtons);
    if (onApiCall) {
      onApiCall(selectedStations);
    }
  };

  /* ------------------------------------------------------------------
  * TSX-Return
  * ------------------------------------------------------------------ */
  return (
    <div className={`flex items-center gap-4`}>
      <div className="grid grid-cols-3 gap-0">
        {labels.map((row, rowIndex) =>
          row.map((label, colIndex) => {
            const isSelected = selectedButtons.has(label);
            const isTopLeft = rowIndex === 0 && colIndex === 0;
            const isTopRight = rowIndex === 0 && colIndex === 2;
            const isBottomLeft = rowIndex === 2 && colIndex === 0;
            const isBottomRight = rowIndex === 2 && colIndex === 2;
            
            let roundedClasses = '';
            if (isTopLeft) roundedClasses = 'rounded-tl-lg';
            if (isTopRight) roundedClasses = 'rounded-tr-lg';
            if (isBottomLeft) roundedClasses = 'rounded-bl-lg';
            if (isBottomRight) roundedClasses = 'rounded-br-lg';
            
            return (
              <button
                key={`${rowIndex}-${colIndex}`}
                onClick={() => handleClick(rowIndex, colIndex)}
                className={`w-14 h-14 text-white font-semibold transition-all duration-200 active:scale-95 transform border-0 shadow-lg hover:shadow-xl ${roundedClasses} ${
                  isSelected 
                    ? 'bg-green-600 hover:bg-green-700' 
                    : 'bg-gray-400 hover:bg-gray-500'
                }`}
              >
                {label}
              </button>
            );
          })
        )}
      </div>
      
      <button
        onClick={handleApiCall}
        disabled={selectedButtons.size === 0 || isGenerateDisabled()}
        className={`px-6 py-2 font-semibold rounded-lg transition-colors duration-200 ${
          selectedButtons.size === 0 || isGenerateDisabled()
            ? 'bg-gray-400 text-gray-600 cursor-not-allowed'
            : 'bg-blue-500 hover:bg-blue-600 text-white'
        }`}
      >
        Stationsabfrage ({selectedButtons.size} ausgewählt)
      </button>
    </div>
  );
};

export default ButtonGrid;