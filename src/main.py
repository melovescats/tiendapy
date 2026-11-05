from datetime import date
from persistencia import (cargar_inventario, guardar_inventario,
                          registrar_venta, cargar_ventas)
from tabulate import tabulate
from validaciones import (ingresar_codigo, ingresar_texto, ingresar_decimal,
                          ingresar_entero, ingresar_categoria, confirmar)
from inventario import (agregar_producto, buscar_por_codigo, buscar_por_categoria,
                        modificar_precio, modificar_stock, eliminar_producto)
from ventas import (agregar_al_carrito, calcular_subtotal, calcular_totales,
                    calcular_cambio, confirmar_venta)
from reportes import (productos_en_alerta, esta_agotado, ventas_del_dia,
                      calcular_resumen, contar_unidades_vendidas,
                      producto_mas_vendido, productos_sin_ventas,
                      categorias_con_movimiento)


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


def menu_eliminar_producto(inventario):
    print()
    print("--- Eliminar producto ---")

    codigo = ingresar_codigo("Código: ")
    producto = buscar_por_codigo(inventario, codigo)
    if producto is None:
        print(f"No existe ningún producto con el código {codigo}.")
        return

    mostrar_tabla([producto])
    if not confirmar("¿Seguro que quieres eliminar este producto?"):
        print("Eliminación cancelada.")
        return

    try:
        eliminar_producto(inventario, codigo)
        print("Producto eliminado.")
    except ValueError as error:
        print("Error:", error)


def armar_carrito(inventario):
    carrito = {}
    print("Agrega productos al carrito. Deja el código vacío para terminar.")

    while True:
        codigo = input("Código: ").strip().upper()
        if codigo == "":
            break

        producto = buscar_por_codigo(inventario, codigo)
        if producto is None:
            print(f"No existe ningún producto con el código {codigo}.")
            continue

        cantidad = ingresar_entero(f"Cantidad de {producto['nombre']}: ")
        try:
            agregar_al_carrito(inventario, carrito, codigo, cantidad)
            print("Agregado al carrito.")
        except ValueError as error:
            print("Error:", error)

    return carrito


def mostrar_detalle_venta(inventario, carrito):
    filas = []
    for codigo, cantidad in carrito.items():
        producto = inventario[codigo]
        valor = producto["precio"] * cantidad
        filas.append([producto["nombre"], cantidad, producto["precio"], valor])

    encabezados = ["Producto", "Cantidad", "Precio", "Valor"]
    print(tabulate(filas, headers=encabezados, tablefmt="grid"))

    subtotal = calcular_subtotal(inventario, carrito)
    descuento, total = calcular_totales(subtotal)
    print("Subtotal:", subtotal)
    print("Descuento:", descuento)
    print("TOTAL A PAGAR:", total)
    return total


def pedir_pago(total):
    while True:
        pago = ingresar_decimal("Pago recibido: ")
        try:
            return calcular_cambio(total, pago)
        except ValueError as error:
            print("Error:", error)
            if not confirmar("¿Intentar de nuevo?"):
                return None


def menu_nueva_venta(inventario):
    print()
    print("--- Nueva venta ---")

    carrito = armar_carrito(inventario)
    if not carrito:
        print("El carrito está vacío. Venta cancelada.")
        return

    total = mostrar_detalle_venta(inventario, carrito)

    cambio = pedir_pago(total)
    if cambio is None:
        print("Venta cancelada. El inventario no cambió.")
        return

    try:
        confirmar_venta(inventario, carrito)
    except ValueError as error:
        print("Error:", error)
        print("Venta cancelada. El inventario no cambió.")
        return

    guardar_inventario(inventario)
    registrar_venta(str(date.today()), total, carrito)
    print("Venta registrada.")
    print("Cambio:", cambio)


def menu_alertas(inventario):
    print()
    print("--- Alertas de stock ---")

    alertas = productos_en_alerta(inventario)
    if not alertas:
        print("No hay productos en alerta. Todo el stock está por encima del mínimo.")
        return

    for proveedor, productos in alertas.items():
        print()
        print("Proveedor:", proveedor)
        filas = []
        for producto in productos:
            if esta_agotado(producto):
                estado = "AGOTADO"
            else:
                estado = "Stock bajo"
            filas.append([producto["codigo"], producto["nombre"],
                          producto["stock"], producto["stock_minimo"], estado])

        encabezados = ["Código", "Nombre", "Stock", "Mínimo", "Estado"]
        print(tabulate(filas, headers=encabezados, tablefmt="grid"))


def menu_cierre_dia(inventario):
    print()
    print("--- Cierre del día ---")

    fecha = str(date.today())
    ventas_dia = ventas_del_dia(cargar_ventas(), fecha)
    total, numero, ticket_promedio = calcular_resumen(ventas_dia)
    conteo = contar_unidades_vendidas(ventas_dia)

    print("Fecha:", fecha)
    print("Total vendido:", total)
    print("Número de ventas:", numero)
    print("Ticket promedio:", ticket_promedio)

    mas_vendido = producto_mas_vendido(conteo)
    if mas_vendido is None:
        print("Producto más vendido: ninguno")
    else:
        codigo, unidades = mas_vendido
        producto = buscar_por_codigo(inventario, codigo)
        if producto is None:
            nombre = codigo
        else:
            nombre = producto["nombre"]
        print(f"Producto más vendido: {nombre} ({unidades} unidades)")

    categorias = categorias_con_movimiento(inventario, conteo)
    if categorias:
        print("Categorías con movimiento:", ", ".join(categorias))
    else:
        print("Categorías con movimiento: ninguna")

    sin_ventas = productos_sin_ventas(inventario, conteo)
    print()
    if sin_ventas:
        print("Productos sin ventas hoy:")
        filas = []
        for producto in sin_ventas:
            filas.append(
                [producto["codigo"], producto["nombre"], producto["stock"]])
        print(tabulate(filas, headers=[
              "Código", "Nombre", "Stock"], tablefmt="grid"))
    else:
        print("Todos los productos tuvieron ventas hoy.")


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
        elif opcion == "5":
            menu_eliminar_producto(inventario)
        elif opcion == "6":
            menu_nueva_venta(inventario)
        elif opcion == "7":
            menu_alertas(inventario)
        elif opcion == "8":
            menu_cierre_dia(inventario)
        elif opcion == "9":
            guardar_inventario(inventario)
            print("Inventario guardado.")
        else:
            print("Error: opción no válida.")


if __name__ == "__main__":
    main()
