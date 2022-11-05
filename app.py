from flask import Flask, request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from Cajero.Cajero import Cajero

# Socket
from socketLC import SocketIOClient

# Herramientas
import json                     # Estructura json
import datetime                 # Manejo de fechas
from decouple import config     # Variables de entorno
from decimal import Decimal

app = Flask(__name__)

app.config['SECRET_KEY'] = config('SECRET_KEY')

# DB
cajero = Cajero()
socketio = SocketIOClient(app)

class DecimalEncoder(json.JSONEncoder):
  def default(self, obj):
    if isinstance(obj, Decimal):
      return float(obj)
    return json.JSONEncoder.default(self, obj)

@app.route("/")
def hello_world():
    return make_response(jsonify({"res": 'Connected'}), 200)

# Conexión
if __name__ == '__main__':
    socketio.run()