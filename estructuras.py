from collections import deque
class Cola:
    def __init__(self):
        self._elementos = []

    def tamanio(self):
        return len(self._elementos)

    def esta_vacia(self):
        return len(self._elementos) == 0 

    def enqueue(self, dato):
        """Agrega un elemento al final de la cola."""
        self._elementos.append(dato)

    def dequeue(self):
        """Remueve y retorna el elemento del frente de la cola."""
        if self.esta_vacia():
            raise IndexError("La cola esta vacia")
        return self._elementos.pop(0)

    def frente(self):
        """Retorna el elemento del frente sin removerlo."""
        if self.esta_vacia():
            raise IndexError("La cola esta vacia")
        return self._elementos[0]

    def a_lista(self):
        """Retorna una copia de los elementos de la cola."""
        return list(self._elementos)

    # -- Metodos especiales ------------------------------------------------

    def __len__(self):
        return len(self._elementos)

    def __iter__(self):
        for elem in self._elementos:
            yield elem

    def __repr__(self):
        elementos = " <- ".join(str(d) for d in self._elementos)
        return f"Cola[{elementos}]"
