from flask import Flask, jsonify, make_response, request

# Socket
from socketLC import SocketIOClient

# Herramientas
from decouple import config     # Variables de entorno

app = Flask(__name__)
app.config['SECRET_KEY'] = config('SECRET_KEY')

# Socket
socketio = SocketIOClient(app)
    
# Conexión
if __name__ == '__main__':    
    socketio.run()