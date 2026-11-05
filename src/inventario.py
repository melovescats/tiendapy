def agregar_producto(inventario, producto):
    if producto["codigo"] in inventario:
        raise ValueError(f"el código {producto['codigo']} ya existe")
    inventario[producto["codigo"]] = producto


if __name__ == "__main__":
    inventario = {}
    nuevo = {
        "codigo": "TST001",
        "nombre": "Producto de prueba",
        "categoria": "Aseo",
        "precio": 1000.0,
        "stock": 5,
        "stock_minimo": 2,
        "proveedor": "Proveedor X",
    }
    agregar_producto(inventario, nuevo)
    print("Productos:", len(inventario))
    try:
        agregar_producto(inventario, nuevo)
    except ValueError as error:
        print("Error:", error)
