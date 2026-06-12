import http.server
import socketserver
import json
import traceback
from Core.process import Process
from Core.algorithms.fcfs import run_fcfs
from Core.algorithms.sjf import run_sjf
from Core.algorithms.priority import run_priority
from Core.algorithms.round_robin import run_round_robin
from Core.metrics import calculate_global_metrics

PORT = 8000

class SimuladorHandler(http.server.SimpleHTTPRequestHandler):
    def _send_cors_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')

    def do_OPTIONS(self):
        self.send_response(200)
        self._send_cors_headers()
        self.end_headers()

    def do_GET(self):
        if self.path == '/':
            self.path = '/UI/index.html'
        return super().do_GET()

    def do_POST(self):
        if self.path == '/simulate':
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode('utf-8'))
                
                procesos_raw = data.get('procesos', '').strip().split('\n')
                algoritmo = data.get('algoritmo', 'fcfs')
                quantum = data.get('quantum', 3)
                
                lista_procesos = []
                for linea in procesos_raw:
                    partes = linea.split(',')
                    if len(partes) >= 3:
                        pid = partes[0].strip()
                        llegada = int(partes[1].strip())
                        rafaga = int(partes[2].strip())
                        prioridad = int(partes[3].strip()) if len(partes) > 3 else 0
                        lista_procesos.append(Process(pid, llegada, rafaga, prioridad))
                
                resultados = []
                if algoritmo == 'fcfs':
                    resultados = run_fcfs(lista_procesos)
                elif algoritmo == 'sjf':
                    resultados = run_sjf(lista_procesos)
                elif algoritmo == 'priority':
                    resultados = run_priority(lista_procesos)
                elif algoritmo == 'rr':
                    resultados = run_round_robin(lista_procesos, quantum)
                    
                metricas = calculate_global_metrics(resultados)
                
                response_data = {
                    'procesos': [
                        {
                            'pid': p.pid,
                            'turnaround_time': p.turnaround_time,
                            'waiting_time': p.waiting_time,
                            'response_time': p.response_time,
                            'completion_time': p.completion_time
                        } for p in resultados
                    ],
                    'metricas': metricas
                }
                
                self.send_response(200)
                self._send_cors_headers()
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(response_data).encode('utf-8'))
                
            except Exception as e:
                print(traceback.format_exc())
                self.send_response(200)
                self._send_cors_headers()
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))

if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), SimuladorHandler) as httpd:
        print(f"Servidor web iniciado en http://localhost:{PORT}")
        httpd.serve_forever()