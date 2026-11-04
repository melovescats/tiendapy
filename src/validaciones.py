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


if __name__ == "__main__":
    codigo = ingresar_codigo("Código: ")
    print("Ingresaste:", codigo)
