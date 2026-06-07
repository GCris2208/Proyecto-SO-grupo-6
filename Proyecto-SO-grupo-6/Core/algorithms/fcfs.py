# Archivo: fcfs.py

def run_fcfs(processes):
    """
    Motor de planificación FCFS (First Come, First Served).
    Asume que la lista 'processes' contiene instancias de la clase Process.
    """
    # Ordenamos por tiempo de llegada (First Come)
    procesos_ordenados = sorted(processes, key=lambda p: p.arrival_time)
    
    tiempo_actual = 0
    
    for proceso in procesos_ordenados:
        # Si el procesador está inactivo esperando a que llegue el proceso
        if tiempo_actual < proceso.arrival_time:
            tiempo_actual = proceso.arrival_time
            
        # El proceso entra a Ejecución
        proceso.state = "Ejecución"
        proceso.start_time = tiempo_actual
        
        # Simulación del tiempo que toma ejecutarse (ráfaga)
        tiempo_actual += proceso.burst_time
        
        # El proceso termina
        proceso.completion_time = tiempo_actual
        proceso.state = "Terminado"
        
        # Cálculos requeridos para métricas
        proceso.turnaround_time = proceso.completion_time - proceso.arrival_time
        proceso.waiting_time = proceso.turnaround_time - proceso.burst_time
        proceso.response_time = proceso.start_time - proceso.arrival_time

    return procesos_ordenados