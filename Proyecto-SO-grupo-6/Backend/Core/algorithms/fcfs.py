from Core.process import ProcessState


def run_fcfs(processes):
    procesos_ordenados = sorted(processes, key=lambda p: p.arrival_time)
    tiempo_actual = 0
    historial_gantt = []

    for proceso in procesos_ordenados:
        if tiempo_actual < proceso.arrival_time:
            tiempo_actual = proceso.arrival_time

        if proceso.arrival_time <= tiempo_actual:
            proceso.state = ProcessState.LISTO

        proceso.state = ProcessState.EJECUTANDO

        # Se registra para el gantt
        historial_gantt.append(
            {
                "pid": proceso.pid,
                "start": tiempo_actual,
                "end": tiempo_actual + proceso.burst_time
            }
        )

        proceso.start_time = tiempo_actual
        tiempo_actual += proceso.burst_time

        proceso.completion_time = tiempo_actual
        proceso.state = ProcessState.TERMINADO

        proceso.turnaround_time = proceso.completion_time - proceso.arrival_time
        proceso.waiting_time = proceso.turnaround_time - proceso.burst_time
        proceso.response_time = proceso.start_time - proceso.arrival_time

    return procesos_ordenados, historial_gantt
