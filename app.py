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
            print('Insertar un nuevo transacción')

            id = input("Ingrese id: ")
            nombre = input("Ingrese nombre: ")

            nuevo_registro = Registro(id, nombre)
            cajero.new_transaction(nuevo_registro)
        elif option == "2":
            print('Consultar todas las transacciones')
            cajero.get_all_transactions()
        elif option == "3":
            print('Consultar transacción')
        elif option == "4":
            print('Eliminar transacción')
        elif option == "5":
            print('Salir')
            break
        else:
            print('Opción no válida')
