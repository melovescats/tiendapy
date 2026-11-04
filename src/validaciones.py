categorias = ["Lacteos", "Bebidas", "Aseo", "Abarrotes", "Snacks"]


def ingresar_entero(mensaje):
    while True:
        try:
            valor = int(input(mensaje))
            if valor <= 0:
                print("Error: el valor debe ser mayor que cero.")
                continue
            return valor
        except ValueError:
            print("Error: debes ingresar un número entero.")


def ingresar_decimal(mensaje):
    while True:
        try:
            valor = float(input(mensaje))
            if valor <= 0:
                print("Error: el valor debe ser mayor que cero.")
                continue
            return valor
        except ValueError:
            print("Error: debes ingresar un número válido.")


def ingresar_texto(mensaje):
    while True:
        texto = input(mensaje).strip()
        if texto == "":
            print("Error: este campo no puede estar vacío.")
            continue
        return texto


def ingresar_codigo(mensaje):
    return ingresar_texto(mensaje).upper()


def ingresar_categoria(mensaje):
    while True:
        categoria = input(mensaje).strip().capitalize()
        if categoria in categorias:
            return categoria
        print("Error: las categorías válidas son:", ", ".join(categorias))


def confirmar(mensaje):
    while True:
        respuesta = input(mensaje + " (s/n): ").strip().lower()
        if respuesta == "s":
            return True
        if respuesta == "n":
            return False
        print("Error: responde con 's' o 'n'.")


if __name__ == "__main__":
    categoria = ingresar_categoria("Categoría: ")
    print("Categoría:", categoria)
    if confirmar("¿Guardar?"):
        print("Guardado")
    else:
        print("Cancelado")
