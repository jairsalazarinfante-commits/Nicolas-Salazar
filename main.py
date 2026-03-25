
import tkinter as tk
from tkinter import messagebox
from impresora import Impresora


class AplicacionImpresora:

    def __init__(self):
        # Crear ventana
        self.root = tk.Tk()
        self.root.title("Simulador de Impresora")
        self.root.geometry("600x500")

        # Crear la impresora
        self.impresora = Impresora(callback_estado=self.actualizar_gui)

        # ---- FORMULARIO ----
        tk.Label(self.root, text="AGREGAR DOCUMENTO", font=("Arial", 14, "bold")).pack(pady=10)

        # Nombre
        tk.Label(self.root, text="Nombre:").pack()
        self.entry_nombre = tk.Entry(self.root, width=30)
        self.entry_nombre.pack()

        # Paginas
        tk.Label(self.root, text="Numero de paginas:").pack()
        self.entry_paginas = tk.Entry(self.root, width=30)
        self.entry_paginas.pack()

        # Tiempo por pagina
        tk.Label(self.root, text="Tiempo por pagina (segundos):").pack()
        self.entry_tiempo = tk.Entry(self.root, width=30)
        self.entry_tiempo.pack()

        # ---- BOTONES ----
        tk.Button(self.root, text="Agregar a la Cola", command=self.agregar_documento,
                  bg="green", fg="white", width=20).pack(pady=10)

        tk.Button(self.root, text="Iniciar Impresion", command=self.impresora.iniciar_impresion,
                  bg="blue", fg="white", width=20).pack(pady=5)

        tk.Button(self.root, text="Detener Impresion", command=self.impresora.detener_impresion,
                  bg="red", fg="white", width=20).pack(pady=5)

        # ---- ESTADO ----
        tk.Label(self.root, text="ESTADO", font=("Arial", 12, "bold")).pack(pady=10)

        self.label_estado = tk.Label(self.root, text="Sin documentos en cola", font=("Arial", 11))
        self.label_estado.pack()

        self.label_pagina = tk.Label(self.root, text="", font=("Arial", 10))
        self.label_pagina.pack()

        # ---- COLA ----
        tk.Label(self.root, text="COLA DE IMPRESION", font=("Arial", 12, "bold")).pack(pady=10)

        self.listbox_cola = tk.Listbox(self.root, width=50, height=6)
        self.listbox_cola.pack()

        # ---- HISTORIAL ----
        tk.Label(self.root, text="HISTORIAL", font=("Arial", 12, "bold")).pack(pady=10)

        self.listbox_historial = tk.Listbox(self.root, width=50, height=4)
        self.listbox_historial.pack()

    def agregar_documento(self):
        nombre = self.entry_nombre.get().strip()
        paginas = self.entry_paginas.get().strip()
        tiempo = self.entry_tiempo.get().strip()

        # Validar campos
        if not nombre or not paginas or not tiempo:
            messagebox.showwarning("Error", "Llena todos los campos")
            return

        try:
            paginas = int(paginas)
            tiempo = float(tiempo)
        except ValueError:
            messagebox.showerror("Error", "Paginas debe ser entero y tiempo debe ser numero")
            return

        # Agregar a la cola
        doc = self.impresora.agregar_documento(nombre, paginas, tiempo)

        # Limpiar campos
        self.entry_nombre.delete(0, tk.END)
        self.entry_paginas.delete(0, tk.END)
        self.entry_tiempo.delete(0, tk.END)

        # Actualizar lista
        self.refrescar_cola()
        messagebox.showinfo("OK", f"{doc.nombre} agregado a la cola")

    def actualizar_gui(self, evento, datos):
        """Se llama desde el hilo de impresion. Usa root.after para ser seguro."""
        self.root.after(0, self.procesar_evento, evento, datos)

    def procesar_evento(self, evento, datos):
        if evento == "imprimiendo_pagina":
            doc = datos["documento"]
            pag = datos["pagina"]
            total = datos["total_paginas"]
            self.label_estado.config(text=f"Imprimiendo: {doc.nombre}")
            self.label_pagina.config(text=f"Pagina {pag} de {total}")
            self.refrescar_cola()

        elif evento == "documento_completado":
            self.refrescar_cola()
            self.refrescar_historial()

        elif evento == "impresion_finalizada":
            self.label_estado.config(text="Sin documentos en cola")
            self.label_pagina.config(text="")
            self.refrescar_cola()

        elif evento == "sin_documentos":
            messagebox.showinfo("Aviso", "No hay documentos en la cola")

    def refrescar_cola(self):
        self.listbox_cola.delete(0, tk.END)

        # Documento imprimiendose
        if self.impresora.documento_actual:
            doc = self.impresora.documento_actual
            self.listbox_cola.insert(tk.END, f">> {doc.nombre} - {doc.num_paginas} pags - IMPRIMIENDO")

        # Documentos en espera
        for doc in self.impresora.obtener_cola():
            self.listbox_cola.insert(tk.END, f"   {doc.nombre} - {doc.num_paginas} pags - En cola")

    def refrescar_historial(self):
        self.listbox_historial.delete(0, tk.END)
        for doc in self.impresora.obtener_historial():
            self.listbox_historial.insert(tk.END, f"{doc.nombre} - {doc.num_paginas} pags - Completado")

    def ejecutar(self):
        self.root.mainloop()


# ---- PUNTO DE ENTRADA ----
if __name__ == "__main__":
    app = AplicacionImpresora()
    app.ejecutar()