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


if __name__ == "__main__":
    from persistencia import cargar_inventario

    inventario = cargar_inventario()
    carrito = {"LAC001": 2, "BEB001": 1}
    print(calcular_subtotal(inventario, carrito))

    for valor in [49999, 50000, 99999, 100000]:
        print(valor, calcular_porcentaje_descuento(valor))
