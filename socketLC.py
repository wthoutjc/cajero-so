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
        self.tiempo_llegada = 0
        self.counter = 0

        self.stop_thread = False

        self.nodo = Nodo('Inicial')
        print('Iniciando servicio')
        self.nodo.iniciar_servicio(self.nodo)

        self.socketio = SocketIO(app, cors_allowed_origins='*', async_mode="threading")

        @self.socketio.on('connect')
        def on_connect():
            self.thread_crear_procesos = Thread(target=self.crear_procesos)
            self.thread_crear_procesos.start()
            self.socketio.emit('cycle', 0)
        
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
        
        @self.socketio.on('unblocked')
        def on_stop(data):
            self.nodo.eliminar(self.nodo.get_next(), self.nodo)
            self.nodo.set_all_process([])

            self.nodo.iterar_procesos(self.nodo.get_next())
            procesos = self.nodo.get_all_process()

            self.socketio.emit('data', procesos)
            self.socketio.emit('unblocked', {"ok": True, "message": 'Proceso desbloqueado satisfactoriamente'})
            self.stop_thread = False

    def crear_procesos(self):
        self.nodo.set_all_process([])

        nuevo_nodo = Nodo('Proceso', self.tiempo_llegada, fake.random_int(2, 10))
        self.nodo.nuevo_nodo(self.nodo.get_next(), nuevo_nodo)

        self.tiempo_llegada += 1

        self.nodo.iterar_procesos(self.nodo.get_next())
        procesos = self.nodo.get_all_process()

        self.socketio.emit('data', procesos)
        time.sleep(20)
        self.crear_procesos()
    
    def atender_procesos(self):
        if self.nodo.get_next().type == 'Inicial':
            self.stop_thread = True
            self.counter = 0
            self.socketio.emit('cycle', self.counter)
        elif self.counter == self.nodo.get_next().tiempo_final + 1:
            if self.nodo.get_next().density >= 5:
                self.stop_thread = True
                self.socketio.emit('blocked', True)
            else:
                self.nodo.eliminar(self.nodo.get_next(), self.nodo)
                self.nodo.set_all_process([])
                self.nodo.iterar_procesos(self.nodo.get_next())
                procesos = self.nodo.get_all_process()

                self.socketio.emit('data', procesos)
    
    def iniciar_ciclo(self):
        if not self.stop_thread:
            self.socketio.emit('cycle', self.counter)
            self.counter += 1
            self.atender_procesos()
            time.sleep(1)
            self.iniciar_ciclo()

    def run(self):
        self.socketio.run(self.app, port=8000, host="0.0.0.0", debug=True) #host="0.0.0.0" port=80
        eventlet.monkey_patch(socket=True, select=True)


