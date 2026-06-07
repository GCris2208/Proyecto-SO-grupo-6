class Process:
    def __init__(self, pid, arrival_time, burst_time, priority=0):
        """
        Clase que representa el Bloque de Control de Procesos (PCB).
        Sigue estrictamente las especificaciones de la Unidad 4 y la rúbrica del proyecto.
        """
        # 1. Datos de Entrada (Configurados por el usuario o archivo de texto)
        self.pid = pid                    # Identificador único del proceso (ej. "P1", "P2")
        self.arrival_time = arrival_time   # Tiempo de llegada del proceso al sistema
        self.burst_time = burst_time       # Tiempo de ráfaga (duración total en CPU)
        self.priority = priority           # Nivel de prioridad (esencial para el algoritmo de Prioridades)
        
        # 2. Control de Estado Dinámico 
        # Ajustado estrictamente a los estados exigidos por el profesor:
        # "Nuevo", "Listo", "Ejecutando", "Terminado"
        self.state = "Nuevo" 
        
        # Variable de control para algoritmos apropiativos (como Round Robin)
        # Al inicio, el tiempo restante para terminar es exactamente la ráfaga completa
        self.remaining_time = burst_time 
        
        # 3. Variables temporales para el cálculo de Métricas Obligatorias
        self.start_time = -1              # Instante en que toca la CPU por PRIMERA vez (para Tiempo de Respuesta)
        self.completion_time = 0          # Instante exacto en que el proceso termina (Estado: Terminado)
        
        # Resultados finales del rendimiento del proceso
        self.turnaround_time = 0          # Tiempo de Retorno (Tiempo total en el sistema)
        self.waiting_time = 0             # Tiempo de Espera (Tiempo en colas de listo)
        self.response_time = 0            # Tiempo de Respuesta (Desde que llega hasta que se le atiende)

    def __repr__(self):
        """
        Función especial de Python para imprimir el proceso de forma limpia en la terminal.
        Muy útil para las fases de prueba (debugging).
        """
        return (f"Proceso({self.pid} | Llegada: {self.arrival_time} | "
                f"Ráfaga: {self.burst_time} | Prioridad: {self.priority} | Estado: {self.state})")