from Nodo.Nodo import Nodo
from Registro.Registro import Registro

class Cajero(Nodo):
    def __init__(self, numero_transacciones=0):
        super().__init__()
        self.numero_transacciones = numero_transacciones
        self.cab = None

    def start_service(self, nodo):
        self.set_next(nodo)

    def new_transaction(self, next:Registro):
        next.set_next(self.next) # Apunta al nodo de manera circular
        self.set_next(next)
        self.numero_transacciones += 1
        print('Transacción exitosa')

    def get_all_transactions(self):
        '''
        Método que recorre toda la lista circular
        '''
        self.cab = self.get_next()
        if type(self.cab) is Registro:
            print(self.cab.nombre, self.cab.id)
            self.cab = self.cab.get_next()
            self.get_all_transactions()