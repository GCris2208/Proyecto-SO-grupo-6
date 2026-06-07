# Archivo: Core/algorithms/round_robin.py
from collections import deque

def run_round_robin(processes, quantum):
    """
    Motor de planificación Round Robin.
    Implementa un enfoque apropiativo utilizando un Quantum de tiempo.
    """
    # Hacemos una copia para no alterar la lista original directamente
    procesos_pendientes = sorted(processes, key=lambda p: p.arrival_time)
    procesos_terminados = []
    
    # Ready Queue nativa de alta eficiencia
    ready_queue = deque()
    tiempo_actual = 0
    
    # Bucle principal: se ejecuta mientras haya procesos en cualquier parte del sistema
    while procesos_pendientes or ready_queue:
        
        # 1. Ingresar a la cola los procesos que acaban de llegar al sistema
        # Se iteran hacia atrás para poder eliminarlos de la lista de pendientes de forma segura
        llegaron_ahora = [p for p in procesos_pendientes if p.arrival_time <= tiempo_actual]
        for p in llegaron_ahora:
            p.state = "Listo"
            ready_queue.append(p)
            procesos_pendientes.remove(p)
            
        # 2. Si la cola está vacía pero aún hay procesos en el futuro, adelantamos el reloj
        if not ready_queue:
            tiempo_actual = procesos_pendientes[0].arrival_time
            continue
            
        # 3. Extraemos el siguiente proceso a ejecutar
        proceso_actual = ready_queue.popleft()
        proceso_actual.state = "Ejecutando"
        
        # Si es la primera vez que toca la CPU, registramos su Tiempo de Respuesta
        if proceso_actual.start_time == -1:
            proceso_actual.start_time = tiempo_actual
            
        # 4. Determinamos cuánto tiempo se va a ejecutar (El Quantum o lo que le quede de ráfaga)
        tiempo_ejecucion = min(proceso_actual.remaining_time, quantum)
        
        # Avanzamos el reloj del sistema
        tiempo_actual += tiempo_ejecucion
        proceso_actual.remaining_time -= tiempo_ejecucion
        
        # 5. VERIFICACIÓN CRÍTICA: Revisar si llegaron procesos nuevos MIENTRAS este se ejecutaba
        # Deben entrar a la cola ANTES de que el proceso actual regrese a ella
        llegaron_durante_ejecucion = [p for p in procesos_pendientes if p.arrival_time <= tiempo_actual]
        for p in llegaron_durante_ejecucion:
            p.state = "Listo"
            ready_queue.append(p)
            procesos_pendientes.remove(p)
            
        # 6. Evaluación de finalización del proceso
        if proceso_actual.remaining_time > 0:
            # Se le acabó el quantum pero no ha terminado. Vuelve a la fila.
            proceso_actual.state = "Listo"
            ready_queue.append(proceso_actual)
        else:
            # El proceso terminó su ráfaga por completo
            proceso_actual.state = "Terminado"
            proceso_actual.completion_time = tiempo_actual
            
            # Cálculos de métricas finales
            proceso_actual.turnaround_time = proceso_actual.completion_time - proceso_actual.arrival_time
            proceso_actual.waiting_time = proceso_actual.turnaround_time - proceso_actual.burst_time
            proceso_actual.response_time = proceso_actual.start_time - proceso_actual.arrival_time
            
            procesos_terminados.append(proceso_actual)
            
    return procesos_terminados