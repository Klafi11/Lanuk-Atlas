
/* Interfaces der Anwendung*/

interface Tag {
    id: string;
    value: [{ [key: number]: string}];
    intro?: string; 
    
}

interface Page {
    tags: Tag[];
}

interface StructuredSum {
    summarization: string; 
    citations: string[];   
  }

interface DataReport {
    data: Array<Record<string, any>>;
  }

interface HeadingStruc {
    headings: string[]; 
  }


interface TimeSeriesDeviation {
  Jahr: number;     
  Abweichung: number; 
  Temperatur: number; 
}


interface TimeSeriesEntry {
  values: TimeSeriesDeviation[];
  ref: Record<string, number>; 
}


interface TimeSeriesData {
  [key: number]: TimeSeriesEntry;
}

interface ButtonGridProps {
  onApiCall?: (selectedStations: string[]) => void;
  selectedButtons: Set<string>;
  setSelectedButtons: React.Dispatch<React.SetStateAction<Set<string>>>;
  isGenerateDisabled: () => boolean;
}

export type {Page, Tag, StructuredSum, DataReport, HeadingStruc, TimeSeriesData, TimeSeriesDeviation, ButtonGridProps}


