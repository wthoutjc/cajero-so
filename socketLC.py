from flask_socketio import SocketIO
from flask_cors import CORS

# Hilos
from threading import Thread

# Herramientas
import logging
import datetime
import eventlet

from random import seed
from random import random

seed(datetime.datetime.now())

# LOGS
logging.basicConfig(filename='client.log', level=logging.DEBUG)

class SocketIOClient(object):
    def __init__(self, app):
        self.app = app
        CORS(self.app)
        self.socketio = SocketIO(app, cors_allowed_origins='*', async_mode="threading")
        self.connected_clients = {}

        @self.socketio.on('connect')
        def on_connect():
            # global thread
            print(f'Cliente ff conectado satisfactoriamente')

            # if not thread.is_alive():
            #     thread = RandomThread()
            #     thread.start()
        
        @self.socketio.on('disconnect')
        def on_disconnect():
            print(f'Cliente ff desconectado satisfactoriamente.')
        
    def run(self):
        self.socketio.run(self.app, port=8000, host="0.0.0.0", debug=True) #host="0.0.0.0" port=80
        eventlet.monkey_patch(socket=True, select=True)


