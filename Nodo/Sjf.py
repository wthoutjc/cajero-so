class Sjf():
    def __init__(self):
        self.procesos = []
    
    def ordenar(self):
        '''
        Ordena los nodos de acuerdo a la rafaga
        '''
        n = len(self.procesos)

        for i in range(n - 1):
            for j in range(n-1-i):
                if j == 0:
                    pass
                elif self.procesos[j][2] > self.procesos[j+1][2]:
                    self.procesos[j], self.procesos[j+1] = self.procesos[j+1], self.procesos[j]
    
    def nuevo_proceso(self, proceso):
        self.procesos.append(proceso)
        self.ordenar()
    
    def get_procesos(self):
        return self.procesos
    
    def borrar_nodo(self):
        '''
        Borra un nodo
        '''
        self.procesos.pop(0)