import typing

if typing.TYPE_CHECKING:
    from Client.Client import Client

class Nodo:
    def __init__(self):
        self.next = None
        self.socketio = None

        self.clientes = []

    def set_next(self, next):
        self.next = next

    def get_next(self):
        return self.next

    def start_service(self, nodo):
        self.set_next(nodo)

    def nuevo_nodo(self, nodo, new_nodo: 'Client'):
        '''
        Inicia un nuevo cliente
        Args:
            -new_nodo: Client
        '''
        print(type(nodo.get_next()))
        if type(nodo.get_next()) == type(new_nodo):
            self.nuevo_nodo(nodo.get_next(), new_nodo)
        else:
            # Es cajero
            new_nodo.set_next(nodo.get_next()) # Apunta al nodo de manera circular
            nodo.set_next(new_nodo)
            print(f'Agregando -> Nombre: {new_nodo.nombre}; Número de transacciones: {new_nodo.numero_transacciones}')

    def atender_cliente(self, nodo, nodo_inicial):
        '''
        Método que atiende un cliente
        Args:
            -id: str
        '''
        if nodo.numero_transacciones == 0:
            self.response = {
                'message': f'El cliente {nodo.nombre} no tiene transacciones pendientes',
            }
        elif nodo.numero_transacciones > 0 and nodo.numero_transacciones <= 5:
            self.delete_client(nodo, nodo_inicial)
            self.response = {
                'message': f'El cliente {nodo.nombre} ha sido atendido satisfactoriamente',
            }
        elif nodo.numero_transacciones > 5:
            nodo.numero_transacciones -= 5
            self.delete_client(nodo, nodo_inicial)
            self.nuevo_nodo(self.get_next(), nodo)
            self.response = {
                'message': f'Al cliente {nodo.nombre} se le han restado 5 transacciones',
            }
        else:
            self.response = {
                'message': 'El cliente no existe',
            }

    def delete_client(self, nodo, nodo_inicial):
        '''
        Método que elimina un cliente
        Args:
            -id: str
        '''
        print(f'Eliminando -> Nombre: {nodo.nombre}; Número de transacciones: {nodo.numero_transacciones}')
        nodo_inicial.set_next(nodo.get_next())
    
    def push_all_clients(self, nodo, type_client):
        '''
        Retorna todos los clientes
        '''
        if type(nodo) == type(type_client):
            self.clientes.append([nodo.nombre, nodo.numero_transacciones])
            self.push_all_clients(nodo.get_next(), type_client)
    
    def set_all_clients(self, clientes):
        '''
        Setea todos los clientes
        '''
        self.clientes = clientes

    def get_all_clients(self):
        '''
        Retorna todos los clientes
        '''
        return self.clientes

    def get_response(self):
        '''
        Retorna la respuesta
        '''
        return self.response