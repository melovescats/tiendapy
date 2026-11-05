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


if __name__ == "__main__":
    from persistencia import cargar_inventario

    inventario = cargar_inventario()

    print(buscar_por_codigo(inventario, "LAC001"))
    print(buscar_por_codigo(inventario, "XXX999"))

    for producto in buscar_por_categoria(inventario, "Bebidas"):
        print(producto["codigo"], producto["nombre"])
    print(buscar_por_categoria(inventario, "Frutas"))
