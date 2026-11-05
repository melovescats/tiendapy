def esta_agotado(producto):
    return producto["stock"] == 0


def productos_en_alerta(inventario):
    alertas = {}
    for producto in inventario.values():
        if producto["stock"] <= producto["stock_minimo"]:
            proveedor = producto["proveedor"]
            if proveedor not in alertas:
                alertas[proveedor] = []
            alertas[proveedor].append(producto)
    return alertas


if __name__ == "__main__":
    from persistencia import cargar_inventario

    inventario = cargar_inventario()
    alertas = productos_en_alerta(inventario)

    for proveedor, productos in alertas.items():
        print(proveedor)
        for producto in productos:
            if esta_agotado(producto):
                estado = "AGOTADO"
            else:
                estado = "stock bajo"
            print(
                f"  {producto['codigo']} {producto['nombre']} - stock {producto['stock']} ({estado})")
