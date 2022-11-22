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

        self.lienzo_gantt = []

        self.stop_thread = False

        self.nodo = Nodo('Inicial')

        self.socketio = SocketIO(app, cors_allowed_origins='*', async_mode="threading")
        self.socketio.emit('cycle', 0)

        @self.socketio.on('connect')
        def on_connect():
            self.thread_crear_procesos = Thread(target=self.crear_procesos)
            self.thread_crear_procesos.start()
            self.socketio.emit('data', [])
            
        @self.socketio.on('disconnect')
        def on_disconnect():
            self.stop_thread = True
    
        @self.socketio.on('start')
        def on_start(data):
            self.stop_thread = False
            self.thread_iniciar_ciclo = Thread(target=self.iniciar_ciclo)
            self.thread_iniciar_ciclo.start()

        @self.socketio.on('stop')
        def on_stop(data):
            self.stop_thread = True

    def crear_procesos(self):
        self.nodo.nuevo_nodo(Nodo('Proceso', self.id, self.tiempo_llegada, fake.random_int(2, 10)))

        self.id += 1
        self.tiempo_llegada += 1

        self.nodo.ordenar()

        lienzo_tabla = self.nodo.get_lienzo_tabla()

        self.socketio.emit('data-table', lienzo_tabla)
        time.sleep(10)
        self.crear_procesos()
    
    def atender_procesos(self):
        procesos = self.nodo.get_procesos()
        if self.continue_node:
            self.continue_node = False
            self.nodo.atender_nodo(procesos[0])
            self.lienzo_gantt.append(procesos[0].copy())

            lienzo_tabla = self.nodo.get_lienzo_tabla()

            self.socketio.emit('data', self.lienzo_gantt)
            self.socketio.emit('data-table', lienzo_tabla)
        if procesos[0][7] != 0 and (procesos[0][7] + procesos[0][3]) == self.counter - 1:
            self.nodo.atender_nodo(procesos[1])
            self.lienzo_gantt.append(procesos[1].copy())

            procesos[0][2] = procesos[0][2] - procesos[0][7]
            procesos[0][1] = self.tiempo_llegada
            self.nodo.nuevo_nodo(Nodo('Proceso', procesos[0][0], procesos[0][1], procesos[0][2]))
            self.nodo.eliminar()

            self.tiempo_llegada += 1

            lienzo_tabla = self.nodo.get_lienzo_tabla()

            self.socketio.emit('data', self.lienzo_gantt)
            self.socketio.emit('data-table', lienzo_tabla)
        elif self.counter == procesos[0][4] + 1:
            self.nodo.atender_nodo(procesos[1])
            self.lienzo_gantt.append(procesos[1].copy())
            self.nodo.eliminar()

            lienzo_tabla = self.nodo.get_lienzo_tabla()

            self.socketio.emit('data', self.lienzo_gantt)
            self.socketio.emit('data-table', lienzo_tabla)
            
    def iniciar_ciclo(self):
        if not self.stop_thread:
            self.socketio.emit('cycle', self.counter)
            self.counter += 1
            time.sleep(1)
            self.atender_procesos()
            self.iniciar_ciclo()

    def run(self):
        self.socketio.run(self.app, port=8000, host="0.0.0.0", debug=True) #host="0.0.0.0" port=80
        eventlet.monkey_patch(socket=True, select=True)


