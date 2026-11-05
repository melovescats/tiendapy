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

    modificar_precio(inventario, "TST001", 1500.0)
    modificar_stock(inventario, "TST001", 20)
    print(inventario["TST001"]["precio"], inventario["TST001"]["stock"])

    try:
        modificar_precio(inventario, "TST001", -5)
    except ValueError as error:
        print("Error:", error)

    try:
        modificar_stock(inventario, "XXX999", 10)
    except ValueError as error:
        print("Error:", error)
