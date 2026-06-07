# Archivo: main_test.py (Solo para probar en terminal)

from Core.process import Process
from Core.algorithms.round_robin import run_round_robin
from Core.metrics import calculate_global_metrics

# Creamos 3 procesos de prueba simulando lo que haría el file_handler
p1 = Process("P1", arrival_time=0, burst_time=8)
p2 = Process("P2", arrival_time=1, burst_time=4)
p3 = Process("P3", arrival_time=2, burst_time=9)

lista_procesos = [p1, p2, p3]

print("--- INICIANDO SIMULADOR: ROUND ROBIN (Quantum=3) ---")
# Ejecutamos el algoritmo
resultados = run_round_robin(lista_procesos, quantum=3)

# Imprimimos resultados individuales
for p in resultados:
    print(f"{p.pid} | Retorno: {p.turnaround_time} | Espera: {p.waiting_time}")

# Calculamos e imprimimos métricas globales
metricas = calculate_global_metrics(resultados)
print("\n--- MÉTRICAS GLOBALES ---")
print(f"Tiempo Promedio de Espera: {metricas['promedio_espera']}")
print(f"Uso de CPU: {metricas['utilizacion_cpu']}%")