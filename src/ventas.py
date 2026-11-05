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


if __name__ == "__main__":
    from persistencia import cargar_inventario

    inventario = cargar_inventario()
    carrito = {}

    agregar_al_carrito(inventario, carrito, "LAC001", 2)
    agregar_al_carrito(inventario, carrito, "LAC001", 3)
    print(carrito)

    pruebas = [("LAC002", 4), ("BEB002", 1), ("XXX999", 1),
               ("LAC001", 0), ("LAC001", 31)]
    for codigo, cantidad in pruebas:
        try:
            agregar_al_carrito(inventario, carrito, codigo, cantidad)
        except ValueError as error:
            print("Error:", error)

    print(carrito)
