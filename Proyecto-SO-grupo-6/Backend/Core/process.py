from enum import Enum


class ProcessState(Enum):
    NUEVO = "Nuevo"
    LISTO = "Listo"
    EJECUTANDO = "Ejecutando"
    TERMINADO = "Terminado"


class Process:
    def __init__(self, pid, arrival_time, burst_time, priority=0):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.priority = priority

        self.state = ProcessState.NUEVO
        self.remaining_time = burst_time

        self.start_time = -1
        self.completion_time = 0

        self.turnaround_time = 0
        self.waiting_time = 0
        self.response_time = 0
        self.interrupciones = 0

    def __repr__(self):
        return f"Proceso({self.pid} | Llegada: {self.arrival_time} | Ráfaga: {self.burst_time} | Prioridad: {self.priority} | Estado: {self.state})"
