# Archivo: UI/interface.py

import sys
import os

# Para poder importar desde las otras carpetas
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Utils.file_handler import load_processes_from_csv
from Core.metrics import calculate_global_metrics
from UI.results_display import print_metrics_table, print_gantt_chart

# Importar algoritmos
from Core.algorithms.fcfs import run_fcfs
from Core.algorithms.sjf import run_sjf
from Core.algorithms.priority import run_priority
from Core.algorithms.round_robin import run_round_robin

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main_menu():
    procesos_actuales = []
    
    while True:
        clear_screen()
        print("==================================================")
        print(" SIMULADOR DE PLANIFICACIÓN DE CPU - EQUIPO 6")
        print("==================================================")
        print(f"Procesos cargados actualmente: {len(procesos_actuales)}")
        print("--------------------------------------------------")
        print("1. Cargar procesos desde archivo (.txt o .csv)")
        print("2. Ejecutar FCFS (First Come, First Served)")
        print("3. Ejecutar SJF (Shortest Job First)")
        print("4. Ejecutar Prioridades")
        print("5. Ejecutar Round Robin")
        print("6. Salir del simulador")
        print("==================================================")
        
        opcion = input("Seleccione una opción (1-6): ")
        
        if opcion == '1':
            ruta = input("Ingrese el nombre del archivo (ej. procesos.txt): ")
            procesos_actuales = load_processes_from_csv(ruta)
            if procesos_actuales:
                print(f"¡Se cargaron {len(procesos_actuales)} procesos correctamente!")
            input("\nPresione ENTER para continuar...")
            
        elif opcion in ['2', '3', '4', '5']:
            if not procesos_actuales:
                print("\nERROR: Primero debe cargar procesos (Opción 1).")
                input("Presione ENTER para continuar...")
                continue
                
            resultados = []
            nombre_algo = ""
            import copy
            procesos_copia = copy.deepcopy(procesos_actuales)
            
            if opcion == '2':
                resultados = run_fcfs(procesos_copia)
                nombre_algo = "FCFS"
            elif opcion == '3':
                resultados = run_sjf(procesos_copia)
                nombre_algo = "SJF (No Apropiativo)"
            elif opcion == '4':
                resultados = run_priority(procesos_copia)
                nombre_algo = "Prioridades (No Apropiativo)"
            elif opcion == '5':
                while True:
                    try:
                        entrada = input("Ingrese el valor del Quantum (ej. 3): ")
                        quantum = int(entrada)
                        if quantum <= 0:
                            print("El Quantum debe ser un número mayor a cero. Intente de nuevo.")
                            continue
                        break
                    except ValueError:
                        print("Error: Debe ingresar un número entero válido. No presione Enter en blanco ni use letras.")
                resultados = run_round_robin(procesos_copia, quantum)
                nombre_algo = f"Round Robin (Quantum={quantum})"
            metricas = calculate_global_metrics(resultados)
            clear_screen()
            print_metrics_table(resultados, metricas, nombre_algo)
            print_gantt_chart(resultados)
            input("Presione ENTER para volver al menú principal...")
        elif opcion == '6':
            print("Saliendo del simulador... ¡Hasta luego!")
            break
        else:
            print("Opción no válida. Intente de nuevo.")
            input("Presione ENTER para continuar...")

if __name__ == "__main__":
    main_menu()