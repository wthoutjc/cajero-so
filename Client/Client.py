from Nodo.Nodo import Nodo

class Client(Nodo):
    def __init__(self, nombre, numero_transacciones=0):
        super().__init__()
        self.nombre = nombre
        self.numero_transacciones = numero_transacciones