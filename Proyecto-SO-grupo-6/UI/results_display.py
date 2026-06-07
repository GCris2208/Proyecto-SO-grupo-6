# Archivo: UI/results_display.py

def print_metrics_table(procesos, metricas_globales, nombre_algoritmo):
    """
    Imprime una tabla profesional con los resultados de cada proceso y las métricas globales.
    """
    print("\n" + "="*70)
    print(f" RESULTADOS DE LA SIMULACIÓN : {nombre_algoritmo.upper()} ".center(70, "="))
    print("="*70)
    
    # Encabezado de la tabla
    print(f"{'PID':<6} | {'Llegada':<8} | {'Ráfaga':<7} | {'Prioridad':<10} | {'Retorno':<8} | {'Espera':<7} | {'Respuesta':<10}")
    print("-" * 70)
    
    # Ordenar por PID para que la tabla sea fácil de leer
    procesos_ordenados = sorted(procesos, key=lambda p: p.pid)
    
    for p in procesos_ordenados:
        print(f"{p.pid:<6} | {p.arrival_time:<8} | {p.burst_time:<7} | {p.priority:<10} | {p.turnaround_time:<8} | {p.waiting_time:<7} | {p.response_time:<10}")
    
    print("-" * 70)
    
    # Imprimir Métricas Globales
    if metricas_globales:
        print("\n[ MÉTRICAS GLOBALES DEL SISTEMA ]")
        print(f"➢ Tiempo Promedio de Retorno (Turnaround): {metricas_globales['promedio_retorno']} ms")
        print(f"➢ Tiempo Promedio de Espera (Waiting):     {metricas_globales['promedio_espera']} ms")
        print(f"➢ Tiempo Promedio de Respuesta (Response): {metricas_globales['promedio_respuesta']} ms")
        print(f"➢ Utilización de la CPU:                   {metricas_globales['utilizacion_cpu']} %")
        print(f"➢ Tiempo Total de Simulación:              {metricas_globales['tiempo_total']} ms\n")

def print_gantt_chart(procesos):
    """
    Genera un Diagrama de Gantt simplificado en texto mostrando el orden de finalización.
    """
    print("="*70)
    print(" DIAGRAMA DE GANTT (Orden de Finalización) ".center(70, "="))
    print("="*70)
    
    # Ordenar los procesos por su tiempo de finalización
    procesos_gantt = sorted(procesos, key=lambda p: p.completion_time)
    
    gantt_bar = "|"
    gantt_times = "0"
    
    for p in procesos_gantt:
        # Añadir el proceso a la barra
        espacio = " " * 3
        gantt_bar += f"{espacio}{p.pid}{espacio}|"
        
        # Añadir el tiempo en la parte inferior
        tiempo_str = str(p.completion_time)
        espacios_necesarios = len(f"{espacio}{p.pid}{espacio}|") - len(tiempo_str)
        gantt_times += " " * espacios_necesarios + tiempo_str
        
    print(gantt_bar)
    print(gantt_times)
    print("="*70 + "\n")