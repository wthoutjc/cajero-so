from flask import Flask, jsonify, make_response

# Socket
from socketLC import SocketIOClient

# Herramientas
from decouple import config     # Variables de entorno

app = Flask(__name__)
app.config['SECRET_KEY'] = config('SECRET_KEY')

# Socket
socketio = SocketIOClient(app)

@app.route("/")
def hello_world():
    return make_response(jsonify({"res": 'Connected'}), 200)

# Conexión
if __name__ == '__main__':
    socketio.run()