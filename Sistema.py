import random  


MIN_STOCK_DEFAULT = 5 
DIAS_VALIDOS = ["lunes","martes","miercoles","jueves","viernes","sabado","domingo"]


def simular_catalogo_inicial():
    nombres = ["LAPICERA AZUL", "CUADERNO A4", "RESALTADOR", "REGLA 30CM", "GOMA DE BORRAR"]
    cods    = ["A1Z9", "B2Y8", "C3X7", "D4W6", "E5V5"]  
    productos = []
    for i in range(len(nombres)):
        stock_inicial = random.randint(0, 20)  
        productos.append([i+1, cods[i], nombres[i], stock_inicial, MIN_STOCK_DEFAULT])
    return productos

VENTAS = []

def normalizar_codigo(cod):
    return cod.strip().upper()

def codigo_valido(cod):
    return cod.isalnum() and (3 <= len(cod) <= 10)

def normalizar_dia(d):
    d2 = d.strip().lower()
    return d2

def dia_valido(d):
    return d in DIAS_VALIDOS

def leer_entero_positivo(mensaje):
    while True:
        try:
            valor = int(input(mensaje))
            if valor <= 0:
                print("Debe ser un entero positivo.")
                continue
            return valor
        except ValueError:
            print("Entrada inválida. Ingrese un número entero.")

def leer_entero_incluyendo_cero(mensaje):
    while True:
        try:
            valor = int(input(mensaje))
            if valor < 0:
                print("Debe ser un entero mayor o igual a 0.")
                continue
            return valor
        except ValueError:
            print("Entrada inválida. Ingrese un número entero.")


def buscar_producto_por_codigo(productos, cod):
    cod = normalizar_codigo(cod)
    for i in range(len(productos)):
        if productos[i][1] == cod:
            return i
    return -1

def mostrar_stock(productos):
    print("\n=== STOCK ACTUAL ===")
    print("ID | COD | NOMBRE                  | STOCK | MIN")
    for p in productos:
        linea = f"{str(p[0]).zfill(2)} | {p[1]:<4} | {p[2]:<22} | {str(p[3]).zfill(5)} | {p[4]}"
        print(linea)
    print()

def productos_bajo_minimo(productos):
    bajos = []
    for p in productos:
        if p[3] < p[4]:
            bajos.append(p)
    return bajos

def fabricar(productos):
    cod = normalizar_codigo(input("Código del producto a fabricar: "))
    if not codigo_valido(cod):
        print("Código inválido (alfanumérico, 3..10).")
        return
    idx = buscar_producto_por_codigo(productos, cod)
    if idx == -1:
        print("No existe un producto con ese código.")
        return
    cant = leer_entero_positivo("Cantidad fabricada: ")
    productos[idx][3] += cant
    print("Fabricación registrada. Nuevo stock:", productos[idx][3])

def ajustar_inventario(productos):
    cod = normalizar_codigo(input("Código del producto a ajustar: "))
    if not codigo_valido(cod):
        print("Código inválido (alfanumérico, 3..10).")
        return
    idx = buscar_producto_por_codigo(productos, cod)
    if idx == -1:
        print("No existe un producto con ese código.")
        return
   
    try:
        ajuste = int(input("Ingrese ajuste (positivo o negativo): "))
    except ValueError:
        print("Ajuste inválido.")
        return
    nuevo = productos[idx][3] + ajuste
    if nuevo < 0:
        print("Ajuste rechazado: el stock no puede ser negativo.")
        return
    productos[idx][3] = nuevo
    print("Ajuste aplicado. Nuevo stock:", productos[idx][3])

def registrar_venta(productos):
    cod = normalizar_codigo(input("Código del producto: "))
    if not codigo_valido(cod):
        print("Código inválido (alfanumérico, 3..10).")
        return
    idx = buscar_producto_por_codigo(productos, cod)
    if idx == -1:
        print("No existe un producto con ese código.")
        return
    cant = leer_entero_positivo("Cantidad a vender: ")
    if productos[idx][3] < cant:
        print("Venta rechazada: stock insuficiente.")
        return
    dia = normalizar_dia(input("Día de la semana (lunes..domingo): "))
    if not dia_valido(dia):
        print("Día inválido.")
        return
    productos[idx][3] -= cant
    VENTAS.append([dia, idx, cant])
    print("Venta registrada. Nuevo stock:", productos[idx][3])

def registrar_devolucion(productos):
    cod = normalizar_codigo(input("Código del producto: "))
    if not codigo_valido(cod):
        print("Código inválido (alfanumérico, 3..10).")
        return
    idx = buscar_producto_por_codigo(productos, cod)
    if idx == -1:
        print("No existe un producto con ese código.")
        return
    cant = leer_entero_positivo("Cantidad a devolver: ")
   
    productos[idx][3] += cant
    
    dia = normalizar_dia(input("Día de la semana (lunes..domingo): "))
    if not dia_valido(dia):
        print("Día inválido, se registrará como 'lunes'.")
        dia = "lunes"
    VENTAS.append([dia, idx, -cant])
    print("Devolución registrada. Nuevo stock:", productos[idx][3])

