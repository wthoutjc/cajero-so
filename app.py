from Cajero.Cajero import Cajero
from Registro.Registro import Registro

cajero = Cajero()

if __name__ == '__main__':
    # Comienza a apuntar a si mismo
    cajero.start_service(cajero)
    while True:
        print("""
        Menú:
            1. Insertar un nuevo registro
            2. Consultar todos los registros
            3. Consultar registro
            4. Eliminar registro
            5. Salir
        """)
        option = input("Opción: ")
        if option == "1":
            print('Insertar un nuevo registro')

            nombre = input("Ingrese nombre: ")
            id = input("Ingrese id: ")

            nuevo_registro = Registro(id, nombre)
            cajero.new_transaction(nuevo_registro)
        elif option == "2":
            print('Consultar todos los registros')
            cajero.get_all_transactions()
        elif option == "3":
            print('Consultar registro')
        elif option == "4":
            print('Eliminar registro')
        elif option == "5":
            print('Salir')
            break
        else:
            print('Opción no válida')
