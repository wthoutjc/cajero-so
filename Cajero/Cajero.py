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
        '''
        Inicia una nueva transacción
        Args:
            -next: Registro
        '''
        next.set_next(self.next) # Apunta al nodo de manera circular
        self.set_next(next)
        self.numero_transacciones += 1
        print('Transacción exitosa')

    def get_all_transactions(self, nodo):
        '''
        Método que recorre toda la lista circular
        Args:
            -nodo: Registro | Cajero
        '''
        # Verificar que nodo sea de tipo Cajero
        if isinstance(nodo, Cajero):
            print('Total de transacciones: ', self.numero_transacciones)
        elif isinstance(nodo, Registro):
            print(f'ID: {nodo.id}, Nombre: {nodo.nombre}')
            self.get_all_transactions(nodo.get_next())
    
    def find_transaction(self, nodo, id):
        '''
        Método que busca una transacción
        Args:
            -id: str
        '''
        if isinstance(nodo, Registro):
            if nodo.id == id:
                print(f'ID: {nodo.id}, Nombre: {nodo.nombre}')
            self.find_transaction(nodo.get_next(), id)
    
    def delete_transaction(self, nodo, id):
        '''
        Método que elimina una transacción
        Args:
            -id: str
        '''
        if isinstance(nodo, Registro):
            if isinstance(nodo.get_next(), Registro):
                if nodo.get_next().id == id:
                    print(f'Eliminando -> ID: {nodo.get_next().id}, Nombre: {nodo.get_next().nombre}')
                    nodo.set_next(nodo.get_next().get_next())
                    self.numero_transacciones -= 1
            self.delete_transaction(nodo.get_next(), id)