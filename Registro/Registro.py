from Nodo.Nodo import Nodo

class Registro(Nodo):
    def __init__(self, id, nombre, numero_transacciones=0):
        super().__init__()
        self.id = id
        self.nombre = nombre
        self.numero_transacciones = numero_transacciones