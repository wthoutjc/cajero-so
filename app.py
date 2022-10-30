'''
Por:
    - Juan Camilo Ramírez Rátiva - 20181020089
    - Gabriel David Hernández Vargas - 20181020059

Universidad Distrital Francisco José de Caldas
Sistemas Operativos
'''

from Cajero.Cajero import Cajero
from Registro.Registro import Registro

cajero = Cajero()

if __name__ == '__main__':
    # Comienza a apuntar a si mismo
    cajero.start_service(cajero)

    while True:
        print("""
        Menú:
            1. Insertar una nueva transacción
            2. Consultar todas las transacciones
            3. Consultar transacción
            4. Eliminar transacción
            5. Salir
        """)

        option = input("Opción: ")

        if option == "1":
            print('Insertar una nueva transacción')

            id = input("Ingrese id: ")
            nombre = input("Ingrese nombre: ")

            nuevo_registro = Registro(id, nombre)
            cajero.new_transaction(nuevo_registro)
        elif option == "2":
            print('Todas las transacciones')
            cajero.get_all_transactions(cajero.get_next())
        elif option == "3":
            print('Consultar transacción')
            id = input("Ingrese id: ")
            cajero.find_transaction(cajero.get_next(), id)
        elif option == "4":
            print('Eliminar transacción')
            id = input("Ingrese id: ")
            cajero.delete_transaction(cajero.get_next(), id)
        elif option == "5":
            print('Salir')
            break
        else:
            print('Opción no válida')
