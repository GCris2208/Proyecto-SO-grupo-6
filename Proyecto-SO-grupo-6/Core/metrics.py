
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

    utilizacion_cpu = (suma_burst / tiempo_total_simulacion) * \
        100 if tiempo_total_simulacion > 0 else 0

    return {
        "promedio_retorno": round(promedio_turnaround, 2),
        "promedio_espera": round(promedio_waiting, 2),
        "promedio_respuesta": round(promedio_response, 2),
        "utilizacion_cpu": round(utilizacion_cpu, 2),
        "tiempo_total": tiempo_total_simulacion
    }
