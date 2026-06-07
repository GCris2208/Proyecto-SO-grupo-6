# Archivo: Core/metrics.py

def calculate_global_metrics(procesos_terminados):
    """
    Calcula las métricas globales del sistema según las exigencias del proyecto.
    Recibe una lista de objetos Process que ya pasaron por un algoritmo y están en estado "Terminado".
    """
    if not procesos_terminados:
        return None

    cantidad = len(procesos_terminados)
    
    # Sumatorias globales
    suma_turnaround = sum(p.turnaround_time for p in procesos_terminados)
    suma_waiting = sum(p.waiting_time for p in procesos_terminados)
    suma_response = sum(p.response_time for p in procesos_terminados)
    suma_burst = sum(p.burst_time for p in procesos_terminados)
    
    # Cálculos de promedios
    promedio_turnaround = suma_turnaround / cantidad
    promedio_waiting = suma_waiting / cantidad
    promedio_response = suma_response / cantidad
    
    # Cálculo de Utilización de CPU (%)
    # Tiempo total = Desde que llegó el primer proceso hasta que terminó el último
    tiempo_inicio_absoluto = min(p.arrival_time for p in procesos_terminados)
    tiempo_fin_absoluto = max(p.completion_time for p in procesos_terminados)
    tiempo_total_simulacion = tiempo_fin_absoluto - tiempo_inicio_absoluto
    
    # Evitar división por cero por seguridad
    if tiempo_total_simulacion > 0:
        utilizacion_cpu = (suma_burst / tiempo_total_simulacion) * 100
    else:
        utilizacion_cpu = 0

    return {
        "promedio_retorno": round(promedio_turnaround, 2),
        "promedio_espera": round(promedio_waiting, 2),
        "promedio_respuesta": round(promedio_response, 2),
        "utilizacion_cpu": round(utilizacion_cpu, 2),
        "tiempo_total": tiempo_total_simulacion
    }