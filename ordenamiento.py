def ingresar_lista() -> list[float]:
    while True:
        try:
            entrada = input(" Ingrese los números separados por espacio: ").split()
            if len(entrada) == 0:
                print(" Debe ingresar al menos un número.")
                continue
            lista = [float(x) for x in entrada]
            return lista
        except ValueError:
            print(" Ingrese solo números válidos separados por espacio.")


def mostrar_lista(lista: list[float], titulo: str = "Lista") -> None:
    elementos = []
    for x in lista:
        if x == int(x):
            elementos.append(str(int(x)))
        else:
            elementos.append(f"{x:.2f}")
    print(f"  {titulo}: [{', '.join(elementos)}]")
#metodo burbuja
def burbuja(lista: list[float], mostrar_pasos: bool = True) -> list[float]:
    arr = lista.copy()        # Copia para no modificar la original
    n = len(arr)              # Tamaño de la lista
    intercambios_totales = 0  # Contador de intercambios

    if mostrar_pasos:
        mostrar_lista(arr, "  Lista inicial")
    for i in range(n - 1):
        intercambiado = False 
        for j in range(n - 1 - i):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j] 
                intercambiado = True
                intercambios_totales += 1
        if mostrar_pasos:
            mostrar_lista(arr, f"    Pasada {i + 1}")
        if not intercambiado:
            if mostrar_pasos:
                print("    ✓ No hubo intercambios, lista ordenada.")
            break

    if mostrar_pasos:
        print(f" Total de intercambios: {intercambios_totales}")
        mostrar_lista(arr, "Lista ordenada")

    return arr
#insercion
def insercion(lista: list[float], mostrar_pasos: bool = True) -> list[float]:
    arr = lista.copy()
    n = len(arr)

    if mostrar_pasos:
        mostrar_lista(arr, "  Lista inicial")
    for i in range(1, n):
        clave = arr[i]
        j = i - 1 
        while j >= 0 and arr[j] > clave:
            arr[j + 1] = arr[j]  
            j = j - 1
        arr[j + 1] = clave

        if mostrar_pasos:
            if clave == int(clave):
                clave_str = str(int(clave))
            else:
                clave_str = f"{clave:.2f}"
            mostrar_lista(arr, f"    Paso {i} (insertando {clave_str})")

    if mostrar_pasos:
        mostrar_lista(arr, "Lista ordenada")

    return arr
#seleccion
def seleccion(lista: list[float], mostrar_pasos: bool = True) -> list[float]:
    arr = lista.copy()
    n = len(arr)

    if mostrar_pasos:
        mostrar_lista(arr, "  Lista inicial")

    for i in range(n - 1):
        min_idx = i                      # Suponemos que el mínimo es el actual
        for j in range(i + 1, n):        # Buscamos en el resto de la lista
            if arr[j] < arr[min_idx]:    # Si encontramos uno más pequeño
                min_idx = j              # Actualizamos el índice del mínimo
        if min_idx != i:
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
        if mostrar_pasos:
            if arr[i] == int(arr[i]):
                min_str = str(int(arr[i]))
            else:
                min_str = f"{arr[i]:.2f}"
            mostrar_lista(arr, f"    Paso {i + 1} (mínimo: {min_str})")

    if mostrar_pasos:
        mostrar_lista(arr, "Lista ordenada")

    return arr
#merge
def _merge(izquierda: list[float], derecha: list[float]) -> list[float]:

    resultado: list[float] = []
    i = 0  # Índice para recorrer la sublista izquierda
    j = 0  # Índice para recorrer la sublista derecha

    # Comparar elemento por elemento de ambas sublistas
    while i < len(izquierda) and j < len(derecha):
        if izquierda[i] <= derecha[j]:
            resultado.append(izquierda[i])  # El de la izquierda es menor
            i = i + 1
        else:
            resultado.append(derecha[j])    # El de la derecha es menor
            j = j + 1
    while i < len(izquierda):
        resultado.append(izquierda[i])
        i = i + 1

    while j < len(derecha):
        resultado.append(derecha[j])
        j = j + 1

    return resultado


def _merge_sort_recursivo(arr: list[float], profundidad: int = 0, mostrar_pasos: bool = True) -> list[float]:
    if len(arr) <= 1:
        return arr
    medio = len(arr) // 2          # División entera (parte la lista a la mitad)
    izquierda = arr[:medio]        # Desde el inicio hasta el medio
    derecha = arr[medio:]          # Desde el medio hasta el final

    if mostrar_pasos:
        indent = "    " + "  " * profundidad  
        mostrar_lista(izquierda, f"{indent}↙ Izq")
        mostrar_lista(derecha, f"{indent}↘ Der")
    izquierda_ordenada = _merge_sort_recursivo(izquierda, profundidad + 1, mostrar_pasos)
    derecha_ordenada = _merge_sort_recursivo(derecha, profundidad + 1, mostrar_pasos)
    combinada = _merge(izquierda_ordenada, derecha_ordenada)

    if mostrar_pasos:
        indent = "    " + "  " * profundidad
        mostrar_lista(combinada, f"{indent} Merge")

    return combinada


def merge_sort(lista: list[float], mostrar_pasos: bool = True) -> list[float]:
    arr = lista.copy()

    if mostrar_pasos:
        mostrar_lista(arr, "  Lista inicial")

    resultado = _merge_sort_recursivo(arr, 0, mostrar_pasos)

    if mostrar_pasos:
        mostrar_lista(resultado, "  ✅ Lista ordenada")

    return resultado

