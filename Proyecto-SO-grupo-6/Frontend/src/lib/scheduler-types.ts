export interface Proceso {
  pid: string;
  llegada: number;
  rafaga: number;
  prioridad: number;
}

export interface ProcesoResultado {
  pid: string;
  turnaround_time: number;
  waiting_time: number;
  response_time: number;
  completion_time: number;
}

export interface Metricas {
  promedio_retorno: number;
  promedio_espera: number;
  promedio_respuesta: number;
  utilizacion_cpu: number;
  tiempo_total: number;
  tiempo_ocioso: number;
  procesos_convoy: string[];
  interrupciones: number;
}

export interface GanttBlock {
  pid: string;
  start: number;
  end: number;
}

export interface SimulacionNormal {
  procesos: ProcesoResultado[];
  metricas: Metricas;
  gantt: GanttBlock[];
}

export interface RankingItem {
  algoritmo: string;
  criterio_principal: number;
  criterio_secundario: number;
  todas_las_metricas: {
    awt: number;
    att: number;
    art: number;
    interrupciones: number;
  };
}

export interface SimulacionComparar {
  ganadores: string[];
  ranking: RankingItem[];
}

export type Algoritmo = "FCFS" | "SJF" | "SRTF" | "Prioridad" | "rr" | "comparar";
export type Criterio = "awt" | "att" | "art";

export const CRITERIO_LABEL: Record<Criterio, string> = {
  awt: "Menor Espera",
  att: "Menor Retorno",
  art: "Menor Respuesta",
};
