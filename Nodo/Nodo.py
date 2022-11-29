# Herramientas
import datetime

# Fake data
from faker import Faker
Faker.seed(datetime.datetime.now())
fake = Faker('es-ES')

# Algorithms
from Nodo.Fcfs import Fcfs
from Nodo.Sjf import Sjf
from Nodo.Rr import Rr

class Nodo:
    def __init__(self, id=None, tiempo_llegada=0, rafaga=0, rafaga_ejecutada=0):
        self.id = id

        self.tiempo_llegada = tiempo_llegada
        self.rafaga = rafaga
        self.rafaga_ejecutada = rafaga_ejecutada
        self.tiempo_comienzo = 0
        self.tiempo_final = 0
        self.tiempo_retorno = 0
        self.tiempo_espera = 0
        self.blocked = 0

        self.rr = Rr()
        self.fcfs = Fcfs()
        self.sjf = Sjf()

        self.procesos = []

    def nuevo_nodo(self, new_nodo, no_option=False):
        '''
        Inicia un nuevo proceso
        Args:
            -new_nodo: Client
        '''
        option = fake.random_element(['rr']) if not no_option else 'process' #'fcfs', 'sjf'
        nuevo_nodo = [
            new_nodo.id, 
            new_nodo.tiempo_llegada, 
            new_nodo.rafaga
        ]
        if option == 'rr':
            self.rr.nuevo_proceso(nuevo_nodo)
        elif option == 'fcfs':
            self.fcfs.nuevo_proceso(nuevo_nodo)
        elif option == 'sjf':
            self.sjf.nuevo_proceso(nuevo_nodo)
        else:
            self.procesos.append([new_nodo.id, new_nodo.tiempo_llegada, new_nodo.rafaga, 0, 0, 0, 0, 0, 0])

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
            7 blocked,
            8 rafaga_ejecutada
        '''
        nodo_anterior = self.procesos[0]

        print(f'NODO ANT -> #{nodo_anterior[0]} T. Llegada {nodo_anterior[1]} - Rafaga {nodo_anterior[2]} - Rafaga Ejecutada {nodo_anterior[8]} - T.Comienzo {nodo_anterior[3]} - T. Final {nodo_anterior[4]} - T. Retorno {nodo_anterior[5]} - T. Espera {nodo_anterior[6]} - BLoqueo {nodo_anterior[7]}')
        nodo[3] = 0 if nodo_anterior == nodo else nodo_anterior[4] # Tiempo de comienzo
        nodo[7] = fake.random_int(min= 0, max = nodo[2] - 1) # Bloqueo
        if self.rr.get_quantum():
            if nodo[7] == 0 and nodo[2] > self.rr.get_quantum():
                nodo[7] = self.rr.get_quantum()
            elif nodo[7] > self.rr.get_quantum():
                nodo[7] = self.rr.get_quantum()
        nodo[8] = nodo[2] - ((nodo[2] - nodo[7]) if nodo[7] > 0 else 0) # Rafaga ejecutada
        nodo[4] = nodo[8] + nodo[3] # Tiempo final
        nodo[5] = nodo[4] - nodo[1] # Tiempo de retorno
        nodo[6] = nodo[5] - nodo[8] # Tiempo de espera
        print(f'NODO ACT -> #{nodo[0]} T. Llegada {nodo[1]} - Rafaga {nodo[2]} - Rafaga Ejecutada {nodo[8]} - T.Comienzo {nodo[3]} - T. Final {nodo[4]} - T. Retorno {nodo[5]} - T. Espera {nodo[6]} - BLoqueo {nodo[7]}')

    def cargar_proceso(self):
        '''
        Retorna un proceso
        '''
        rr_procesos = self.rr.get_procesos()
        tam_rr_procesos = len(rr_procesos)

        if tam_rr_procesos > 0:
            self.nuevo_nodo(Nodo(rr_procesos[0][0],rr_procesos[0][1],rr_procesos[0][2]), True)
            self.rr.borrar_nodo()
        else:
            sjf_procesos = self.sjf.get_procesos()
            tam_sjf_procesos = len(sjf_procesos)
            if tam_sjf_procesos > 0:
                self.nuevo_nodo(Nodo(sjf_procesos[0][0], sjf_procesos[0][1],sjf_procesos[0][2]), True)
                self.sjf.borrar_nodo()
            else:
                fcfs_procesos = self.fcfs.get_procesos()
                tam_fcfs_procesos = len(fcfs_procesos)
                if tam_fcfs_procesos > 0:
                    self.nuevo_nodo(Nodo(fcfs_procesos[0][0], fcfs_procesos[0][1], fcfs_procesos[0][2]), True)
                    self.fcfs.borrar_nodo()

    def eliminar(self):
        '''
        Método que elimina un proceso
        Args:
            -id: str
        '''
        print(f'Eliminando proceso #{self.procesos[0][0]}')
        self.procesos.pop(0)

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