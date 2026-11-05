from persistencia import cargar_inventario, guardar_inventario
from tabulate import tabulate
from validaciones import (ingresar_codigo, ingresar_texto,
                          ingresar_decimal, ingresar_entero, ingresar_categoria)
from inventario import agregar_producto, buscar_por_codigo


def mostrar_menu():
    print()
    print("--- TIENDAPY ---")
    print("1. Ver inventario")
    print("2. Agregar producto")
    print("3. Consultar producto")
    print("4. Modificar producto")
    print("5. Eliminar producto")
    print("6. Nueva venta")
    print("7. Alertas de stock")
    print("8. Cierre del día")
    print("9. Guardar inventario")
    print("0. Salir")


def mostrar_inventario(inventario):
    if not inventario:
        print("El inventario está vacío.")
        return

    filas = []
    for producto in inventario.values():
        filas.append([
            producto["codigo"],
            producto["nombre"],
            producto["categoria"],
            producto["precio"],
            producto["stock"],
            producto["stock_minimo"],
            producto["proveedor"],
        ])

    encabezados = ["Código", "Nombre", "Categoría",
                   "Precio", "Stock", "Mínimo", "Proveedor"]
    print(tabulate(filas, headers=encabezados, tablefmt="grid"))


def menu_agregar_producto(inventario):
    print()
    print("--- Agregar producto ---")

    codigo = ingresar_codigo("Código: ")
    if buscar_por_codigo(inventario, codigo) is not None:
        print(f"Error: el código {codigo} ya existe.")
        return

    producto = {
        "codigo": codigo,
        "nombre": ingresar_texto("Nombre: "),
        "categoria": ingresar_categoria("Categoría: "),
        "precio": ingresar_decimal("Precio: "),
        "stock": ingresar_entero("Stock: "),
        "stock_minimo": ingresar_entero("Stock mínimo: "),
        "proveedor": ingresar_texto("Proveedor: "),
    }

    try:
        agregar_producto(inventario, producto)
        print("Producto agregado.")
    except ValueError as error:
        print("Error:", error)


def main():
    inventario = cargar_inventario()

    while True:
        mostrar_menu()
        opcion = input("Elige una opción: ").strip()

        if opcion == "0":
            guardar_inventario(inventario)
            print("Inventario guardado. ¡Hasta pronto!")
            break
        elif opcion == "1":
            mostrar_inventario(inventario)
        elif opcion == "2":
            menu_agregar_producto(inventario)
        elif opcion == "9":
            guardar_inventario(inventario)
            print("Inventario guardado.")
        elif opcion in ["3", "4", "5", "6", "7", "8"]:
            print("Esta opción todavía no está lista.")
        else:
            print("Error: opción no válida.")


if __name__ == "__main__":
    main()
