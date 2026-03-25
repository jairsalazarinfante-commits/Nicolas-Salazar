import threading
import time
from estructuras import Cola

class Documento:
    """Representa un documento de impresion."""

    _contador = 0

    def __init__(self, nombre, num_paginas, tiempo_por_pagina):
        Documento._contador += 1
        self.id = Documento._contador
        self.nombre = nombre
        self.num_paginas = num_paginas
        self.tiempo_por_pagina = tiempo_por_pagina
        self.pagina_actual = 0
        self.estado = "En cola"

    def tiempo_total(self):
        """Tiempo total estimado de impresion en segundos."""
        return self.num_paginas * self.tiempo_por_pagina

    def progreso(self):
        """Porcentaje de progreso de impresion (0.0 a 1.0)."""
        if self.num_paginas == 0:
            return 1.0
        return self.pagina_actual / self.num_paginas

    def __repr__(self):
        return (
            f"{self.nombre} ({self.num_paginas} pags, "
            f"{self.tiempo_por_pagina}s/pag)"
        )


class HistorialImpresion:
    """
    Historial de documentos impresos, implementado con una Cola.
    Los documentos completados se registran en orden cronologico.
    """

    def __init__(self):
        self._cola_historial = Cola()

    def registrar(self, documento):
        """Registra un documento completado en el historial."""
        self._cola_historial.enqueue(documento)

    def obtener_historial(self):
        """Retorna todos los documentos del historial como lista."""
        return self._cola_historial.a_lista()

    def tamanio(self):
        return self._cola_historial.tamanio


class Impresora:
    """
    Controlador de impresion que gestiona la cola de impresion,
    la simulacion de impresion y el historial.
    """

    def __init__(self, callback_estado=None):
        self.cola_impresion = Cola()
        self.historial = HistorialImpresion()
        self.documento_actual = None
        self.imprimiendo = False
        self._hilo_impresion = None
        self._detener = False
        self._lock = threading.Lock()
        self.callback_estado = callback_estado

    # -- Metodos publicos --------------------------------------------------

    def agregar_documento(self, nombre, num_paginas, tiempo_por_pagina):
        """Crea un documento y lo agrega a la cola de impresion."""
        doc = Documento(nombre, num_paginas, tiempo_por_pagina)
        with self._lock:
            self.cola_impresion.enqueue(doc)
        self._notificar("documento_agregado", {"documento": doc})
        return doc

    def iniciar_impresion(self):
        """Inicia el proceso de impresion en un hilo separado."""
        if self.imprimiendo:
            return
        if self.cola_impresion.esta_vacia() and self.documento_actual is None:
            self._notificar("sin_documentos", {})
            return

        self._detener = False
        self.imprimiendo = True
        self._hilo_impresion = threading.Thread(
            target=self._ciclo_impresion, daemon=True
        )
        self._hilo_impresion.start()
        self._notificar("impresion_iniciada", {})

    def detener_impresion(self):
        """Solicita detener la impresion despues del documento actual."""
        self._detener = True
        self._notificar("impresion_detenida", {})

    def obtener_cola(self):
        """Retorna una lista con los documentos en cola."""
        with self._lock:
            return self.cola_impresion.a_lista()

    def obtener_historial(self):
        """Retorna el historial de documentos impresos."""
        return self.historial.obtener_historial()

    def obtener_documentos_en_cola_count(self):
        """Retorna la cantidad de documentos en la cola."""
        with self._lock:
            return self.cola_impresion.tamanio

    # -- Ciclo de impresion (hilo secundario) ------------------------------

    def _ciclo_impresion(self):
        """Ciclo principal de impresion que procesa documentos de la cola."""
        while not self._detener:
            with self._lock:
                if self.cola_impresion.esta_vacia():
                    break
                self.documento_actual = self.cola_impresion.dequeue()

            doc = self.documento_actual
            doc.estado = "Imprimiendo"
            self._notificar("imprimiendo_documento", {"documento": doc})

            for pagina in range(1, doc.num_paginas + 1):
                if self._detener:
                    break
                doc.pagina_actual = pagina
                self._notificar("imprimiendo_pagina", {
                    "documento": doc,
                    "pagina": pagina,
                    "total_paginas": doc.num_paginas
                })
                time.sleep(doc.tiempo_por_pagina)

            doc.estado = "Completado"
            doc.pagina_actual = doc.num_paginas
            self.historial.registrar(doc)
            self._notificar("documento_completado", {"documento": doc})
            self.documento_actual = None

        self.imprimiendo = False
        self.documento_actual = None
        self._notificar("impresion_finalizada", {})

    # -- Notificaciones ----------------------------------------------------

    def _notificar(self, evento, datos):
        """Envia una notificacion de cambio de estado al callback."""
        if self.callback_estado:
            self.callback_estado(evento, datos)
