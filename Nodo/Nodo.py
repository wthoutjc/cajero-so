# Herramientas
import datetime

# Fake data
from faker import Faker
Faker.seed(datetime.datetime.now())
fake = Faker('es-ES')

class Nodo:
    def __init__(self, type, id=None, tiempo_llegada=0, rafaga=0):
        self.next = None
        self.socketio = None
        self.type = type
        self.id = id

        # FCFS
        self.tiempo_llegada = tiempo_llegada
        self.rafaga = rafaga
        self.tiempo_comienzo = 0
        self.tiempo_final = 0
        self.tiempo_retorno = 0
        self.tiempo_espera = 0

        # Density
        self.blocked = 0

        self.procesos = []
        self.lienzo_tabla = []

    def nuevo_nodo(self, new_nodo):
        '''
        Inicia un nuevo proceso
        Args:
            -new_nodo: Client
        '''
        nuevo_nodo = [
            new_nodo.id, 
            new_nodo.tiempo_llegada, 
            new_nodo.rafaga, 
            new_nodo.tiempo_comienzo, 
            new_nodo.tiempo_final, 
            new_nodo.tiempo_retorno, 
            new_nodo.tiempo_espera, 
            new_nodo.blocked
        ]

        # print(f'Agregando Nodo: {new_nodo.type} - Densidad: {new_nodo.density} - Tiempo de llegada: {new_nodo.tiempo_llegada} - Rafaga: {new_nodo.rafaga} - Tiempo de comienzo: {new_nodo.tiempo_comienzo} - Tiempo final: {new_nodo.tiempo_final} - Tiempo de retorno: {new_nodo.tiempo_retorno} - Tiempo de espera: {new_nodo.tiempo_espera} -  Bloqueo: {new_nodo.blocked}')
        self.procesos.append(nuevo_nodo)
        self.lienzo_tabla.append(nuevo_nodo.copy())

    def atender_nodo(self, nodo):
        '''
        Atiende un nodo
            0 id, 
            1 tiempo_llegada, 
            2 rafaga, 
            3 tiempo_comienzo, 
            4 tiempo_final, 
            5 tiempo_retorno, 
            6 tiempo_espera, 
            7 blocked
        '''
        nodo_anterior = self.procesos[0]

        print(f'NODO ANT -> #{nodo_anterior[0]} T. Llegada {nodo_anterior[1]} - Rafaga {nodo_anterior[2]} - T.Comienzo {nodo_anterior[3]} - T. Final {nodo_anterior[4]} - T. Retorno {nodo_anterior[5]} - T. Espera {nodo_anterior[6]} - BLoqueo {nodo_anterior[7]}')
        if nodo_anterior != nodo:
            if nodo_anterior[7] != 0:
                nodo[3] =  (nodo_anterior[2] + nodo_anterior[3]) - (nodo_anterior[2] - nodo_anterior[7])
            else:
                nodo[3] = nodo_anterior[2] + nodo_anterior[3] # Tiempo de comienzo
        else:
            nodo[3] = 0
        nodo[4] = nodo[3] + nodo[2] # Tiempo final
        nodo[5] = nodo[4] - nodo[1] # Tiempo de retorno
        nodo[6] = nodo[5] - nodo[2] # Tiempo de espera
        nodo[7] = fake.random_int(min= 0, max = nodo[2] - 1) # Bloqueo
        # nodo[7] = 0 # Bloqueo
        print(f'NODO ACT -> #{nodo[0]} T. Llegada {nodo[1]} - Rafaga {nodo[2]} - T.Comienzo {nodo[3]} - T. Final {nodo[4]} - T. Retorno {nodo[5]} - T. Espera {nodo[6]} - BLoqueo {nodo[7]}')

    def eliminar(self):
        '''
        Método que elimina un proceso
        Args:
            -id: str
        '''
        print(f'Eliminando proceso #{self.procesos[0][0]}')
        self.procesos.pop(0)
    
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

    def set_procesos(self, procesos):
        '''
        Setea todos los procesos
        '''
        self.procesos = procesos

    def get_procesos(self):
        '''
        Retorna todos los procesos
        '''
        return self.procesos
    
    def get_lienzo_tabla(self):
        '''
        Retorna el lienzo de la tabla
        '''
        return self.lienzo_tabla