import typing

if typing.TYPE_CHECKING:
    from Client.Client import Client

class Nodo:
    def __init__(self, numero_clientes = 0):
        self.next = None
        self.socketio = None
        self.numero_clientes = numero_clientes
        self.response = None

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
            self.numero_clientes += 1
            print(f'Agregando -> Nombre: {new_nodo.nombre}; Número de transacciones: {new_nodo.numero_transacciones}')

    def atender_cliente(self, nodo):
        '''
        Método que atiende un cliente
        Args:
            -id: str
        '''
        if nodo.numero_transacciones == 0:
            self.response = {
                'message': 'El cliente no tiene transacciones pendientes',
            }
        if nodo.numero_transacciones > 0 and nodo.numero_transacciones <= 5:
            nodo.numero_transacciones = 0
            self.delete_client(nodo, id)
            self.response = {
                'message': 'Cliente atendido satisfactoriamente',
            }
        elif nodo.numero_transacciones > 5:
            nodo.numero_transacciones -= 5
            self.delete_client(nodo, id)
            self.nuevo_nodo(self.get_next(), nodo)
            self.response = {
                'message': 'Al cliente se le han restado 5 transacciones',
            }

    def delete_client(self, nodo):
        '''
        Método que elimina un cliente
        Args:
            -id: str
        '''
        print(f'Eliminando -> ID: {nodo.get_next().id}, Nombre: {nodo.get_next().nombre}')
        nodo.set_next(nodo.get_next().get_next())
        self.numero_clientes -= 1   
    
    def push_all_clients(self, nodo, type_client):
        '''
        Retorna todos los clientes
        '''
        if type(nodo.get_next()) == type(type_client):
            self.clientes.append([nodo.get_next().nombre, nodo.get_next().numero_transacciones])
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

    def get_numero_clientes(self):
        '''
        Retorna el número de clientes
        '''
        return self.numero_clientes

    def get_response(self):
        '''
        Retorna la respuesta
        '''
        return self.response