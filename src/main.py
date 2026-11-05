from persistencia import cargar_inventario, guardar_inventario
from tabulate import tabulate
from validaciones import (ingresar_codigo, ingresar_texto,
                          ingresar_decimal, ingresar_entero, ingresar_categoria)
from inventario import (agregar_producto, buscar_por_codigo,
                        buscar_por_categoria, modificar_precio, modificar_stock)


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


def mostrar_tabla(productos):
    filas = []
    for producto in productos:
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


def mostrar_inventario(inventario):
    if not inventario:
        print("El inventario está vacío.")
        return
    mostrar_tabla(inventario.values())


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


def menu_consultar_producto(inventario):
    print()
    print("--- Consultar producto ---")
    print("1. Por código")
    print("2. Por categoría")
    opcion = input("Elige una opción: ").strip()

    if opcion == "1":
        codigo = ingresar_codigo("Código: ")
        producto = buscar_por_codigo(inventario, codigo)
        if producto is None:
            print(f"No existe ningún producto con el código {codigo}.")
        else:
            mostrar_tabla([producto])
    elif opcion == "2":
        categoria = ingresar_categoria("Categoría: ")
        encontrados = buscar_por_categoria(inventario, categoria)
        if not encontrados:
            print(f"No hay productos en la categoría {categoria}.")
        else:
            mostrar_tabla(encontrados)
    else:
        print("Error: opción no válida.")


def menu_modificar_producto(inventario):
    print()
    print("--- Modificar producto ---")

    codigo = ingresar_codigo("Código: ")
    producto = buscar_por_codigo(inventario, codigo)
    if producto is None:
        print(f"No existe ningún producto con el código {codigo}.")
        return

    mostrar_tabla([producto])
    print("1. Modificar precio")
    print("2. Modificar stock")
    opcion = input("Elige una opción: ").strip()

    try:
        if opcion == "1":
            nuevo_precio = ingresar_decimal("Nuevo precio: ")
            modificar_precio(inventario, codigo, nuevo_precio)
            print("Precio actualizado.")
        elif opcion == "2":
            nuevo_stock = ingresar_entero("Nuevo stock: ")
            modificar_stock(inventario, codigo, nuevo_stock)
            print("Stock actualizado.")
        else:
            print("Error: opción no válida.")
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
        elif opcion == "3":
            menu_consultar_producto(inventario)
        elif opcion == "4":
            menu_modificar_producto(inventario)
        elif opcion == "9":
            guardar_inventario(inventario)
            print("Inventario guardado.")
        elif opcion in ["5", "6", "7", "8"]:
            print("Esta opción todavía no está lista.")
        else:
            print("Error: opción no válida.")


if __name__ == "__main__":
    main()