def reporte_ventas_por_dia_y_producto(productos):
    cod = normalizar_codigo(input("Código del producto: "))
    if not codigo_valido(cod):
        print("Código inválido (alfanumérico, 3..10).")
        return
    idx = buscar_producto_por_codigo(productos, cod)
    if idx == -1:
        print("No existe un producto con ese código.")
        return
    dia = normalizar_dia(input("Día de la semana (lunes..domingo): "))
    if not dia_valido(dia):
        print("Día inválido.")
        return
    total = 0
    for v in VENTAS:
        if v[0] == dia and v[1] == idx:
            total += v[2]
    
    print(f"Producto: {productos[idx][2]} | Día: {dia} | Cantidad neta vendida: {total}")

def ordenar_por_stock_desc(productos):
    
    copia = []
    for p in productos:
        copia.append([p[0], p[1], p[2], p[3], p[4]])
    n = len(copia)
    for i in range(n-1):
        max_i = i
        for j in range(i+1, n):
            if copia[j][3] > copia[max_i][3]:
                max_i = j
        if max_i != i:
            aux = copia[i]
            copia[i] = copia[max_i]
            copia[max_i] = aux
    return copia

def informe_final(productos):
    ordenados = ordenar_por_stock_desc(productos)
    print("\n=== INFORME FINAL (ordenado por stock desc) ===")
    print("COD | NOMBRE                  | STOCK | MIN | ALERTA")
    for p in ordenados:
        alerta = "BAJO MIN" if p[3] < p[4] else ""
        print(f"{p[1]:<4} | {p[2]:<22} | {str(p[3]).zfill(5)} | {p[4]}   | {alerta}")
    print()

def ver_alertas(productos):
    bajos = productos_bajo_minimo(productos)
    if len(bajos) == 0:
        print("No hay productos por debajo del stock mínimo.")
        return
    print("\n=== ALERTAS: Bajo stock mínimo ===")
    for p in bajos:
        print(f"{p[1]} - {p[2]} (stock {p[3]} < min {p[4]})")
    print()

def actualizar_minimo(productos):
    
    nuevo = leer_entero_positivo("Nuevo stock mínimo recomendado para TODOS los productos: ")
    for i in range(len(productos)):
        productos[i][4] = nuevo
    print("Stock mínimo actualizado.")

def menu_inventario(productos):
    while True:
        print("\n--- MENÚ INVENTARIO ---")
        print("1) Ver stock")
        print("2) Fabricar (ingresar producción)")
        print("3) Ajustar inventario (±)")
        print("4) Ver productos bajo mínimo")
        print("5) Informe final")
        print("6) Cambiar stock mínimo global")
        print("7) Salir a menú principal")
        op = input("Opción: ").strip()
        if op == "1":
            mostrar_stock(productos)
        elif op == "2":
            fabricar(productos)
        elif op == "3":
            ajustar_inventario(productos)
        elif op == "4":
            ver_alertas(productos)
        elif op == "5":
            informe_final(productos)
        elif op == "6":
            actualizar_minimo(productos)
        elif op == "7":
            break
        else:
            print("Opción inválida.")

def menu_ventas(productos):
    while True:
        print("\n--- MENÚ VENTAS ---")
        print("1) Ver stock")
        print("2) Registrar venta")
        print("3) Registrar devolución")
        print("4) Reporte de ventas por día y producto")
        print("5) Ver alertas de bajo stock")
        print("6) Informe final")
        print("7) Salir a menú principal")
        op = input("Opción: ").strip()
        if op == "1":
            mostrar_stock(productos)
        elif op == "2":
            registrar_venta(productos)
        elif op == "3":
            registrar_devolucion(productos)
        elif op == "4":
            reporte_ventas_por_dia_y_producto(productos)
        elif op == "5":
            ver_alertas(productos)
        elif op == "6":
            informe_final(productos)
        elif op == "7":
            break
        else:
            print("Opción inválida.")


def main():
    print("=== Sistema de Inventario (Prototipo) ===")
    productos = simular_catalogo_inicial()
    mostrar_stock(productos)

    while True:
        print("\nPERFILES:")
        print("1) Inventario")
        print("2) Ventas")
        print("3) Salir")
        op = input("Elegí un perfil: ").strip()
        if op == "1":
            menu_inventario(productos)
        elif op == "2":
            menu_ventas(productos)
        elif op == "3":
            print("Fin del sistema.")
            break
        else:
            print("Opción inválida.")

if __name__ == "__main__":
    main()