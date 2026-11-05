def agregar_producto(inventario, producto):
    if producto["codigo"] in inventario:
        raise ValueError(f"el código {producto['codigo']} ya existe")
    inventario[producto["codigo"]] = producto


def buscar_por_codigo(inventario, codigo):
    return inventario.get(codigo)


def buscar_por_categoria(inventario, categoria):
    encontrados = []
    for producto in inventario.values():
        if producto["categoria"] == categoria:
            encontrados.append(producto)
    return encontrados


def modificar_precio(inventario, codigo, nuevo_precio):
    if codigo not in inventario:
        raise ValueError(f"el código {codigo} no existe")
    if nuevo_precio <= 0:
        raise ValueError("el precio debe ser mayor que cero")
    inventario[codigo]["precio"] = nuevo_precio


def modificar_stock(inventario, codigo, nuevo_stock):
    if codigo not in inventario:
        raise ValueError(f"el código {codigo} no existe")
    if nuevo_stock < 0:
        raise ValueError("el stock no puede ser negativo")
    inventario[codigo]["stock"] = nuevo_stock


def eliminar_producto(inventario, codigo):
    if codigo not in inventario:
        raise ValueError(f"el código {codigo} no existe")
    del inventario[codigo]


if __name__ == "__main__":
    inventario = {
        "TST001": {
            "codigo": "TST001",
            "nombre": "Producto de prueba",
            "categoria": "Aseo",
            "precio": 1000.0,
            "stock": 5,
            "stock_minimo": 2,
            "proveedor": "Proveedor X",
        }
    }

    eliminar_producto(inventario, "TST001")
    print("Productos:", len(inventario))

    try:
        eliminar_producto(inventario, "TST001")
    except ValueError as error:
        print("Error:", error)
