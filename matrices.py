def ingresar_matriz(nombre=""):
    titulo = f"({nombre})" if nombre else ""
    print(f"--- Ingrese la matriz {titulo} ---")
    while True:
        try:
            filas = int(input("Cantidad de filas: "))
            columnas = int(input("Cantidad de columnas: "))
            if filas <= 0 or columnas <= 0:
                print("Las dimensiones deben ser mayores a 0")
                continue
            break
        except ValueError:
            print("Ingrese números enteros válidos")

    matriz = []
    print(f"Ingrese los valores de la matriz {filas}x{columnas}:")
    for i in range(filas):
        fila = []
        for j in range(columnas):
            while True:
                try:
                    val = float(input(f"  Elemento [{i+1}][{j+1}]: "))
                    fila.append(val)
                    break
                except ValueError:
                    print("Ingrese un número válido")
        matriz.append(fila)
    return matriz
def mostrar_matriz(matriz, nombre="Resultado"):
    print(f"\n  {nombre} ({len(matriz)}x{len(matriz[0])}):")
    for fila in matriz:
        print("  | " + "\t".join(f"{val:8.2f}" for val in fila) + " |")
    print()
def ingresar_vector(nombre="vector"):
    while True:
        try:
            n = int(input(f"\n  Ingrese el número de elementos del {nombre}: "))
            if n <= 0:
                print("  El tamaño debe ser mayor a 0.")
                continue
            break
        except ValueError:
            print("  Ingrese un número entero válido.")

    while True:
        try:
            entrada = input(f"  Ingrese los {n} elementos separados por espacio: ").split()
            if len(entrada) != n:
                print(f"  Debe ingresar exactamente {n} elementos.")
                continue
            vector = [float(x) for x in entrada]
            return vector
        except ValueError:
            print("  Ingrese solo números válidos.")
def mostrar_vector(vector, titulo="Vector"):
    elementos = []
    for x in vector:
        if x == int(x):
            elementos.append(str(int(x)))
        else:
            elementos.append(f"{x:.2f}")
    print(f"  {titulo}: [{', '.join(elementos)}]")
# Sumatoria de matrices
def sumar_matrices(a, b):
    """Suma dos matrices del mismo tamaño."""
    if len(a) != len(b) or len(a[0]) != len(b[0]):
        print("Las matrices deben tener las mismas dimensiones para poder sumarse")
        return None
    return [[a[i][j] + b[i][j] for j in range(len(a[0]))] for i in range(len(a))]
# Restar matrices
def restar_matrices(a, b):
    """Resta dos matrices del mismo tamaño (A - B)."""
    if len(a) != len(b) or len(a[0]) != len(b[0]):
        print("Las matrices deben tener las mismas dimensiones para poder restarse")
        return None
    return [[a[i][j] - b[i][j] for j in range(len(a[0]))] for i in range(len(a))]
# Multiplicar matrices
def multiplicar_matrices(a, b):
    """Multiplica dos matrices (A × B)."""
    if len(a[0]) != len(b):
        print("Dimensiones no compatibles: columnas de A deben ser iguales a filas de B")
        return None
    resultado = []
    for i in range(len(a)):
        fila = []
        for j in range(len(b[0])):
            suma = 0
            for k in range(len(b)):
                suma = suma + a[i][k] * b[k][j]
            fila.append(suma)
        resultado.append(fila)
    return resultado
# Multiplicar por escalar
def multiplicar_por_escalar(matriz, escalar):
    """Multiplica cada elemento de la matriz por un escalar."""
    resultado = []
    for fila in matriz:
        nueva_fila = []
        for elemento in fila:
            nueva_fila.append(elemento * escalar)
        resultado.append(nueva_fila)
    return resultado
# Transpuesta
def transpuesta(matriz):
    """Calcula la transpuesta de una matriz."""
    return [[matriz[j][i] for j in range(len(matriz))] for i in range(len(matriz[0]))]
# Determinante
def determinante(matriz):
    """Calcula el determinante de una matriz cuadrada (recursivo por cofactores)."""
    n = len(matriz)
    if any(len(fila) != n for fila in matriz):
        print("La matriz debe ser cuadrada para calcular el determinante.")
        return None

    if n == 1:
        return matriz[0][0]
    if n == 2:
        return matriz[0][0] * matriz[1][1] - matriz[0][1] * matriz[1][0]

    det = 0.0
    for j in range(n):
        submatriz = [
            [matriz[i][k] for k in range(n) if k != j]
            for i in range(1, n)
        ]
        cofactor = ((-1) ** j) * matriz[0][j] * determinante(submatriz)
        det += cofactor
    return det
# Producto punto
def producto_punto(vector_a, vector_b):
    """Calcula el producto punto de dos vectores."""
    if len(vector_a) != len(vector_b):
        print("Los vectores deben tener la misma longitud")
        return None
    suma = 0
    for i in range(len(vector_a)):
        suma = suma + vector_a[i] * vector_b[i]
    return suma
# Producto cruz
def producto_cruz(a, b):
    """Calcula el producto cruz de dos vectores de 3 elementos."""
    if len(a) != 3 or len(b) != 3:
        print("Ambos vectores deben tener exactamente 3 elementos")
        return None
    x = a[1] * b[2] - a[2] * b[1]
    y = a[2] * b[0] - a[0] * b[2]
    z = a[0] * b[1] - a[1] * b[0]
    return [x, y, z]
# Inversa de una matriz
def inversa(matriz):
    """Calcula la inversa de una matriz cuadrada."""
    n = len(matriz)
    if any(len(fila) != n for fila in matriz):
        print("La matriz debe ser cuadrada para calcular la inversa.")
        return None

    det = determinante(matriz)
    if det is None:
        return None
    if det == 0:
        print("La matriz no tiene inversa (determinante = 0)")
        return None

    cofactores = []
    for i in range(n):
        fila = []
        for j in range(n):
            submatriz = []
            for fi in range(n):
                if fi == i:
                    continue
                nueva_fila = []
                for co in range(n):
                    if co == j:
                        continue
                    nueva_fila.append(matriz[fi][co])
                submatriz.append(nueva_fila)
            signo = (-1) ** (i + j)
            cofactor = signo * determinante(submatriz)
            fila.append(cofactor)
        cofactores.append(fila)

    adjunta = transpuesta(cofactores)
    inversa_mat = []
    for fila in adjunta:
        nueva_fila = []
        for elemento in fila:
            nueva_fila.append(elemento / det)
        inversa_mat.append(nueva_fila)
    return inversa_mat
# Producto de una matriz por un vector
def producto_matriz_vector(matriz, vector):
    """Multiplica una matriz por un vector columna."""
    if len(matriz[0]) != len(vector):
        print(f"Dimensiones incompatibles: la matriz tiene {len(matriz[0])} columnas pero el vector tiene {len(vector)} elementos.")
        return None
    resultado = []
    for i in range(len(matriz)):
        suma = 0
        for j in range(len(vector)):
            suma = suma + matriz[i][j] * vector[j]
        resultado.append(suma)
    return resultado


if __name__ == "__main__":
    print("Ejecute main.py para usar el menú principal")