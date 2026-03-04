"""
Programa principal que integra:
- Operaciones con matrices (matrices.py)
- Algoritmos de ordenamiento (ordenamiento.py)
"""

import matrices
import ordenamiento


def menu_principal():
    while True:
        print("\n" + "=" * 50)
        print("MENÚ PRINCIPAL")
        print("=" * 50)
        print("  1.Ordenamiento")
        print("  2.Matrices")
        print("  3.Salir")
        print("=" * 50)
        opcion = input("  Seleccione una opción: ").strip()
        if opcion == "1":
            menu_ordenamiento()
        elif opcion == "2":
            menu_matrices()
        elif opcion == "3":
            print("\n¡Hasta luego!")
            break
        else:
            print("  ⚠ Opción no válida. Intente de nuevo.")


def menu_ordenamiento():
    while True:
        print("\n" + "=" * 50)
        print(" MENÚ DE ORDENAMIENTO")
        print("=" * 50)
        print("  1. Burbuja")
        print("  2. Inserción")
        print("  3. Selección")
        print("  4. Merge Sort")
        print("  5.Volver al menú principal")
        print("=" * 50)
        opcion = input("  Seleccione una opción: ").strip()
        if opcion == "1":
            lista = ordenamiento.ingresar_lista()
            ordenamiento.burbuja(lista)
        elif opcion == "2":
            lista = ordenamiento.ingresar_lista()
            ordenamiento.insercion(lista)
        elif opcion == "3":
            lista = ordenamiento.ingresar_lista()
            ordenamiento.seleccion(lista)
        elif opcion == "4":
            lista = ordenamiento.ingresar_lista()
            ordenamiento.merge_sort(lista)
        elif opcion == "5":
            break
        else:
            print("Opción no válida. Intente de nuevo.")


def menu_matrices():
    while True:
        print("\n" + "=" * 50)
        print(" MENÚ DE MATRICES")
        print("=" * 50)
        print("  1.Sumar matrices")
        print("  2.Restar matrices")
        print("  3.Multiplicar matrices")
        print("  4.Multiplicar por escalar")
        print("  5.Transpuesta")
        print("  6.Determinante")
        print("  7.Inversa de una matriz")
        print("  8.Producto Matriz × Vector")
        print("  9.Volver al menú principal")
        print("=" * 50)
        opcion = input("  Seleccione una opción: ").strip()

        if opcion == "1":
            matriz1 = matrices.ingresar_matriz("Matriz A")
            matriz2 = matrices.ingresar_matriz("Matriz B")
            resultado = matrices.sumar_matrices(matriz1, matriz2)
            if resultado is not None:
                matrices.mostrar_matriz(resultado, "A + B")

        elif opcion == "2":
            matriz1 = matrices.ingresar_matriz("Matriz A")
            matriz2 = matrices.ingresar_matriz("Matriz B")
            resultado = matrices.restar_matrices(matriz1, matriz2)
            if resultado is not None:
                matrices.mostrar_matriz(resultado, "A - B")

        elif opcion == "3":
            matriz1 = matrices.ingresar_matriz("Matriz A")
            matriz2 = matrices.ingresar_matriz("Matriz B")
            resultado = matrices.multiplicar_matrices(matriz1, matriz2)
            if resultado is not None:
                matrices.mostrar_matriz(resultado, "A × B")

        elif opcion == "4":
            matriz = matrices.ingresar_matriz("Matriz")
            try:
                escalar = float(input("  Ingrese el escalar: "))
            except ValueError:
                print(" Ingrese un número válido.")
                continue
            resultado = matrices.multiplicar_por_escalar(matriz, escalar)
            matrices.mostrar_matriz(resultado, f"Matriz × {escalar}")

        elif opcion == "5":
            matriz = matrices.ingresar_matriz("Matriz")
            resultado = matrices.transpuesta(matriz)
            matrices.mostrar_matriz(resultado, "Transpuesta")

        elif opcion == "6":
            matriz = matrices.ingresar_matriz("Matriz (cuadrada)")
            det = matrices.determinante(matriz)
            if det is not None:
                print(f"\n Determinante = {det:.4f}")

        elif opcion == "7":
            matriz = matrices.ingresar_matriz("Matriz (cuadrada)")
            inv = matrices.inversa(matriz)
            if inv is not None:
                matrices.mostrar_matriz(inv, "Matriz Inversa (A⁻¹)")

        elif opcion == "8":
            matriz = matrices.ingresar_matriz("Matriz")
            print(f"\n  La matriz tiene {len(matriz[0])} columnas.")
            print(f"  El vector debe tener {len(matriz[0])} elementos.")
            vector = matrices.ingresar_vector("Vector")
            res = matrices.producto_matriz_vector(matriz, vector)
            if res is not None:
                matrices.mostrar_vector(res, "Resultado (Matriz × Vector)")

        elif opcion == "9":
            break
        else:
            print("Opción no válida. Intente de nuevo.")


if __name__ == "__main__":
    menu_principal()
