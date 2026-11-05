def calcular_subtotal(inventario, carrito):
    subtotal = 0
    for codigo, cantidad in carrito.items():
        subtotal += inventario[codigo]["precio"] * cantidad
    return subtotal


def calcular_porcentaje_descuento(subtotal):
    if subtotal >= 100000:
        return 0.10
    if subtotal >= 50000:
        return 0.05
    return 0.0


def agregar_al_carrito(inventario, carrito, codigo, cantidad):
    if codigo not in inventario:
        raise ValueError(f"el código {codigo} no existe")
    if cantidad <= 0:
        raise ValueError("la cantidad debe ser mayor que cero")

    producto = inventario[codigo]
    disponible = producto["stock"] - carrito.get(codigo, 0)
    if cantidad > disponible:
        raise ValueError(
            f"stock insuficiente de {producto['nombre']} ({disponible} disponibles)")

    carrito[codigo] = carrito.get(codigo, 0) + cantidad


def calcular_totales(subtotal):
    porcentaje = calcular_porcentaje_descuento(subtotal)
    descuento = round(subtotal * porcentaje, 2)
    total = round(subtotal - descuento, 2)
    return descuento, total


def calcular_cambio(total, pago):
    if pago < total:
        raise ValueError(
            f"el pago es insuficiente (faltan {round(total - pago, 2)})")
    return round(pago - total, 2)


def confirmar_venta(inventario, carrito):
    if not carrito:
        raise ValueError("el carrito está vacío")

    for codigo, cantidad in carrito.items():
        if codigo not in inventario:
            raise ValueError(f"el código {codigo} no existe")
        if cantidad > inventario[codigo]["stock"]:
            raise ValueError(
                f"stock insuficiente de {inventario[codigo]['nombre']}")

    for codigo, cantidad in carrito.items():
        inventario[codigo]["stock"] -= cantidad


if __name__ == "__main__":
    inventario = {
        "TST001": {"codigo": "TST001", "nombre": "Producto uno", "stock": 5},
        "TST002": {"codigo": "TST002", "nombre": "Producto dos", "stock": 3},
    }

    confirmar_venta(inventario, {"TST001": 2, "TST002": 3})
    print(inventario["TST001"]["stock"], inventario["TST002"]["stock"])

    try:
        confirmar_venta(inventario, {})
    except ValueError as error:
        print("Error:", error)

    try:
        confirmar_venta(inventario, {"TST001": 1, "TST002": 1})
    except ValueError as error:
        print("Error:", error)
    print(inventario["TST001"]["stock"], inventario["TST002"]["stock"])
