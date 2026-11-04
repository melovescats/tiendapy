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


def cargar_inventario():
    inventario = {}

    try:
        with open(ruta_inventario, "r", encoding="utf-8") as archivo:
            for numero, linea in enumerate(archivo, start=1):
                linea = linea.strip()
                if linea == "":
                    continue

                try:
                    producto = linea_a_producto(linea)
                except ValueError as error:
                    print(f"Advertencia: línea {numero} omitida ({error}).")
                    continue

                if producto["codigo"] in inventario:
                    print(
                        f"Advertencia: línea {numero} omitida (código repetido).")
                    continue

                inventario[producto["codigo"]] = producto
    except FileNotFoundError:
        print("No se encontró el archivo de inventario. Se inicia con uno vacío.")

    return inventario


if __name__ == "__main__":
    inventario = cargar_inventario()
    print("Productos cargados:", len(inventario))
    for producto in inventario.values():
        print(producto)
