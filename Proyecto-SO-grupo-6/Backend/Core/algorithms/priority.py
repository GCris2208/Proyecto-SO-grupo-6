from Core.process import ProcessState


def run_priority(processes):
    procesos_pendientes = processes.copy()
    procesos_terminados = []
    tiempo_actual = 0
    historial_gantt = []

    while procesos_pendientes:
        procesos_disponibles = [
            p for p in procesos_pendientes if p.arrival_time <= tiempo_actual]

        if not procesos_disponibles:
            tiempo_proximo_proceso = min(
                p.arrival_time for p in procesos_pendientes)
            tiempo_actual = tiempo_proximo_proceso
            continue

        for p in procesos_disponibles:
            if p.state == ProcessState.NUEVO:
                p.state = ProcessState.LISTO

        if not procesos_disponibles:
            procesos_pendientes.sort(key=lambda p: p.arrival_time)
            tiempo_actual = procesos_pendientes[0].arrival_time
            continue

        proceso_actual = min(procesos_disponibles, key=lambda p: (
            p.priority, p.arrival_time, p.pid))

        procesos_pendientes.remove(proceso_actual)

        proceso_actual.state = ProcessState.EJECUTANDO
        # Se registra para el gantt
        historial_gantt.append(
            {
                "pid": proceso_actual.pid,
                "start": tiempo_actual,
                "end": tiempo_actual + proceso_actual.burst_time
            }
        )

        proceso_actual.start_time = tiempo_actual
        tiempo_actual += proceso_actual.burst_time

        proceso_actual.completion_time = tiempo_actual
        proceso_actual.state = ProcessState.TERMINADO

        proceso_actual.turnaround_time = proceso_actual.completion_time - \
            proceso_actual.arrival_time
        proceso_actual.waiting_time = proceso_actual.turnaround_time - proceso_actual.burst_time
        proceso_actual.response_time = proceso_actual.start_time - proceso_actual.arrival_time

        procesos_terminados.append(proceso_actual)

    return procesos_terminados, historial_gantt
