from flask_socketio import SocketIO
from flask_cors import CORS

# Herramientas
import logging
import eventlet
import time
import datetime

# Cajero
from Nodo.Nodo import Nodo

# Fake data
from faker import Faker
Faker.seed(datetime.datetime.now())

# LOGS
logging.basicConfig(filename='client.log', level=logging.DEBUG)

# Fake data
fake = Faker('es-ES')

# Hilos
from threading import Thread

class SocketIOClient(object):
    def __init__(self, app):
        self.app = app
        CORS(self.app)

        self.continue_node = True

        self.tiempo_llegada = 0
        self.id = 0
        self.counter = 0
        self.quantum = 4

        self.lienzo_procesos = []

        self.stop_thread = False
        self.stop_cargar_proceso = False

        self.nodo = Nodo()
        self.nodo.rr.set_quantum(self.quantum)

        self.socketio = SocketIO(app, cors_allowed_origins='*', async_mode="threading")
        self.socketio.emit('cycle', 0)

        @self.socketio.on('connect')
        def on_connect():
            self.thread_crear_procesos = Thread(target=self.crear_procesos)
            self.thread_crear_procesos.start()
            self.socketio.emit('data', [])
            self.socketio.emit('traffic_light-data', [])
            
        @self.socketio.on('disconnect')
        def on_disconnect():
            self.stop_thread = True
    
        @self.socketio.on('start')
        def on_start(data):
            self.stop_thread = False
            self.thread_iniciar_ciclo = Thread(target=self.iniciar_ciclo)
            self.thread_envejer_procesos = Thread(target=self.envejer_procesos)

            self.thread_iniciar_ciclo.start()
            self.thread_envejer_procesos.start()

        @self.socketio.on('stop')
        def on_stop(data):
            self.stop_thread = True
        
        @self.socketio.on('quantum')
        def on_stop(data):
            print(f'Quantum: {data}')
            self.quantum = data
            self.nodo.rr.set_quantum(data)
        
        @self.socketio.on('rr-new_process')
        def on_rr_new_process(data):
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
            print('Nuevo proceso en RR')
            procesos = self.nodo.get_procesos()
            print(f'PROCESOS: {procesos}')
            if procesos and procesos[0] and procesos[0][9] != 'rr':
                print(procesos)
                print(self.counter)
                self.nodo.cargar_proceso()
                print(f'NUEVA RAFAGA {(procesos[0][2] + procesos[0][3]) - (self.counter - 1)}')
                procesos[0][2] = self.counter - procesos[0][3]
                procesos[0][4] = self.counter


                self.nodo.atender_nodo(procesos[1])
                self.lienzo_procesos.append(procesos[1].copy())
                
                self.nodo.nuevo_nodo(Nodo(procesos[0][0], procesos[0][1], procesos[0][2]), False, procesos[0][9])
                self.nodo.eliminar()

                self.socketio.emit('data', self.lienzo_procesos)
                self.socketio.emit('data-table', self.lienzo_procesos)

                self.socketio.emit('round_robin-data', self.nodo.rr.get_procesos())
                self.socketio.emit('sjf-data', self.nodo.sjf.get_procesos())
                self.socketio.emit('fcfs-data', self.nodo.fcfs.get_procesos())

    def envejer_procesos(self):
        time.sleep(25)
        print('Envejecer procesos')
        self.nodo.envejecimiento_nodos()
        self.envejer_procesos()

    def crear_procesos(self):
        self.nodo.nuevo_nodo(Nodo(self.id, 0, fake.random_int(2, 10)))

        self.id += 1
        self.tiempo_llegada += 1

        self.socketio.emit('data-table', self.lienzo_procesos)

        self.socketio.emit('round_robin-data', self.nodo.rr.get_procesos())
        self.socketio.emit('sjf-data', self.nodo.sjf.get_procesos())
        self.socketio.emit('fcfs-data', self.nodo.fcfs.get_procesos())

        time.sleep(10)
        self.crear_procesos()
    
    def atender_procesos(self):
        try:
            if not self.stop_cargar_proceso:
                self.nodo.cargar_proceso()
                self.stop_cargar_proceso = True
            procesos = self.nodo.get_procesos()
            if self.continue_node: # Primer nodo
                self.socketio.emit('traffic_light-data', [procesos[0]])
                self.continue_node = False
                self.nodo.atender_nodo(procesos[0])
                self.lienzo_procesos.append(procesos[0].copy())
            elif procesos[0][7] != 0 and (procesos[0][7] + procesos[0][3]) == self.counter - 1: # Presenta bloqueo
                self.nodo.cargar_proceso()
                self.socketio.emit('traffic_light-data', [procesos[0], procesos[1]])
                self.nodo.atender_nodo(procesos[1])
                self.lienzo_procesos.append(procesos[1].copy())

                procesos[0][2] = procesos[0][2] - procesos[0][7]
                self.nodo.nuevo_nodo(Nodo(procesos[0][0], procesos[0][1], procesos[0][2]), False, procesos[0][9])
                self.nodo.eliminar()
            elif self.counter == procesos[0][4] + 1: # Proceso normal
                self.nodo.cargar_proceso()
                self.socketio.emit('traffic_light-data', [procesos[0], procesos[1]])
                self.nodo.atender_nodo(procesos[1])
                self.lienzo_procesos.append(procesos[1].copy())
                self.nodo.eliminar()
        except ValueError as e:
            print(e)
        finally:
            self.socketio.emit('data', self.lienzo_procesos)
            self.socketio.emit('data-table', self.lienzo_procesos)

            self.socketio.emit('round_robin-data', self.nodo.rr.get_procesos())
            self.socketio.emit('sjf-data', self.nodo.sjf.get_procesos())
            self.socketio.emit('fcfs-data', self.nodo.fcfs.get_procesos())
            
    def iniciar_ciclo(self):
        if not self.stop_thread:
            self.socketio.emit('cycle', self.counter)
            self.counter += 1
            time.sleep(1)
            self.atender_procesos()
            self.iniciar_ciclo()

    def run(self):
        self.socketio.run(self.app, port=8000, host="0.0.0.0", debug=True)
        eventlet.monkey_patch(socket=True, select=True)


