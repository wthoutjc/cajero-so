from flask import Flask, jsonify, make_response, request

# Socket
from socketLC import SocketIOClient

# Herramientas
from decouple import config     # Variables de entorno

# Type Client
from Client.Client import Client

app = Flask(__name__)
app.config['SECRET_KEY'] = config('SECRET_KEY')

# Socket
socketio = SocketIOClient(app)

@app.route("/", methods=['POST'])
def atender_cliente():
    if request.method == 'POST':
        socketio.nodo.atender_cliente(socketio.nodo.get_next(), socketio.nodo)

        socketio.nodo.set_all_clients([])
        socketio.nodo.push_all_clients(socketio.nodo.get_next(), Client('Juan', 5))
        clientes = socketio.nodo.get_all_clients()

        socketio.socketio.emit('data', clientes)

        return make_response(jsonify({
            'message': socketio.nodo.response['message'],
            'ok': True
        }), 200)
    
# Conexión
if __name__ == '__main__':    
    socketio.run()