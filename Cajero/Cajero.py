from Nodo.Nodo import Nodo
from Registro.Registro import Registro

class Cajero(Nodo):
    def __init__(self, numero_clientes=0):
        super().__init__()
        self.numero_clientes = numero_clientes
        self.controller = None
        self.response = None
        self.turno = 0

    def set_controller(self, controller):
        '''
        Importamos todas las funciones de controller
        '''
        self.controller = controller

    def start_service(self, nodo):
        self.set_next(nodo)

    def new_client(self, nodo, new_nodo:Registro):
        '''
        Inicia un nuevo cliente
        Args:
            -new_nodo: Registro
        '''
        if type(nodo.get_next()) == Registro:
            self.new_client(nodo.get_next(), new_nodo)
        else:
            # Es cajero
            new_nodo.set_next(nodo.get_next()) # Apunta al nodo de manera circular
            nodo.set_next(new_nodo)
            self.numero_clientes += 1
            print(f'Agregando -> ID: {new_nodo.id}, Nombre: {new_nodo.nombre}')

    def get_all_clients(self, nodo):
        '''
        Método que recorre toda la lista circular
        Args:
            -nodo: Registro | Cajero
        '''
        # Verificar que nodo sea de tipo Cajero
        if isinstance(nodo, Cajero):
            print('Total de clientes: ', self.numero_clientes)
        elif isinstance(nodo, Registro):
            print(f'ID: {nodo.id}, Nombre: {nodo.nombre}')
            self.get_all_clients(nodo.get_next())
    
    def find_client(self, nodo, id):
        '''
        Método que busca un cliente
        Args:
            -id: str
        '''
        if isinstance(nodo, Registro):
            self.turno += 1
            if nodo.id == id:
                self.response = {
                    'id': nodo.id,
                    'nombre': nodo.nombre,
                    'transacciones': nodo.numero_transacciones,
                    'turno': self.turno
                }
            self.find_client(nodo.get_next(), id)
    
    def add_transaction(self, nodo, id):
        '''
        Método que añade una transacción a un cliente
        Args:
            -id: str
        '''
        if isinstance(nodo, Registro):
            self.turno += 1
            if nodo.id == id:
                nodo.numero_transacciones += 1
                self.response = {
                    'id': nodo.id,
                    'nombre': nodo.nombre,
                    'transacciones': nodo.numero_transacciones,
                    'turno': self.turno
                }
            self.add_transaction(nodo.get_next(), id)

    def atender_cliente(self, nodo, id):
        '''
        Método que atiende un cliente
        Args:
            -id: str
        '''
        if isinstance(nodo, Registro):
            self.turno += 1
            if nodo.id == id:
                if self.turno == 1:
                    if nodo.numero_transacciones == 0:
                        self.response = {
                            'message': 'El cliente no tiene transacciones pendientes',
                        }
                    if nodo.numero_transacciones > 0 and nodo.numero_transacciones <= 5:
                        nodo.numero_transacciones = 0
                        self.delete_client(nodo, id)
                        self.turno = 0
                        self.new_client(self.get_next(), nodo)
                        self.response = {
                            'message': 'Cliente atendido satisfactoriamente',
                        }
                    elif nodo.numero_transacciones > 5:
                        nodo.numero_transacciones -= 5
                        self.delete_client(nodo, id)
                        self.turno = 0
                        self.new_client(self.get_next(), nodo)
                        self.response = {
                            'message': 'Al cliente se le han restado 5 transacciones',
                        }
                else:
                    self.response = {
                        'message': 'El cliente no tiene el turno 1',
                    }
            self.atender_cliente(nodo.get_next(), id)

    def delete_client(self, nodo, id):
        '''
        Método que elimina un cliente
        Args:
            -id: str
        '''
        if isinstance(nodo, Registro):
            if isinstance(nodo.get_next(), Registro):
                if nodo.get_next().id == id:
                    print(f'Eliminando -> ID: {nodo.get_next().id}, Nombre: {nodo.get_next().nombre}')
                    nodo.set_next(nodo.get_next().get_next())
                    self.numero_clientes -= 1
            self.delete_client(nodo.get_next(), id)
        elif isinstance(nodo, Cajero):
            if isinstance(nodo.get_next(), Registro):
                if nodo.get_next().id == id:
                    print(f'Eliminando -> ID: {nodo.get_next().id}, Nombre: {nodo.get_next().nombre}')
                    nodo.set_next(nodo.get_next().get_next())
                    self.numero_clientes -= 1
    
    def set_turno(self, turno):
        '''
        Setea el turno
        '''
        self.turno = turno

    def get_response(self):
        '''
        Retorna la respuesta
        '''
        return self.response