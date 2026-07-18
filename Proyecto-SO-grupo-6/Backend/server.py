from flask import Flask, request, jsonify
from flask_cors import CORS
import traceback
import copy

# Importaciones
from Core.process import Process
from Core.algorithms.fcfs import run_fcfs
from Core.algorithms.srtf import run_srtf
from Core.algorithms.sjf import run_sjf
from Core.algorithms.priority import run_priority
from Core.algorithms.round_robin import run_round_robin
from Core.metrics import calculate_global_metrics
from Utils.file_handler import parse_process_data
from Core.algorithms.comparator import calcular_promedios, evaluar_ganadores

# Inicialización de la aplicación Flask
app = Flask(__name__)
# Habilitar CORS para permitir peticiones desde el frontend
CORS(app)


@app.route('/simulate', methods=['POST'])
def simulate():
    try:
        # 1. Obtener y leer los datos en JSON automáticamente
        data = request.json
        if not data:
            return jsonify({"error": "No se recibieron datos JSON"}), 400

        procesos_raw = data.get('procesos', '').strip().split('\n')
        algoritmo = data.get('algoritmo', 'fcfs').lower()
        quantum = data.get('quantum', 3)

        # 2. Parsear los procesos
        lista_procesos, errores_parseo = parse_process_data(procesos_raw)

        if errores_parseo:
            mensaje_error = "Corrige los siguientes errores:\n" + \
                "\n".join(errores_parseo)
            return jsonify({"error": mensaje_error}), 400

        if not lista_procesos:
            return jsonify({"error": "No se ingresaron procesos válidos."}), 400

        # 3. Lógica para el modo "Comparar Todos"
        if algoritmo == 'comparar':
            criterio_1 = data.get('criterio_1', 'awt')
            criterio_2 = data.get('criterio_2', 'art')
            quantum = int(data.get('quantum', 2))

        # Función local para contar cuántas veces cambia de proceso el procesador
            def contar_interrupciones(gantt):
                if not gantt:
                    return 0
                interrupciones = 0
                pid_actual = gantt[0]['pid']
                for bloque in gantt[1:]:
                    if bloque['pid'] != pid_actual:
                        interrupciones += 1
                        pid_actual = bloque['pid']
                return interrupciones

            # Ejecuta todos los algoritmos (pasando copy.deepcopy() y guardando el gantt)
            res_fcfs, gantt_fcfs = run_fcfs(copy.deepcopy(lista_procesos))
            res_sjf, gantt_sjf = run_sjf(copy.deepcopy(lista_procesos))
            res_srtf, gantt_srtf = run_srtf(copy.deepcopy(lista_procesos))
            res_prio, gantt_prio = run_priority(copy.deepcopy(lista_procesos))
            res_rr, gantt_rr = run_round_robin(
                copy.deepcopy(lista_procesos), quantum)

            # Calcula promedios e inyectar las interrupciones calculadas
            resultados = {
                "FCFS": {**calcular_promedios(res_fcfs), "interrupciones": contar_interrupciones(gantt_fcfs)},
                "SJF": {**calcular_promedios(res_sjf), "interrupciones": contar_interrupciones(gantt_sjf)},
                "SRTF": {**calcular_promedios(res_srtf), "interrupciones": contar_interrupciones(gantt_srtf)},
                "Prioridad": {**calcular_promedios(res_prio), "interrupciones": contar_interrupciones(gantt_prio)},
                "Round Robin": {**calcular_promedios(res_rr), "interrupciones": contar_interrupciones(gantt_rr)}
            }

            # Obtener el ganador (o ganadores)
            ganadores, ranking_completo = evaluar_ganadores(
                resultados, criterio_1, criterio_2)

            respuesta_comparacion = {
                "ganadores": [g["algoritmo"] for g in ganadores],
                "ranking": ranking_completo
            }
            return jsonify(respuesta_comparacion), 200

        # 4. Lógica para Simulación Normal (Un solo algoritmo)
        resultados = []
        historial_gantt = []

        if algoritmo == 'fcfs':
            resultados, historial_gantt = run_fcfs(lista_procesos)
        elif algoritmo == 'sjf':
            resultados, historial_gantt = run_sjf(lista_procesos)
        elif algoritmo == 'priority':
            resultados, historial_gantt = run_priority(lista_procesos)
        elif algoritmo == 'srtf':
            resultados, historial_gantt = run_srtf(lista_procesos)
        elif algoritmo == 'rr':
            try:
                quantum = int(quantum)
                if quantum <= 0:
                    raise ValueError
            except (ValueError, TypeError):
                return jsonify({"error": "Para Round Robin, el Quantum debe ser un número entero mayor a 0."}), 400

            resultados, historial_gantt = run_round_robin(
                lista_procesos, quantum)
        else:
            return jsonify({"error": "Algoritmo no reconocido"}), 400

# 5. Cálculo de métricas globales
        metricas = calculate_global_metrics(resultados)

        # proceso convoy
        metricas['procesos_convoy'] = [
            p.pid for p in resultados if p.waiting_time > 15]

        # RECUENTO DE INTERRUPCIONES PARA MODO NORMAL
        interrupciones = 0
        if historial_gantt:
            pid_actual = historial_gantt[0]['pid']
            for bloque in historial_gantt[1:]:
                if bloque['pid'] != pid_actual:
                    interrupciones += 1
                    pid_actual = bloque['pid']

        # Sobrescribimos el valor erróneo de metrics.py
        metricas['interrupciones'] = interrupciones

        # 6. Construir la respuesta final de la simulación
        response_data = {
            'procesos': [
                {
                    'pid': p.pid,
                    'turnaround_time': p.turnaround_time,
                    'waiting_time': p.waiting_time,
                    'response_time': p.response_time,
                    'completion_time': p.completion_time,
                } for p in resultados
            ],
            'metricas': metricas,
            'gantt': historial_gantt
        }

        return jsonify(response_data), 200

    except Exception as e:
        # En caso de error interno, imprimir en consola y devolver 500 al cliente
        print(traceback.format_exc())
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    PORT = 8000
    print(f"Servidor Flask iniciado en http://localhost:{PORT}")
    # debug=True permite que el servidor se reinicie solo si haces cambios en el código
    app.run(host='0.0.0.0', port=PORT, debug=True)
