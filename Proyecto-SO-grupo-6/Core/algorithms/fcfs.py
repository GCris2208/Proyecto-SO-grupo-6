def run_fcfs(processes):
    procesos_ordenados = sorted(processes, key=lambda p: p.arrival_time)
    tiempo_actual = 0
    
    for proceso in procesos_ordenados:
        if tiempo_actual < proceso.arrival_time:
            tiempo_actual = proceso.arrival_time
            
        proceso.state = "Ejecución"
        proceso.start_time = tiempo_actual
        tiempo_actual += proceso.burst_time
        
        proceso.completion_time = tiempo_actual
        proceso.state = "Terminado"
        
        proceso.turnaround_time = proceso.completion_time - proceso.arrival_time
        proceso.waiting_time = proceso.turnaround_time - proceso.burst_time
        proceso.response_time = proceso.start_time - proceso.arrival_time

    return procesos_ordenados