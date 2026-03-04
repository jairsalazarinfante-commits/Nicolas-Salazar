"""
Módulo de algoritmos de ordenamiento.
Permite al usuario ingresar una lista de números y ordenarla con:
- Método Burbuja (Bubble Sort)
- Método de Inserción (Insertion Sort)
- Método de Selección (Selection Sort)
- Merge Sort
"""


# ═══════════════════════════════════════════════════════════
#              FUNCIONES AUXILIARES
# ═══════════════════════════════════════════════════════════

def ingresar_lista() -> list[float]:
    """Solicita al usuario ingresar una lista de números."""
    while True:
        try:
            entrada = input("\n  Ingrese los números separados por espacio: ").split()
            if len(entrada) == 0:
                print("  ⚠ Debe ingresar al menos un número.")
                continue
            lista = [float(x) for x in entrada]
            return lista
        except ValueError:
            print("  ⚠ Ingrese solo números válidos separados por espacio.")


def mostrar_lista(lista: list[float], titulo: str = "Lista") -> None:
    """Muestra una lista con formato en la consola."""
    elementos = []
    for x in lista:
        if x == int(x):
            elementos.append(str(int(x)))
        else:
            elementos.append(f"{x:.2f}")
    print(f"  {titulo}: [{', '.join(elementos)}]")


# ═══════════════════════════════════════════════════════════
#                 1. BURBUJA (BUBBLE SORT)
# ═══════════════════════════════════════════════════════════
#
# ¿Cómo funciona?
#   Recorre la lista comparando pares ADYACENTES (vecinos).
#   Si el de la izquierda es MAYOR que el de la derecha, los INTERCAMBIA.
#   Después de cada pasada, el número más grande "sube" al final
#   como una burbuja.
#
# Complejidad: O(n²)
#
# Ejemplo visual:
#   [5, 3, 8, 1]
#   Pasada 1: compara 5>3? sí → [3, 5, 8, 1]
#             compara 5>8? no → [3, 5, 8, 1]
#             compara 8>1? sí → [3, 5, 1, 8]  ← el 8 subió al final
#   Pasada 2: compara 3>5? no → [3, 5, 1, 8]
#             compara 5>1? sí → [3, 1, 5, 8]  ← el 5 subió
#   Pasada 3: compara 3>1? sí → [1, 3, 5, 8]  ✅ Ordenado
# ═══════════════════════════════════════════════════════════

def burbuja(lista: list[float], mostrar_pasos: bool = True) -> list[float]:
    """Ordena una lista usando el método de burbuja."""
    arr = lista.copy()        # Copia para no modificar la original
    n = len(arr)              # Tamaño de la lista
    intercambios_totales = 0  # Contador de intercambios

    if mostrar_pasos:
        print("\n  ┌─────────────────────────────────────────┐")
        print("  │      MÉTODO BURBUJA (Bubble Sort)       │")
        print("  └─────────────────────────────────────────┘")
        mostrar_lista(arr, "  Lista inicial")

    # Pasada externa: se repite n-1 veces
    for i in range(n - 1):
        intercambiado = False  # Bandera para optimización

        # Pasada interna: compara pares adyacentes
        # (n - 1 - i) porque los últimos i elementos ya están ordenados
        for j in range(n - 1 - i):

            # Si el elemento actual es MAYOR que el siguiente → intercambiar
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]  # Intercambio
                intercambiado = True
                intercambios_totales += 1

        if mostrar_pasos:
            mostrar_lista(arr, f"    Pasada {i + 1}")

        # Optimización: si no hubo intercambios, ya está ordenada
        if not intercambiado:
            if mostrar_pasos:
                print("    ✓ No hubo intercambios, lista ordenada.")
            break

    if mostrar_pasos:
        print(f"  📊 Total de intercambios: {intercambios_totales}")
        mostrar_lista(arr, "  ✅ Lista ordenada")

    return arr


# ═══════════════════════════════════════════════════════════
#              2. INSERCIÓN (INSERTION SORT)
# ═══════════════════════════════════════════════════════════
#
# ¿Cómo funciona?
#   Imagina que tienes cartas en la mano ordenadas.
#   Tomas una carta nueva y la INSERTAS en su posición correcta
#   desplazando las demás hacia la derecha.
#
# Complejidad: O(n²)
#
# Ejemplo visual:
#   [5, 3, 8, 1]
#   Paso 1: tomar 3 → ¿dónde va? antes del 5 → [3, 5, 8, 1]
#   Paso 2: tomar 8 → ¿dónde va? ya está bien  → [3, 5, 8, 1]
#   Paso 3: tomar 1 → ¿dónde va? al inicio      → [1, 3, 5, 8] ✅
# ═══════════════════════════════════════════════════════════

