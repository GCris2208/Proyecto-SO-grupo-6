from collections import deque

class QueueManager:
    def __init__(self):
        # Utilización de la estructura eficiente collections.deque para la Ready Queue
        self.ready_queue = deque()
        self.finished_processes = []

    def add_process(self, process):
        self.ready_queue.append(process)

    def pop_process(self):
        if self.ready_queue:
            return self.ready_queue.popleft()
        return None
        
    def is_empty(self):
        return len(self.ready_queue) == 0