
def calculate_global_metrics(procesos_terminados):
    if not procesos_terminados:
        return None

    cantidad = len(procesos_terminados)

    suma_turnaround = sum(p.turnaround_time for p in procesos_terminados)
    suma_waiting = sum(p.waiting_time for p in procesos_terminados)
    suma_response = sum(p.response_time for p in procesos_terminados)
    suma_burst = sum(p.burst_time for p in procesos_terminados)

    promedio_turnaround = suma_turnaround / cantidad
    promedio_waiting = suma_waiting / cantidad
    promedio_response = suma_response / cantidad

    tiempo_inicio_absoluto = min(p.arrival_time for p in procesos_terminados)
    tiempo_fin_absoluto = max(p.completion_time for p in procesos_terminados)
    tiempo_total_simulacion = tiempo_fin_absoluto - tiempo_inicio_absoluto

    tiempo_ocioso = tiempo_total_simulacion - suma_burst
    procesos_convoy = [
        p.pid for p in procesos_terminados if p.waiting_time >= 15]
    total_interrupciones = sum(getattr(p, 'interrupciones', 0)
                               for p in procesos_terminados)

    utilizacion_cpu = (suma_burst / tiempo_total_simulacion) * \
        100 if tiempo_total_simulacion > 0 else 0

    # Tod.os los valores seran truncados a 2 decimales en el front
    return {
        "promedio_retorno": promedio_turnaround,
        "promedio_espera": promedio_waiting,
        "promedio_respuesta": promedio_response,
        "utilizacion_cpu": utilizacion_cpu,
        "tiempo_total": tiempo_total_simulacion,
        "tiempo_ocioso": tiempo_ocioso,
        "procesos_convoy": procesos_convoy,
        "interrupciones": total_interrupciones
    }