def insercion(lista: list[float], mostrar_pasos: bool = True) -> list[float]:
    """Ordena una lista usando el método de inserción."""
    arr = lista.copy()
    n = len(arr)

    if mostrar_pasos:
        print("\n  ┌─────────────────────────────────────────┐")
        print("  │    MÉTODO INSERCIÓN (Insertion Sort)    │")
        print("  └─────────────────────────────────────────┘")
        mostrar_lista(arr, "  Lista inicial")

    # Empezamos desde el segundo elemento (índice 1)
    for i in range(1, n):
        clave = arr[i]  # El elemento que vamos a insertar
        j = i - 1       # Empezamos a comparar con el anterior

        # Mover los elementos mayores que 'clave' una posición a la derecha
        while j >= 0 and arr[j] > clave:
            arr[j + 1] = arr[j]  # Desplazar a la derecha
            j = j - 1            # Ir al anterior

        # Insertar 'clave' en su posición correcta
        arr[j + 1] = clave

        if mostrar_pasos:
            if clave == int(clave):
                clave_str = str(int(clave))
            else:
                clave_str = f"{clave:.2f}"
            mostrar_lista(arr, f"    Paso {i} (insertando {clave_str})")

    if mostrar_pasos:
        mostrar_lista(arr, "  ✅ Lista ordenada")

    return arr


# ═══════════════════════════════════════════════════════════
#              3. SELECCIÓN (SELECTION SORT)
# ═══════════════════════════════════════════════════════════
#
# ¿Cómo funciona?
#   Busca el MÍNIMO de toda la lista y lo pone en la posición 0.
#   Luego busca el mínimo del resto y lo pone en la posición 1.
#   Y así sucesivamente...
#
# Complejidad: O(n²)
#
# Ejemplo visual:
#   [5, 3, 8, 1]
#   Paso 1: mínimo = 1 (pos 3) → intercambiar con pos 0 → [1, 3, 8, 5]
#   Paso 2: mínimo = 3 (pos 1) → ya está en su lugar    → [1, 3, 8, 5]
#   Paso 3: mínimo = 5 (pos 3) → intercambiar con pos 2 → [1, 3, 5, 8] ✅
# ═══════════════════════════════════════════════════════════

def seleccion(lista: list[float], mostrar_pasos: bool = True) -> list[float]:
    """Ordena una lista usando el método de selección."""
    arr = lista.copy()
    n = len(arr)

    if mostrar_pasos:
        print("\n  ┌─────────────────────────────────────────┐")
        print("  │    MÉTODO SELECCIÓN (Selection Sort)    │")
        print("  └─────────────────────────────────────────┘")
        mostrar_lista(arr, "  Lista inicial")

    for i in range(n - 1):
        # Buscar el índice del elemento MÍNIMO desde la posición i en adelante
        min_idx = i                      # Suponemos que el mínimo es el actual
        for j in range(i + 1, n):        # Buscamos en el resto de la lista
            if arr[j] < arr[min_idx]:    # Si encontramos uno más pequeño
                min_idx = j              # Actualizamos el índice del mínimo

        # Intercambiar: poner el mínimo en la posición i
        if min_idx != i:
            arr[i], arr[min_idx] = arr[min_idx], arr[i]

        if mostrar_pasos:
            if arr[i] == int(arr[i]):
                min_str = str(int(arr[i]))
            else:
                min_str = f"{arr[i]:.2f}"
            mostrar_lista(arr, f"    Paso {i + 1} (mínimo: {min_str})")

    if mostrar_pasos:
        mostrar_lista(arr, "  ✅ Lista ordenada")

    return arr


# ═══════════════════════════════════════════════════════════
#                    4. MERGE SORT
# ═══════════════════════════════════════════════════════════
#
# ¿Cómo funciona? (Divide y Vencerás)
#   1. DIVIDIR la lista por la mitad, una y otra vez, hasta
#      tener listas de 1 elemento (que ya están "ordenadas").
#   2. COMBINAR (merge) las sublistas de forma ordenada.
#
# Complejidad: O(n log n) — ¡Más rápido que los anteriores!
#
# Ejemplo visual:
#   [5, 3, 8, 1]
#        DIVIDIR
#       /        \
#   [5, 3]      [8, 1]       ← dividir en 2
#    / \          / \
#  [5] [3]     [8] [1]       ← listas de 1 elemento
#    \ /          \ /
#   [3, 5]      [1, 8]       ← combinar ordenando
#       \        /
#   [1, 3, 5, 8]             ← combinar final ✅
# ═══════════════════════════════════════════════════════════

def _merge(izquierda: list[float], derecha: list[float]) -> list[float]:
    """
    Combina (mezcla) dos sublistas YA ORDENADAS en una sola lista ordenada.

    Ejemplo:
      izquierda = [3, 5]    derecha = [1, 8]
      Paso 1: ¿3 vs 1?  → 1 es menor  → resultado = [1]
      Paso 2: ¿3 vs 8?  → 3 es menor  → resultado = [1, 3]
      Paso 3: ¿5 vs 8?  → 5 es menor  → resultado = [1, 3, 5]
      Paso 4: queda 8   →              → resultado = [1, 3, 5, 8]
    """
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

    # Agregar los elementos que quedaron (solo una lista tendrá sobrantes)
    while i < len(izquierda):
        resultado.append(izquierda[i])
        i = i + 1

    while j < len(derecha):
        resultado.append(derecha[j])
        j = j + 1

    return resultado


