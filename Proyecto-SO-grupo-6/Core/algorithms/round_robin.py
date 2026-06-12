from collections import deque

def run_round_robin(processes, quantum):
    procesos_pendientes = sorted(processes, key=lambda p: p.arrival_time)
    procesos_terminados = []
    ready_queue = deque()
    tiempo_actual = 0
    
    while procesos_pendientes or ready_queue:
        llegaron_ahora = [p for p in procesos_pendientes if p.arrival_time <= tiempo_actual]
        for p in llegaron_ahora:
            p.state = "Listo"
            ready_queue.append(p)
            procesos_pendientes.remove(p)
            
        if not ready_queue:
            tiempo_actual = procesos_pendientes[0].arrival_time
            continue
            
        proceso_actual = ready_queue.popleft()
        
        if proceso_actual.start_time == -1:
            proceso_actual.start_time = tiempo_actual
            
        proceso_actual.state = "Ejecutando"
        tiempo_ejecucion = min(proceso_actual.remaining_time, quantum)
        tiempo_actual += tiempo_ejecucion
        proceso_actual.remaining_time -= tiempo_ejecucion
        
        llegaron_durante_ejecucion = [p for p in procesos_pendientes if p.arrival_time <= tiempo_actual]
        for p in llegaron_durante_ejecucion:
            p.state = "Listo"
            ready_queue.append(p)
            procesos_pendientes.remove(p)
            
        if proceso_actual.remaining_time > 0:
            proceso_actual.state = "Listo"
            ready_queue.append(proceso_actual)
        else:
            proceso_actual.state = "Terminado"
            proceso_actual.completion_time = tiempo_actual
            proceso_actual.turnaround_time = proceso_actual.completion_time - proceso_actual.arrival_time
            proceso_actual.waiting_time = proceso_actual.turnaround_time - proceso_actual.burst_time
            proceso_actual.response_time = proceso_actual.start_time - proceso_actual.arrival_time
            procesos_terminados.append(proceso_actual)
            
    return procesos_terminados