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


def guardar_inventario(inventario):
    with open(ruta_inventario, "w", encoding="utf-8") as archivo:
        for producto in inventario.values():
            archivo.write(producto_a_linea(producto) + "\n")


def registrar_venta(fecha, total, items):
    partes = []
    for codigo, cantidad in items.items():
        partes.append(f"{codigo}:{cantidad}")
    detalle = ";".join(partes)

    with open(ruta_ventas, "a", encoding="utf-8") as archivo:
        archivo.write(f"{fecha}|{total}|{detalle}\n")


def cargar_ventas():
    ventas = []

    try:
        with open(ruta_ventas, "r", encoding="utf-8") as archivo:
            for numero, linea in enumerate(archivo, start=1):
                linea = linea.strip()
                if linea == "":
                    continue

                try:
                    fecha, total, detalle = linea.split("|")
                    items = {}
                    for par in detalle.split(";"):
                        codigo, cantidad = par.split(":")
                        items[codigo] = int(cantidad)
                    venta = {"fecha": fecha, "total": float(
                        total), "items": items}
                except ValueError:
                    print(
                        f"Advertencia: venta de la línea {numero} omitida (formato inválido).")
                    continue

                ventas.append(venta)
    except FileNotFoundError:
        pass

    return ventas


if __name__ == "__main__":
    import os
    print("Archivo de ventas:", os.path.abspath(ruta_ventas))
    registrar_venta("2026-11-20", 18400.0, {"LAC001": 2, "BEB001": 1})
    ventas = cargar_ventas()
    print("Ventas cargadas:", len(ventas))
