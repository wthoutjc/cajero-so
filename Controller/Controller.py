'''
0: Welcome screen
1: Registrarse
2: Notificación
3: Iniciar sesión
'''
from tkinter import mainloop

# Components
from Controller.ButtonController import ButtonController

class Controller():
    def __init__(self, cajero):
        self.view = None
        self.status = 0
        self.cajero = cajero
        self.button_controller = ButtonController(self.get_status, self.get_view, self.cajero)

    def set_status(self, status: int):
        '''
        Cambia el estado del programa
        '''
        self.status = status
    
    def set_view(self, view):
        '''
        Importamos todas las funciones de view
        '''
        self.view = view
    
    def get_view(self):
        '''
        Retorna la vista
        '''
        return self.view

    def get_status(self):
        '''
        Retorna el estado del programa
        '''
        return self.status

    def function_button0(self):
        '''
        Función del boton 0
        '''
        self.button_controller.button0()

    def function_button1(self):
        '''
        Función del boton 1
        '''
        self.button_controller.button1()

    def function_button2(self):
        '''
        Función del boton 2
        '''
        self.button_controller.button2()

    def function_button3(self):
        '''
        Función del boton 3
        '''
        self.button_controller.button3()

    def function_button4(self):
        '''
        Función del boton 4
        '''
        self.button_controller.button4()

    def function_button5(self):
        '''
        Función del boton 5
        '''
        self.button_controller.button5()

    def start_service(self):
        '''
        Inicia el servicio
        '''
        print('Iniciando servicio...')
        self.cajero.start_service(self.cajero) # Comienza a apuntar a si mismo
        self.view.get_root()
        self.view.screen_welcome()
        mainloop()