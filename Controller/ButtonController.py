from Registro.Registro import Registro

class ButtonController():
    def __init__(self, get_status, get_view, cajero):
        self.get_status = get_status
        self.get_view = get_view
        self.cajero = cajero

    def button0(self):
        if self.get_status() == 0:
            self.get_view().screen_login()
        elif self.get_status() == 1:
            self.get_view().screen_welcome()
        elif self.get_status() == 3:
            self.get_view().screen_welcome()
        elif self.get_status() == 4:
            '''
            Añadir transacción
            '''
            id = self.get_view().get_login_id()
            self.cajero.add_transaction(self.cajero.get_next(), id)
            self.cajero.set_turno(0)
            new_user = self.cajero.get_response()
            self.get_view().screen_davivienda(
                    new_user['nombre'],
                    new_user['id'],
                    new_user['transacciones'],
                    new_user['turno'],
                    )
        else:
            print(self.get_status())

    def button1(self):
        if self.get_status() == 0:
            self.get_view().screen_register()
        elif self.get_status() == 1:
            '''
            Inicia proceso de registro
            '''
            name = self.get_view().get_register_name() 
            id = self.get_view().get_register_id()
            
            if name and id:
                self.cajero.find_client(self.cajero.get_next(), id)
                client = self.cajero.get_response()
                self.cajero.set_turno(0)
                try:
                    nombre = client['nombre']
                except KeyError:
                    nombre = None
                except TypeError:
                    nombre = None

                if nombre == None:
                    registro = Registro(id, name)
                    self.cajero.new_client(
                            self.cajero.get_next(), 
                            registro
                        )
                    self.get_view().screen_notification('Cliente agregado satisfactoriamente')
                else:
                    self.get_view().screen_notification('Usuario ya registrado')
            else:
                self.get_view().screen_notification('Los datos no son válidos')
        elif self.get_status() == 2:
            self.get_view().screen_welcome()
        elif self.get_status() == 3:
            id = self.get_view().get_login_id()

            self.cajero.find_client(self.cajero.get_next(), id)
            user = self.cajero.get_response()
            try:
                nombre = user['nombre']
            except KeyError:
                nombre = None
            except TypeError:
                nombre = None
            if user and nombre:
                self.get_view().screen_davivienda(
                    user['nombre'],
                    user['id'],
                    user['transacciones'],
                    user['turno'],
                    )
                self.cajero.set_turno(0)
            else:
                self.get_view().screen_notification('El usuario no existe')
        elif self.get_status() == 4:
            id = self.get_view().get_login_id()

            # Operación
            self.cajero.atender_cliente(self.cajero.get_next(), id)
            result= self.cajero.get_response()
            self.cajero.set_turno(0)
            self.get_view().screen_notification(result['message'])
        elif self.get_status() == 5:
            id = self.get_view().get_login_id()

            self.cajero.find_client(self.cajero.get_next(), id)
            user = self.cajero.get_response()
            if user:
                self.get_view().screen_davivienda(
                    user['nombre'],
                    user['id'],
                    user['transacciones'],
                    user['turno'],
                    )
                self.cajero.set_turno(0)
            else:
                self.get_view().screen_notification('El usuario no existe')
        else:
            print(self.get_status())

    def button2(self):
        pass

    def button3(self):
        if self.get_status() == 4:
            '''
            Cerrar sesión
            '''
            self.get_view().screen_welcome()
        else:
            print(self.get_status())

    def button4(self):
        pass

    def button5(self):
        pass