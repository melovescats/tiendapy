ruta_inventario = "data/inventario.txt"
ruta_ventas = "data/ventas.txt"


def linea_a_producto(linea):
    campos = linea.split("|")
    if len(campos) != 7:
        raise ValueError("la línea debe tener 7 campos")

    codigo, nombre, categoria, precio, stock, stock_minimo, proveedor = campos

    producto = {
        "codigo": codigo.strip(),
        "nombre": nombre.strip(),
        "categoria": categoria.strip(),
        "precio": float(precio),
        "stock": int(stock),
        "stock_minimo": int(stock_minimo),
        "proveedor": proveedor.strip(),
    }

    if producto["codigo"] == "":
        raise ValueError("el código está vacío")
    if producto["precio"] <= 0:
        raise ValueError("el precio debe ser mayor que cero")
    if producto["stock"] < 0 or producto["stock_minimo"] < 0:
        raise ValueError("el stock no puede ser negativo")

    return producto


def producto_a_linea(producto):
    return "|".join([
        producto["codigo"],
        producto["nombre"],
        producto["categoria"],
        str(producto["precio"]),
        str(producto["stock"]),
        str(producto["stock_minimo"]),
        producto["proveedor"],
    ])


if __name__ == "__main__":
    linea = "LAC001|Leche entera 1L|Lacteos|4200.0|35|10|Alqueria"
    producto = linea_a_producto(linea)
    print(producto)
    print(producto_a_linea(producto))
    print(producto_a_linea(producto) == linea)
