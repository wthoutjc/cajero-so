from Nodo.Nodo import Nodo

class Registro(Nodo):
    def __init__(self, id, nombre):
        super().__init__()
        self.id = id
        self.nombre = nombre