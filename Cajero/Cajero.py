from Nodo.Nodo import Nodo
from Registro.Registro import Registro

class Cajero(Nodo):
    def __init__(self, numero_transacciones=0):
        super().__init__()
        self.numero_transacciones = numero_transacciones

    def start_service(self, nodo):
        self.set_next(nodo)

    def new_transaction(self, next):
        print(type(self.next))
        if type(self.next) is Registro:
            self.next.set_next(next)
        self.set_next(next)
        self.numero_transacciones += 1
        print('Transacción exitosa')

    def get_all_transactions(self):
        for i in range(self.numero_transacciones):
            if type(self.next) is Registro:
                print(self.next.get_next())

    def __str__(self):
        return str(self.data)