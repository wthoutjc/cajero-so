'''
Por:
    - Juan Camilo Ramírez Rátiva - 20181020089
    - Gabriel David Hernández Vargas - 20181020059

Universidad Distrital Francisco José de Caldas
Sistemas Operativos
'''

from View.View import View
from Controller.Controller import Controller
from Cajero.Cajero import Cajero

if __name__ == '__main__':
    cajero = Cajero()
    
    controller = Controller(cajero)
    cajero.set_controller(controller)

    view = View('Cajero', controller)
    controller.set_view(view)
    controller.start_service()