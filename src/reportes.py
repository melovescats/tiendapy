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


if __name__ == "__main__":
    ventas = [
        {"fecha": "2026-11-20", "total": 18400.0,
            "items": {"LAC001": 2, "BEB001": 1}},
        {"fecha": "2026-11-20", "total": 5800.0, "items": {"BEB001": 1}},
        {"fecha": "2026-11-21", "total": 9000.0, "items": {"ASE002": 2}},
    ]

    dia = ventas_del_dia(ventas, "2026-11-20")
    print(len(dia))
    print(calcular_resumen(dia))
    print(calcular_resumen(ventas_del_dia(ventas, "2026-11-25")))
