from collections import deque
from Core.process import ProcessState


def run_round_robin(processes, quantum):
    procesos_pendientes = sorted(
        processes.copy(), key=lambda p: p.arrival_time)
    procesos_terminados = []
    ready_queue = deque()
    tiempo_actual = 0
    historial_gantt = []

    while procesos_pendientes or ready_queue:
        llegaron_ahora = [
            p for p in procesos_pendientes if p.arrival_time <= tiempo_actual]

        for p in llegaron_ahora:
            if p.state == ProcessState.NUEVO:
                p.state = ProcessState.LISTO
            ready_queue.append(p)
            procesos_pendientes.remove(p)

        if not ready_queue:
            tiempo_actual = procesos_pendientes[0].arrival_time
            continue

        proceso_actual = ready_queue.popleft()

        if proceso_actual.start_time == -1:
            proceso_actual.start_time = tiempo_actual

        proceso_actual.state = ProcessState.EJECUTANDO

        if not historial_gantt or historial_gantt[-1] != proceso_actual.pid:
            # Se registra para el gantt asegurando que no este repetido
            historial_gantt.append(
                {
                    "pid": proceso_actual.pid,
                    "start": tiempo_actual,
                    "end": tiempo_actual  # Lo inicializamos igual
                }
            )

        tiempo_ejecucion = min(proceso_actual.remaining_time, quantum)
        tiempo_actual += tiempo_ejecucion
        proceso_actual.remaining_time -= tiempo_ejecucion

        # Se marca el final de ese proceso en el gantt
        historial_gantt[-1]["end"] = tiempo_actual

        llegaron_durante_ejecucion = [
            p for p in procesos_pendientes if p.arrival_time <= tiempo_actual]

        for p in llegaron_durante_ejecucion:
            if p.state == ProcessState.NUEVO:
                p.state = ProcessState.LISTO
            ready_queue.append(p)
            procesos_pendientes.remove(p)

        if proceso_actual.remaining_time > 0:
            proceso_actual.state = ProcessState.LISTO
            ready_queue.append(proceso_actual)
            proceso_actual.interrupciones += 1
        else:
            proceso_actual.state = ProcessState.TERMINADO
            proceso_actual.completion_time = tiempo_actual
            proceso_actual.turnaround_time = proceso_actual.completion_time - \
                proceso_actual.arrival_time
            proceso_actual.waiting_time = proceso_actual.turnaround_time - proceso_actual.burst_time
            proceso_actual.response_time = proceso_actual.start_time - proceso_actual.arrival_time
            procesos_terminados.append(proceso_actual)

    return procesos_terminados, historial_gantt