def _merge_sort_recursivo(arr: list[float], profundidad: int = 0, mostrar_pasos: bool = True) -> list[float]:
    """Implementación recursiva de Merge Sort."""

    # Caso base: una lista de 0 o 1 elemento ya está ordenada
    if len(arr) <= 1:
        return arr

    # DIVIDIR: encontrar el punto medio y partir en dos
    medio = len(arr) // 2          # División entera (parte la lista a la mitad)
    izquierda = arr[:medio]        # Desde el inicio hasta el medio
    derecha = arr[medio:]          # Desde el medio hasta el final

    if mostrar_pasos:
        indent = "    " + "  " * profundidad  # Indentación para visualizar la recursión
        mostrar_lista(izquierda, f"{indent}↙ Izq")
        mostrar_lista(derecha, f"{indent}↘ Der")

    # CONQUISTAR: ordenar cada mitad (llamada RECURSIVA)
    izquierda_ordenada = _merge_sort_recursivo(izquierda, profundidad + 1, mostrar_pasos)
    derecha_ordenada = _merge_sort_recursivo(derecha, profundidad + 1, mostrar_pasos)

    # COMBINAR: mezclar las dos mitades ordenadas
    combinada = _merge(izquierda_ordenada, derecha_ordenada)

    if mostrar_pasos:
        indent = "    " + "  " * profundidad
        mostrar_lista(combinada, f"{indent}🔗 Merge")

    return combinada


def merge_sort(lista: list[float], mostrar_pasos: bool = True) -> list[float]:
    """Ordena una lista usando Merge Sort (divide y vencerás)."""
    arr = lista.copy()

    if mostrar_pasos:
        print("\n  ┌─────────────────────────────────────────┐")
        print("  │            MERGE SORT                   │")
        print("  └─────────────────────────────────────────┘")
        mostrar_lista(arr, "  Lista inicial")

    resultado = _merge_sort_recursivo(arr, 0, mostrar_pasos)

    if mostrar_pasos:
        mostrar_lista(resultado, "  ✅ Lista ordenada")

    return resultado


# ═══════════════════════════════════════════════════════════
#                    MENÚ PRINCIPAL
# ═══════════════════════════════════════════════════════════

def menu_ordenamiento() -> None:
    """Menú interactivo para los algoritmos de ordenamiento."""
    while True:
        print("\n" + "=" * 50)
        print("     📊  ALGORITMOS DE ORDENAMIENTO  📊")
        print("=" * 50)
        print("  1. 🫧  Método Burbuja")
        print("  2. 📥  Método Inserción")
        print("  3. 🎯  Método Selección")
        print("  4. 🔀  Merge Sort")
        print("  5. 📋  Comparar todos los métodos")
        print("  0. ↩️   Volver al menú principal")
        print("=" * 50)

        opcion = input("  Seleccione una opción: ").strip()

        if opcion == "0":
            break

        if opcion not in ("1", "2", "3", "4", "5"):
            print("  ⚠ Opción no válida. Intente de nuevo.")
            continue

        # Pedir la lista al usuario
        lista = ingresar_lista()

        if opcion == "1":
            burbuja(lista)

        elif opcion == "2":
            insercion(lista)

        elif opcion == "3":
            seleccion(lista)

        elif opcion == "4":
            merge_sort(lista)

        elif opcion == "5":
            # Comparar los 4 métodos con la misma lista
            print("\n" + "═" * 55)
            print("    COMPARACIÓN DE TODOS LOS MÉTODOS DE ORDENAMIENTO")
            print("═" * 55)
            mostrar_lista(lista, "\n  📋 Lista original")

            print("\n  " + "─" * 45)
            res_burbuja = burbuja(lista)

            print("\n  " + "─" * 45)
            res_insercion = insercion(lista)

            print("\n  " + "─" * 45)
            res_seleccion = seleccion(lista)

            print("\n  " + "─" * 45)
            res_merge = merge_sort(lista)

            # Resumen final
            print("\n  " + "═" * 45)
            print("  ✅ RESUMEN DE RESULTADOS:")
            mostrar_lista(res_burbuja, "    Burbuja   ")
            mostrar_lista(res_insercion, "    Inserción ")
            mostrar_lista(res_seleccion, "    Selección ")
            mostrar_lista(res_merge, "    Merge Sort")

            if res_burbuja == res_insercion == res_seleccion == res_merge:
                print("\n  ✅ Todos los métodos producen el mismo resultado.")
            else:
                print("\n  ⚠ ¡Atención! Los resultados difieren.")


if __name__ == "__main__":
    menu_ordenamiento()
