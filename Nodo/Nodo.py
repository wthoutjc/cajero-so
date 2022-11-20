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
        self.tiempo_final = self.tiempo_comienzo + self.rafaga
        self.tiempo_retorno = self.tiempo_final - self.tiempo_llegada
        self.tiempo_espera = self.tiempo_retorno - self.rafaga

        # Density
        self.density = fake.random_int(min=0, max=6)
        self.blocked = 0

        self.procesos = []

        # Table data
        self.table_data = []
            
    def set_next(self, next):
        self.next = next

    def get_next(self):
        return self.next

    def iniciar_servicio(self, nodo):
        self.set_next(nodo)

    def nuevo_nodo(self, nodo, new_nodo):
        '''
        Inicia un nuevo proceso
        Args:
            -new_nodo: Client
        '''
        if nodo.get_next().type == new_nodo.type:
            self.nuevo_nodo(nodo.get_next(), new_nodo)
        else:
            # Es nodo inicial
            new_nodo.tiempo_comienzo = nodo.rafaga + nodo.tiempo_comienzo
            new_nodo.tiempo_final = (nodo.rafaga + nodo.tiempo_comienzo) + new_nodo.rafaga
            new_nodo.tiempo_retorno = ((nodo.rafaga + nodo.tiempo_comienzo) + new_nodo.rafaga) - new_nodo.tiempo_llegada
            new_nodo.tiempo_espera = (((nodo.rafaga + nodo.tiempo_comienzo) + new_nodo.rafaga) - new_nodo.tiempo_llegada) - new_nodo.rafaga

            # Estado de bloqueado
            new_nodo.blocked = fake.random_int(min=0, max=new_nodo.rafaga - 1) if new_nodo.density >= 5 else 0

            new_nodo.tiempo_final = new_nodo.tiempo_final if new_nodo.blocked == 0 else  new_nodo.tiempo_final - new_nodo.blocked

            new_nodo.set_next(nodo.get_next()) # Apunta al nodo de manera circular
            nodo.set_next(new_nodo)
            print(f'Agregando Nodo: {new_nodo.type} - Densidad: {new_nodo.density} - Tiempo de llegada: {new_nodo.tiempo_llegada} - Rafaga: {new_nodo.rafaga} - Tiempo de comienzo: {new_nodo.tiempo_comienzo} - Tiempo final: {new_nodo.tiempo_final} - Tiempo de retorno: {new_nodo.tiempo_retorno} - Tiempo de espera: {new_nodo.tiempo_espera} -  Bloqueo: {new_nodo.blocked}')
            self.table_data.append([new_nodo.id, new_nodo.tiempo_llegada, new_nodo.rafaga, new_nodo.tiempo_comienzo, new_nodo.tiempo_final, new_nodo.tiempo_retorno, new_nodo.tiempo_espera, new_nodo.blocked])

    def eliminar(self, nodo, nodo_inicial):
        '''
        Método que elimina un proceso
        Args:
            -id: str
        '''
        print(f'Eliminando -> {nodo.type} - Tiempo de llegada: {nodo.tiempo_llegada} - Rafaga: {nodo.rafaga} - Tiempo de comienzo: {nodo.tiempo_comienzo} - Tiempo final: {nodo.tiempo_final} - Tiempo de retorno: {nodo.tiempo_retorno} - Tiempo de espera: {nodo.tiempo_espera}')
        nodo_inicial.set_next(nodo.get_next())
    
    def iterar_procesos(self, nodo):
        '''
        Retorna todos los procesos
        '''
        if nodo.type == 'Proceso':
            self.procesos.append([nodo.id, nodo.tiempo_llegada, nodo.rafaga, nodo.tiempo_comienzo, nodo.tiempo_final, nodo.tiempo_retorno, nodo.tiempo_espera, nodo.blocked])
            self.iterar_procesos(nodo.get_next())
    
    def set_all_process(self, procesos):
        '''
        Setea todos los procesos
        '''
        self.procesos = procesos

    def get_all_process(self):
        '''
        Retorna todos los procesos
        '''
        return self.procesos
    
    def get_data_table(self):
        '''
        Retorna todos los procesos
        '''
        return self.table_data