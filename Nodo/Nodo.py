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
    def __init__(self, id=None, tiempo_llegada=0, rafaga=0, rafaga_ejecutada=0, origin=None):
        self.id = id
        self.origin = origin

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

    def nuevo_nodo(self, new_nodo, no_option=False, origin=None):
        '''
        Inicia un nuevo proceso
        Args:
            -new_nodo: Client
        '''
        option = fake.random_element(['rr','fcfs', 'sjf']) if not no_option else 'process' 
        nuevo_nodo = [
            new_nodo.id, 
            new_nodo.tiempo_llegada, 
            new_nodo.rafaga
        ]
        if origin:
            if origin == 'rr':
                self.rr.nuevo_proceso(nuevo_nodo)
            elif origin == 'fcfs':
                self.fcfs.nuevo_proceso(nuevo_nodo)
            elif origin == 'sjf':
                self.sjf.nuevo_proceso(nuevo_nodo)
        elif option == 'rr':
            self.rr.nuevo_proceso(nuevo_nodo)
        elif option == 'fcfs':
            self.fcfs.nuevo_proceso(nuevo_nodo)
        elif option == 'sjf':
            self.sjf.nuevo_proceso(nuevo_nodo)
        else:
            self.procesos.append([new_nodo.id, new_nodo.tiempo_llegada, new_nodo.rafaga, 0, 0, 0, 0, 0, 0, new_nodo.origin])

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
        nodo[3] = nodo[1] if nodo_anterior == nodo else nodo_anterior[4] + nodo[1] # Tiempo de comienzo

        if nodo[9] == 'rr':
            nodo[7] = fake.random_int(min= 0, max = nodo[2] - 1) # Bloqueo
            if self.rr.get_quantum():
                if nodo[7] == 0 and nodo[2] > self.rr.get_quantum():
                    nodo[7] = self.rr.get_quantum()
                elif nodo[7] > self.rr.get_quantum():
                    nodo[7] = self.rr.get_quantum()
        elif nodo[9] == 'fcfs':
            nodo[7] = fake.random_int(min= 0, max = nodo[2] - 1) # Bloqueo
        elif nodo[9] == 'sjf':
            nodo[7] = fake.random_int(min= 0, max = nodo[2] - 1) # Bloqueo
        nodo[8] = nodo[2] - ((nodo[2] - nodo[7]) if nodo[7] > 0 else 0) # Rafaga ejecutada
        nodo[4] = nodo[8] + nodo[3] # Tiempo final
        nodo[5] = nodo[4] - nodo[1] # Tiempo de retorno
        nodo[6] = nodo[5] - nodo[8] # Tiempo de espera

    def cargar_proceso(self):
        '''
        Retorna un proceso
        '''
        rr_procesos = self.rr.get_procesos()
        tam_rr_procesos = len(rr_procesos)

        if tam_rr_procesos > 0:
            print('Extrae de RR')
            nuevo_nodo = Nodo(rr_procesos[0][0],rr_procesos[0][1],rr_procesos[0][2])
            nuevo_nodo.set_origin('rr')
            self.nuevo_nodo(nuevo_nodo, True)
            self.rr.borrar_nodo()
        else:
            sjf_procesos = self.sjf.get_procesos()
            tam_sjf_procesos = len(sjf_procesos)
            if tam_sjf_procesos > 0:
                print('Extrae de SJF')
                nuevo_nodo = Nodo(sjf_procesos[0][0], sjf_procesos[0][1],sjf_procesos[0][2])
                nuevo_nodo.set_origin('sjf')
                self.nuevo_nodo(nuevo_nodo, True)
                self.sjf.borrar_nodo()
            else:
                fcfs_procesos = self.fcfs.get_procesos()
                tam_fcfs_procesos = len(fcfs_procesos)
                if tam_fcfs_procesos > 0:
                    print('Extrae de FCFS')
                    nuevo_nodo = Nodo(fcfs_procesos[0][0], fcfs_procesos[0][1], fcfs_procesos[0][2])
                    nuevo_nodo.set_origin('fcfs')
                    self.nuevo_nodo(nuevo_nodo, True)
                    self.fcfs.borrar_nodo()

    def envejecimiento_nodos(self):
        '''
        Pasa el primero de  fcfs a sjf y el primero de sjf a rr
        '''
        fcfs_procesos = self.fcfs.get_procesos()
        tam_fcfs_procesos = len(fcfs_procesos)
        if tam_fcfs_procesos > 0:
            print('Envejece FCFS')
            nuevo_nodo = Nodo(fcfs_procesos[0][0], fcfs_procesos[0][1], fcfs_procesos[0][2])
            self.nuevo_nodo(nuevo_nodo, True, 'sjf')
            self.fcfs.borrar_nodo()
        sjf_procesos = self.sjf.get_procesos()
        tam_sjf_procesos = len(sjf_procesos)
        if tam_sjf_procesos > 0:
            print('Envejece SJF')
            nuevo_nodo = Nodo(sjf_procesos[0][0], sjf_procesos[0][1], sjf_procesos[0][2])
            self.nuevo_nodo(nuevo_nodo, True, 'rr')
            self.sjf.borrar_nodo()

    def eliminar(self):
        '''
        M??todo que elimina un proceso
        Args:
            -id: str
        '''
        self.procesos.pop(0)

    def set_procesos(self, procesos):
        '''
        Setea todos los procesos
        '''
        self.procesos = procesos
    
    def set_origin(self, origin):
        '''
        Setea el origen de los procesos
        '''
        self.origin = origin
    
    def get_origin(self):
        '''
        Retorna el origen de los procesos
        '''
        return self.origin

    def get_procesos(self):
        '''
        Retorna todos los procesos
        '''
        return self.procesos
    