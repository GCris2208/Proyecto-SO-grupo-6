# Archivo: Core/algorithms/priority.py

def run_priority(processes):
    """
    Motor de planificación por Prioridades (No Apropiativo).
    Convención: Un valor numérico MENOR significa MAYOR prioridad (ej. 1 es más prioritario que 5).
    """
    # Trabajamos con una copia para no mutar los datos originales
    procesos_pendientes = processes.copy()
    procesos_terminados = []
    tiempo_actual = 0
    
    # Bucle hasta que no queden procesos por ejecutar
    while procesos_pendientes:
        # 1. Identificar quiénes están en la sala de espera (ya llegaron)
        procesos_disponibles = [p for p in procesos_pendientes if p.arrival_time <= tiempo_actual]
        
        # Si nadie ha llegado aún, el procesador avanza el tiempo hasta el próximo
        if not procesos_disponibles:
            procesos_pendientes.sort(key=lambda p: p.arrival_time)
            tiempo_actual = procesos_pendientes[0].arrival_time
            continue
            
        # 2. LÓGICA DE PRIORIDAD: Elegir el proceso con el número de prioridad más bajo
        # Si hay un empate en prioridad, desempatamos por el que llegó primero (arrival_time)
        proceso_actual = min(procesos_disponibles, key=lambda p: (p.priority, p.arrival_time))
        
        # Lo sacamos de la lista de pendientes para procesarlo
        procesos_pendientes.remove(proceso_actual)
        
        # 3. El proceso entra a Ejecución
        proceso_actual.state = "Ejecutando"
        proceso_actual.start_time = tiempo_actual
        
        # Avanzamos el reloj simulando la CPU (No apropiativo = consume toda su ráfaga)
        tiempo_actual += proceso_actual.burst_time
        
        # 4. El proceso termina y registramos su salida
        proceso_actual.completion_time = tiempo_actual
        proceso_actual.state = "Terminado"
        
        # 5. Cálculos exactos de métricas para la rúbrica
        proceso_actual.turnaround_time = proceso_actual.completion_time - proceso_actual.arrival_time
        proceso_actual.waiting_time = proceso_actual.turnaround_time - proceso_actual.burst_time
        proceso_actual.response_time = proceso_actual.start_time - proceso_actual.arrival_time
        
        procesos_terminados.append(proceso_actual)
        
    return procesos_terminados