from flask_socketio import SocketIO
from flask_cors import CORS

# Herramientas
import logging
import eventlet
import time
import datetime

# Cajero
from Nodo.Nodo import Nodo
from Client.Client import Client

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
        self.nodo = Nodo()
        self.app = app
        print('Iniciando servicio..')
        self.nodo.start_service(self.nodo)
        CORS(self.app)

        self.socketio = SocketIO(app, cors_allowed_origins='*', async_mode="threading")

        @self.socketio.on('connect')
        def on_connect():
            self.thread_client = Thread(target=self.generate_client)
            self.thread_client.start()
        
        @self.socketio.on('disconnect')
        def on_disconnect():
            self.thread_client = None
    
    def generate_client(self):
        self.nodo.set_all_clients([])

        self.nodo.nuevo_nodo(self.nodo.get_next(), Client(fake.name(), fake.random_int(1, 10)))
        self.nodo.push_all_clients(self.nodo.get_next(), Client('Juan', 5))
        clientes = self.nodo.get_all_clients()

        print(clientes)

        self.socketio.emit('data', clientes)
        time.sleep(10)
        self.generate_client()

    def run(self):
        self.socketio.run(self.app, port=8000, host="0.0.0.0", debug=True) #host="0.0.0.0" port=80
        eventlet.monkey_patch(socket=True, select=True)


