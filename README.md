# TiendaPy 

Aplicación de consola en Python para controlar el inventario y las ventas de una tienda de barrio "Don Aurelio", permite registrar productos, procesar ventas con descuento, controlar el stock mínimo y generar el cierre del día. La información se guarda en archivos txt

## Integrantes

- Karen Melisa Guerrero Jiménez - 20241015005

## Requisitos

- Python 3.10 o superior
- Librería `tabulate` (se instala con `requirements.txt`)

## Instalación

```bash
git clone https://github.com/melovescats/tiendapy.git
cd tiendapy
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

En Mac o Linux, el entorno se activa con `source venv/bin/activate`.

## Ejecución

Desde la carpeta raíz del proyecto (la que contiene `src/` y `data/`):

```bash
python src/main.py
```

Es importante ejecutarlo desde la raíz, porque las rutas de los archivos de datos son relativas a esa carpeta

## Funcionalidades

1. **Ver inventario:** se ve una tabla con todos los productos
2. **Agregar producto:** el código no puede repetirse
3. **Consultar producto:** por código o por categoría
4. **Modificar producto:** precio o stock
5. **Eliminar producto:** con confirmación
6. **Nueva venta:** carrito con varios productos, descuento, pago, cambio y descuento de stock
7. **Alertas de stock:** productos con stock menor o igual al mínimo, agrupados por proveedor, con los agotados identificados
8. **Cierre del día:** total vendido, número de ventas, ticket promedio, producto más vendido, categorías con movimiento y productos sin ventas
9. **Guardar inventario:** también se guarda al salir

## Reglas de negocio

- No se puede vender más del stock disponible
- No se permiten precios ni cantidades negativas o iguales a cero
- Subtotal de $50.000 o más: descuento del 5 %. Subtotal de $100.000 o más: descuento del 10 %
- El pago no puede ser inferior al total a pagar
- Los códigos de producto no pueden repetirse

## Estructura del proyecto

```
tienda/
├── README.md
├── requirements.txt
├── data/
│   ├── inventario.txt
│   └── ventas.txt
└── src/
    ├── main.py            # menú principal y flujo general
    ├── inventario.py      # agregar, buscar, modificar y eliminar productos
    ├── ventas.py          # carrito, descuentos y cambio
    ├── reportes.py        # alertas y cierre del día
    ├── persistencia.py    # lectura y escritura de archivos
    └── validaciones.py    # captura segura de datos
```

## Formato de los archivos

`data/inventario.txt`: un producto por línea, con campos separados por `|`:

```
codigo|nombre|categoria|precio|stock|stock_minimo|proveedor
LAC001|Leche entera 1L|Lacteos|4200.0|35|10|Alqueria
```

`data/ventas.txt`: una venta por línea, con el formato `fecha|total|codigo:cantidad;codigo:cantidad`:

```
2026-11-20|18400.0|LAC001:2;BEB001:1
```

## Decisiones de diseño

- **Sin clases.** Cada producto es un diccionario y el inventario es un diccionario del cual la llave es el código, lo que facilitando la busqueda y dtetectando códigos repetido
- **Módulos desacoplados.** Las funciones de `inventario.py`, `ventas.py` y `reportes.py` solo calculan y devuelven datos o lanzan `ValueError` con `raise` cuando no se cumple alguna de las reglas y para capturar los errores y mostrar los mensajes se usó `main.py`
- **Robustez.** Las entradas se validan en `validaciones.py` y el programa no se detiene por errores de digitación, si `inventario.txt` no existe, arranca con un inventario vacío, y las líneas malas de los archivos se omiten con una advertencia
- **Archivos.** Se abren siempre con `with` así se cierran incluso si hay errror
- **Venta atómica.** `confirmar_venta` revisa todo el carrito antes de descontar el stock entonces una venta rechazada no deja el inventario a medias