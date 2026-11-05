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


def ventas_del_dia(ventas, fecha):
    del_dia = []
    for venta in ventas:
        if venta["fecha"] == fecha:
            del_dia.append(venta)
    return del_dia


def calcular_resumen(ventas_dia):
    numero = len(ventas_dia)

    total = 0.0
    for venta in ventas_dia:
        total += venta["total"]

    if numero == 0:
        ticket_promedio = 0.0
    else:
        ticket_promedio = round(total / numero, 2)

    return total, numero, ticket_promedio


def contar_unidades_vendidas(ventas_dia):
    conteo = {}
    for venta in ventas_dia:
        for codigo, cantidad in venta["items"].items():
            conteo[codigo] = conteo.get(codigo, 0) + cantidad
    return conteo


def producto_mas_vendido(conteo):
    if not conteo:
        return None

    mejor = None
    for codigo, cantidad in conteo.items():
        if mejor is None or cantidad > conteo[mejor]:
            mejor = codigo
    return mejor, conteo[mejor]


def productos_sin_ventas(inventario, conteo):
    sin_ventas = []
    for codigo, producto in inventario.items():
        if codigo not in conteo:
            sin_ventas.append(producto)
    return sin_ventas


def categorias_con_movimiento(inventario, conteo):
    categorias = []
    for codigo in conteo:
        if codigo in inventario:
            categoria = inventario[codigo]["categoria"]
            if categoria not in categorias:
                categorias.append(categoria)
    return categorias


if __name__ == "__main__":
    from persistencia import cargar_inventario

    inventario = cargar_inventario()
    ventas_dia = [
        {"fecha": "2026-11-20", "total": 18400.0,
            "items": {"LAC001": 2, "BEB001": 1}},
        {"fecha": "2026-11-20", "total": 5800.0, "items": {"BEB001": 1}},
        {"fecha": "2026-11-20", "total": 14100.0,
            "items": {"BEB001": 1, "ASE002": 2}},
    ]

    conteo = contar_unidades_vendidas(ventas_dia)
    print(conteo)
    print(producto_mas_vendido(conteo))
    print(producto_mas_vendido({}))

    sin_ventas = productos_sin_ventas(inventario, conteo)
    print(len(sin_ventas))
    for producto in sin_ventas:
        print(producto["codigo"])

    print(categorias_con_movimiento(inventario, conteo))
