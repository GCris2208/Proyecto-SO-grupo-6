
def calcular_promedios(procesos_terminados):
    cantidad = len(procesos_terminados)
    if cantidad == 0:
        return {"awt": 0, "att": 0, "art": 0, "interrupciones": 0}

    return {
        "awt": sum(p.waiting_time for p in procesos_terminados) / cantidad,
        "att": sum(p.turnaround_time for p in procesos_terminados) / cantidad,
        "art": sum(p.response_time for p in procesos_terminados) / cantidad,
        "interrupciones": sum(p.interrupciones for p in procesos_terminados)
    }


def evaluar_ganadores(resultados_algoritmos, criterio_1, criterio_2):
    # resultados_algoritmos es un diccionario con los promedios de cada algoritmo

    # 1. Convertimos el diccionario a una lista para poder ordenarla
    lista_clasificacion = []
    for nombre_algoritmo, metricas in resultados_algoritmos.items():
        lista_clasificacion.append({
            "algoritmo": nombre_algoritmo,
            "criterio_principal": metricas[criterio_1],
            "criterio_secundario": metricas[criterio_2],
            "todas_las_metricas": metricas
        })

    # 2. Ordenamos usando tuplas (de menor a mayor tiempo)
    lista_clasificacion.sort(key=lambda x: (
        x["criterio_principal"], x["criterio_secundario"]))

    # 3. Detectar si hay un empate técnico en el primer lugar
    ganadores = [lista_clasificacion[0]]
    for i in range(1, len(lista_clasificacion)):
        if (lista_clasificacion[i]["criterio_principal"] == ganadores[0]["criterio_principal"] and
                lista_clasificacion[i]["criterio_secundario"] == ganadores[0]["criterio_secundario"]):
            ganadores.append(lista_clasificacion[i])
        else:
            break  # Si ya no es igual al primero, rompemos el ciclo

    return ganadores, lista_clasificacion
