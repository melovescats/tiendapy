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


if __name__ == "__main__":
    print(calcular_totales(14200.0))
    print(calcular_totales(60000.0))
    print(calcular_totales(120000.0))

    print(calcular_cambio(57000.0, 60000.0))
    print(calcular_cambio(57000.0, 57000.0))
    try:
        calcular_cambio(57000.0, 50000.0)
    except ValueError as error:
        print("Error:", error)
