import threading
import time

# ---- PILA ----

class Pila:
    """Pila (LIFO) usando lista interna."""

    def __init__(self):
        self._elementos = []

    def push(self, dato):
        """Agrega un elemento a la cima."""
        self._elementos.append(dato)

    def pop(self):
        """Remueve y retorna el elemento de la cima."""
        if self.esta_vacia():
            raise IndexError("La pila esta vacia")
        return self._elementos.pop()

    def cima(self):
        """Retorna el elemento de la cima sin removerlo."""
        if self.esta_vacia():
            raise IndexError("La pila esta vacia")
        return self._elementos[-1]

    def esta_vacia(self):
        return len(self._elementos) == 0

    def tamanio(self):
        return len(self._elementos)

    def a_lista(self):
        """Retorna copia de los elementos (cima al final)."""
        return list(self._elementos)

    def __len__(self):
        return len(self._elementos)

    def __repr__(self):
        return f"Pila{self._elementos}"


# ---- TAREA ----

class Tarea:
    """Representa una tarea del robot."""

    _contador = 0

    def __init__(self, tipo, tiempo_ejecucion):
        Tarea._contador += 1
        self.id = Tarea._contador
        self.tipo = tipo                          # "Sensores" o "Movimiento"
        self.tiempo_ejecucion = tiempo_ejecucion  # segundos
        self.estado = "En pila"                   # "En pila", "Ejecutando", "Completada"

    def __repr__(self):
        return f"Tarea {self.id}: {self.tipo} ({self.tiempo_ejecucion}s)"


# ---- ROBOT ----

class Robot:
    """Robot explorador que ejecuta tareas usando una Pila."""

    def __init__(self, callback=None):
        self.pila_tareas = Pila()
        self.tarea_actual = None
        self.ejecutando = False
        self._hilo = None
        self._detener = False
        self._lock = threading.Lock()
        self.historial = []
        self.callback = callback

    def agregar_tarea(self, tipo, tiempo):
        """Agrega una tarea a la pila."""
        tarea = Tarea(tipo, tiempo)
        with self._lock:
            self.pila_tareas.push(tarea)
        self._notificar("tarea_agregada", {"tarea": tarea})
        return tarea

    def iniciar_ejecucion(self):
        """Inicia la ejecucion de tareas en un hilo."""
        if self.ejecutando:
            return
        if self.pila_tareas.esta_vacia() and self.tarea_actual is None:
            self._notificar("sin_tareas", {})
            return

        self._detener = False
        self.ejecutando = True
        self._hilo = threading.Thread(target=self._ciclo_ejecucion, daemon=True)
        self._hilo.start()
        self._notificar("ejecucion_iniciada", {})

    def detener_ejecucion(self):
        """Detiene la ejecucion."""
        self._detener = True

    def obtener_pila(self):
        """Retorna la pila como lista (cima primero)."""
        with self._lock:
            lista = self.pila_tareas.a_lista()
            lista.reverse()  # Cima primero
            return lista

    def _ciclo_ejecucion(self):
        """Ciclo que ejecuta tareas de la pila una por una."""
        while not self._detener:
            with self._lock:
                if self.pila_tareas.esta_vacia():
                    break
                self.tarea_actual = self.pila_tareas.pop()

            tarea = self.tarea_actual
            tarea.estado = "Ejecutando"
            self._notificar("ejecutando_tarea", {"tarea": tarea})

            # Simular ejecucion esperando el tiempo
            tiempo_restante = tarea.tiempo_ejecucion
            while tiempo_restante > 0 and not self._detener:
                time.sleep(0.5)
                tiempo_restante -= 0.5
                self._notificar("progreso_tarea", {
                    "tarea": tarea,
                    "restante": max(0, tiempo_restante),
                    "total": tarea.tiempo_ejecucion
                })

            # Completar tarea
            tarea.estado = "Completada"
            self.historial.append(tarea)
            self._notificar("tarea_completada", {"tarea": tarea})
            self.tarea_actual = None

        self.ejecutando = False
        self.tarea_actual = None
        self._notificar("ejecucion_finalizada", {})

    def _notificar(self, evento, datos):
        if self.callback:
            self.callback(evento, datos)
