# Archivo: sjf.py

def run_sjf(processes):
    """
    Motor de planificación SJF (Shortest Job First) - Variante No Apropiativa.
    Asume que la lista 'processes' contiene instancias de la clase Process.
    """
    procesos_pendientes = processes.copy()
    procesos_terminados = []
    tiempo_actual = 0
    
    # Mientras haya procesos por ejecutar
    while procesos_pendientes:
        # 1. ¿Quiénes ya llegaron al sistema en este momento exacto?
        procesos_disponibles = [p for p in procesos_pendientes if p.arrival_time <= tiempo_actual]
        
        # Si no hay nadie disponible, el procesador se queda inactivo hasta que llegue el próximo
        if not procesos_disponibles:
            # Ordenamos para ver quién es el próximo en llegar
            procesos_pendientes.sort(key=lambda p: p.arrival_time)
            tiempo_actual = procesos_pendientes[0].arrival_time
            continue
            
        # 2. Lógica SJF: De los disponibles, elegimos el que tenga la ráfaga MÁS CORTA
        proceso_actual = min(procesos_disponibles, key=lambda p: p.burst_time)
        
        # Lo sacamos de la lista de pendientes
        procesos_pendientes.remove(proceso_actual)
        
        # 3. El proceso entra a Ejecución
        proceso_actual.state = "Ejecución"
        proceso_actual.start_time = tiempo_actual
        
        # Simulación de la CPU trabajando
        tiempo_actual += proceso_actual.burst_time
        
        # 4. El proceso termina y calculamos sus métricas
        proceso_actual.completion_time = tiempo_actual
        proceso_actual.state = "Terminado"
        
        # Las ecuaciones matemáticas requeridas en su anteproyecto
        proceso_actual.turnaround_time = proceso_actual.completion_time - proceso_actual.arrival_time
        proceso_actual.waiting_time = proceso_actual.turnaround_time - proceso_actual.burst_time
        proceso_actual.response_time = proceso_actual.start_time - proceso_actual.arrival_time
        
        procesos_terminados.append(proceso_actual)
        
    return procesos_terminados