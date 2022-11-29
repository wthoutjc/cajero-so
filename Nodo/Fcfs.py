class Fcfs():
    def __init__(self):
        self.procesos = []

    def nuevo_proceso(self, proceso):
        self.procesos.append(proceso)
    
    def get_procesos(self):
        return self.procesos
    
    def borrar_nodo(self):
        '''
        Borra un nodo
        '''
        self.procesos.pop(0)