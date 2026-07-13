from Core.process import ProcessState


def run_srtf(processes):
    procesos_pendientes = processes.copy()
    procesos_terminados = []
    historial_gantt = []
    tiempo_actual = 0
    proceso_actual = None

    while procesos_pendientes or proceso_actual:
        # 1. Filtrar los procesos que ya llegaron a la cola
        llegados = [
            p for p in procesos_pendientes if p.arrival_time <= tiempo_actual]

        # Cambiar estado de Nuevo a Listo para los que van entrando al sistema
        for p in llegados:
            if p.state == ProcessState.NUEVO:
                p.state = ProcessState.LISTO

        # Creamos la lista de candidatos (los que llegaron + el que está corriendo)
        candidatos = list(llegados)
        if proceso_actual and proceso_actual.remaining_time > 0:
            candidatos.append(proceso_actual)

        # Si no hay nadie listo, la CPU está ociosa. Avanzamos al siguiente arribo.
        if not candidatos:
            proximo_arribo = min(p.arrival_time for p in procesos_pendientes)
            tiempo_actual = proximo_arribo
            continue

        # Seleccionar el proceso con el menor tiempo restante (desempata por tiempo de llegada o PID)
        mejor_proceso = min(candidatos, key=lambda p: (
            p.remaining_time, p.arrival_time, p.pid))

        # 3. Manejar la Apropiación (Preemption) e Interrupciones
        if proceso_actual and proceso_actual != mejor_proceso and proceso_actual.remaining_time > 0:
            proceso_actual.state = ProcessState.LISTO
            proceso_actual.interrupciones += 1
            # Se devuelve a la lista de pendientes para que vuelva a competir
            if proceso_actual not in procesos_pendientes:
                procesos_pendientes.append(proceso_actual)

        # 4. Asignar el nuevo proceso a la CPU
        proceso_actual = mejor_proceso
        if proceso_actual in procesos_pendientes:
            procesos_pendientes.remove(proceso_actual)

        # Registrar tiempo de primera respuesta
        if proceso_actual.start_time == -1:
            proceso_actual.start_time = tiempo_actual

        proceso_actual.state = ProcessState.EJECUTANDO

        # Registrar en el historial de Gantt (evitando duplicar si continúa el mismo proceso)
        if not historial_gantt or historial_gantt[-1] != proceso_actual.pid:
            historial_gantt.append(
                {
                    "pid": proceso_actual.pid,
                    "start": tiempo_actual,
                    "end": tiempo_actual  # Se inicializa igual, se actualizará al final
                }
            )

        # Ejecutar por exactamente 1 unidad de tiempo
        tiempo_actual += 1
        proceso_actual.remaining_time -= 1

        # Se actualiza tiempo al actual
        historial_gantt[-1]["end"] = tiempo_actual

        # 5. Si el proceso termina su ráfaga por completo
        if proceso_actual.remaining_time == 0:
            proceso_actual.state = ProcessState.TERMINADO
            proceso_actual.completion_time = tiempo_actual
            proceso_actual.turnaround_time = proceso_actual.completion_time - \
                proceso_actual.arrival_time
            proceso_actual.waiting_time = proceso_actual.turnaround_time - proceso_actual.burst_time
            proceso_actual.response_time = proceso_actual.start_time - proceso_actual.arrival_time
            procesos_terminados.append(proceso_actual)
            proceso_actual = None  # Liberar la CPU

    return procesos_terminados, historial_gantt
