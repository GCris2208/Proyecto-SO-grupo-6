import os
from Core.process import Process


def parse_process_data(lineas):
    """
    Recibe una lista de líneas de texto y genera una lista de objetos Process.
    """
    procesos = []
    errores = []
    pids_vistos = set()  # Agregamos esto

    # Se recorre y se toma en cuenta el numero de línea para reportar errores
    for i, linea in enumerate(lineas, start=1):
        linea = linea.strip()
        # Ignorar líneas en blanco o encabezados
        if not linea or linea.lower().startswith("pid"):
            continue

        datos = linea.replace(',', ' ').split()

        if len(datos) not in [3, 4]:
            errores.append(
                f"Línea {i}: Formato incorrecto. Usa 'PID, Llegada, Ráfaga, [Prioridad opcional]'.")
            continue

        try:
            # Valida que el id tenga formado P + número
            pid = datos[0].strip().upper()
            if not pid.startswith("P") or not pid[1:].isdigit():
                errores.append(
                    f"Línea {i}: El ID debe ser la letra 'P' seguida de un número (Ej. P1, P2).")
                continue

            # Valida que el ID no este duplicado
            if pid in pids_vistos:
                errores.append(
                    f"Línea {i}: El ID '{pid}' está duplicado. Cada proceso debe tener un nombre único.")
                continue
            pids_vistos.add(pid)

            # Valida que los tiempos sean enteros y no negativos
            arrival_time = int(datos[1].strip())
            if arrival_time < 0:
                errores.append(
                    f"Línea {i}: El tiempo de llegada de {pid} no puede ser negativo.")
                continue

            burst_time = int(datos[2].strip())
            if burst_time <= 0:
                errores.append(
                    f"Línea {i}: La ráfaga de {pid} debe ser mayor a 0.")
                continue

            # Si no hay prioridad, asigna 1 por defecto
            prioridad = int(datos[3].strip()) if len(
                datos) > 3 and datos[3].strip() else 1

            nuevo_proceso = Process(pid, arrival_time, burst_time, prioridad)

            procesos.append(nuevo_proceso)

        except ValueError:
            errores.append(
                f"Línea {i}: Los tiempos y la prioridad deben ser números enteros.")

    return procesos, errores


def load_processes_from_csv(filepath):
    """
    Lee un archivo físico y usa parse_process_data para procesarlo.
    """
    if not os.path.exists(filepath):
        print(f"Error: No se encontró el archivo {filepath}")
        return []

    with open(filepath, 'r', encoding='utf-8') as file:
        lineas = file.readlines()
        return parse_process_data(lineas)
