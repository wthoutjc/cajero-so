class Rr():
    def __init__(self):
        self.procesos = []
        self.quantum = None
    
    def set_quantum(self, quantum):
        self.quantum = quantum
    
    def get_quantum(self):
        return self.quantum

    def nuevo_proceso(self, proceso):
        self.procesos.append(proceso)
    
    def get_procesos(self):
        return self.procesos
    
    def borrar_nodo(self):
        '''
        Borra un nodo
        '''
        self.procesos.pop(0)