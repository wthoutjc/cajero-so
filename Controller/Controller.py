from tkinter import mainloop

# Components
from Cajero.Cajero import Cajero
from Controller.ButtonController import ButtonController

class Controller():
    def __init__(self):
        self.view = None
        self.status = 0
        self.cajero = Cajero()
        self.button_controller = ButtonController(self.get_status)

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
        self.cajero.start_service(self.cajero) # Comienza a apuntar a si mismo
        self.view.get_root()
        self.view.screen_login()
        mainloop()