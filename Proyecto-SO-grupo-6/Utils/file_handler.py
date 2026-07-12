# Archivo: Utils/file_handler.py
import os
from Core.process import Process


def load_processes_from_csv(filepath):
    """
    Lee un archivo de texto/csv y genera una lista de objetos Process.
    El formato esperado por línea es: PID, Tiempo_Llegada, Tiempo_Rafaga, Prioridad
    Ejemplo: P1, 0, 5, 2
    """
    procesos = []

    if not os.path.exists(filepath):
        print(f"Error: No se encontró el archivo {filepath}")
        return procesos

    with open(filepath, 'r', encoding='utf-8') as file:
        lineas = file.readlines()

        for linea in lineas:
            linea = linea.strip()
            # Ignorar líneas en blanco o encabezados (que empiecen con letras, ej. "PID")
            if not linea or linea.lower().startswith("pid"):
                continue

            datos = linea.split(',')

            # Aseguramos que la línea tenga al menos PID, Llegada y Ráfaga
            if len(datos) >= 3:
                try:
                    pid = datos[0].strip()
                    arrival_time = int(datos[1].strip())
                    burst_time = int(datos[2].strip())
                    # Si no hay prioridad en el archivo, asignamos 0 por defecto
                    priority = int(datos[3].strip()) if len(datos) > 3 else 0

                    nuevo_proceso = Process(
                        pid, arrival_time, burst_time, priority)
                    procesos.append(nuevo_proceso)
                except ValueError:
                    print(
                        f"Advertencia: Error de formato en la línea: {linea}")

    return procesos
